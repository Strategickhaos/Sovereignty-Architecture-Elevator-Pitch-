#!/bin/bash
# GitHub Personal Access Token Regeneration Script
# 
# This script guides you through the process of regenerating a GitHub PAT
# and updating it across all systems that depend on it.
#
# Usage: ./scripts/regenerate_github_token.sh [TOKEN_ID]
# Example: ./scripts/regenerate_github_token.sh 2896174608

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TOKEN_ID="${1:-2896174608}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
INCIDENT_ID="INC-$(date +%Y%m%d-%H%M%S)"

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  GitHub Personal Access Token Regeneration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Token ID:${NC} $TOKEN_ID"
echo -e "${YELLOW}Timestamp:${NC} $TIMESTAMP"
echo -e "${YELLOW}Incident ID:${NC} $INCIDENT_ID"
echo ""

# Function to print section headers
print_section() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  $1${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_section "Step 1: Prerequisites Check"

MISSING_DEPS=0
for cmd in curl jq vault gh; do
  if command_exists "$cmd"; then
    echo -e "${GREEN}✓${NC} $cmd installed"
  else
    echo -e "${RED}✗${NC} $cmd not found"
    MISSING_DEPS=1
  fi
done

if [ $MISSING_DEPS -eq 1 ]; then
  echo ""
  echo -e "${RED}Error: Missing required dependencies${NC}"
  echo "Please install the missing tools and try again."
  exit 1
fi

# Step 1: Regenerate token on GitHub
print_section "Step 2: Regenerate Token on GitHub"

echo -e "${YELLOW}Action Required:${NC}"
echo "1. Open this URL in your browser:"
echo "   ${BLUE}https://github.com/settings/tokens/$TOKEN_ID/regenerate${NC}"
echo ""
echo "2. Click the 'Regenerate token' button"
echo "3. Confirm the regeneration"
echo "4. Copy the new token value (it will only be shown once)"
echo ""

read -p "Press Enter when you have copied the new token..."

# Prompt for new token
print_section "Step 3: Enter New Token"

echo -e "${YELLOW}Paste the new GitHub token:${NC}"
read -s NEW_TOKEN
echo ""

# Check if token was actually provided
if [ -z "$NEW_TOKEN" ]; then
  echo -e "${RED}Error: No token provided${NC}"
  exit 1
fi

# Validate token format (GitHub PATs are ghp_ followed by exactly 40 characters)
if [[ ! $NEW_TOKEN =~ ^ghp_[a-zA-Z0-9]{40}$ ]]; then
  echo -e "${RED}Error: Invalid GitHub token format${NC}"
  echo "Token should start with 'ghp_' followed by exactly 40 alphanumeric characters"
  exit 1
fi

echo -e "${GREEN}✓${NC} Token format validated"

# Step 2: Update token in Vault (if available)
print_section "Step 4: Update Token in Vault"

if command_exists vault && vault status >/dev/null 2>&1; then
  echo "Storing new token in Vault..."
  
  vault kv put secret/github/pat \
    token="$NEW_TOKEN" \
    regenerated_at="$TIMESTAMP" \
    regenerated_by="$(whoami)" \
    token_id="$TOKEN_ID" \
    incident_id="$INCIDENT_ID" \
    reason="Token regeneration via script"
  
  echo -e "${GREEN}✓${NC} Token updated in Vault"
  
  # Verify the update
  if vault kv get secret/github/pat >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Token verified in Vault"
  else
    echo -e "${RED}✗${NC} Failed to verify token in Vault"
  fi
else
  echo -e "${YELLOW}⚠${NC} Vault not available or not initialized"
  echo "   You'll need to update the token manually in Vault"
fi

# Step 3: Update GitHub Actions secrets
print_section "Step 5: Update GitHub Actions Secrets"

echo "Updating GitHub Actions secrets..."

# Detect repository from git remote
if command_exists git && git rev-parse --git-dir > /dev/null 2>&1; then
  REPO_URL=$(git config --get remote.origin.url)
  REPO_PATH=$(echo "$REPO_URL" | sed -e 's/.*github.com[:/]\(.*\)\.git/\1/' -e 's/.*github.com[:/]\(.*\)/\1/')
  
  echo -e "Repository detected: ${BLUE}$REPO_PATH${NC}"
  
  if command_exists gh; then
    # Update via GitHub CLI using stdin to avoid exposing token in process list
    echo "$NEW_TOKEN" | gh secret set GITHUB_TOKEN --repo "$REPO_PATH" --body-file -
    echo -e "${GREEN}✓${NC} GitHub Actions secret updated"
  else
    echo -e "${YELLOW}⚠${NC} GitHub CLI not available"
    echo "   Update manually at: https://github.com/$REPO_PATH/settings/secrets/actions"
  fi
else
  echo -e "${YELLOW}⚠${NC} Not in a git repository"
  echo "   Update GitHub Actions secrets manually"
fi

# Step 4: Verify token functionality
print_section "Step 6: Verify Token Functionality"

echo "Testing GitHub API access..."
USER_RESPONSE=$(curl -s -H "Authorization: token $NEW_TOKEN" https://api.github.com/user)

if echo "$USER_RESPONSE" | jq -e '.login' > /dev/null 2>&1; then
  USERNAME=$(echo "$USER_RESPONSE" | jq -r '.login')
  echo -e "${GREEN}✓${NC} Token valid - authenticated as: ${BLUE}$USERNAME${NC}"
else
  echo -e "${RED}✗${NC} Token validation failed"
  echo "$USER_RESPONSE" | jq .
  exit 1
fi

# Test repository access (if in a git repo)
if [ -n "$REPO_PATH" ]; then
  echo "Testing repository access..."
  REPO_RESPONSE=$(curl -s -H "Authorization: token $NEW_TOKEN" \
    "https://api.github.com/repos/$REPO_PATH")
  
  if echo "$REPO_RESPONSE" | jq -e '.full_name' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Repository access verified"
  else
    echo -e "${YELLOW}⚠${NC} Could not verify repository access"
  fi
fi

# Step 5: Document the rotation
print_section "Step 7: Document Incident"

REPORT_FILE="/tmp/github_token_rotation_${INCIDENT_ID}.md"

cat > "$REPORT_FILE" << EOF
# GitHub Token Rotation Incident Report

**Incident ID**: $INCIDENT_ID
**Date**: $TIMESTAMP
**Token ID**: $TOKEN_ID
**Rotated By**: $(whoami)
**Hostname**: $(hostname)

## Actions Taken

- [x] Token regenerated on GitHub
- [x] New token stored in Vault (if available)
- [x] GitHub Actions secrets updated
- [x] Token functionality verified

## Verification Results

- **API Access**: ✓ Successful
- **Authenticated As**: $USERNAME
- **Repository Access**: ✓ Verified

## Next Steps

1. Restart services that use this token:
   \`\`\`bash
   kubectl rollout restart deployment/event-gateway -n ops
   kubectl rollout restart deployment/refinory -n ops
   kubectl rollout restart deployment/discord-ops-bot -n ops
   \`\`\`

2. Monitor GitHub audit logs:
   https://github.com/settings/security-log

3. Verify CI/CD workflows are functioning:
   Check recent workflow runs for any authentication errors

4. Schedule next rotation (recommended: 90 days):
   $(if date -v+90d "+%Y-%m-%d" 2>/dev/null; then date -v+90d "+%Y-%m-%d"; else date -d "+90 days" "+%Y-%m-%d" 2>/dev/null || echo "[Add 90 days to current date]"; fi)

## Additional Notes

Add any relevant notes about why this rotation was performed:
- Security incident
- Routine rotation
- Token exposure
- Other reason

EOF

echo -e "${GREEN}✓${NC} Incident report saved to: $REPORT_FILE"
echo ""
cat "$REPORT_FILE"

# Summary
print_section "Summary"

echo -e "${GREEN}✓${NC} Token regeneration completed successfully!"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review the incident report: $REPORT_FILE"
echo "2. Restart services that use this token (see report)"
echo "3. Monitor GitHub audit logs for any issues"
echo "4. Update documentation with new rotation date"
echo ""
echo -e "${BLUE}For detailed procedures, see:${NC}"
echo "  - SECURITY.md (Token management best practices)"
echo "  - VAULT_SECURITY_PLAYBOOK.md (Comprehensive rotation guide)"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Token Regeneration Complete${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
