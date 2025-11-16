#!/bin/bash
# require_disclaimer.sh - UPL-Safe Disclaimer Enforcement
# Blocks commits without proper disclaimers

set -euo pipefail

file="$1"
disclaimer_text="INTERNAL DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED"

if [[ ! -f "$file" ]]; then
    echo "ERROR: File not found: $file"
    exit 1
fi

# Check for required disclaimer in governance/legal files
if [[ "$file" =~ (governance|templates|upl_compliance|legal).*\.(md|yaml|json|txt)$ ]]; then
    if ! grep -q "$disclaimer_text" "$file"; then
        echo "❌ ERROR: Missing required disclaimer in $file"
        echo "   Required text: $disclaimer_text"
        echo "   Add this disclaimer to the top of the file."
        exit 1
    fi
    echo "✅ Disclaimer check passed for $file"
fi

exit 0