#!/bin/bash
# verify_ledger_signature.sh - Verify embedded GPG signature in YAML ledger
# Part of Appendix C: Legal Standards for AI Conversation Logs
# Usage: ./verify_ledger_signature.sh <ledger_file.yml>

set -e

LEDGER_FILE="${1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file exists
if [ -z "$LEDGER_FILE" ] || [ ! -f "$LEDGER_FILE" ]; then
    echo -e "${RED}Error: Ledger file not found${NC}"
    echo "Usage: $0 <ledger_file.yml>"
    exit 1
fi

echo -e "${YELLOW}Verifying ledger signature: ${LEDGER_FILE}${NC}"

# Extract content before signature
if ! sed '/^signatures:/,$d' "$LEDGER_FILE" > /tmp/ledger_content_$$.yml; then
    echo -e "${RED}Error: Could not extract content${NC}"
    exit 1
fi

# Extract signature
if ! grep -A 100 "signature: |" "$LEDGER_FILE" | grep -v "signature: |" | sed 's/^      //' > /tmp/ledger_signature_$$.asc; then
    echo -e "${RED}Error: Could not extract signature${NC}"
    rm /tmp/ledger_content_$$.yml
    exit 1
fi

# Check if signature was found
if [ ! -s /tmp/ledger_signature_$$.asc ]; then
    echo -e "${RED}Error: No signature found in ledger${NC}"
    echo "Sign the ledger with: ./sign_ledger_entry.sh $LEDGER_FILE"
    rm /tmp/ledger_content_$$.yml /tmp/ledger_signature_$$.asc
    exit 1
fi

# Verify signature
echo "Verifying GPG signature..."
if gpg --verify /tmp/ledger_signature_$$.asc /tmp/ledger_content_$$.yml 2>&1; then
    echo ""
    echo -e "${GREEN}✓ Signature verification PASSED${NC}"
    echo -e "${GREEN}  Ledger entry is authentic and unmodified${NC}"
    
    # Extract and display key info
    KEY_ID=$(grep "key_id:" "$LEDGER_FILE" | head -1 | sed 's/.*: "\(.*\)"/\1/')
    SIGNER=$(grep "signer:" "$LEDGER_FILE" | head -1 | sed 's/.*: "\(.*\)"/\1/')
    SIGNED_AT=$(grep "signed_at:" "$LEDGER_FILE" | head -1 | sed 's/.*: "\(.*\)"/\1/')
    
    echo ""
    echo "Signature details:"
    echo "  Signer: $SIGNER"
    echo "  Key ID: $KEY_ID"
    echo "  Signed at: $SIGNED_AT"
    
    rm /tmp/ledger_content_$$.yml /tmp/ledger_signature_$$.asc
    exit 0
else
    echo ""
    echo -e "${RED}✗ Signature verification FAILED${NC}"
    echo -e "${RED}  Warning: Ledger may have been tampered with!${NC}"
    rm /tmp/ledger_content_$$.yml /tmp/ledger_signature_$$.asc
    exit 1
fi
