obj-m += sagco_cpu_mod.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

install:
	sudo insmod sagco_cpu_mod.ko
	# Device node is automatically created by udev/devtmpfs at /dev/sagco_cpu
	# If needed manually: sudo mknod /dev/sagco_cpu c 10 <dynamic_minor>
	@echo "Note: Device node created automatically by kernel at /dev/sagco_cpu"
