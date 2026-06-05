# SAGCO CPU Examples

This directory contains example programs demonstrating how to use the SAGCO CPU kernel module from userspace.

## test_sagco.c

A comprehensive test suite that exercises all features of the SAGCO CPU module:

- Version query
- Basic arithmetic operations (ADD, MUL, DIV)
- Complex expressions
- Error handling

### Building

```bash
make
```

### Running

Make sure the kernel module is loaded first:

```bash
cd ..
sudo insmod sagco_cpu_mod.ko
```

Then run the test suite:

```bash
cd examples
sudo ./test_sagco
```

Or run a specific test:

```bash
sudo ./test_sagco 2  # Run only addition test
```

### Example Output

```
========================================
  SAGCO CPU Kernel Module Test Suite
  Strategickhaos DAO LLC
========================================

✓ Device opened: /dev/sagco_cpu

Test: Get Version
-----------------
Module Version: 0x010200 (v1.2.0)
✓ Test passed

Test: Addition (5 + 3)
----------------------
Bytecode: [0x01 0x05 0x01 0x03 0x10 0xff]
Expected: 8
Result:   8
✓ Test passed

...

========================================
  ALL TESTS PASSED ✓
========================================
```

## Writing Your Own Programs

Include the necessary headers and define the structures:

```c
#include <sys/ioctl.h>
#include <stdint.h>

#define SAGCO_DEV_PATH "/dev/sagco_cpu"
#define SAGCO_MAGIC 'S'

struct sagco_bc {
    uint8_t code[1024];
    size_t len;
};

#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, struct sagco_bc)
#define SAGCO_GET_VERSION   _IOR(SAGCO_MAGIC, 2, unsigned long)
```

Then open the device and use ioctl:

```c
int fd = open(SAGCO_DEV_PATH, O_RDWR);
if (fd < 0) {
    perror("open");
    return 1;
}

struct sagco_bc bc;
bc.code[0] = 0x01; // PUSH
bc.code[1] = 42;
bc.code[2] = 0xff; // HALT
bc.len = 3;

long result = ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
printf("Result: %ld\n", result);

close(fd);
```
