#!/usr/bin/env bash
###############################################################################
# dskmon.sh - Disk Telemetry Monitor
###############################################################################

INTERVAL="${SAGCO_TELEMETRY_INTERVAL:-5}"
LOG_FILE="${SAGCO_LOG_DIR:-/var/log/sagco}/telemetry/dskmon.log"

echo "=== SAGCO-OS Disk Monitor Started at $(date) ===" | tee -a "${LOG_FILE}"

while true; do
    timestamp=$(date +%s)
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    
    if command -v df &> /dev/null; then
        disk_stats=$(df -h / | awk 'NR==2 {print $2,$3,$4,$5}' | sed 's/%//')
        disk_total=$(echo ${disk_stats} | awk '{print $1}')
        disk_used=$(echo ${disk_stats} | awk '{print $2}')
        disk_free=$(echo ${disk_stats} | awk '{print $3}')
        disk_used_pct=$(echo ${disk_stats} | awk '{print $4}')
        
        echo "${datetime} | Disk: ${disk_used}/${disk_total} (${disk_used_pct}%)" | tee -a "${LOG_FILE}"
        echo "{\"timestamp\":${timestamp},\"disk_total\":\"${disk_total}\",\"disk_used\":\"${disk_used}\",\"disk_used_pct\":${disk_used_pct}}" >> "${LOG_FILE}.json"
    else
        echo "${datetime} | Disk: N/A" | tee -a "${LOG_FILE}"
    fi
    
    sleep ${INTERVAL}
done
