#!/usr/bin/env python3
"""
demo_benchmark.py

Demonstration of the benchmark harness components:
1. Sensor normalizer usage
2. Example detection latency calculation
3. Sample benchmark flow
"""

import json
import time
from datetime import datetime
from sensor_normalizer import resmon_to_bool, prom_to_bool


def demo_sensor_normalization():
    """Demonstrate sensor normalization"""
    print("=" * 70)
    print("DEMO: Sensor Normalization")
    print("=" * 70)
    
    # ResMon states
    print("\n1. ResMon State Normalization:")
    resmon_states = ["Resonant", "Dissonant", "Collapsed"]
    for state in resmon_states:
        normalized = resmon_to_bool(state)
        status = "UP ✓" if normalized else "DOWN ✗"
        print(f"   {state:12} → {status}")
    
    # Prometheus metrics
    print("\n2. Prometheus Metric Normalization:")
    prom_samples = [
        ({"tun0_up": 1, "up": 1}, "Both interface and service up"),
        ({"tun0_up": 0, "up": 1}, "Interface down, service up"),
        ({"tun0_up": 1, "up": 0}, "Interface up, service down"),
        ({"tun0_up": 0, "up": 0}, "Both down"),
    ]
    for sample, description in prom_samples:
        normalized = prom_to_bool(sample)
        status = "UP ✓" if normalized else "DOWN ✗"
        print(f"   {description:35} → {status}")


def demo_detection_latency():
    """Demonstrate detection latency calculation"""
    print("\n" + "=" * 70)
    print("DEMO: Detection Latency Calculation")
    print("=" * 70)
    
    # Simulated scenario: VPN drops at T=0
    fault_time = datetime.fromisoformat("2026-01-23T10:00:00")
    
    # Sensor detections (simulated)
    resmon_log = [
        {"ts": "2026-01-23T10:00:01", "state": "Resonant"},
        {"ts": "2026-01-23T10:00:02", "state": "Dissonant"},
        {"ts": "2026-01-23T10:00:03", "state": "Collapsed"},
    ]
    
    prometheus_log = [
        {"ts": "2026-01-23T10:00:05", "tun0_up": 1, "up": 1},
        {"ts": "2026-01-23T10:00:10", "tun0_up": 0, "up": 1},
    ]
    
    print(f"\nFault injected at: {fault_time.isoformat()}")
    print("\nResMon Detection Timeline:")
    
    for entry in resmon_log:
        event_time = datetime.fromisoformat(entry["ts"])
        normalized = resmon_to_bool(entry["state"])
        latency = (event_time - fault_time).total_seconds()
        
        if not normalized:  # First detection of "down" state
            print(f"  ⚠️  First detection at T+{latency}s: {entry['state']}")
            print(f"     Detection latency: {latency} seconds")
            break
        else:
            print(f"  ✓  T+{latency}s: {entry['state']} (still up)")
    
    print("\nPrometheus Detection Timeline:")
    for i, entry in enumerate(prometheus_log):
        event_time = datetime.fromisoformat(entry["ts"])
        normalized = prom_to_bool(entry)
        latency = (event_time - fault_time).total_seconds()
        
        if not normalized:  # First detection of "down" state
            print(f"  ⚠️  First detection at T+{latency}s")
            print(f"     Detection latency: {latency} seconds")
            break
        else:
            print(f"  ✓  T+{latency}s: Interface and service up")


def demo_benchmark_flow():
    """Demonstrate complete benchmark flow"""
    print("\n" + "=" * 70)
    print("DEMO: Complete Benchmark Flow")
    print("=" * 70)
    
    print("""
Benchmark Process:

1. Start Sensors
   - ResMon:     ./bench/sensors/resmon/run.sh
   - Prometheus: (existing Prometheus instance)
   - Classic:    (legacy monitoring)

2. Inject Fault Scenario
   Example: sudo ip link set tun0 down
   
3. Collect Logs
   - ResMon:     bench/sensors/resmon/log.jsonl
   - Prometheus: query via API
   - Classic:    /var/log/vpnmon.log

4. Normalize States (using sensor_normalizer.py)
   - All sensors → boolean up/down
   - Consistent timestamps
   
5. Calculate Metrics
   - Detection latency = time(first_down) - time(fault)
   - Recovery latency = time(first_up) - time(recovery)
   - False positives = unexpected state changes
   - Coherence = agreement between sensors

6. Generate Reports
   - CSV table: sensor × metric
   - Graphs: latency distributions
   - Timeline: state coherence visualization
   
✅ Results are reproducible and measurable!
    """)


def demo_json_output_format():
    """Show expected JSON output formats"""
    print("\n" + "=" * 70)
    print("DEMO: ResMon JSON Output Formats")
    print("=" * 70)
    
    # Example state.json
    state_json = {
        "seq": 1737621600,
        "timestamp": "2026-01-23T10:00:00+00:00",
        "state": "Resonant",
        "interface": {
            "name": "tun0",
            "up": True
        },
        "route": {
            "target": "10.8.0.1",
            "via_vpn": True
        },
        "transport": {
            "latency_ms": 45.2,
            "tcp_check": True
        }
    }
    
    # Example log.jsonl entry
    log_entry = {
        "ts": "2026-01-23T10:00:00+00:00",
        "state": "Resonant",
        "latency": 45.2,
        "interface_up": True,
        "route_ok": True,
        "tcp_ok": True
    }
    
    print("\nstate.json (current state snapshot):")
    print(json.dumps(state_json, indent=2))
    
    print("\nlog.jsonl (time-series entry):")
    print(json.dumps(log_entry))


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ResMon Benchmark Harness - Component Demonstration")
    print("=" * 70)
    
    demo_sensor_normalization()
    demo_detection_latency()
    demo_benchmark_flow()
    demo_json_output_format()
    
    print("\n" + "=" * 70)
    print("✅ All demonstrations complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Start ResMon sensor: ./bench/sensors/resmon/run.sh")
    print("  2. Run tests: python3 bench/tests/test_sensor_normalizer.py")
    print("  3. Integrate with analyze_detection.py for full benchmarking")
    print()
