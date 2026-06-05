#!/usr/bin/env python3
"""
TRIG6 Potentiometer - System Health Scoring
Computes f = R·(1-D)·(1-N)·eq in [0,1]
Modes: SAFE / DEGRADED / FULL + proof_threshold + optimization aggression
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
from enum import Enum
import math


class SystemMode(Enum):
    """System operating modes based on health score"""
    SAFE = "SAFE"          # Conservative operation, high safety margins
    DEGRADED = "DEGRADED"  # Reduced capacity, stability priority
    FULL = "FULL"          # Full capacity operation


@dataclass
class TRIG6Params:
    """
    TRIG6 Potentiometer Parameters
    R: Resource availability [0, 1]
    D: Degradation factor [0, 1]
    N: Noise/variance factor [0, 1]
    eq: Equilibrium/stability factor [0, 1]
    """
    R: float  # Resource availability (1 = full, 0 = depleted)
    D: float  # Degradation (1 = fully degraded, 0 = no degradation)
    N: float  # Noise (1 = maximum noise, 0 = no noise)
    eq: float  # Equilibrium (1 = perfect equilibrium, 0 = chaos)
    
    def __post_init__(self):
        """Validate parameters are in [0, 1]"""
        for field in ['R', 'D', 'N', 'eq']:
            value = getattr(self, field)
            if not 0 <= value <= 1:
                raise ValueError(f"{field} must be in [0, 1], got {value}")


@dataclass
class SystemHealth:
    """System health assessment"""
    f: float  # Health score [0, 1]
    mode: SystemMode
    proof_threshold: float  # Rigor required for proof validation [0, 1]
    opt_aggression: float  # Optimization aggression level [0, 1]
    params: TRIG6Params
    timestamp: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for logging"""
        result = asdict(self)
        result['mode'] = self.mode.value
        return result


class TRIG6Potentiometer:
    """
    TRIG6 Potentiometer - System Health Scoring
    
    This is NOT a "P(correct) oracle" or cosmology law.
    This is a system potentiometer: a health score that tells
    your OS how hard it can push.
    
    Formula: f = R·(1-D)·(1-N)·eq
    where f ∈ [0, 1]
    
    Interpretation:
    - f close to 1: System healthy, full capacity available
    - f close to 0: System stressed, reduce blast radius
    """
    
    # Mode thresholds
    SAFE_THRESHOLD = 0.75      # f >= 0.75: FULL mode
    DEGRADED_THRESHOLD = 0.40  # 0.40 <= f < 0.75: DEGRADED mode
                               # f < 0.40: SAFE mode
    
    def __init__(self):
        self.history = []
        
    def compute_R(self, cpu_available: float, memory_available: float, 
                  io_available: float = 1.0) -> float:
        """
        Compute Resource availability
        
        Args:
            cpu_available: CPU availability [0, 1] (1 - cpu_percent/100)
            memory_available: Memory availability [0, 1] (1 - mem_percent/100)
            io_available: I/O availability [0, 1] (optional)
        
        Returns:
            R: Resource availability [0, 1]
        """
        # Weighted average: CPU and memory are most important
        R = (0.4 * cpu_available + 
             0.4 * memory_available + 
             0.2 * io_available)
        return max(0.0, min(1.0, R))
    
    def compute_D(self, cpu_diff: float, memory_diff: float,
                  thermal_factor: float = 0.0) -> float:
        """
        Compute Degradation factor
        
        Args:
            cpu_diff: CPU differential from baseline [0, 1]
            memory_diff: Memory differential from baseline [0, 1]
            thermal_factor: Thermal degradation [0, 1] (optional)
        
        Returns:
            D: Degradation factor [0, 1]
        """
        # Higher differentials = more degradation
        D = (0.4 * cpu_diff + 
             0.4 * memory_diff + 
             0.2 * thermal_factor)
        return max(0.0, min(1.0, D))
    
    def compute_N(self, variance: float, load_variance: float = 0.0) -> float:
        """
        Compute Noise factor
        
        Args:
            variance: Overall system variance [0, 1]
            load_variance: Load average variance [0, 1] (optional)
        
        Returns:
            N: Noise factor [0, 1]
        """
        # Weighted average of variance metrics
        N = 0.7 * variance + 0.3 * load_variance
        return max(0.0, min(1.0, N))
    
    def compute_eq(self, process_stability: float = 1.0,
                   network_stability: float = 1.0) -> float:
        """
        Compute Equilibrium factor
        
        Args:
            process_stability: Process count stability [0, 1]
            network_stability: Network I/O stability [0, 1]
        
        Returns:
            eq: Equilibrium factor [0, 1]
        """
        # Geometric mean for equilibrium (all must be stable)
        eq = math.sqrt(process_stability * network_stability)
        return max(0.0, min(1.0, eq))
    
    def compute_health_score(self, params: TRIG6Params) -> float:
        """
        Compute health score f
        
        Formula: f = R·(1-D)·(1-N)·eq
        
        Args:
            params: TRIG6 parameters
        
        Returns:
            f: Health score [0, 1]
        """
        f = params.R * (1 - params.D) * (1 - params.N) * params.eq
        return max(0.0, min(1.0, f))
    
    def determine_mode(self, f: float) -> SystemMode:
        """
        Determine system mode based on health score
        
        Args:
            f: Health score [0, 1]
        
        Returns:
            SystemMode
        """
        if f >= self.SAFE_THRESHOLD:
            return SystemMode.FULL
        elif f >= self.DEGRADED_THRESHOLD:
            return SystemMode.DEGRADED
        else:
            return SystemMode.SAFE
    
    def compute_proof_threshold(self, f: float, mode: SystemMode) -> float:
        """
        Compute proof validation threshold
        
        When health is low, we require higher proof rigor.
        Inverse relationship: lower health = higher threshold = more rigorous checking.
        This ensures the system is more careful when stressed.
        
        Args:
            f: Health score [0, 1]
            mode: Current system mode
        
        Returns:
            proof_threshold: [0, 1], higher = more rigorous
        """
        # Inverse relationship: lower health = higher threshold
        base_threshold = 1.0 - f
        
        # Mode adjustments
        if mode == SystemMode.SAFE:
            # Maximum rigor in safe mode
            return min(0.95, base_threshold * 1.2)
        elif mode == SystemMode.DEGRADED:
            # Moderate rigor
            return min(0.85, base_threshold * 1.1)
        else:  # FULL mode
            # Minimum rigor, allow optimization
            return max(0.3, base_threshold * 0.8)
    
    def compute_opt_aggression(self, f: float, mode: SystemMode) -> float:
        """
        Compute optimization aggression level
        
        When health is high, we can be more aggressive
        
        Args:
            f: Health score [0, 1]
            mode: Current system mode
        
        Returns:
            opt_aggression: [0, 1], higher = more aggressive
        """
        # Direct relationship: higher health = higher aggression
        if mode == SystemMode.FULL:
            # Maximum aggression in full mode
            return min(1.0, f * 1.2)
        elif mode == SystemMode.DEGRADED:
            # Moderate aggression
            return f * 0.8
        else:  # SAFE mode
            # Minimal aggression
            return max(0.1, f * 0.5)
    
    def assess(self, params: TRIG6Params, timestamp: float) -> SystemHealth:
        """
        Complete system health assessment
        
        Args:
            params: TRIG6 parameters
            timestamp: Current timestamp
        
        Returns:
            SystemHealth with score, mode, thresholds
        """
        # Compute health score
        f = self.compute_health_score(params)
        
        # Determine mode
        mode = self.determine_mode(f)
        
        # Compute thresholds
        proof_threshold = self.compute_proof_threshold(f, mode)
        opt_aggression = self.compute_opt_aggression(f, mode)
        
        health = SystemHealth(
            f=f,
            mode=mode,
            proof_threshold=proof_threshold,
            opt_aggression=opt_aggression,
            params=params,
            timestamp=timestamp
        )
        
        # Store in history
        self.history.append(health)
        
        return health
    
    def get_system_contract(self, health: SystemHealth) -> str:
        """
        Get the system contract based on current health
        
        This is your OS's contract with itself:
        "When my health falls, I narrow my blast radius."
        
        Args:
            health: Current system health
        
        Returns:
            Contract string
        """
        if health.mode == SystemMode.FULL:
            return (f"FULL MODE: Health={health.f:.3f}. "
                   f"All systems operational. Optimization aggressive (α={health.opt_aggression:.2f}). "
                   f"Proof rigor moderate (τ={health.proof_threshold:.2f}).")
        elif health.mode == SystemMode.DEGRADED:
            return (f"DEGRADED MODE: Health={health.f:.3f}. "
                   f"Reducing capacity. Optimization conservative (α={health.opt_aggression:.2f}). "
                   f"Proof rigor elevated (τ={health.proof_threshold:.2f}).")
        else:  # SAFE
            return (f"SAFE MODE: Health={health.f:.3f}. "
                   f"Minimal blast radius. Optimization minimal (α={health.opt_aggression:.2f}). "
                   f"Proof rigor maximum (τ={health.proof_threshold:.2f}).")


if __name__ == "__main__":
    import time
    
    # Demo usage
    print("🎚️  TRIG6 Potentiometer Demo")
    print("=" * 60)
    
    trig6 = TRIG6Potentiometer()
    
    # Scenario 1: Healthy system
    print("\n🟢 Scenario 1: Healthy System")
    params1 = TRIG6Params(R=0.85, D=0.10, N=0.05, eq=0.95)
    health1 = trig6.assess(params1, time.time())
    print(f"   Params: R={params1.R}, D={params1.D}, N={params1.N}, eq={params1.eq}")
    print(f"   Health score f = {health1.f:.3f}")
    print(f"   Mode: {health1.mode.value}")
    print(f"   Contract: {trig6.get_system_contract(health1)}")
    
    # Scenario 2: Degraded system
    print("\n🟡 Scenario 2: Degraded System")
    params2 = TRIG6Params(R=0.60, D=0.35, N=0.25, eq=0.70)
    health2 = trig6.assess(params2, time.time())
    print(f"   Params: R={params2.R}, D={params2.D}, N={params2.N}, eq={params2.eq}")
    print(f"   Health score f = {health2.f:.3f}")
    print(f"   Mode: {health2.mode.value}")
    print(f"   Contract: {trig6.get_system_contract(health2)}")
    
    # Scenario 3: Critical system
    print("\n🔴 Scenario 3: Critical System")
    params3 = TRIG6Params(R=0.40, D=0.60, N=0.45, eq=0.50)
    health3 = trig6.assess(params3, time.time())
    print(f"   Params: R={params3.R}, D={params3.D}, N={params3.N}, eq={params3.eq}")
    print(f"   Health score f = {health3.f:.3f}")
    print(f"   Mode: {health3.mode.value}")
    print(f"   Contract: {trig6.get_system_contract(health3)}")
    
    print("\n✅ TRIG6 Potentiometer operational")
    print("\n📝 Remember: This is NOT a P(correct) oracle.")
    print("   This is a system potentiometer: f = health score.")
    print("   When f falls, we narrow the blast radius. 🎯")
