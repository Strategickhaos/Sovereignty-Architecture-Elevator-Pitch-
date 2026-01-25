#!/usr/bin/env python3
"""
System Health Controller - Integrates RESMON, TRIG6, and F1
Flight controller for Strategickhaos OS
"""

import time
import json
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

try:
    from .resmon import RESMON, SystemMetrics, MetricDifferential
    from .trig6 import TRIG6Potentiometer, TRIG6Params, SystemHealth, SystemMode
    from .f1_lemma import F1Lemma, gamma_from_health_score
except ImportError:
    # For running as a script
    from resmon import RESMON, SystemMetrics, MetricDifferential
    from trig6 import TRIG6Potentiometer, TRIG6Params, SystemHealth, SystemMode
    from f1_lemma import F1Lemma, gamma_from_health_score


class SystemHealthController:
    """
    System Health Controller
    
    Integrates:
    - RESMON → real metrics (CPU, load, variance, process health, thermal)
    - TRIG6 → health score f = R·(1-D)·(1-N)·eq
    - F1 → stability tracking with bounded product lemma
    
    Pipeline: RESMON → TRIG6 → compiler threshold
    """
    
    def __init__(self, log_dir: str = "./logs/system_health"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.resmon = RESMON(baseline_samples=10, sample_interval=0.5)
        self.trig6 = TRIG6Potentiometer()
        self.f1 = F1Lemma()
        
        # State
        self.baseline_established = False
        self.boot_time = time.time()
        self.tick_count = 0
        self.last_health: Optional[SystemHealth] = None
        
        # Configuration
        self.config = {
            'enable_logging': True,
            'log_interval_ticks': 10,  # Log every 10 ticks
            'thermal_critical_celsius': 85.0,
            'memory_critical_percent': 95.0,
            'enable_f1_tracking': True
        }
    
    def initialize(self) -> None:
        """
        Initialize system - establish baseline
        Call this on boot
        """
        print("🚀 System Health Controller - Initializing")
        print("=" * 60)
        
        print("\n📊 Establishing baseline metrics...")
        baseline = self.resmon.establish_baseline()
        self.baseline_established = True
        
        print(f"✅ Baseline established:")
        print(f"   CPU: {baseline.cpu_baseline:.1f}%")
        print(f"   Load: {baseline.load_baseline[0]:.2f}")
        print(f"   Memory: {baseline.memory_baseline:.1f}%")
        print(f"   I/O: {baseline.io_baseline:.2f} MB/s")
        print(f"   Network: {baseline.network_baseline:.2f} MB/s")
        
        # Initial health check
        health = self.assess_health()
        print(f"\n💚 Initial health: f={health.f:.3f}, mode={health.mode.value}")
        
        self._log_boot(baseline, health)
        print("\n✅ System Health Controller operational")
    
    def assess_health(self) -> SystemHealth:
        """
        Complete health assessment
        
        Returns:
            SystemHealth with current status
        """
        if not self.baseline_established:
            raise RuntimeError("Baseline not established. Call initialize() first.")
        
        # Collect metrics
        metrics = self.resmon.collect_metrics()
        diff = self.resmon.compute_differential(metrics)
        
        # Compute TRIG6 params
        params = self._compute_trig6_params(metrics, diff)
        
        # Assess with TRIG6
        health = self.trig6.assess(params, metrics.timestamp)
        
        # Track with F1 if enabled
        if self.config['enable_f1_tracking']:
            gamma = 1.0
            if self.last_health:
                gamma = gamma_from_health_score(health.f, self.last_health.f)
            self.f1.add_bound(self.tick_count, health.f, gamma)
        
        self.last_health = health
        self.tick_count += 1
        
        # Log if needed
        if self.config['enable_logging'] and self.tick_count % self.config['log_interval_ticks'] == 0:
            self._log_tick(metrics, diff, health)
        
        return health
    
    def _compute_trig6_params(self, metrics: SystemMetrics, diff: MetricDifferential) -> TRIG6Params:
        """
        Compute TRIG6 parameters from RESMON metrics
        
        Args:
            metrics: Current system metrics
            diff: Differential from baseline
        
        Returns:
            TRIG6Params
        """
        # R: Resource availability
        cpu_available = 1.0 - (metrics.cpu_percent / 100.0)
        mem_available = 1.0 - (metrics.memory_percent / 100.0)
        R = self.trig6.compute_R(cpu_available, mem_available)
        
        # D: Degradation
        thermal_factor = 0.0
        if metrics.thermal_celsius:
            # Normalize thermal to [0, 1] based on critical threshold
            thermal_factor = max(0.0, min(1.0, 
                metrics.thermal_celsius / self.config['thermal_critical_celsius']))
        D = self.trig6.compute_D(diff.cpu_diff, diff.memory_diff, thermal_factor)
        
        # N: Noise
        load_variance = diff.load_diff  # Already normalized
        N = self.trig6.compute_N(diff.variance, load_variance)
        
        # eq: Equilibrium
        # Process stability: assume stable if count isn't changing wildly
        # Network stability: based on network I/O consistency
        process_stability = 1.0  # Simplified: assume stable
        network_stability = 1.0 - diff.network_diff  # Less diff = more stable
        eq = self.trig6.compute_eq(process_stability, network_stability)
        
        return TRIG6Params(R=R, D=D, N=N, eq=eq)
    
    def get_compiler_config(self) -> Dict:
        """
        Get compiler configuration based on current health
        
        Returns compiler flags and thresholds
        
        Returns:
            dict with compiler configuration
        """
        if not self.last_health:
            # Default conservative config if no health data
            return {
                'mode': 'SAFE',
                'proof_threshold': 0.9,
                'opt_level': 0,
                'parallel_jobs': 1,
                'enable_aggressive_opts': False,
                'memory_limit_mb': 1024
            }
        
        health = self.last_health
        
        if health.mode == SystemMode.FULL:
            return {
                'mode': 'FULL',
                'proof_threshold': health.proof_threshold,
                'opt_level': 3,
                'parallel_jobs': int(health.params.R * 8),  # Scale with resources
                'enable_aggressive_opts': True,
                'memory_limit_mb': 8192,
                'aggressive_inlining': health.opt_aggression > 0.7,
                'enable_lto': health.opt_aggression > 0.6
            }
        elif health.mode == SystemMode.DEGRADED:
            return {
                'mode': 'DEGRADED',
                'proof_threshold': health.proof_threshold,
                'opt_level': 2,
                'parallel_jobs': max(2, int(health.params.R * 4)),
                'enable_aggressive_opts': False,
                'memory_limit_mb': 4096,
                'aggressive_inlining': False,
                'enable_lto': False
            }
        else:  # SAFE
            return {
                'mode': 'SAFE',
                'proof_threshold': health.proof_threshold,
                'opt_level': 1,
                'parallel_jobs': 1,
                'enable_aggressive_opts': False,
                'memory_limit_mb': 2048,
                'aggressive_inlining': False,
                'enable_lto': False,
                'enable_safety_checks': True
            }
    
    def _log_boot(self, baseline, health: SystemHealth) -> None:
        """Log boot event"""
        log_file = self.log_dir / f"boot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = {
            'event': 'boot',
            'timestamp': time.time(),
            'timestamp_iso': datetime.now().isoformat(),
            'baseline': {
                'cpu': baseline.cpu_baseline,
                'load': baseline.load_baseline,
                'memory': baseline.memory_baseline,
                'io': baseline.io_baseline,
                'network': baseline.network_baseline
            },
            'initial_health': health.to_dict(),
            'compiler_config': self.get_compiler_config()
        }
        
        with open(log_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log_tick(self, metrics: SystemMetrics, diff: MetricDifferential, health: SystemHealth) -> None:
        """Log periodic tick"""
        log_file = self.log_dir / f"ticks_{datetime.now().strftime('%Y%m%d')}.jsonl"
        data = {
            'event': 'tick',
            'tick': self.tick_count,
            'timestamp': metrics.timestamp,
            'timestamp_iso': datetime.fromtimestamp(metrics.timestamp).isoformat(),
            'metrics': {
                'cpu_percent': metrics.cpu_percent,
                'load_avg': metrics.load_average[0],
                'memory_percent': metrics.memory_percent,
                'thermal_celsius': metrics.thermal_celsius
            },
            'differential': {
                'variance': diff.variance,
                'cpu_diff': diff.cpu_diff,
                'memory_diff': diff.memory_diff
            },
            'health': health.to_dict(),
            'compiler_config': self.get_compiler_config()
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def log_compile_event(self, event_type: str, details: Optional[Dict] = None) -> None:
        """
        Log compilation event
        
        Args:
            event_type: Type of event (e.g., 'start', 'end', 'proof_check')
            details: Additional details
        """
        log_file = self.log_dir / f"compile_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        health = self.assess_health()
        
        data = {
            'event': event_type,
            'timestamp': time.time(),
            'timestamp_iso': datetime.now().isoformat(),
            'health': health.to_dict(),
            'compiler_config': self.get_compiler_config(),
            'details': details or {}
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def get_system_status(self) -> Dict:
        """
        Get current system status
        
        Returns:
            dict with complete status
        """
        health = self.assess_health()
        
        stability = None
        if self.config['enable_f1_tracking']:
            stability = self.f1.get_stability_rate(window=3)
        
        return {
            'health': health.to_dict(),
            'compiler_config': self.get_compiler_config(),
            'stability_rate': stability,
            'tick_count': self.tick_count,
            'uptime_seconds': time.time() - self.boot_time,
            'contract': self.trig6.get_system_contract(health)
        }


if __name__ == "__main__":
    # Demo usage
    print("🎮 System Health Controller Demo")
    print("=" * 60)
    
    controller = SystemHealthController(log_dir="./logs/demo")
    
    # Initialize
    controller.initialize()
    
    # Simulate some activity
    print("\n🔄 Simulating system activity...")
    for i in range(5):
        time.sleep(1)
        status = controller.get_system_status()
        
        print(f"\n⏱️  Tick {status['tick_count']}:")
        print(f"   Health: f={status['health']['f']:.3f}")
        print(f"   Mode: {status['health']['mode']}")
        print(f"   Compiler: {status['compiler_config']['mode']} "
              f"(opt_level={status['compiler_config']['opt_level']}, "
              f"jobs={status['compiler_config']['parallel_jobs']:.0f})")
        
        if status['stability_rate']:
            print(f"   Stability: Γ={status['stability_rate']:.4f}")
    
    # Simulate compilation
    print("\n🔨 Simulating compilation event...")
    controller.log_compile_event('start', {'target': 'demo_project'})
    time.sleep(0.5)
    controller.log_compile_event('end', {'target': 'demo_project', 'success': True})
    
    print("\n✅ System Health Controller demo complete")
    print(f"📁 Logs written to: {controller.log_dir}")
