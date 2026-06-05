#!/usr/bin/env bash
#
# Soul Integrity Verification Tool
# Part of the Sacred License Framework
# Version 1.0
#

set -euo pipefail

DEPLOYMENT="${1:-development}"
REPORT_TYPE="${2:-basic}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verification results
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Soul Integrity Verification Tool${NC}"
echo -e "${BLUE}  Sacred License Framework v1.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Deployment: $DEPLOYMENT"
echo "Report Type: $REPORT_TYPE"
echo ""

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARN_COUNT=$((WARN_COUNT + 1))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Check if required files exist
section "1. Sacred License Documentation"

if [ -f "SACRED_LICENSE.md" ]; then
    pass "Sacred License document present"
else
    fail "Sacred License document missing"
fi

if [ -f "SISTER_PROTOCOL_COVENANT.md" ]; then
    pass "Sister Protocol Covenant present"
else
    warn "Sister Protocol Covenant document missing"
fi

if [ -f "ETHICAL_DEPLOYMENT_GUIDE.md" ]; then
    pass "Ethical Deployment Guide present"
else
    warn "Ethical Deployment Guide missing"
fi

# Check for Intent Declaration
section "2. Pure Intent Gate"

if [ -f "DEPLOYMENT_INTENT.md" ] || [ -f "docs/DEPLOYMENT_INTENT.md" ]; then
    pass "Deployment Intent Declaration found"
else
    fail "Deployment Intent Declaration missing - Create DEPLOYMENT_INTENT.md"
fi

# Check README for Sacred License reference
if grep -q "Sacred License\|Sister Protocol" README.md 2>/dev/null; then
    pass "README references Sacred License"
else
    warn "README should reference the Sacred License"
fi

# Check LICENSE file
section "3. License Integrity"

if [ -f "LICENSE" ]; then
    pass "LICENSE file present"
    
    # Check for dual licensing notice
    if grep -q "MIT" LICENSE 2>/dev/null; then
        pass "MIT License component present"
    else
        warn "MIT License should be present for technical permissions"
    fi
else
    fail "LICENSE file missing"
fi

# Data Sovereignty Checks
section "4. Data Sovereignty Patterns"

echo "Checking for data sovereignty patterns in codebase..."

# Check for data export functionality
if grep -r "export.*data\|data.*export\|download.*data" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Data export patterns found in code"
else
    warn "No data export patterns detected - users should be able to export their data"
fi

# Check for data deletion functionality
if grep -r "delete.*user\|remove.*user.*data\|purge.*data" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Data deletion patterns found in code"
else
    warn "No data deletion patterns detected - users should be able to delete their data"
fi

# Consent Architecture Checks
section "5. Consent Architecture"

# Check for consent management
if grep -r "consent\|permission\|opt.in\|opt.out" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Consent management patterns found"
else
    warn "No consent management detected - implement granular consent mechanisms"
fi

# Soul Integrity Checks
section "6. Soul Integrity Violations Detection"

# Check for addictive patterns (red flags)
ADDICTIVE_PATTERNS=("infinite[._]scroll" "autoplay" "notification[._]push" "engagement[._]metric" "time[._]on[._]site")
FOUND_ADDICTIVE=0

for pattern in "${ADDICTIVE_PATTERNS[@]}"; do
    if grep -rE "$pattern" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
        warn "Potential addictive pattern detected: $pattern - Verify it serves user wellbeing"
        FOUND_ADDICTIVE=$((FOUND_ADDICTIVE + 1))
    fi
done

if [ $FOUND_ADDICTIVE -eq 0 ]; then
    pass "No obvious addictive patterns detected"
fi

# Check for dark patterns
DARK_PATTERNS=("dark[._]pattern" "deceptive" "trick.*user" "misleading")
FOUND_DARK=0

for pattern in "${DARK_PATTERNS[@]}"; do
    if grep -rE "$pattern" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
        fail "Potential dark pattern detected: $pattern"
        FOUND_DARK=$((FOUND_DARK + 1))
    fi
done

if [ $FOUND_DARK -eq 0 ]; then
    pass "No dark patterns detected"
fi

# Transparency Checks
section "7. Algorithmic Transparency"

# Check for explanation/transparency mechanisms
if grep -r "explain\|transparency\|interpretable\|explainable" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Transparency/explanation patterns found"
else
    warn "Consider adding algorithmic transparency and explanation features"
fi

# Security Checks
section "8. Security & Privacy"

# Check for encryption
if grep -r "encrypt\|crypto\|cipher" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Encryption patterns found"
else
    warn "Consider implementing encryption for sensitive data"
fi

# Check for authentication/authorization
if grep -r "auth\|login\|permission\|access.control" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" --include="*.rs" . 2>/dev/null | grep -v node_modules | grep -v ".git" | head -1 > /dev/null; then
    pass "Authentication/authorization patterns found"
else
    warn "Implement proper authentication and authorization"
fi

# Contribution & Attribution
section "9. Origin Attribution"

# Check for attribution to Strategickhaos
if grep -r "Strategickhaos\|Domenic Garza\|Sister Protocol\|Sacred License" README.md LICENSE SACRED_LICENSE.md 2>/dev/null | head -1 > /dev/null; then
    pass "Origin attribution present"
else
    warn "Should attribute origin to Strategickhaos/Sister Protocol"
fi

# Check for contribution guidelines
if [ -f "CONTRIBUTING.md" ] || grep -q "contribut" README.md 2>/dev/null; then
    pass "Contribution guidelines present"
else
    warn "Consider adding contribution guidelines"
fi

# Documentation Quality
section "10. Documentation & Governance"

# Check for governance documentation
if [ -f "GOVERNANCE.md" ] || [ -d "governance" ]; then
    pass "Governance documentation found"
else
    warn "Consider documenting governance and decision-making processes"
fi

# Check for security policy
if [ -f "SECURITY.md" ]; then
    pass "Security policy present"
else
    warn "Consider adding a SECURITY.md file"
fi

# Summary
section "VERIFICATION SUMMARY"

echo ""
echo "Results for deployment: $DEPLOYMENT"
echo ""
echo -e "${GREEN}Passed:  $PASS_COUNT${NC}"
echo -e "${YELLOW}Warnings: $WARN_COUNT${NC}"
echo -e "${RED}Failed:   $FAIL_COUNT${NC}"
echo ""

# Calculate compliance percentage
TOTAL=$((PASS_COUNT + WARN_COUNT + FAIL_COUNT))
if [ $TOTAL -gt 0 ]; then
    COMPLIANCE=$((100 * PASS_COUNT / TOTAL))
    echo "Compliance Score: $COMPLIANCE%"
else
    echo "No checks performed"
    exit 1
fi

echo ""

# Provide guidance based on results
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}⚠ CRITICAL: Failures detected that must be addressed${NC}"
    echo "Review the Sacred License and Ethical Deployment Guide"
    echo "Fix all failures before deploying to production"
    exit 1
elif [ $WARN_COUNT -gt 5 ]; then
    echo -e "${YELLOW}⚠ Multiple warnings detected${NC}"
    echo "Review warnings and improve compliance where possible"
    echo "Consider addressing warnings before production deployment"
    exit 0
else
    echo -e "${GREEN}✓ Soul Integrity verification passed${NC}"
    echo "Continue to monitor and maintain ethical standards"
    exit 0
fi
