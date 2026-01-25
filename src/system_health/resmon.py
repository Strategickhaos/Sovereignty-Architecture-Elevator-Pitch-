#!/usr/bin/env python3
"""
RESMON - Resource Monitor
Real metrics collection: CPU, load, variance, process health, thermal
"""

import psutil
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
import os


@dataclass
class SystemMetrics:
    """Real-time system metrics"""
    timestamp: float
    cpu_percent: float
    cpu_count: int
    load_average: List[float]
    memory_percent: float
    memory_available_gb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    thermal_celsius: Optional[float]  # May not be available on all systems


@dataclass
class MetricBaseline:
    """Baseline metrics for differential calculation"""
    cpu_baseline: float
    load_baseline: List[float]
    memory_baseline: float
    io_baseline: float
    network_baseline: float
    
    @classmethod
    def from_metrics(cls, metrics: SystemMetrics) -> 'MetricBaseline':
        """Create baseline from current metrics"""
        return cls(
            cpu_baseline=metrics.cpu_percent,
            load_baseline=metrics.load_average,
            memory_baseline=metrics.memory_percent,
            io_baseline=metrics.disk_io_read_mb + metrics.disk_io_write_mb,
            network_baseline=metrics.network_sent_mb + metrics.network_recv_mb
        )


@dataclass
class MetricDifferential:
    """Differential vs baseline"""
    cpu_diff: float  # Percentage difference
    load_diff: float  # Average load difference
    memory_diff: float
    io_diff: float
    network_diff: float
    variance: float  # Overall variance score [0, 1]


class RESMON:
    """
    Resource Monitor - Collects real system metrics
    Tracks baselines and computes differentials
    """
    
    def __init__(self, baseline_samples: int = 10, sample_interval: float = 0.5):
        self.baseline_samples = baseline_samples
        self.sample_interval = sample_interval
        self.baseline: Optional[MetricBaseline] = None
        self.last_io_counters = None
        self.last_net_counters = None
        self.last_time = None
        
    def _get_thermal(self) -> Optional[float]:
        """Get thermal reading if available"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Try common sensor names
                    for sensor in ['coretemp', 'cpu_thermal', 'k10temp']:
                        if sensor in temps:
                            return temps[sensor][0].current
                    # Fallback to first available
                    first_sensor = next(iter(temps.values()))
                    if first_sensor:
                        return first_sensor[0].current
        except:
            pass
        return None
    
    def collect_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        current_time = time.time()
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        # Load average (Unix-like systems)
        try:
            load_avg = list(os.getloadavg())
        except:
            load_avg = [0.0, 0.0, 0.0]
        
        # Memory metrics
        mem = psutil.virtual_memory()
        memory_percent = mem.percent
        memory_available_gb = mem.available / (1024**3)
        
        # I/O metrics (rate per second)
        io = psutil.disk_io_counters()
        if self.last_io_counters and self.last_time:
            time_delta = current_time - self.last_time
            disk_read_mb = (io.read_bytes - self.last_io_counters.read_bytes) / (1024**2) / time_delta
            disk_write_mb = (io.write_bytes - self.last_io_counters.write_bytes) / (1024**2) / time_delta
        else:
            disk_read_mb = 0.0
            disk_write_mb = 0.0
        self.last_io_counters = io
        
        # Network metrics (rate per second)
        net = psutil.net_io_counters()
        if self.last_net_counters and self.last_time:
            time_delta = current_time - self.last_time
            net_sent_mb = (net.bytes_sent - self.last_net_counters.bytes_sent) / (1024**2) / time_delta
            net_recv_mb = (net.bytes_recv - self.last_net_counters.bytes_recv) / (1024**2) / time_delta
        else:
            net_sent_mb = 0.0
            net_recv_mb = 0.0
        self.last_net_counters = net
        
        self.last_time = current_time
        
        # Process count
        process_count = len(psutil.pids())
        
        # Thermal
        thermal = self._get_thermal()
        
        return SystemMetrics(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            cpu_count=cpu_count,
            load_average=load_avg,
            memory_percent=memory_percent,
            memory_available_gb=memory_available_gb,
            disk_io_read_mb=disk_read_mb,
            disk_io_write_mb=disk_write_mb,
            network_sent_mb=net_sent_mb,
            network_recv_mb=net_recv_mb,
            process_count=process_count,
            thermal_celsius=thermal
        )
    
    def establish_baseline(self) -> MetricBaseline:
        """
        Establish baseline by taking multiple samples
        Returns average baseline metrics
        """
        samples = []
        for i in range(self.baseline_samples):
            metrics = self.collect_metrics()
            samples.append(metrics)
            if i < self.baseline_samples - 1:
                time.sleep(self.sample_interval)
        
        # Average the samples
        avg_cpu = sum(s.cpu_percent for s in samples) / len(samples)
        avg_load = [
            sum(s.load_average[0] for s in samples) / len(samples),
            sum(s.load_average[1] for s in samples) / len(samples),
            sum(s.load_average[2] for s in samples) / len(samples)
        ]
        avg_mem = sum(s.memory_percent for s in samples) / len(samples)
        avg_io = sum(s.disk_io_read_mb + s.disk_io_write_mb for s in samples) / len(samples)
        avg_net = sum(s.network_sent_mb + s.network_recv_mb for s in samples) / len(samples)
        
        self.baseline = MetricBaseline(
            cpu_baseline=avg_cpu,
            load_baseline=avg_load,
            memory_baseline=avg_mem,
            io_baseline=avg_io,
            network_baseline=avg_net
        )
        return self.baseline
    
    def compute_differential(self, metrics: SystemMetrics) -> MetricDifferential:
        """
        Compute differential vs baseline
        Returns normalized differentials [0, 1] where 0 is baseline, 1 is max deviation
        """
        if not self.baseline:
            raise ValueError("Baseline not established. Call establish_baseline() first.")
        
        # CPU differential (normalized to 100%)
        cpu_diff = abs(metrics.cpu_percent - self.baseline.cpu_baseline) / 100.0
        
        # Load average differential (normalized by CPU count)
        load_diff = abs(metrics.load_average[0] - self.baseline.load_baseline[0]) / max(metrics.cpu_count, 1)
        
        # Memory differential
        memory_diff = abs(metrics.memory_percent - self.baseline.memory_baseline) / 100.0
        
        # I/O differential (assume max 1000 MB/s as normalization)
        current_io = metrics.disk_io_read_mb + metrics.disk_io_write_mb
        io_diff = abs(current_io - self.baseline.io_baseline) / 1000.0
        io_diff = min(io_diff, 1.0)  # Cap at 1.0
        
        # Network differential (assume max 100 MB/s as normalization)
        current_net = metrics.network_sent_mb + metrics.network_recv_mb
        net_diff = abs(current_net - self.baseline.network_baseline) / 100.0
        net_diff = min(net_diff, 1.0)  # Cap at 1.0
        
        # Overall variance (weighted average)
        variance = (
            0.3 * cpu_diff +
            0.2 * load_diff +
            0.2 * memory_diff +
            0.15 * io_diff +
            0.15 * net_diff
        )
        variance = min(variance, 1.0)  # Cap at 1.0
        
        return MetricDifferential(
            cpu_diff=cpu_diff,
            load_diff=load_diff,
            memory_diff=memory_diff,
            io_diff=io_diff,
            network_diff=net_diff,
            variance=variance
        )
    
    def to_dict(self, metrics: SystemMetrics, differential: Optional[MetricDifferential] = None) -> Dict:
        """Convert metrics to dictionary for logging/serialization"""
        result = asdict(metrics)
        result['timestamp_iso'] = datetime.fromtimestamp(metrics.timestamp).isoformat()
        if differential:
            result['differential'] = asdict(differential)
        if self.baseline:
            result['baseline'] = asdict(self.baseline)
        return result


if __name__ == "__main__":
    # Demo usage
    print("🔍 RESMON - Resource Monitor Demo")
    print("=" * 50)
    
    resmon = RESMON(baseline_samples=5, sample_interval=0.3)
    
    print("\n📊 Establishing baseline...")
    baseline = resmon.establish_baseline()
    print(f"✅ Baseline established:")
    print(f"   CPU: {baseline.cpu_baseline:.1f}%")
    print(f"   Load: {baseline.load_baseline[0]:.2f}")
    print(f"   Memory: {baseline.memory_baseline:.1f}%")
    
    print("\n📈 Current metrics:")
    for i in range(3):
        metrics = resmon.collect_metrics()
        diff = resmon.compute_differential(metrics)
        
        print(f"\n   Sample {i+1}:")
        print(f"   CPU: {metrics.cpu_percent:.1f}% (diff: {diff.cpu_diff:.3f})")
        print(f"   Load: {metrics.load_average[0]:.2f} (diff: {diff.load_diff:.3f})")
        print(f"   Memory: {metrics.memory_percent:.1f}% (diff: {diff.memory_diff:.3f})")
        print(f"   Variance: {diff.variance:.3f}")
        
        time.sleep(1)
    
    print("\n✅ RESMON operational")
