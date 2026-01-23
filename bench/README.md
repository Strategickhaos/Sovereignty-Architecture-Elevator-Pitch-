# Sandbox Benchmark Harness

A comprehensive testing framework for validating network fault detection and recovery capabilities across different monitoring systems.

## Overview

This benchmark harness provides:
- **Reproducible fault injection** - Controlled network failures (VPN drops, latency spikes)
- **Multi-sensor comparison** - Test ResMon, Prometheus, and classic watchdog systems
- **Quantitative metrics** - Detection latency, recovery latency, false positive rates
- **Ground truth timeline** - Precise fault injection timestamps for analysis

## Directory Structure

```text
/bench
  /scenarios/          # Fault scenario definitions (YAML)
    vpn_drop.yaml      # VPN interface drop test
    latency_ramp.yaml  # Progressive latency increase
  /sensors/            # Sensor implementations
    resmon/            # ResMon state monitor
      run.sh
      config.yaml
    prom_node_exporter/ # Prometheus node_exporter
      docker-compose.yaml
      prometheus.yml
    classic_watchdog/   # Simple ping-based watchdog
      run.sh
  /injectors/          # Fault injection scripts
    vpn_toggle.sh      # VPN interface control
    netem.sh           # Network latency injection
  /runner/             # Orchestration and analysis
    bench_run.py       # Scenario orchestrator
    analyze_detection.py # Metric extraction
  /results/
    raw/               # Raw timeline and sensor logs
    derived/           # Analyzed metrics (CSV)
```

## Quick Start

### 1. Prerequisites

```bash
# Python 3 with PyYAML
pip install pyyaml

# Network tools (for fault injection)
sudo apt-get install iproute2 iputils-ping

# Optional: Docker for Prometheus sensor
sudo apt-get install docker.io docker-compose
```

### 2. Run a Benchmark Scenario

```bash
# Run VPN drop scenario (requires root for network manipulation)
sudo ./bench/runner/bench_run.py bench/scenarios/vpn_drop.yaml | tee bench/results/raw/timeline_vpn_drop.jsonl

# Run latency ramp scenario
sudo ./bench/runner/bench_run.py bench/scenarios/latency_ramp.yaml | tee bench/results/raw/timeline_latency_ramp.jsonl
```

### 3. Start Sensors (in separate terminals)

```bash
# ResMon sensor
./bench/sensors/resmon/run.sh

# Classic watchdog
./bench/sensors/classic_watchdog/run.sh > bench/results/raw/watchdog.log

# Prometheus (with Docker)
cd bench/sensors/prom_node_exporter
docker-compose up -d
```

### 4. Analyze Results

```bash
./bench/runner/analyze_detection.py \
  bench/results/raw/timeline_vpn_drop.jsonl \
  --resmon bench/sensors/resmon/log.jsonl \
  --prometheus bench/sensors/prom_node_exporter/log.jsonl \
  --watchdog bench/results/raw/watchdog.log \
  --output bench/results/derived/detection_latency.csv
```

## Scenario Definitions

### VPN Drop (`vpn_drop.yaml`)

Simulates a complete VPN tunnel failure:
- **0s**: Baseline measurement
- **10s**: Drop tun0 interface (`vpn_down`)
- **20s**: Restore tun0 interface (`vpn_up`)
- **60s**: End scenario

**Metrics:**
- Detection latency: Time to mark unhealthy after fault
- Recovery latency: Time to mark healthy after restore
- False positive rate: Unhealthy events outside fault window

### Latency Ramp (`latency_ramp.yaml`)

Progressive network degradation:
- **0s**: Set RTT to 20ms
- **10s**: Increase to 100ms
- **20s**: Increase to 250ms
- **30s**: Increase to 500ms
- **40s**: Increase to 800ms
- **50s**: Clear latency

**Metrics:**
- State transition curve: Mapping RTT → Resonant/Dissonant/Collapsed states

### Route Hijack (`route_hijack.yaml`)

BGP route hijack simulation - redirects traffic via an alternate gateway:
- **0s**: Baseline measurement
- **15s**: Hijack route to 8.8.8.8/32 via 10.0.0.1 (`route_hijack`)
- **45s**: Restore original route (`route_restore`)
- **90s**: End scenario

**Metrics:**
- Route detection latency: Time to detect routing anomaly
- Connectivity impact: Packet loss during route change
- Convergence time: Time for system to adapt to new route

## Fault Injectors

### `vpn_toggle.sh`

Controls VPN interface state:
```bash
# Bring interface down
sudo IF=tun0 ./bench/injectors/vpn_toggle.sh down

# Bring interface up
sudo IF=tun0 ./bench/injectors/vpn_toggle.sh up
```

### `netem.sh`

Network emulation for latency injection:
```bash
# Add 250ms latency to eth0
sudo IF=eth0 ./bench/injectors/netem.sh set 250

# Clear latency
sudo IF=eth0 ./bench/injectors/netem.sh clear
```

### `route_toggle.sh`

Route manipulation for BGP hijack simulation:
```bash
# Hijack route to 8.8.8.8/32 via 10.0.0.1
sudo ./bench/injectors/route_toggle.sh hijack 8.8.8.8/32 10.0.0.1

# Restore original route
sudo ./bench/injectors/route_toggle.sh restore 8.8.8.8/32

# Show current route
./bench/injectors/route_toggle.sh show 8.8.8.8
```

## Sensor Contracts

### ResMon

Monitors `/flamelang/membrane/net_watchdog/state.json` and logs state transitions.

**Output format** (`log.jsonl`):
```json
{"ts":"2026-01-23T03:21:54.123Z","state":"Resonant"}
{"ts":"2026-01-23T03:22:10.540Z","state":"Collapsed"}
{"ts":"2026-01-23T03:22:20.200Z","state":"Resonant"}
```

**States:**
- `Resonant`: Healthy network
- `Dissonant`: Degraded network
- `Collapsed`: Failed network

### Prometheus (node_exporter)

Exposes metrics on `:9100` and logs scrape results.

**Output format** (`log.jsonl`):
```json
{"ts":"2026-01-23T03:21:54.100Z","up":1,"tun0_up":1}
{"ts":"2026-01-23T03:22:10.600Z","up":1,"tun0_up":0}
{"ts":"2026-01-23T03:22:20.250Z","up":1,"tun0_up":1}
```

**Metrics:**
- `up`: Node exporter health (1=up, 0=down)
- `tun0_up`: VPN interface state (1=up, 0=down)

### Classic Watchdog

Simple ping-based health checker.

**Output format** (text log):
```text
2026-01-23T03:21:54Z OK
2026-01-23T03:22:10Z FAIL
2026-01-23T03:22:20Z OK
```

## Ground Truth Timeline

The orchestrator (`bench_run.py`) emits a precise timeline of fault injections:

```json
{"event":"scenario_start","ts":"2026-01-23T03:21:50.000Z","id":"vpn_drop"}
{"event":"action","ts":"2026-01-23T03:22:00.010Z","action":"vpn_down","params":{}}
{"event":"action","ts":"2026-01-23T03:22:10.005Z","action":"vpn_up","params":{}}
{"event":"scenario_end","ts":"2026-01-23T03:22:50.000Z"}
```

This provides the exact timestamps for analysis.

## Metric Extraction

The `analyze_detection.py` script compares ground truth with sensor logs:

**Output CSV:**
```csv
scenario,sensor,fault,event_type,latency_ms
vpn_drop,resmon,down,detect,150
vpn_drop,resmon,up,recover,250
vpn_drop,prometheus,down,detect,450
vpn_drop,prometheus,up,recover,300
```

**Metrics:**
- `detect`: Latency from fault start to detection
- `recover`: Latency from fault end to recovery

## Creating New Scenarios

Add a YAML file to `/bench/scenarios/`:

```yaml
id: custom_scenario
description: "Your scenario description"
duration_s: 120

timeline:
  - t: 0
    action: "baseline"
  - t: 30
    action: "vpn_down"
  - t: 60
    action: "vpn_up"

metrics:
  - name: your_metric
    description: "What you're measuring"
```

**Supported actions:**
- `baseline`: No-op for baseline measurement
- `vpn_down`: Drop VPN interface
- `vpn_up`: Restore VPN interface
- `latency_set`: Set network latency (requires `params: {ms: N}`)
- `latency_clear`: Remove network latency
- `route_hijack`: Hijack route (requires `params: {target: "X.X.X.X/N", via: "Y.Y.Y.Y"}`)
- `route_restore`: Restore original route (requires `params: {target: "X.X.X.X/N"}`)

## Requirements

- **Python 3.x** with PyYAML
- **Root/sudo access** for network manipulation
- **iproute2** (`ip` and `tc` commands)
- **jq** (for ResMon log parsing)
- **Docker** (optional, for Prometheus sensor)

## Safety Notes

⚠️ **This harness manipulates network interfaces and requires root privileges.**

- Run in isolated test environments (VMs, containers, sandboxes)
- Do NOT run on production systems
- VPN drops will interrupt network connectivity
- Latency injection affects all traffic on the interface

## Example Workflow

```bash
# 1. Start all sensors
./bench/sensors/resmon/run.sh &
./bench/sensors/classic_watchdog/run.sh > bench/results/raw/watchdog.log &
cd bench/sensors/prom_node_exporter && docker-compose up -d && cd -

# 2. Run benchmark
sudo ./bench/runner/bench_run.py bench/scenarios/vpn_drop.yaml | \
  tee bench/results/raw/timeline_vpn_drop.jsonl

# 3. Analyze results
./bench/runner/analyze_detection.py \
  bench/results/raw/timeline_vpn_drop.jsonl \
  --resmon bench/sensors/resmon/log.jsonl \
  --output bench/results/derived/metrics.csv

# 4. View results
cat bench/results/derived/metrics.csv
```

## Next Steps

Future enhancements:
- **Partial connectivity** - Packet loss and jitter scenarios
- **State coherence analysis** - Cross-sensor agreement metrics
- **Automated report generation** - HTML dashboards with charts
- **CI integration** - Automated regression testing
- **Multi-node scenarios** - Distributed system testing

## License

Part of the Sovereignty Architecture project.
