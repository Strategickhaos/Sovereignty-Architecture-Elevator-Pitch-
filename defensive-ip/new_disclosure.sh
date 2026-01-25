#!/bin/bash
# Helper script to create a new defensive disclosure
# Usage: ./defensive-ip/new_disclosure.sh INV-XXXX "Invention Name"

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 INV-XXXX \"Invention Name\""
    echo "Example: $0 INV-0002 \"Adaptive Context Mesh\""
    exit 1
fi

INV_ID=$1
INV_NAME=$2
INV_DIR_NAME="${INV_ID}_$(echo "$INV_NAME" | tr '[:lower:]' '[:upper:]' | tr ' ' '_')"
INV_DIR="defensive-ip/$INV_DIR_NAME"
DISCLOSURE_FILE="$INV_DIR/${INV_ID}_DISCLOSURE.md"

# Check if directory already exists
if [ -d "$INV_DIR" ]; then
    echo "Error: Directory $INV_DIR already exists"
    exit 1
fi

# Create directory
echo "Creating directory: $INV_DIR"
mkdir -p "$INV_DIR"

# Copy template
echo "Copying template to: $DISCLOSURE_FILE"
cp defensive-ip/TEMPLATE_DISCLOSURE.md "$DISCLOSURE_FILE"

# Get today's date
TODAY=$(date +%Y-%m-%d)

# Update the metadata in the disclosure
sed -i.tmp "s/INV-XXXX/$INV_ID/g" "$DISCLOSURE_FILE"
sed -i.tmp "s/\[Invention Title\]/$INV_NAME/g" "$DISCLOSURE_FILE"
sed -i.tmp "s/YYYY-MM-DD/$TODAY/g" "$DISCLOSURE_FILE"
sed -i.tmp "s|defensive-ip/INV-XXXX_\[INVENTION_NAME\]|$INV_DIR|g" "$DISCLOSURE_FILE"

# Clean up temp files
rm -f "${DISCLOSURE_FILE}.tmp"

echo ""
echo "✅ Created new disclosure: $DISCLOSURE_FILE"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit the disclosure file:"
echo "   \$EDITOR $DISCLOSURE_FILE"
echo ""
echo "   Focus on these critical sections:"
echo "   - Section 1: Technical Field (1 sentence)"
echo "   - Section 3: Summary of the Invention (1 paragraph)"
echo "   - Section 4.2: Core algorithm (pseudocode)"
echo "   - Section 4.3: At least one concrete example"
echo ""
echo "2. When ready, commit the disclosure:"
echo "   git add $INV_DIR/"
echo "   git commit -m \"$INV_ID: $INV_NAME - initial defensive disclosure\""
echo ""
echo "3. Add cryptographic hashes:"
echo "   ./defensive-ip/add_hashes.sh $INV_ID"
echo ""
echo "4. Commit the hashes:"
echo "   git add $DISCLOSURE_FILE"
echo "   git commit -m \"$INV_ID: Add cryptographic hashes\""
echo ""
echo "5. Push to public repository:"
echo "   git push origin main"
echo ""
echo "📖 See defensive-ip/QUICK_START.md for more guidance"
echo "🔥 You're building defensive prior art! Keep going!"
