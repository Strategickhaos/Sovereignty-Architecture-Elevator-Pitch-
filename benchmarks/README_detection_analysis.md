# Detection Analysis Benchmark

## Overview

This benchmark harness analyzes detection and recovery performance across multiple sensor systems:
- **ResMon**: Resource Monitor
- **Prometheus**: Metrics collection and alerting
- **Classic Watchdog**: Traditional watchdog timer

## Features

✅ **CSV Table**: Detection, recovery, and false positive metrics per sensor  
✅ **Matplotlib Graphs**: Visual comparison of latency across sensors  
✅ **Coherence Timeline**: State agreement visualization over time  
✅ **Reproducible**: Feed in any scenario YAML, sensor logs, and metrics are automatically computed

## Directory Structure

```
results/
├── raw/                          # Raw sensor logs
│   ├── resmon/
│   │   └── log.jsonl            # ResMon sensor logs
│   ├── prom_node_exporter/
│   │   └── log.jsonl            # Prometheus sensor logs
│   ├── classic_watchdog/
│   │   └── log.txt              # Classic watchdog logs
│   └── timeline_vpn_drop.jsonl  # Ground-truth timeline
└── derived/                      # Analysis outputs
    ├── detection_latency.csv    # Metrics table
    ├── latency_comparison.png   # Detection/recovery graph
    └── coherence_timeline.png   # State coherence visualization
```

## Input File Formats

### Timeline (timeline_vpn_drop.jsonl)
```json
{"event": "action", "action": "vpn_down", "ts": "2026-01-23T07:00:00Z", "description": "VPN connection dropped"}
{"event": "action", "action": "vpn_up", "ts": "2026-01-23T07:05:00Z", "description": "VPN connection restored"}
```

### ResMon Log (resmon/log.jsonl)
```json
{"ts": "2026-01-23T06:59:50Z", "state": "OK"}
{"ts": "2026-01-23T07:00:05Z", "state": "FAIL"}
{"ts": "2026-01-23T07:05:03Z", "state": "OK"}
```

### Prometheus Log (prom_node_exporter/log.jsonl)
```json
{"ts": "2026-01-23T06:59:50Z", "value": 1}
{"ts": "2026-01-23T07:00:08Z", "value": 0}
{"ts": "2026-01-23T07:05:05Z", "value": 1}
```

### Classic Watchdog Log (classic_watchdog/log.txt)
```
2026-01-23T06:59:50Z OK
2026-01-23T07:00:12Z FAIL
2026-01-23T07:05:08Z OK
```

## Usage

### Run Analysis

```bash
cd benchmarks
python3 analyze_detection.py
```

### Output

The script will:
1. Read all sensor logs and the ground-truth timeline
2. Compute detection latency, recovery latency, and false positives
3. Generate CSV table at `results/derived/detection_latency.csv`
4. Create visualization graphs in `results/derived/`

### Metrics Computed

- **Detection Latency**: Time from fault injection to first sensor detection (ms)
- **Recovery Latency**: Time from fault recovery to first sensor confirmation (ms)
- **False Positives**: Number of incorrect failure detections outside fault window

## Example Output

### CSV Table
```csv
scenario,sensor,fault,event_type,latency_ms
vpn_drop,resmon,vpn_down,detect,5000.0
vpn_drop,resmon,vpn_up,recover,3000.0
vpn_drop,resmon,vpn_down,false_positive,0
```

### Graphs Generated

1. **latency_comparison.png**: Bar/line chart comparing detection and recovery latencies
2. **coherence_timeline.png**: Timeline showing state transitions across all sensors

## Extending the Benchmark

To add a new sensor:

1. Add log file path to `SENSORS` dictionary in `analyze_detection.py`
2. Create a loader function (e.g., `load_newsensor()`)
3. Add normalization function to `sensor_normalizer.py` if needed

## Dependencies

- Python 3.7+
- matplotlib >= 3.7.0
- Standard library: json, csv, pathlib, datetime, sys

Install matplotlib only:
```bash
pip install matplotlib
```

Or install all project dependencies:
```bash
pip install -r requirements.sovereignty.txt
```

## Integration

This script can be integrated into automated CI/CD pipelines or one-command runners to:
- Launch sensors
- Inject faults
- Collect logs
- Produce CSV + graphs automatically

## Results

All outputs are deterministic and reproducible, making them suitable for:
- Performance benchmarking
- Sensor comparison studies
- Detection capability validation
- Resilience testing

---

**Author**: Strategickhaos DAO LLC  
**Version**: 1.0  
**Date**: 2026-01-23
