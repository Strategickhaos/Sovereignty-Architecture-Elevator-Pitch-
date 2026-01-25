#!/bin/bash
# Helper script to add hashes to a disclosure after committing
# Usage: ./defensive-ip/add_hashes.sh INV-XXXX

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 INV-XXXX"
    echo "Example: $0 INV-0002"
    exit 1
fi

INV_ID=$1
DISCLOSURE_DIR="defensive-ip/${INV_ID}_*"
DISCLOSURE_FILE=$(find defensive-ip -name "${INV_ID}_DISCLOSURE.md" | head -n 1)

if [ -z "$DISCLOSURE_FILE" ]; then
    echo "Error: Could not find disclosure file for $INV_ID"
    exit 1
fi

echo "Found disclosure: $DISCLOSURE_FILE"

# Get the commit SHA
COMMIT_SHA=$(git rev-parse HEAD)
echo "Commit SHA: $COMMIT_SHA"

# Get the file hash
FILE_HASH=$(sha256sum "$DISCLOSURE_FILE" | awk '{print $1}')
echo "File SHA256: $FILE_HASH"

# Get timestamp
TIMESTAMP=$(git log -1 --format=%cI HEAD)
echo "Timestamp: $TIMESTAMP"

# Get repository URL
REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
echo "Repository: $REPO_URL"

# Create backup
cp "$DISCLOSURE_FILE" "${DISCLOSURE_FILE}.backup"

# Update the hashes in the file
# This uses sed to replace the placeholder text
sed -i.tmp "/^git_commit_sha:/s|:.*|: $COMMIT_SHA|" "$DISCLOSURE_FILE"
sed -i.tmp "/^file_sha256:/s|:.*|: $FILE_HASH|" "$DISCLOSURE_FILE"
sed -i.tmp "/^timestamp:/s|:.*|: $TIMESTAMP|" "$DISCLOSURE_FILE"

# If repository line doesn't exist, add it
if ! grep -q "^repository:" "$DISCLOSURE_FILE"; then
    sed -i.tmp "/^timestamp:.*/a repository:     $REPO_URL" "$DISCLOSURE_FILE"
else
    sed -i.tmp "/^repository:/s|:.*|: $REPO_URL|" "$DISCLOSURE_FILE"
fi

# Clean up temp files
rm -f "${DISCLOSURE_FILE}.tmp"

echo ""
echo "Hashes added to $DISCLOSURE_FILE"
echo ""
echo "Next steps:"
echo "1. Review the changes:"
echo "   git diff $DISCLOSURE_FILE"
echo ""
echo "2. Commit the updated hashes:"
echo "   git add $DISCLOSURE_FILE"
echo "   git commit -m \"$INV_ID: Add cryptographic hashes\""
echo ""
echo "3. Push to public repository:"
echo "   git push origin main"
echo ""
echo "Your disclosure is now cryptographically timestamped! 🔥"
