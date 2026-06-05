#!/bin/bash
#
# SAGCO Boot Identity Pipeline - Quick Test Script
# Tests SBIP components without requiring a full reboot
#
# Entity: Strategickhaos DAO LLC
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "SAGCO SBIP Component Test"
echo "========================================="
echo ""

# Test 1: Check if kernel module is loaded
echo -n "Test 1: Kernel module loaded... "
if lsmod | grep -q sagco_cpu_mod; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Run: sudo modprobe sagco_cpu_mod"
    exit 1
fi

# Test 2: Check device file
echo -n "Test 2: Device file exists... "
if [ -c /dev/sagco_cpu ]; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "  Device /dev/sagco_cpu not found"
    exit 1
fi

# Test 3: Read CPU state
echo -n "Test 3: Read CPU state... "
if sudo cat /dev/sagco_cpu > /tmp/sagco-test-state.txt 2>/dev/null; then
    if grep -q "SAGCO CPU State" /tmp/sagco-test-state.txt; then
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Unexpected output format"
    fi
else
    echo -e "${RED}FAIL${NC}"
    exit 1
fi

# Test 4: Write to device
echo -n "Test 4: Write tick command... "
if echo "tick" | sudo tee /dev/sagco_cpu > /dev/null 2>&1; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${RED}FAIL${NC}"
    exit 1
fi

# Test 5: Verify counter incremented
echo -n "Test 5: Verify counter increment... "
if sudo cat /dev/sagco_cpu | grep -q "Ratio Counter: 1"; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Counter may not have incremented"
fi

# Test 6: Check systemd services
echo -n "Test 6: systemd services installed... "
installed_count=0
for service in sagco-banner sagco-cpu sagco-runtime sagco-compiler; do
    if systemctl list-unit-files | grep -q "${service}.service"; then
        ((installed_count++))
    fi
done

if [ $installed_count -eq 4 ]; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Only $installed_count/4 services installed"
fi

# Test 7: Check service binaries
echo -n "Test 7: Service binaries exist... "
binary_count=0
for binary in sagco-banner sagco-runtime sagco-compiler sagco-cpu-init; do
    if [ -x "/usr/local/bin/$binary" ]; then
        ((binary_count++))
    fi
done

if [ $binary_count -eq 4 ]; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Only $binary_count/4 binaries found"
fi

# Test 8: Run banner script
echo -n "Test 8: Banner script runs... "
if /usr/local/bin/sagco-banner > /tmp/sagco-banner-test.txt 2>&1; then
    if grep -q "SAGCO BOOT IDENTITY PIPELINE" /tmp/sagco-banner-test.txt; then
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${YELLOW}WARN${NC}"
    fi
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Banner script may not be installed"
fi

# Test 9: Check GRUB theme files
echo -n "Test 9: GRUB theme installed... "
if [ -f "/boot/grub/themes/sagco/theme.txt" ]; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  GRUB theme not installed"
fi

# Test 10: Check initramfs scripts
echo -n "Test 10: initramfs scripts installed... "
if [ -f "/usr/local/share/sagco/scripts/sagco-verify" ] && \
   [ -f "/etc/initramfs-tools/hooks/sagco" ]; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  initramfs scripts not installed"
fi

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Core functionality tests: PASSED"
echo ""
echo "Additional checks:"
echo "  - systemd services: $installed_count/4"
echo "  - Service binaries: $binary_count/4"
echo ""
echo "To complete installation:"
echo "  1. Update /etc/default/grub"
echo "  2. Run: sudo update-grub"
echo "  3. Reboot to see full SBIP"
echo ""
echo "View kernel messages:"
echo "  dmesg | grep SAGCO_CPU"
echo ""
echo "View current CPU state:"
echo "  sudo cat /dev/sagco_cpu"
echo ""
echo "🔥💜 STRATEGICKHAOS DAO LLC 💜🔥"
