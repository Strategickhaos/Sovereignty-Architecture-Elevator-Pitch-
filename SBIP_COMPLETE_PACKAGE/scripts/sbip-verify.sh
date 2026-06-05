#!/bin/bash
# SBIP Boot Verification Script
# Verifies that SAGCO CPU module loaded successfully

set -euo pipefail

echo "🔥 SBIP Verification Starting..."

# Check if kernel module loaded
if lsmod | grep -q sagco_cpu_mod; then
    echo "✅ SAGCO CPU Module: LOADED"
else
    echo "❌ SAGCO CPU Module: NOT LOADED"
    exit 1
fi

# Verify dmesg contains legal entity declaration
if dmesg | grep -q "Legal Entity: Strategickhaos DAO LLC"; then
    echo "✅ Legal Entity Declaration: VERIFIED"
else
    echo "❌ Legal Entity Declaration: NOT FOUND"
    exit 1
fi

# Verify /proc/sagco/entity exists and is readable
if [ -r /proc/sagco/entity ]; then
    echo "✅ /proc/sagco/entity: ACCESSIBLE"
    cat /proc/sagco/entity
else
    echo "❌ /proc/sagco/entity: NOT ACCESSIBLE"
    exit 1
fi

# Log successful verification
logger -t sbip "Sovereign boot verification: SUCCESS"
echo "✅ SBIP Verification: COMPLETE"

# Write verification timestamp
mkdir -p /var/lib/sbip
echo "$(date -Iseconds)" > /var/lib/sbip/last_verified_boot

exit 0
