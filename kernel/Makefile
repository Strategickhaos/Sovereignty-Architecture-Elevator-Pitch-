# SAGCO CPU Kernel Module Makefile
# Build system for the SAGCO CPU primitives kernel module

obj-m += sagco_cpu_mod.o

KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

# Default target: build the kernel module
all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

# Clean build artifacts
clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

# Install module (load into kernel)
# Uses insmod instead of manual device node creation
# Device node auto-created by miscdevice at /dev/sagco_cpu
install:
	sudo insmod sagco_cpu_mod.ko

# Uninstall module (remove from kernel)
uninstall:
	sudo rmmod sagco_cpu_mod

# Show module info
info:
	modinfo sagco_cpu_mod.ko

# Check if module is loaded
status:
	lsmod | grep sagco_cpu_mod || echo "Module not loaded"

# View kernel logs related to SAGCO
logs:
	dmesg | grep SAGCO_CPU | tail -20

.PHONY: all clean install uninstall info status logs
