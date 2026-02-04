#!/bin/bash
# SBIP Installation Verification Script
# Strategickhaos DAO LLC - Ratio Ex Nihilo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================================="
echo "   SAGCO Boot Identity Pipeline"
echo "   Installation Verification v1.0"
echo "=================================================="
echo ""

FAILED=0
PASSED=0

# Helper function to check status
check_status() {
    local name="$1"
    local command="$2"
    
    echo -n "Checking $name... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Check kernel module source
echo "=== Kernel Module ==="
check_status "Kernel module source" "test -f '$SCRIPT_DIR/kernel/sagco_cpu_mod.c'"
check_status "Kernel Makefile" "test -f '$SCRIPT_DIR/kernel/Makefile'"

# Check if we can build (requires headers)
if [ -d "/lib/modules/$(uname -r)/build" ]; then
    echo -n "Checking kernel headers... "
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED=$((PASSED + 1))
else
    echo -n "Checking kernel headers... "
    echo -e "${YELLOW}⚠ NOT INSTALLED${NC} (install with: apt install linux-headers-\$(uname -r))"
fi

echo ""
echo "=== Compiler ==="
check_status "Compiler source" "test -f '$SCRIPT_DIR/compiler/flamelang_to_llvm.py'"
check_status "Compiler executable bit" "test -x '$SCRIPT_DIR/compiler/flamelang_to_llvm.py'"

# Check Python
if command -v python3 &>/dev/null; then
    echo -n "Checking Python 3... "
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ PASS${NC} (version: $PYTHON_VERSION)"
    PASSED=$((PASSED + 1))
    
    # Check llvmlite
    echo -n "Checking llvmlite... "
    if python3 -c "import llvmlite" 2>/dev/null; then
        LLVM_VERSION=$(python3 -c "import llvmlite; print(llvmlite.__version__)" 2>/dev/null)
        echo -e "${GREEN}✓ PASS${NC} (version: $LLVM_VERSION)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (install with: pip3 install llvmlite)"
        FAILED=$((FAILED + 1))
    fi
else
    echo -n "Checking Python 3... "
    echo -e "${RED}✗ FAIL${NC}"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Systemd Services ==="
check_status "sagco-banner.service" "test -f '$SCRIPT_DIR/systemd/sagco-banner.service'"
check_status "sagco-runtime.service" "test -f '$SCRIPT_DIR/systemd/sagco-runtime.service'"
check_status "sagco-compiler.service" "test -f '$SCRIPT_DIR/systemd/sagco-compiler.service'"
check_status "sagco-cpu.service" "test -f '$SCRIPT_DIR/systemd/sagco-cpu.service'"

# Check if systemd-analyze is available
if command -v systemd-analyze &>/dev/null; then
    echo -n "Validating service syntax... "
    VALID=true
    for service in "$SCRIPT_DIR/systemd"/*.service; do
        if ! systemd-analyze verify "$service" 2>&1 | grep -q "Failed"; then
            :
        else
            VALID=false
            break
        fi
    done
    
    if [ "$VALID" = true ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
    fi
fi

echo ""
echo "=== Boot Configuration ==="
check_status "GRUB theme" "test -f '$SCRIPT_DIR/boot/grub-theme/theme.txt'"

echo ""
echo "=== Documentation ==="
check_status "README.md" "test -f '$SCRIPT_DIR/README.md'"
check_status "SBIP_SPECIFICATION.md" "test -f '$SCRIPT_DIR/SBIP_SPECIFICATION.md'"

echo ""
echo "=== Functional Tests ==="

# Test compiler if llvmlite is available
if python3 -c "import llvmlite" 2>/dev/null; then
    echo -n "Testing compiler (add 5 3)... "
    RESULT=$("$SCRIPT_DIR/compiler/flamelang_to_llvm.py" --eval "add 5 3" 2>/dev/null | grep -oP 'Result: \K\d+')
    if [ "$RESULT" = "8" ]; then
        echo -e "${GREEN}✓ PASS${NC} (result: $RESULT)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (expected: 8, got: $RESULT)"
        FAILED=$((FAILED + 1))
    fi
    
    echo -n "Testing compiler (mul 7 8)... "
    RESULT=$("$SCRIPT_DIR/compiler/flamelang_to_llvm.py" --eval "mul 7 8" 2>/dev/null | grep -oP 'Result: \K\d+')
    if [ "$RESULT" = "56" ]; then
        echo -e "${GREEN}✓ PASS${NC} (result: $RESULT)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (expected: 56, got: $RESULT)"
        FAILED=$((FAILED + 1))
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC} compiler tests (llvmlite not available)"
fi

echo ""
echo "=================================================="
echo "   VERIFICATION SUMMARY"
echo "=================================================="
echo -e "Tests passed: ${GREEN}$PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "Tests failed: ${RED}$FAILED${NC}"
else
    echo -e "Tests failed: $FAILED"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Build kernel module: cd kernel && make"
    echo "  2. Install services: sudo cp systemd/*.service /etc/systemd/system/"
    echo "  3. Enable services: sudo systemctl enable sagco-banner sagco-runtime"
    echo "  4. Install compiler: sudo cp compiler/flamelang_to_llvm.py /usr/local/bin/"
    echo "  5. Reboot and verify: systemctl status sagco-*"
    exit 0
else
    echo -e "${RED}✗ SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please review the failures above and install missing dependencies."
    exit 1
fi
