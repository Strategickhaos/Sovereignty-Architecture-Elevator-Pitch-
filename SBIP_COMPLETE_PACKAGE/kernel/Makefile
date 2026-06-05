# Makefile for SAGCO CPU Kernel Module
# Strategickhaos DAO LLC - Ratio Ex Nihilo

obj-m += sagco_cpu_mod.o

# Kernel build directory
KDIR := /lib/modules/$(shell uname -r)/build

# Module build directory
PWD := $(shell pwd)

# Default target - build the module
all:
	@echo "Building SAGCO CPU kernel module..."
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	@echo "Build complete. Module: sagco_cpu_mod.ko"

# Install the module
install: all
	@echo "Installing SAGCO CPU module..."
	sudo insmod sagco_cpu_mod.ko
	@echo "Module installed. Checking dmesg..."
	@dmesg | tail -n 10 | grep SAGCO || true
	@echo "Device status:"
	@ls -la /dev/sagco_cpu 2>/dev/null || echo "Device not yet visible (may take a moment)"

# Uninstall the module
uninstall:
	@echo "Uninstalling SAGCO CPU module..."
	sudo rmmod sagco_cpu_mod 2>/dev/null || echo "Module not loaded"
	@echo "Module uninstalled"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	$(MAKE) -C $(KDIR) M=$(PWD) clean
	rm -f *.o *.ko *.mod.c *.mod *.order *.symvers
	@echo "Clean complete"

# Test the module
test: install
	@echo ""
	@echo "=== SAGCO CPU Module Test ==="
	@echo "1. Checking if module is loaded:"
	@lsmod | grep sagco_cpu_mod || echo "Module not found in lsmod"
	@echo ""
	@echo "2. Checking kernel messages:"
	@dmesg | grep SAGCO | tail -n 20
	@echo ""
	@echo "3. Checking device file:"
	@ls -la /dev/sagco_cpu || echo "Device file not found"
	@echo ""
	@echo "=== Test complete ==="

# Show module info
info:
	@echo "SAGCO CPU Module Information:"
	@modinfo sagco_cpu_mod.ko 2>/dev/null || echo "Module not built yet. Run 'make' first."

# Full reinstall
reinstall: uninstall clean all install

.PHONY: all install uninstall clean test info reinstall
