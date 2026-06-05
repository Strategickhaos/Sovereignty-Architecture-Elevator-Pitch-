# SAGCO CPU Primitives Kernel Module

**Version:** 1.2.0 (HARDENED)  
**Entity:** Strategickhaos DAO LLC  
**EIN:** 39-2923503  
**Wyoming:** 2025-001708194  
**License:** GPL v2

## Overview

The SAGCO CPU Primitives Module is a Linux kernel module that exposes SAGCO-specific CPU primitives via the `/dev/sagco_cpu` device. It provides a safe, portable, pure-C bytecode interpreter for executing simple stack-based operations in kernel space.

## Features

- **Pure C Implementation**: No assembly code, ensuring portability across architectures
- **Bounds Checking**: All operations are bounds-checked to prevent buffer overflows
- **Stack-Based VM**: Simple 16-entry stack with arithmetic operations
- **Safe I/O**: Uses fixed-size struct input with length validation
- **Hardened Design**: Multiple security checks and error handling

## Architecture

The module creates a misc device `/dev/sagco_cpu` that accepts ioctl commands:

1. **SAGCO_EXEC_BYTECODE**: Execute bytecode on the stack-based VM
2. **SAGCO_GET_VERSION**: Get the module version

### Supported Opcodes

| Opcode | Hex  | Description |
|--------|------|-------------|
| NOP    | 0x00 | No operation |
| PUSH   | 0x01 | Push byte to stack |
| POP    | 0x02 | Pop from stack |
| ADD    | 0x10 | Pop two, push sum |
| SUB    | 0x11 | Pop two, push difference |
| MUL    | 0x12 | Pop two, push product |
| DIV    | 0x13 | Pop two, push quotient |
| HALT   | 0xFF | Stop execution |

## Building

### Prerequisites

- Linux kernel headers for your running kernel
- GCC compiler
- Make

### Build Instructions

```bash
cd kernel/sagco_cpu
make
```

This will produce `sagco_cpu_mod.ko`.

### Installation

```bash
# Load the module
sudo insmod sagco_cpu_mod.ko

# Or use the Makefile target
sudo make load

# Check that it loaded
lsmod | grep sagco_cpu
ls -l /dev/sagco_cpu

# View kernel messages
dmesg | tail -20
```

### Unloading

```bash
sudo rmmod sagco_cpu_mod

# Or use the Makefile target
sudo make unload
```

## Usage

The module is controlled via ioctl calls from userspace programs. See the `examples/` directory for sample code.

### Example Bytecode Program

Calculate 5 + 3:
```
PUSH 5    (0x01 0x05)
PUSH 3    (0x01 0x03)
ADD       (0x10)
HALT      (0xFF)
```

Result: 8

## Security Considerations

This module runs in Ring 0 (kernel space) and should be used with caution:

- ⚠️ Only load this module on systems where you trust all users
- ⚠️ The device is created with 0666 permissions (world read/write)
- ⚠️ Consider restricting device permissions in production
- ✅ All inputs are bounds-checked
- ✅ No arbitrary code execution - only predefined opcodes
- ✅ Stack overflow/underflow protection
- ✅ Division by zero protection

## Development

### Cleaning Build Artifacts

```bash
make clean
```

### Debugging

View kernel logs in real-time:
```bash
sudo dmesg -w
```

Enable verbose logging:
```bash
# Add to /etc/modprobe.d/sagco_cpu.conf
options sagco_cpu_mod debug=1
```

## Technical Details

- **Device Type**: Misc character device
- **Device Node**: `/dev/sagco_cpu`
- **Major Number**: Dynamic (assigned by kernel)
- **Minor Number**: Dynamic
- **Stack Size**: 16 entries (unsigned long)
- **Max Bytecode Size**: 1024 bytes

## License

Copyright (c) 2025 Strategickhaos DAO LLC

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

## Contact

**Strategickhaos DAO LLC**  
Email: security@strategickhaos.ai

---

*"Ratio Ex Nihilo" - Reason from Nothing*
