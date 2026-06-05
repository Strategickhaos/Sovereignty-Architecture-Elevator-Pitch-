# SAGCO CPU Module Makefile
# Builds the sagco_cpu_mod kernel module
#
# Usage:
#   make          - Build the kernel module
#   make clean    - Remove build artifacts
#   make install  - Install module to system (requires root)
#   make load     - Load the module (requires root)
#   make unload   - Unload the module (requires root)

obj-m += sagco_cpu_mod.o

# Kernel build directory
KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

# Module info
MODULE_NAME := sagco_cpu_mod
MODULE_FILE := $(MODULE_NAME).ko

all:
	@echo "========================================="
	@echo "Building SAGCO CPU Primitives Module"
	@echo "Entity: Strategickhaos DAO LLC"
	@echo "========================================="
	$(MAKE) -C $(KDIR) M=$(PWD) modules
	@echo ""
	@echo "Build complete: $(MODULE_FILE)"
	@echo "Next steps:"
	@echo "  sudo make install  - Install to system"
	@echo "  sudo make load     - Load the module"

clean:
	@echo "Cleaning SAGCO CPU module build artifacts..."
	$(MAKE) -C $(KDIR) M=$(PWD) clean
	@rm -f Module.symvers modules.order
	@echo "Clean complete."

install: all
	@echo "Installing SAGCO CPU module..."
	@if [ ! -f $(MODULE_FILE) ]; then \
		echo "Error: Module file $(MODULE_FILE) not found. Run 'make' first."; \
		exit 1; \
	fi
	install -m 644 $(MODULE_FILE) /lib/modules/$(shell uname -r)/extra/
	depmod -a
	@echo "Module installed successfully."
	@echo "Use 'sudo modprobe sagco_cpu_mod' to load it."

uninstall:
	@echo "Uninstalling SAGCO CPU module..."
	@if lsmod | grep -q $(MODULE_NAME); then \
		echo "Module is loaded. Unloading first..."; \
		rmmod $(MODULE_NAME); \
	fi
	rm -f /lib/modules/$(shell uname -r)/extra/$(MODULE_FILE)
	depmod -a
	@echo "Module uninstalled."

load: install
	@echo "Loading SAGCO CPU module..."
	@if lsmod | grep -q $(MODULE_NAME); then \
		echo "Module already loaded. Unloading first..."; \
		rmmod $(MODULE_NAME); \
	fi
	modprobe $(MODULE_NAME)
	@echo ""
	@echo "Module loaded successfully!"
	@echo "Checking dmesg output..."
	@dmesg | tail -20 | grep SAGCO_CPU || echo "No SAGCO_CPU messages in dmesg"
	@echo ""
	@echo "Device file: /dev/sagco_cpu"
	@ls -l /dev/sagco_cpu 2>/dev/null || echo "Device file not yet created"

unload:
	@echo "Unloading SAGCO CPU module..."
	@if lsmod | grep -q $(MODULE_NAME); then \
		rmmod $(MODULE_NAME); \
		echo "Module unloaded successfully."; \
	else \
		echo "Module not currently loaded."; \
	fi

test:
	@echo "Testing SAGCO CPU module..."
	@if [ ! -c /dev/sagco_cpu ]; then \
		echo "Error: /dev/sagco_cpu not found. Load the module first."; \
		exit 1; \
	fi
	@echo "Reading device state..."
	@cat /dev/sagco_cpu
	@echo ""
	@echo "Sending 'tick' command..."
	@echo "tick" > /dev/sagco_cpu
	@echo "Reading updated state..."
	@cat /dev/sagco_cpu

.PHONY: all clean install uninstall load unload test
