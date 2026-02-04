# Makefile for SAGCO CPU Primitives Kernel Module
# Entity: Strategickhaos DAO LLC
# License: GPL v2

obj-m += sagco_cpu_mod.o

# Kernel build directory (auto-detect or override with KDIR=/path/to/kernel)
KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	depmod -a

load:
	insmod sagco_cpu_mod.ko

unload:
	rmmod sagco_cpu_mod

test: load
	@echo "Module loaded. Check dmesg for output:"
	@dmesg | tail -20

.PHONY: all clean install load unload test
