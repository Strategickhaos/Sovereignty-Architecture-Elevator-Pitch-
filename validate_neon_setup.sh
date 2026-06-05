#!/bin/bash
# Neon Database Integration Validation Script
# This script checks that all Neon configuration files are in place

set -e

echo "=================================================="
echo "Neon Database Integration Validation"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} Found: $1"
        return 0
    else
        echo -e "${RED}✗${NC} Missing: $1"
        return 1
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $1 contains: $2"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing: $2"
        return 1
    fi
}

echo "Checking required files..."
echo ""

all_checks_passed=true

# Check documentation files
check_file "NEON_DATABASE_SETUP.md" || all_checks_passed=false
check_file "QUICKSTART_NEON.md" || all_checks_passed=false

echo ""

# Check configuration files
check_file ".env.example" || all_checks_passed=false
check_file "docker-compose.neon.yml" || all_checks_passed=false
check_file "test_neon_connection.py" || all_checks_passed=false

echo ""

# Check database configuration updates
echo "Checking configuration updates..."
echo ""

check_content ".env.example" "DATABASE_URL" || all_checks_passed=false
check_content ".env.example" "neon.tech" || all_checks_passed=false
check_content "refinory/refinory/config.py" "DATABASE_URL" || all_checks_passed=false
check_content "bootstrap/k8s/secrets.yaml" "DATABASE_URL" || all_checks_passed=false
check_content "bootstrap/k8s/bot-deployment.yaml" "DATABASE_URL" || all_checks_passed=false

echo ""

# Check if test script is executable
if [ -x "test_neon_connection.py" ]; then
    echo -e "${GREEN}✓${NC} test_neon_connection.py is executable"
else
    echo -e "${YELLOW}⚠${NC}  test_neon_connection.py is not executable (run: chmod +x test_neon_connection.py)"
fi

echo ""

# Check README updates
echo "Checking documentation updates..."
echo ""

check_content "README.md" "Neon" || all_checks_passed=false
check_content "README.md" "NEON_DATABASE_SETUP.md" || all_checks_passed=false

echo ""

# Summary
echo "=================================================="
if [ "$all_checks_passed" = true ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Neon database integration is properly configured."
    echo ""
    echo "Next steps:"
    echo "  1. Get your Neon connection string from:"
    echo "     https://console.neon.tech (navigate to your project)"
    echo "  2. Update .env with your DATABASE_URL"
    echo "  3. Run: python test_neon_connection.py"
    echo "  4. Deploy: docker-compose -f docker-compose.neon.yml up -d"
    echo ""
    echo "For detailed instructions, see QUICKSTART_NEON.md"
    exit 0
else
    echo -e "${RED}✗ Some checks failed!${NC}"
    echo ""
    echo "Please ensure all required files are in place."
    exit 1
fi
