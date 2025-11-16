#!/bin/bash
# require_gpg.sh - GPG Signature Verification
# Ensures critical documents are GPG signed

set -euo pipefail

sig_file="$1"

# Verify the signature file exists and is valid
if [[ ! -f "$sig_file" ]]; then
    echo "❌ ERROR: Signature file not found: $sig_file"
    exit 1
fi

# Extract the original file name (remove .asc or .sig extension)
if [[ "$sig_file" =~ \.asc$ ]]; then
    original_file="${sig_file%.asc}"
elif [[ "$sig_file" =~ \.sig$ ]]; then
    original_file="${sig_file%.sig}"
else
    echo "❌ ERROR: Invalid signature file extension: $sig_file"
    echo "   Expected .asc or .sig extension"
    exit 1
fi

# Check if original file exists
if [[ ! -f "$original_file" ]]; then
    echo "❌ ERROR: Original file not found for signature: $original_file"
    exit 1
fi

# Verify GPG signature
if gpg --verify "$sig_file" "$original_file" >/dev/null 2>&1; then
    signer=$(gpg --verify "$sig_file" "$original_file" 2>&1 | grep 'Good signature' | sed 's/.*from "\([^"]*\)".*/\1/')
    echo "✅ Valid GPG signature from: $signer"
    echo "   File: $original_file"
    echo "   Signature: $sig_file"
else
    echo "❌ ERROR: Invalid or missing GPG signature for $original_file"
    echo "   Signature file: $sig_file"
    echo "   All approved documents must be GPG signed."
    exit 1
fi

exit 0