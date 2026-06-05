#!/bin/bash
# SBIP Audit Log Script
# Logs sovereignty verification events

set -euo pipefail

AUDIT_LOG="/var/log/sbip/boot_audit.log"

# Create audit log directory
mkdir -p /var/log/sbip

# Write audit entry
{
    echo "════════════════════════════════════════════════════════════"
    echo "SBIP Boot Audit Entry"
    echo "════════════════════════════════════════════════════════════"
    echo "Timestamp: $(date -Iseconds)"
    echo "Boot ID: $(cat /proc/sys/kernel/random/boot_id 2>/dev/null || echo 'unavailable')"
    echo "Hostname: $(hostname)"
    echo "Kernel: $(uname -r)"
    echo ""
    echo "Sovereignty Status:"
    if [ -f /proc/sagco/entity ]; then
        cat /proc/sagco/entity | sed 's/^/  /'
    else
        echo "  ❌ /proc/sagco/entity not found"
    fi
    echo ""
    echo "Module Status:"
    lsmod | grep sagco_cpu_mod | sed 's/^/  /' || echo "  ❌ sagco_cpu_mod not loaded"
    echo ""
    echo "════════════════════════════════════════════════════════════"
} >> "$AUDIT_LOG"

# Also log to syslog
logger -t sbip-audit "Boot audit entry written to $AUDIT_LOG"

echo "✅ Audit log written to $AUDIT_LOG"

exit 0
