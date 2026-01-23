#!/usr/bin/env bash
# Quick Start Guide for Benchmark Harness
# This script demonstrates the complete workflow

set -euo pipefail

echo "=== Sandbox Benchmark Harness - Quick Start ==="
echo

# Configuration
SCENARIO="${1:-bench/scenarios/vpn_drop.yaml}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TIMELINE_LOG="bench/results/raw/timeline_${TIMESTAMP}.jsonl"

echo "1. Checking prerequisites..."
command -v python3 >/dev/null || { echo "ERROR: python3 not found"; exit 1; }
python3 -c "import yaml" 2>/dev/null || { echo "ERROR: PyYAML not installed (pip install pyyaml)"; exit 1; }
echo "   ✓ Python 3 and PyYAML available"
echo

echo "2. Validating scenario: $SCENARIO"
if [ ! -f "$SCENARIO" ]; then
    echo "   ERROR: Scenario file not found"
    exit 1
fi
python3 -c "import yaml; yaml.safe_load(open('$SCENARIO'))" || { echo "   ERROR: Invalid YAML"; exit 1; }
echo "   ✓ Scenario validated"
echo

echo "3. Available scenarios:"
ls -1 bench/scenarios/*.yaml | while read f; do
    ID=$(python3 -c "import yaml; print(yaml.safe_load(open('$f'))['id'])")
    DESC=$(python3 -c "import yaml; print(yaml.safe_load(open('$f'))['description'])")
    echo "   - $(basename $f): $ID - $DESC"
done
echo

echo "4. Example: Dry-run scenario (no actual network changes)"
echo "   This shows what would happen without requiring root privileges"
echo
python3 -c "
import yaml
from datetime import datetime, timedelta

with open('$SCENARIO') as f:
    scenario = yaml.safe_load(f)

print(f\"   Scenario: {scenario['id']}\")
print(f\"   Duration: {scenario['duration_s']}s\")
print()
print('   Timeline:')

start_time = datetime.utcnow()
for event in sorted(scenario['timeline'], key=lambda e: e['t']):
    action = event['action']
    params = event.get('params', {})
    params_str = f\" with {params}\" if params else \"\"
    print(f\"     {event['t']:3d}s: {action}{params_str}\")
"
echo

echo "5. To run a real benchmark (requires root/sudo):"
echo "   sudo ./bench/runner/bench_run.py $SCENARIO | tee $TIMELINE_LOG"
echo

echo "6. To analyze results:"
echo "   ./bench/runner/analyze_detection.py \\"
echo "     $TIMELINE_LOG \\"
echo "     --resmon bench/sensors/resmon/log.jsonl \\"
echo "     --prometheus bench/sensors/prom_node_exporter/log.jsonl \\"
echo "     --output bench/results/derived/metrics_${TIMESTAMP}.csv"
echo

echo "7. Example analysis with demo data:"
if [ -f "bench/results/raw/example_timeline.jsonl" ]; then
    echo "   Running analysis on example data..."
    ./bench/runner/analyze_detection.py \
        bench/results/raw/example_timeline.jsonl \
        --resmon bench/results/raw/example_resmon.jsonl \
        --prometheus bench/results/raw/example_prometheus.jsonl \
        --output /tmp/demo_metrics.csv
    
    echo
    echo "   Results:"
    column -t -s, /tmp/demo_metrics.csv | sed 's/^/     /'
    rm -f /tmp/demo_metrics.csv
fi
echo

echo "=== Quick Start Complete ==="
echo
echo "For more information, see bench/README.md"
