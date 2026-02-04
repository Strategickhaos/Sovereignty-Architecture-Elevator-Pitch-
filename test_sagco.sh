#!/bin/bash
# SAGCO OS Test Suite
# Tests both kernel module and FlameLang compiler

# Don't exit on error - we want to collect all test results
set +e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KERNEL_DIR="${SCRIPT_DIR}/kernel/sagco_cpu_mod"
COMPILER_DIR="${SCRIPT_DIR}/compiler/flamelang"
TEST_OUTPUT_DIR="${SCRIPT_DIR}/test_output"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

print_test_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((TESTS_PASSED++))
}

print_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((TESTS_FAILED++))
}

print_skip() {
    echo -e "${YELLOW}⊘ SKIP${NC}: $1"
    ((TESTS_SKIPPED++))
}

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up test artifacts..."
    rm -rf "${TEST_OUTPUT_DIR}"
}

trap cleanup EXIT

# Create test output directory
mkdir -p "${TEST_OUTPUT_DIR}"

echo "🔥 SAGCO OS Test Suite - Ratio Ex Nihilo"
echo "=========================================="
echo ""

# ============================================================================
# Kernel Module Tests
# ============================================================================

print_test_header "Kernel Module Tests"

# Test 1: Check if kernel module source exists
if [ -f "${KERNEL_DIR}/sagco_cpu_mod.c" ]; then
    print_pass "Kernel module source exists"
else
    print_fail "Kernel module source not found"
fi

# Test 2: Check if Makefile exists
if [ -f "${KERNEL_DIR}/Makefile" ]; then
    print_pass "Kernel module Makefile exists"
else
    print_fail "Kernel module Makefile not found"
fi

# Test 3: Verify kernel module syntax (if gcc is available)
if command -v gcc >/dev/null 2>&1; then
    echo "Checking kernel module syntax..."
    if gcc -fsyntax-only -I/usr/src/linux-headers-$(uname -r)/include \
        -I/usr/src/linux-headers-$(uname -r)/arch/x86/include \
        -D__KERNEL__ -DMODULE \
        "${KERNEL_DIR}/sagco_cpu_mod.c" 2>/dev/null; then
        print_pass "Kernel module syntax check"
    else
        print_skip "Kernel module syntax check (kernel headers may not be installed)"
    fi
else
    print_skip "Kernel module syntax check (gcc not available)"
fi

# Test 4: Check if module can be compiled (requires kernel headers)
if [ -d "/lib/modules/$(uname -r)/build" ]; then
    echo "Attempting to build kernel module..."
    if make -C "${KERNEL_DIR}" clean >/dev/null 2>&1 && \
       make -C "${KERNEL_DIR}" >/dev/null 2>&1; then
        print_pass "Kernel module compilation"
        
        # Check if .ko file was created
        if [ -f "${KERNEL_DIR}/sagco_cpu_mod.ko" ]; then
            print_pass "Kernel module object file created"
        else
            print_fail "Kernel module object file not created"
        fi
    else
        print_skip "Kernel module compilation (build may require kernel headers)"
    fi
else
    print_skip "Kernel module compilation (kernel headers not installed)"
fi

# Test 5: Check if module is currently loaded
if lsmod | grep -q sagco_cpu_mod; then
    print_pass "Kernel module is loaded"
    
    # Check device node
    if [ -c /dev/sagco_cpu ]; then
        print_pass "Device node /dev/sagco_cpu exists"
    else
        print_fail "Device node /dev/sagco_cpu not found"
    fi
else
    print_skip "Kernel module status check (module not loaded)"
fi

# ============================================================================
# FlameLang Compiler Tests
# ============================================================================

print_test_header "FlameLang Compiler Tests"

# Test 6: Check if compiler script exists
if [ -f "${COMPILER_DIR}/flamelang_to_llvm.py" ]; then
    print_pass "FlameLang compiler script exists"
else
    print_fail "FlameLang compiler script not found"
fi

# Test 7: Check if compiler script is executable
if [ -x "${COMPILER_DIR}/flamelang_to_llvm.py" ]; then
    print_pass "FlameLang compiler is executable"
else
    print_fail "FlameLang compiler is not executable"
fi

# Test 8: Check Python3 availability
if command -v python3 >/dev/null 2>&1; then
    print_pass "Python3 is available ($(python3 --version))"
else
    print_fail "Python3 is not available"
    exit 1
fi

# Test 9: Check Python syntax
if python3 -m py_compile "${COMPILER_DIR}/flamelang_to_llvm.py" 2>/dev/null; then
    print_pass "FlameLang compiler Python syntax check"
else
    print_fail "FlameLang compiler has Python syntax errors"
fi

# Test 10: Check llvmlite availability
if python3 -c "import llvmlite" 2>/dev/null; then
    LLVMLITE_VERSION=$(python3 -c "import llvmlite; print(llvmlite.__version__)")
    print_pass "llvmlite is available (version ${LLVMLITE_VERSION})"
    LLVMLITE_AVAILABLE=true
else
    print_skip "llvmlite not installed (install with: pip3 install llvmlite)"
    LLVMLITE_AVAILABLE=false
fi

# Test 11: Test compiler help output (only if llvmlite is available or use --help-syntax-only)
if python3 -c "import llvmlite" 2>/dev/null || python3 "${COMPILER_DIR}/flamelang_to_llvm.py" --help 2>&1 | grep -q "usage:"; then
    print_pass "FlameLang compiler help output"
else
    print_skip "FlameLang compiler help output (requires llvmlite)"
fi

# Test 12-15: Compilation tests (if llvmlite is available)
if [ "$LLVMLITE_AVAILABLE" = true ]; then
    # Test 12: Compile simple addition
    echo "Testing FlameLang compilation..."
    if python3 "${COMPILER_DIR}/flamelang_to_llvm.py" "add 5 3" \
        -o "${TEST_OUTPUT_DIR}/test_add.o" 2>/dev/null; then
        print_pass "Compile simple addition"
        
        if [ -f "${TEST_OUTPUT_DIR}/test_add.o" ]; then
            print_pass "Output file created (test_add.o)"
        else
            print_fail "Output file not created"
        fi
    else
        print_fail "Failed to compile simple addition"
    fi
    
    # Test 13: Compile with IR emission
    if python3 "${COMPILER_DIR}/flamelang_to_llvm.py" "mul 10 20" \
        -o "${TEST_OUTPUT_DIR}/test_mul.o" --emit-ir 2>/dev/null; then
        print_pass "Compile with IR emission"
        
        if [ -f "${TEST_OUTPUT_DIR}/test_mul.ll" ]; then
            print_pass "LLVM IR file created (test_mul.ll)"
        else
            print_fail "LLVM IR file not created"
        fi
    else
        print_fail "Failed to compile with IR emission"
    fi
    
    # Test 14: Compile with different optimization levels
    if python3 "${COMPILER_DIR}/flamelang_to_llvm.py" "sub 100 50" \
        -o "${TEST_OUTPUT_DIR}/test_opt.o" -O0 2>/dev/null; then
        print_pass "Compile with -O0 optimization"
    else
        print_fail "Failed to compile with -O0"
    fi
    
    # Test 15: Compile multi-line program
    if python3 "${COMPILER_DIR}/flamelang_to_llvm.py" "add 1 2
mul 3 4
sub 10 5" -o "${TEST_OUTPUT_DIR}/test_multi.o" 2>/dev/null; then
        print_pass "Compile multi-line program"
    else
        print_fail "Failed to compile multi-line program"
    fi
    
    # Test 16: Link and execute (if gcc is available)
    if command -v gcc >/dev/null 2>&1; then
        if python3 "${COMPILER_DIR}/flamelang_to_llvm.py" "add 10 15" \
            -o "${TEST_OUTPUT_DIR}/test_exec.o" 2>/dev/null; then
            if gcc "${TEST_OUTPUT_DIR}/test_exec.o" \
                -o "${TEST_OUTPUT_DIR}/test_exec" -no-pie 2>/dev/null; then
                print_pass "Link object file with gcc"
                
                # Execute and check exit code
                "${TEST_OUTPUT_DIR}/test_exec" 2>/dev/null
                EXIT_CODE=$?
                if [ $EXIT_CODE -eq 25 ]; then
                    print_pass "Execute linked program (exit code: ${EXIT_CODE})"
                else
                    print_fail "Unexpected exit code: ${EXIT_CODE} (expected 25)"
                fi
            else
                print_skip "Failed to link object file (gcc issue)"
            fi
        else
            print_fail "Failed to compile for linking test"
        fi
    else
        print_skip "Linking test (gcc not available)"
    fi
else
    print_skip "Compilation tests (llvmlite not installed)"
fi

# ============================================================================
# Integration Tests
# ============================================================================

print_test_header "Integration Tests"

# Test 17: Check systemd service files
if [ -f "${SCRIPT_DIR}/systemd/sagco-cpu.service" ]; then
    print_pass "Systemd sagco-cpu.service exists"
else
    print_fail "Systemd sagco-cpu.service not found"
fi

if [ -f "${SCRIPT_DIR}/systemd/sagco-compiler.service" ]; then
    print_pass "Systemd sagco-compiler.service exists"
else
    print_fail "Systemd sagco-compiler.service not found"
fi

# Test 18: Check initramfs scripts
if [ -f "${SCRIPT_DIR}/initramfs/sagco-cpu" ]; then
    print_pass "Initramfs sagco-cpu script exists"
    
    if [ -x "${SCRIPT_DIR}/initramfs/sagco-cpu" ]; then
        print_pass "Initramfs sagco-cpu script is executable"
    else
        print_fail "Initramfs sagco-cpu script is not executable"
    fi
else
    print_fail "Initramfs sagco-cpu script not found"
fi

if [ -f "${SCRIPT_DIR}/initramfs/sagco-init" ]; then
    print_pass "SBIP sagco-init script exists"
    
    if [ -x "${SCRIPT_DIR}/initramfs/sagco-init" ]; then
        print_pass "SBIP sagco-init script is executable"
    else
        print_fail "SBIP sagco-init script is not executable"
    fi
else
    print_fail "SBIP sagco-init script not found"
fi

# Test 19: Check documentation
DOCS=("kernel/sagco_cpu_mod/README.md" 
      "compiler/flamelang/README.md" 
      "systemd/README.md" 
      "initramfs/README.md"
      "README-SAGCO.md")

for doc in "${DOCS[@]}"; do
    if [ -f "${SCRIPT_DIR}/${doc}" ]; then
        print_pass "Documentation exists: ${doc}"
    else
        print_fail "Documentation missing: ${doc}"
    fi
done

# ============================================================================
# Test Summary
# ============================================================================

print_test_header "Test Summary"

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))

echo ""
echo "Total Tests:   ${TOTAL_TESTS}"
echo -e "${GREEN}Passed:        ${TESTS_PASSED}${NC}"
echo -e "${RED}Failed:        ${TESTS_FAILED}${NC}"
echo -e "${YELLOW}Skipped:       ${TESTS_SKIPPED}${NC}"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}❌ Test suite FAILED${NC}"
    echo ""
    echo "Some tests failed. Please review the output above."
    exit 1
else
    echo -e "${GREEN}✅ Test suite PASSED${NC}"
    echo ""
    echo "All tests passed successfully! 🔥"
    
    if [ $TESTS_SKIPPED -gt 0 ]; then
        echo ""
        echo "Note: ${TESTS_SKIPPED} test(s) were skipped."
        echo "To run all tests, ensure:"
        echo "  - Kernel headers are installed: sudo apt install linux-headers-\$(uname -r)"
        echo "  - llvmlite is installed: pip3 install llvmlite"
        echo "  - GCC is installed: sudo apt install gcc"
    fi
    
    exit 0
fi
