#!/usr/bin/env python3
"""
example_usage.py - Example demonstrating the detection analysis workflow

This script shows how to:
1. Generate sample sensor logs
2. Create a fault injection timeline
3. Run the detection analysis
4. Interpret the results

For production use, replace mock data generation with real sensor outputs.
"""

import json
import datetime
import pathlib
import subprocess
import sys


def format_timestamp(dt: datetime.datetime) -> str:
    """Format datetime to ISO format with 'Z' suffix for UTC"""
    return dt.isoformat().replace("+00:00", "Z")


def generate_mock_scenario():
    """Generate a sample VPN drop scenario with sensor responses"""
    
    root = pathlib.Path(__file__).resolve().parents[1]
    raw_dir = root / "results" / "raw"
    
    # Ensure directories exist
    (raw_dir / "resmon").mkdir(parents=True, exist_ok=True)
    (raw_dir / "prom_node_exporter").mkdir(parents=True, exist_ok=True)
    (raw_dir / "classic_watchdog").mkdir(parents=True, exist_ok=True)
    
    # Define fault injection timeline
    fault_start = datetime.datetime(2026, 1, 23, 7, 0, 0, tzinfo=datetime.timezone.utc)
    fault_end = datetime.datetime(2026, 1, 23, 7, 5, 0, tzinfo=datetime.timezone.utc)
    
    print("🔧 Generating mock scenario: VPN connection drop")
    print(f"   Fault window: {fault_start.isoformat()} to {fault_end.isoformat()}")
    
    # Generate timeline
    timeline_path = raw_dir / "timeline_vpn_drop.jsonl"
    with open(timeline_path, "w") as f:
        f.write(json.dumps({
            "event": "action",
            "action": "vpn_down",
            "ts": format_timestamp(fault_start),
            "description": "VPN connection dropped"
        }) + "\n")
        f.write(json.dumps({
            "event": "action",
            "action": "vpn_up",
            "ts": format_timestamp(fault_end),
            "description": "VPN connection restored"
        }) + "\n")
    print(f"✓ Timeline: {timeline_path}")
    
    # Generate ResMon logs (fast detection: 5s)
    resmon_path = raw_dir / "resmon" / "log.jsonl"
    with open(resmon_path, "w") as f:
        # Before fault
        f.write(json.dumps({
            "ts": format_timestamp(fault_start - datetime.timedelta(seconds=10)),
            "state": "OK"
        }) + "\n")
        # Detection: 5s after fault
        f.write(json.dumps({
            "ts": format_timestamp(fault_start + datetime.timedelta(seconds=5)),
            "state": "FAIL"
        }) + "\n")
        # Still failing
        f.write(json.dumps({
            "ts": format_timestamp(fault_start + datetime.timedelta(seconds=10)),
            "state": "FAIL"
        }) + "\n")
        # Recovery: 3s after restoration
        f.write(json.dumps({
            "ts": format_timestamp(fault_end + datetime.timedelta(seconds=3)),
            "state": "OK"
        }) + "\n")
    print(f"✓ ResMon logs: {resmon_path}")
    
    # Generate Prometheus logs (medium detection: 8s)
    prom_path = raw_dir / "prom_node_exporter" / "log.jsonl"
    with open(prom_path, "w") as f:
        f.write(json.dumps({
            "ts": format_timestamp(fault_start - datetime.timedelta(seconds=10)),
            "value": 1
        }) + "\n")
        f.write(json.dumps({
            "ts": format_timestamp(fault_start + datetime.timedelta(seconds=8)),
            "value": 0
        }) + "\n")
        f.write(json.dumps({
            "ts": format_timestamp(fault_start + datetime.timedelta(seconds=13)),
            "value": 0
        }) + "\n")
        f.write(json.dumps({
            "ts": format_timestamp(fault_end + datetime.timedelta(seconds=5)),
            "value": 1
        }) + "\n")
    print(f"✓ Prometheus logs: {prom_path}")
    
    # Generate Classic Watchdog logs (slow detection: 12s)
    classic_path = raw_dir / "classic_watchdog" / "log.txt"
    with open(classic_path, "w") as f:
        f.write(f"{format_timestamp(fault_start - datetime.timedelta(seconds=10))} OK\n")
        f.write(f"{format_timestamp(fault_start + datetime.timedelta(seconds=12))} FAIL\n")
        f.write(f"{format_timestamp(fault_start + datetime.timedelta(seconds=17))} FAIL\n")
        f.write(f"{format_timestamp(fault_end + datetime.timedelta(seconds=8))} OK\n")
    print(f"✓ Classic Watchdog logs: {classic_path}")
    
    print("\n✅ Mock scenario generated successfully!\n")


def run_analysis():
    """Execute the detection analysis script"""
    print("📊 Running detection analysis...")
    
    benchmarks_dir = pathlib.Path(__file__).parent
    result = subprocess.run(
        [sys.executable, "analyze_detection.py"],
        cwd=benchmarks_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(result.stdout)
        print("✅ Analysis completed successfully!\n")
    else:
        print("❌ Analysis failed:")
        print(result.stderr)
        sys.exit(1)


def display_results():
    """Display the analysis results"""
    root = pathlib.Path(__file__).resolve().parents[1]
    csv_path = root / "results" / "derived" / "detection_latency.csv"
    
    print("📈 Results Summary:")
    print("=" * 70)
    
    with open(csv_path) as f:
        print(f.read())
    
    print("=" * 70)
    print("\n📁 Generated files:")
    derived_dir = root / "results" / "derived"
    for file in sorted(derived_dir.glob("*")):
        print(f"   - {file.relative_to(root)}")
    
    print("\n💡 Next steps:")
    print("   1. View the CSV for quantitative metrics")
    print("   2. Open latency_comparison.png to see detection speeds")
    print("   3. Open coherence_timeline.png to see state agreement")
    print("   4. Integrate into CI/CD for automated benchmarking")


def main():
    """Run the complete example workflow"""
    print("=" * 70)
    print("Detection Analysis Benchmark - Example Usage")
    print("=" * 70)
    print()
    
    # Step 1: Generate mock data
    generate_mock_scenario()
    
    # Step 2: Run analysis
    run_analysis()
    
    # Step 3: Display results
    display_results()
    
    print("\n" + "=" * 70)
    print("✅ Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
