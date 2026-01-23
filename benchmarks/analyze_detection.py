#!/usr/bin/env python3
"""
analyze_detection.py - Benchmark analysis for ResMon vs Prometheus vs Classic Watchdog
Outputs:
  - CSV table of detection/recovery latency per sensor
  - Matplotlib graphs
  - Coherence timeline
  - Summary stats
"""

import json
import csv
import pathlib
import datetime
import matplotlib.pyplot as plt
from sensor_normalizer import resmon_to_bool, prom_to_bool

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"

SENSORS = {
    "resmon": RAW_DIR / "resmon/log.jsonl",
    "prometheus": RAW_DIR / "prom_node_exporter/log.jsonl",
    "classic": RAW_DIR / "classic_watchdog/log.txt",
}

TIMELINE = RAW_DIR / "timeline_vpn_drop.jsonl"
CSV_OUT = RESULTS_DIR / "derived/detection_latency.csv"

# Utility
def parse_iso(ts: str):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def load_timeline(path):
    events = []
    with open(path) as f:
        for line in f:
            e = json.loads(line)
            if e["event"] == "action":
                events.append(e)
    return events


def load_resmon(path):
    samples = []
    with open(path) as f:
        for line in f:
            j = json.loads(line)
            samples.append((parse_iso(j["ts"]), resmon_to_bool(j["state"])))
    return samples


def load_prometheus(path):
    samples = []
    with open(path) as f:
        for line in f:
            j = json.loads(line)
            samples.append((parse_iso(j["ts"]), prom_to_bool(j)))
    return samples


def load_classic(path):
    samples = []
    with open(path) as f:
        for line in f:
            ts, state = line.strip().split()
            samples.append((parse_iso(ts), state == "OK"))
    return samples


def compute_latency(samples, fault_start, fault_end):
    # Detection latency: first sample after fault_start that is False
    detect_latency = next(
        (
            (ts - fault_start).total_seconds() * 1000
            for ts, state in samples
            if ts >= fault_start and not state
        ),
        None,
    )
    # Recovery latency: first sample after fault_end that is True
    recover_latency = next(
        (
            (ts - fault_end).total_seconds() * 1000
            for ts, state in samples
            if ts >= fault_end and state
        ),
        None,
    )
    # False positives: any False outside fault window
    false_positives = sum(
        1 for ts, state in samples if (ts < fault_start or ts > fault_end) and not state
    )
    return detect_latency, recover_latency, false_positives


def main():
    timeline = load_timeline(TIMELINE)
    # Assume only one fault type for simplicity
    fault_evt = next(e for e in timeline if e["action"] == "vpn_down")
    recovery_evt = next(e for e in timeline if e["action"] == "vpn_up")
    fault_start = parse_iso(fault_evt["ts"])
    fault_end = parse_iso(recovery_evt["ts"])

    # Load all sensors
    sensor_data = {
        "resmon": load_resmon(SENSORS["resmon"]),
        "prometheus": load_prometheus(SENSORS["prometheus"]),
        "classic": load_classic(SENSORS["classic"]),
    }

    # Compute metrics
    rows = []
    for name, samples in sensor_data.items():
        detect_ms, recover_ms, false_pos = compute_latency(
            samples, fault_start, fault_end
        )
        rows.append(
            {
                "scenario": "vpn_drop",
                "sensor": name,
                "fault": "vpn_down",
                "event_type": "detect",
                "latency_ms": detect_ms,
            }
        )
        rows.append(
            {
                "scenario": "vpn_drop",
                "sensor": name,
                "fault": "vpn_up",
                "event_type": "recover",
                "latency_ms": recover_ms,
            }
        )
        rows.append(
            {
                "scenario": "vpn_drop",
                "sensor": name,
                "fault": "vpn_down",
                "event_type": "false_positive",
                "latency_ms": false_pos,
            }
        )

    # Write CSV
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV output: {CSV_OUT}")

    # Plot detection/recovery latencies
    plt.figure(figsize=(10, 6))
    for name in sensor_data.keys():
        detect = [
            r["latency_ms"]
            for r in rows
            if r["sensor"] == name and r["event_type"] == "detect"
        ]
        recover = [
            r["latency_ms"]
            for r in rows
            if r["sensor"] == name and r["event_type"] == "recover"
        ]
        plt.plot(detect, label=f"{name} detect", marker="o")
        plt.plot(recover, label=f"{name} recover", marker="x")
    plt.ylabel("Latency (ms)")
    plt.xlabel("Event index")
    plt.title("Detection / Recovery Latency per Sensor")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "derived/latency_comparison.png")

    # Coherence timeline plot
    plt.figure(figsize=(12, 4))
    for idx, (name, samples) in enumerate(sensor_data.items()):
        ts_list = [(ts - sensor_data[name][0][0]).total_seconds() for ts, _ in samples]
        state_list = [1 if s else 0 for _, s in samples]
        plt.step(
            ts_list, [s + idx * 1.5 for s in state_list], where="post", label=name
        )
    plt.yticks([0, 1.5, 3], list(sensor_data.keys()))
    plt.xlabel("Time (s)")
    plt.title("State Coherence Timeline")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "derived/coherence_timeline.png")
    print("Graphs saved in results/derived/")


if __name__ == "__main__":
    main()
