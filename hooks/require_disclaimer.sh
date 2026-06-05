#!/bin/bash
# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================

# require_disclaimer.sh - Universal Disclaimer Enforcement
# Blocks commits without proper STRATEGICKHAOS disclaimers

set -euo pipefail

file="$1"
strategickhaos_disclaimer="STRATEGICKHAOS DAO LLC"
legal_disclaimer="INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED"

if [[ ! -f "$file" ]]; then
    echo "ERROR: File not found: $file"
    exit 1
fi

# Check for STRATEGICKHAOS disclaimer in code files
if [[ "$file" =~ \.(py|yaml|yml|sh|rs)$ ]] || [[ "$file" =~ ^Dockerfile ]] || [[ "$file" =~ docker-compose ]]; then
    if ! grep -q "$strategickhaos_disclaimer" "$file"; then
        echo "❌ ERROR: Missing STRATEGICKHAOS disclaimer in $file"
        echo "   Run: python3 add_disclaimers.py"
        echo "   Or manually add the universal disclaimer to the top of the file."
        exit 1
    fi
    echo "✅ STRATEGICKHAOS disclaimer check passed for $file"
fi

# Check for legal disclaimer in governance/legal files
if [[ "$file" =~ (governance|templates|upl_compliance|legal).*\.(md|yaml|json|txt)$ ]]; then
    if ! grep -q "$legal_disclaimer" "$file"; then
        echo "⚠️  WARNING: Consider adding legal disclaimer to $file"
        echo "   Suggested text: $legal_disclaimer"
    fi
fi

exit 0