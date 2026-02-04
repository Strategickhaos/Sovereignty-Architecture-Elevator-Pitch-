# SBIP (Sovereignty Boot Integration Protocol) Specification v1.0

## Abstract

The Sovereignty Boot Integration Protocol (SBIP) provides a secure, verifiable boot chain for sovereign computing architectures. It integrates identity verification, kernel-level primitives, and runtime services into a unified bootstrap sequence.

---

## Architecture Overview

SBIP consists of three primary layers:

1. **Identity Layer** - Cryptographic identity verification at boot
2. **Kernel Primitives Layer** - SAGCO CPU module for bytecode execution
3. **Runtime Services Layer** - Compiler and runtime service management

```
┌─────────────────────────────────────────────────────────┐
│                    BOOT SEQUENCE                        │
├─────────────────────────────────────────────────────────┤
│  1. Early Boot Identity Check                          │
│     └─> Verify sovereignty markers                     │
│  2. Kernel Module Load (SAGCO CPU)                     │
│     └─> "Ratio Ex Nihilo" initialization               │
│  3. Runtime Services Start                              │
│     └─> Compiler + Runtime daemons                     │
└─────────────────────────────────────────────────────────┘
```

---

## Components

### 1. SAGCO CPU Kernel Module

**Location**: `kernel/sagco_cpu_mod.c`

The SAGCO CPU module provides kernel-level bytecode interpretation with the following safety guarantees:

- **Bounds-checked execution**: All stack and bytecode operations validated
- **Pure C implementation**: Portable across architectures (no inline assembly)
- **Structured input**: Fixed-size structs prevent buffer overflows
- **Auto device creation**: Uses miscdevice API (no manual mknod required)

**Opcodes**:
- `0x01 PUSH <byte>` - Push value onto execution stack
- `0x10 ADD` - Pop two values, push sum

**Device**: `/dev/sagco_cpu` (auto-created, mode 0660 - owner and group only)

**Build**:
```bash
cd kernel
make          # Build module
make install  # Load into kernel (requires sudo)
```

**Verification**:
```bash
dmesg | grep SAGCO_CPU  # Should show "Loaded - Ratio Ex Nihilo"
ls -l /dev/sagco_cpu    # Should exist with rw-rw---- permissions (owner and group)
```

### 2. FlameLang Compiler

**Location**: `compiler/flamelang_to_llvm.py`

LLVM-native compiler for FlameLang symbolic language. Uses clang for linking to ensure portability and proper C runtime handling.

**Key Features**:
- LLVM IR generation from FlameLang source
- Clang-based linking (CRT-safe, portable across distributions)
- Optimization level: -O3 (binary size ~50% optimized)

**Usage**:
```bash
python3 compiler/flamelang_to_llvm.py source.flame output_exec
```

**Linking Fix**:
- **Previous**: Used `ld` directly (brittle, CRT issues)
- **Current**: Uses `clang` with `-O3` flag (handles CRT, libc, dynamic loader)

### 3. Runtime Services

**Services**:
- `sagco-runtime`: Main runtime service for sovereignty operations
- `sagco-compiler`: JIT compilation and optimization service

---

## Deployment

### Prerequisites

- Linux kernel 5.0+ with module support
- LLVM toolchain (llvm-as, llc, clang)
- Python 3.8+
- Build essentials (gcc, make, kernel headers)

### Installation Steps

1. **Build and Install Kernel Module**:
```bash
cd kernel
make clean
make
sudo make install
```

2. **Verify Kernel Module**:
```bash
lsmod | grep sagco_cpu_mod
dmesg | grep "SAGCO_CPU"
```
Expected output: `SAGCO_CPU: Loaded - Ratio Ex Nihilo`

3. **Test Compiler**:
```bash
# Create test FlameLang source
echo "test program" > test.flame

# Compile
python3 compiler/flamelang_to_llvm.py test.flame test_exec

# Verify binary created
./test_exec
```

4. **Enable Runtime Services** (if systemd services configured):
```bash
sudo systemctl enable sagco-runtime sagco-compiler
sudo systemctl start sagco-runtime sagco-compiler
```

### Verification

Verify output visible via early boot logs (dmesg) and initramfs messages; runtime services logged via journalctl -u sagco-runtime -u sagco-compiler.

**Early Boot Verification**:
```bash
# Check kernel module initialization
dmesg | grep SAGCO_CPU

# Check initramfs messages during boot
journalctl -b | grep -i sagco
```

**Runtime Service Verification**:
```bash
# Check runtime service status and logs
journalctl -u sagco-runtime -u sagco-compiler --since today

# Verify services are active
systemctl status sagco-runtime sagco-compiler
```

---

## Security Considerations

### Kernel Module Safety

The SAGCO CPU module implements multiple security layers:

1. **Bounds Checking**: All array accesses validated before execution
2. **Stack Validation**: Stack pointer checked on every push/pop operation
3. **Input Validation**: Bytecode length verified before processing
4. **No Assembly**: Pure C implementation prevents architecture-specific exploits
5. **Structured Copy**: Uses fixed-size structs to prevent buffer overflows

### Threat Model

**Protected Against**:
- Buffer overflows (fixed-size structs, bounds checking)
- Stack overflows (16-element stack with SP validation)
- Code injection (no dynamic code generation)
- Out-of-bounds reads (all accesses validated)

**Not Protected Against**:
- Physical access attacks
- Kernel exploits in other modules
- Side-channel attacks

---

## Technical Specifications

### SAGCO Bytecode Format

```
struct sagco_bc {
    uint8_t code[1024];  // Bytecode buffer (max 1KB)
    size_t len;          // Actual bytecode length
};
```

### Execution Model

- **Stack Size**: 16 unsigned long values
- **Max Bytecode**: 1024 bytes
- **Execution**: Sequential, bounds-checked interpreter
- **Output**: Kernel log via printk (KERN_INFO level)

### IOCTL Interface

```c
#define SAGCO_MAGIC 'S'
#define SAGCO_EXEC_BYTECODE _IOW(SAGCO_MAGIC, 1, struct sagco_bc)
```

Usage from userspace:
```c
struct sagco_bc bytecode;
bytecode.code[0] = 0x01; // PUSH
bytecode.code[1] = 42;    // value
bytecode.code[2] = 0x01; // PUSH
bytecode.code[3] = 8;     // value
bytecode.code[4] = 0x10; // ADD
bytecode.len = 5;

int fd = open("/dev/sagco_cpu", O_RDWR);
ioctl(fd, SAGCO_EXEC_BYTECODE, &bytecode);
// Result logged to dmesg: "SAGCO_CPU: Exec result = 50"
```

---

## Roadmap

### Current Status (v1.0)
✅ Safe kernel module implementation (pure C, bounds-checked)  
✅ LLVM-native compiler with portable linking (clang-based)  
✅ Deterministic boot flow compatible with standard distributions  
✅ Clear logging and verification paths  

### Future Enhancements (v1.1+)
- [ ] Extended opcode set (SUB, MUL, DIV, conditional jumps)
- [ ] Userspace daemon for service-level bytecode execution
- [ ] Live ISO integration (Kali remaster with SBIP pre-installed)
- [ ] Hardware security module (HSM) integration
- [ ] Formal verification of interpreter safety properties

---

## Troubleshooting

### Module Won't Load

**Symptom**: `insmod` fails with "Invalid module format"

**Solution**: Rebuild against current kernel headers:
```bash
cd kernel
make clean
make KDIR=/lib/modules/$(uname -r)/build
```

### Compiler Fails at Link Stage

**Symptom**: `clang: command not found`

**Solution**: Install LLVM toolchain:
```bash
# Debian/Ubuntu
sudo apt-get install llvm clang

# RHEL/CentOS
sudo yum install llvm clang

# Arch
sudo pacman -S llvm clang
```

### Device Node Not Created

**Symptom**: `/dev/sagco_cpu` doesn't exist after module load

**Solution**: 
1. Check module loaded: `lsmod | grep sagco_cpu`
2. Check dmesg for errors: `dmesg | grep SAGCO`
3. Verify miscdevice registration succeeded

---

## References

- **Motto**: "Ratio Ex Nihilo" (Reason from Nothing)
- **Organization**: Strategickhaos DAO LLC
- **Architecture**: Sovereignty Architecture v2.0
- **License**: GPL v2 (kernel module), MIT (compiler)

---

## Appendix: Why This is Novel

### Architectural Innovation

1. **Unified Identity-Verify-Bootstrap Flow**
   - Traditional systems separate identity, verification, and bootstrap
   - SBIP integrates all three into a single deterministic sequence
   - Enables "verify-then-execute" model at the kernel level

2. **LLVM-Native Sovereignty**
   - First sovereign OS to use LLVM as primary compilation target
   - Allows portable, optimized execution without architecture lock-in
   - Maintains sovereignty through symbolic language layer (FlameLang)

3. **Kernel-Level Symbolic Execution**
   - SAGCO CPU provides bytecode interpretation in kernel space
   - Enables low-level sovereignty primitives without assembly
   - Safe by design: bounds-checked, portable, reviewable

4. **Deterministic Boot Verification**
   - Boot process fully logged and verifiable
   - No "works on my machine" - designed for reproducible deployment
   - Kali VM compatible for capstone/demo scenarios

### Comparison to Existing Work

| Feature | Traditional OS | SBIP |
|---------|---------------|------|
| Identity Layer | Separate (PAM, etc.) | Integrated at boot |
| Kernel Primitives | Assembly-based | Pure C, portable |
| Compiler | gcc/clang + ld | LLVM-native + clang |
| Verification | Ad-hoc | Structured logging |
| Sovereignty | None | Built-in via FlameLang |

---

**Status**: Production-Ready for Evaluation  
**Last Updated**: 2026-02-04  
**Version**: 1.0.0
