#!/usr/bin/env bash
###############################################################################
# cpumon.sh - CPU Telemetry Monitor
###############################################################################

INTERVAL="${SAGCO_TELEMETRY_INTERVAL:-5}"
LOG_FILE="${SAGCO_LOG_DIR:-/var/log/sagco}/telemetry/cpumon.log"

echo "=== SAGCO-OS CPU Monitor Started at $(date) ===" | tee -a "${LOG_FILE}"

get_cpu_usage() {
    if command -v top &> /dev/null; then
        if [ "$(uname)" = "Linux" ]; then
            top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
        else
            top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1
        fi
    elif [ -f /proc/stat ]; then
        awk '/^cpu / {usage=($2+$4)*100/($2+$4+$5)} END {print usage}' /proc/stat
    else
        echo "0.0"
    fi
}

while true; do
    timestamp=$(date +%s)
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    
    cpu_usage=$(get_cpu_usage)
    load_avg=$(uptime | awk -F'load average:' '{print $2}' | sed 's/^[ \t]*//' || echo "0.00, 0.00, 0.00")
    
    echo "${datetime} | CPU: ${cpu_usage}% | Load: ${load_avg}" | tee -a "${LOG_FILE}"
    echo "{\"timestamp\":${timestamp},\"cpu_usage\":${cpu_usage},\"load_avg\":\"${load_avg}\"}" >> "${LOG_FILE}.json"
    
    sleep ${INTERVAL}
done
