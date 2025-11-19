#!/bin/bash
###############################################################################
# DoLM Installation Verification Script
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "DoLM Installation Verification"
echo "==============================="
echo

# Check Docker
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ Docker daemon not running${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Docker not installed${NC}"
    exit 1
fi

# Check Python
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ (${PYTHON_VERSION})${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

# Check watchdog package
echo -n "Checking watchdog package... "
if python3 -c "import watchdog" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}✗ Not installed (optional for testing)${NC}"
fi

# Check files
echo -n "Checking dolm_daemon.py... "
if [ -f "dolm_daemon.py" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    exit 1
fi

echo -n "Checking Dockerfile... "
if [ -f "Dockerfile" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    exit 1
fi

echo -n "Checking activation scripts... "
if [ -f "activate-dolm.sh" ] && [ -f "activate-dolm.ps1" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    exit 1
fi

# Check if container is running
echo -n "Checking if DoLM daemon is running... "
if docker ps --format '{{.Names}}' | grep -q "^dolm-daemon$"; then
    echo -e "${GREEN}✓ Running${NC}"
    
    # Show logs
    echo
    echo "Recent logs:"
    docker logs --tail 5 dolm-daemon
    
    # Check vault
    VAULT_PATH="${DOLM_VAULT_PATH:-$HOME/strategic-khaos-private/dolm-vault}"
    echo
    echo -n "Checking vault at $VAULT_PATH... "
    if [ -d "$VAULT_PATH" ]; then
        echo -e "${GREEN}✓${NC}"
        echo "  TODOs: $(find $VAULT_PATH/todos -name "*.md" 2>/dev/null | wc -l) notes"
        echo "  Errors: $(find $VAULT_PATH/errors -name "*.md" 2>/dev/null | wc -l) notes"
    else
        echo -e "${YELLOW}✗ Not found${NC}"
    fi
else
    echo -e "${YELLOW}✗ Not running${NC}"
    echo
    echo "To start DoLM, run:"
    echo "  ./activate-dolm.sh"
fi

echo
echo -e "${GREEN}Verification complete!${NC}"
