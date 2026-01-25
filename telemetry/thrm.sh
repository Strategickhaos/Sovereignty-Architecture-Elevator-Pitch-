#!/usr/bin/env bash
###############################################################################
# thrm.sh - Thermal Telemetry Monitor
###############################################################################

INTERVAL="${SAGCO_TELEMETRY_INTERVAL:-5}"
LOG_FILE="${SAGCO_LOG_DIR:-/var/log/sagco}/telemetry/thrm.log"

echo "=== SAGCO-OS Thermal Monitor Started at $(date) ===" | tee -a "${LOG_FILE}"

get_cpu_temp() {
    if [ -d /sys/class/thermal ]; then
        for zone in /sys/class/thermal/thermal_zone*/temp; do
            if [ -f "${zone}" ]; then
                temp=$(cat "${zone}")
                temp_c=$((temp / 1000))
                if [ ${temp_c} -gt 0 ] && [ ${temp_c} -lt 150 ]; then
                    echo ${temp_c}
                    return
                fi
            fi
        done
    fi
    echo "0"
}

while true; do
    timestamp=$(date +%s)
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    
    cpu_temp=$(get_cpu_temp)
    
    if [ ${cpu_temp} -gt 0 ]; then
        if [ ${cpu_temp} -lt 60 ]; then
            thermal_status="NORMAL"
        elif [ ${cpu_temp} -lt 75 ]; then
            thermal_status="WARM"
        elif [ ${cpu_temp} -lt 90 ]; then
            thermal_status="HOT"
        else
            thermal_status="CRITICAL"
        fi
        echo "${datetime} | CPU Temp: ${cpu_temp}°C | Status: ${thermal_status}" | tee -a "${LOG_FILE}"
    else
        thermal_status="UNKNOWN"
        echo "${datetime} | CPU Temp: N/A | Status: ${thermal_status}" | tee -a "${LOG_FILE}"
    fi
    
    echo "{\"timestamp\":${timestamp},\"cpu_temp\":${cpu_temp},\"thermal_status\":\"${thermal_status}\"}" >> "${LOG_FILE}.json"
    
    sleep ${INTERVAL}
done
