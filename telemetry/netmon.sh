#!/usr/bin/env bash
###############################################################################
# netmon.sh - Network Telemetry Monitor
#
# Monitors network activity and reports metrics for the SAGCO-OS telemetry
# system as part of the OPS1 Operations Mesh subsystem.
#
# Part of: SAGCO-OS Telemetry Arsenal
# DNA: SAGCO-ATG-...-OPS1-...
###############################################################################

INTERVAL="${SAGCO_TELEMETRY_INTERVAL:-5}"
LOG_FILE="${SAGCO_LOG_DIR:-/var/log/sagco}/telemetry/netmon.log"

# Header
echo "=== SAGCO-OS Network Monitor Started at $(date) ===" | tee -a "${LOG_FILE}"

while true; do
    timestamp=$(date +%s)
    datetime=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Network interface statistics (cross-platform)
    if command -v ip &> /dev/null; then
        # Linux with ip command
        rx_bytes=$(cat /sys/class/net/eth0/statistics/rx_bytes 2>/dev/null || echo "0")
        tx_bytes=$(cat /sys/class/net/eth0/statistics/tx_bytes 2>/dev/null || echo "0")
    elif command -v netstat &> /dev/null; then
        # Fallback to netstat
        rx_bytes=$(netstat -ib 2>/dev/null | awk '/^en0/ {print $7}' | head -1 || echo "0")
        tx_bytes=$(netstat -ib 2>/dev/null | awk '/^en0/ {print $10}' | head -1 || echo "0")
    else
        rx_bytes="0"
        tx_bytes="0"
    fi
    
    # Connection count
    if command -v ss &> /dev/null; then
        connections=$(ss -tan | grep ESTAB | wc -l)
    elif command -v netstat &> /dev/null; then
        connections=$(netstat -an 2>/dev/null | grep ESTABLISHED | wc -l)
    else
        connections="0"
    fi
    
    # Format output
    echo "${datetime} | RX: ${rx_bytes} bytes | TX: ${tx_bytes} bytes | Connections: ${connections}" | tee -a "${LOG_FILE}"
    
    # JSON format for machine parsing
    echo "{\"timestamp\":${timestamp},\"rx_bytes\":${rx_bytes},\"tx_bytes\":${tx_bytes},\"connections\":${connections}}" >> "${LOG_FILE}.json"
    
    sleep ${INTERVAL}
done
