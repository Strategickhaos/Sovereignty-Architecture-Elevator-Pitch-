# Makefile for SAGCO CPU Module

obj-m += sagco_cpu_mod.o

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

install:
	sudo cp sagco_cpu_mod.ko /lib/modules/$(shell uname -r)/extra/ || true
	sudo mkdir -p /lib/modules/$(shell uname -r)/extra/ && sudo cp sagco_cpu_mod.ko /lib/modules/$(shell uname -r)/extra/
	sudo depmod -a
	@echo "sagco_cpu_mod" | sudo tee -a /etc/modules >/dev/null || true

uninstall:
	sudo rm -f /lib/modules/$(shell uname -r)/extra/sagco_cpu_mod.ko
	sudo depmod -a
	sudo sed -i '/sagco_cpu_mod/d' /etc/modules

.PHONY: all clean install uninstall
