#!/usr/bin/env bash
###############################################################################
# memmon.sh - Memory Telemetry Monitor
###############################################################################

INTERVAL="${SAGCO_TELEMETRY_INTERVAL:-5}"
LOG_FILE="${SAGCO_LOG_DIR:-/var/log/sagco}/telemetry/memmon.log"

echo "=== SAGCO-OS Memory Monitor Started at $(date) ===" | tee -a "${LOG_FILE}"

while true; do
    timestamp=$(date +%s)
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ -f /proc/meminfo ]; then
        mem_total=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
        mem_free=$(awk '/^MemFree:/ {print $2}' /proc/meminfo)
        mem_used=$((mem_total - mem_free))
        mem_used_pct=$(awk "BEGIN {printf \"%.1f\", ($mem_used * 100.0 / $mem_total)}")
        
        echo "${datetime} | Mem: ${mem_used}/${mem_total} KB (${mem_used_pct}%)" | tee -a "${LOG_FILE}"
        echo "{\"timestamp\":${timestamp},\"mem_total\":${mem_total},\"mem_used\":${mem_used},\"mem_used_pct\":${mem_used_pct}}" >> "${LOG_FILE}.json"
    else
        echo "${datetime} | Mem: N/A" | tee -a "${LOG_FILE}"
    fi
    
    sleep ${INTERVAL}
done
