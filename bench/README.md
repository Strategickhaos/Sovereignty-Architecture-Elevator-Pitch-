# Benchmark Harness - Sensor Normalization

This directory contains the benchmark harness for testing VPN monitoring sensors with measurable and deterministic results.

## Overview

The benchmark harness enables consistent comparison between different monitoring sensors (ResMon, Prometheus, Classic) by:

1. **Normalizing sensor outputs** to boolean up/down states
2. **Deterministic state classification** with clear thresholds
3. **Reproducible measurements** for detection latency and recovery time

## Directory Structure

```
bench/
├── sensor_normalizer.py          # Core normalization functions
├── sensors/
│   └── resmon/
│       ├── run.sh                # ResMon sensor implementation
│       ├── state.json            # Current state (generated)
│       └── log.jsonl             # Time-series log (generated)
└── tests/
    └── test_sensor_normalizer.py # Unit tests
```

## Components

### 1. sensor_normalizer.py

Provides mapping functions to normalize sensor outputs:

- **`resmon_to_bool(state: str) -> bool`**: Maps ResMon states to boolean
  - `Resonant` → `True` (system is up)
  - `Dissonant` → `False` (degraded/down)
  - `Collapsed` → `False` (down)

- **`prom_to_bool(prom_sample: dict) -> bool`**: Maps Prometheus metrics to boolean
  - Requires both `tun0_up` and `up` to be truthy
  - Returns `True` only if interface and service are up

### 2. ResMon Sensor (sensors/resmon/run.sh)

Deterministic VPN state classification with clear thresholds:

**State Classification Rules:**
- **Resonant**: latency < 200ms, all checks pass
- **Dissonant**: 200-500ms latency, checks pass
- **Collapsed**: TCP down, interface down, or latency ≥ 500ms

**Checks Performed:**
1. Interface check: Is `tun0` up?
2. Route check: Does traffic to target route via VPN?
3. TCP probe: Can we connect to the target?
4. Latency measurement: What is the ping average?

**Configuration:**
```bash
CHECK_HOST=10.8.0.1    # Target host to monitor
CHECK_PORT=22          # Port to probe
```

**Outputs:**
- `state.json`: Current state snapshot (queryable by benchmarks)
- `log.jsonl`: Time-series log of all state changes

### 3. Tests

Run the test suite:
```bash
python3 bench/tests/test_sensor_normalizer.py
```

## Usage

### Running the ResMon Sensor

```bash
# Start the sensor (runs continuously)
./bench/sensors/resmon/run.sh

# Or with custom configuration
CHECK_HOST=10.8.0.2 CHECK_PORT=443 ./bench/sensors/resmon/run.sh
```

### Using the Normalizer in Benchmarks

```python
from bench.sensor_normalizer import resmon_to_bool, prom_to_bool

# Normalize ResMon state
is_up = resmon_to_bool("Resonant")  # True

# Normalize Prometheus metrics
is_up = prom_to_bool({"tun0_up": 1, "up": 1})  # True
```

### Example Benchmark Flow

1. **Start sensors** (ResMon, Prometheus, Classic)
2. **Inject fault** (drop VPN, add latency, hijack route)
3. **Collect sensor logs** with timestamps
4. **Normalize states** using `sensor_normalizer.py`
5. **Calculate metrics**:
   - Detection latency: Time from fault to first detection
   - Recovery latency: Time from recovery to sensor acknowledgment
   - False positives: Incorrect state changes
   - State coherence: Agreement between sensors

## Benefits

✅ **Consistent Comparison**: All sensors normalized to boolean up/down
✅ **Deterministic Results**: Clear thresholds, no fuzzy logic
✅ **Reproducible**: Same fault scenario produces same measurements
✅ **Measurable Claims**: Prove ResMon detection capabilities with data

## Next Steps

- Integrate with `bench_run.py` or `analyze_detection.py`
- Add Prometheus and Classic sensors
- Implement fault injection scenarios
- Create analysis scripts for CSV tables and graphs
- Generate coherence timeline visualizations
