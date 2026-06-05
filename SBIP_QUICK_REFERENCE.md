# SBIP Quick Reference Guide

Quick reference for using the SBIP (Sovereignty Boot Integration Protocol) implementation.

## Quick Start

### Compiler Usage

```bash
# Compile a FlameLang program
python3 compiler/flamelang_to_llvm.py source.flame output_exec

# Test
./output_exec
echo $?  # Should print 0
```

### Kernel Module

```bash
# Build
cd kernel
make

# Install (load into kernel)
sudo make install

# Verify
dmesg | grep SAGCO_CPU
# Expected: "SAGCO_CPU: Loaded - Ratio Ex Nihilo"

# Check device
ls -l /dev/sagco_cpu
# Expected: crw-rw---- ... /dev/sagco_cpu

# Uninstall
sudo make uninstall
```

## Key Features

### Compiler
- ✅ LLVM-native compilation pipeline
- ✅ Clang-based linking (portable, CRT-safe)
- ✅ Auto-detects LLVM tool versions
- ✅ -O3 optimization (~50% size reduction)

### Kernel Module
- ✅ Pure C implementation (no assembly)
- ✅ Comprehensive bounds checking
- ✅ Stack validation on every operation
- ✅ Secure permissions (0660 - owner/group only)
- ✅ Auto device creation (no manual mknod)

## Verification Commands

### Check Compiler Works
```bash
echo "# test" > /tmp/test.flame
python3 compiler/flamelang_to_llvm.py /tmp/test.flame /tmp/test
/tmp/test && echo "✅ Compiler works!"
```

### Check Kernel Module
```bash
# Module loaded?
lsmod | grep sagco_cpu_mod

# Device exists?
ls -l /dev/sagco_cpu

# Logs
dmesg | grep SAGCO_CPU | tail
```

### Check Documentation
```bash
# View specification
cat SBIP_SPEC_v1.0.md

# View implementation summary
cat SBIP_IMPLEMENTATION_SUMMARY.md

# View compiler docs
cat compiler/README.md

# View kernel docs
cat kernel/README.md
```

## Troubleshooting

### Compiler Issues

**Problem**: `llvm-as: command not found`

**Solution**:
```bash
# Debian/Ubuntu
sudo apt-get install llvm clang

# RHEL/CentOS
sudo yum install llvm clang

# Check installed
which llvm-as-18 llc-18 clang
```

### Kernel Module Issues

**Problem**: Module won't build

**Solution**:
```bash
# Install kernel headers
sudo apt-get install linux-headers-$(uname -r)

# Clean and rebuild
cd kernel
make clean
make
```

**Problem**: Module won't load

**Solution**:
```bash
# Check error
sudo dmesg | tail

# Verify kernel version matches
modinfo kernel/sagco_cpu_mod.ko | grep vermagic
uname -r
```

## Security Notes

- Device permissions: 0660 (owner and group only)
- Stack size: 16 elements (prevents overflow)
- Bytecode max: 1024 bytes (prevents DoS)
- All operations: bounds-checked
- No assembly: portable and reviewable

## IOCTL Example

```c
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdint.h>

#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, struct sagco_bc)

struct sagco_bc {
    uint8_t code[1024];
    size_t len;
};

int main() {
    int fd = open("/dev/sagco_cpu", O_RDWR);
    
    struct sagco_bc bc = {
        .code = {0x01, 42, 0x01, 8, 0x10},  // PUSH 42, PUSH 8, ADD
        .len = 5
    };
    
    ioctl(fd, SAGCO_EXEC_BYTECODE, &bc);
    // Check dmesg: "SAGCO_CPU: Exec result = 50"
    
    close(fd);
    return 0;
}
```

## Opcodes

| Code | Mnemonic | Args | Description |
|------|----------|------|-------------|
| 0x01 | PUSH     | byte | Push value onto stack |
| 0x10 | ADD      | -    | Pop two values, push sum |

## Important Files

- `SBIP_SPEC_v1.0.md` - Complete specification
- `SBIP_IMPLEMENTATION_SUMMARY.md` - Implementation details
- `compiler/flamelang_to_llvm.py` - Compiler source
- `kernel/sagco_cpu_mod.c` - Kernel module source
- `kernel/Makefile` - Build system

## Motto

**"Ratio Ex Nihilo"** - Reason from Nothing

---

For complete documentation, see:
- SBIP_SPEC_v1.0.md
- SBIP_IMPLEMENTATION_SUMMARY.md
- compiler/README.md
- kernel/README.md
