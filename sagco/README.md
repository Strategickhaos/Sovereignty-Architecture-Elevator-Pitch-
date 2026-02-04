# SAGCO - Sovereignty Architecture Guaranteed Compute Overlay

**CPU Layer Implementation with LLVM Backend and Optional VM Interpreter**

## Overview

SAGCO provides a dual-mode execution environment for FlameLang:
1. **Native Mode**: Compile to LLVM IR → Native machine code (x86_64) for maximum performance
2. **VM Mode**: Compile to bytecode → Interpret in sandboxed SAGCO-CPU VM for portability

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FlameLang Source Code                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
         ┌────────────────┐  ┌────────────────┐
         │ LLVM Backend   │  │ Bytecode Gen   │
         │ (Native)       │  │ (VM)           │
         └────────┬───────┘  └───────┬────────┘
                  │                  │
                  ▼                  ▼
         ┌────────────────┐  ┌────────────────┐
         │ x86_64 Binary  │  │ SAGCO Bytecode │
         │ (Direct CPU)   │  │ (.bc files)    │
         └────────────────┘  └───────┬────────┘
                                     │
                                     ▼
                            ┌────────────────┐
                            │ SAGCO-CPU VM   │
                            │ (Interpreter)  │
                            └────────────────┘
```

## Quick Start

### 1. Compile to Native Code

```bash
# Compile FlameLang to native binary
cd sagco/compiler
python3 flamelang_compiler.py native source.flame

# Link and execute
clang ../artifacts/example.o -o ../artifacts/example
../artifacts/example
```

### 2. Compile to VM Bytecode

```bash
# Compile FlameLang to bytecode
python3 flamelang_compiler.py vm source.flame

# Execute in VM
cd ../vm
python3 sagco_cpu_vm.py ../artifacts/example.bc
```

### 3. Run VM as Daemon

```bash
# Start VM daemon (monitors directory for .bc files)
python3 sagco_cpu_vm.py --daemon --load-dir ../artifacts --debug
```

## Components

### Compiler (`sagco/compiler/`)
- **flamelang_compiler.py**: FlameLang compiler with dual backends
  - LLVM backend for native code generation
  - Bytecode backend for VM execution
  - Supports: `native`, `vm`, `ir` modes

### Virtual Machine (`sagco/vm/`)
- **sagco_cpu_vm.py**: Stack-based bytecode interpreter
  - Opcodes: PUSH, POP, ADD, SUB, MUL, DIV, HALT
  - Daemon mode for continuous execution
  - Bytecode verification before execution

### SBIP Integration (`sagco/sbip/`)
- **sagco-init**: Initramfs boot script for Stage 2 verification
- **sagco-cpu.service**: Systemd service for VM daemon (Stage 3)

### Documentation (`sagco/docs/`)
- **CPU_LAYER_CAPSTONE.md**: CPU layer for Capstone project
- **CPU_LAYER_SBIP_SPEC.md**: SBIP specification and integration
- **CPU_LAYER_ATTORNEY_MEMO.md**: Patent/IP considerations
- **IMPLEMENTATION_GUIDE.md**: Full installation and usage guide

## Features

### Native Mode
✅ **Performance**: Native CPU execution (no interpretation overhead)  
✅ **LLVM Optimization**: Industry-standard optimization pipeline  
✅ **Platform Support**: x86_64 primary, extensible to ARM64, RISC-V  
✅ **Toolchain**: Standard LLVM/Clang tools

### VM Mode
✅ **Portability**: Bytecode runs on any platform with Python 3.8+  
✅ **Sandboxing**: Systemd security hardening + resource limits  
✅ **Debugging**: Stack traces and execution logging  
✅ **Dynamic**: No recompilation needed for bytecode updates

### SBIP Integration
✅ **Stage 1**: Identity verification (initramfs)  
✅ **Stage 2**: Artifact verification and optional execution (sagco-init)  
✅ **Stage 3**: VM daemon service (systemd)  
✅ **Security**: Cryptographic hash verification of all artifacts

## Installation

See [IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md) for complete instructions.

**Quick Install:**
```bash
# System setup (requires root)
sudo mkdir -p /opt/sagco/{compiler,vm,artifacts,sbip}
sudo cp -r sagco/* /opt/sagco/
sudo chmod +x /opt/sagco/compiler/flamelang_compiler.py
sudo chmod +x /opt/sagco/vm/sagco_cpu_vm.py

# Install systemd service
sudo cp sagco/sbip/sagco-cpu.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagco-cpu.service
sudo systemctl start sagco-cpu.service
```

## Bytecode Format

SAGCO uses a simple stack-based bytecode format:

| Opcode | Hex  | Name | Args | Description |
|--------|------|------|------|-------------|
| PUSH   | 0x01 | PUSH | val  | Push value onto stack |
| POP    | 0x02 | POP  | -    | Pop and output value |
| ADD    | 0x10 | ADD  | -    | Add top two stack values |
| SUB    | 0x11 | SUB  | -    | Subtract top two values |
| MUL    | 0x12 | MUL  | -    | Multiply top two values |
| DIV    | 0x13 | DIV  | -    | Divide top two values |
| CALL   | 0x20 | CALL | -    | Function call (future) |
| RET    | 0x21 | RET  | -    | Return (future) |
| HALT   | 0xFF | HALT | -    | Stop execution |

**Example:** `01 05 01 03 10 FF` = push 5, push 3, add, halt → Result: 8

## Dependencies

### Native Compilation
- LLVM toolchain (`llvm`, `clang`)
- llvmlite Python library (optional but recommended)

```bash
sudo apt-get install llvm clang
pip3 install llvmlite
```

### VM Execution
- Python 3.8 or later (no other dependencies)

```bash
python3 --version  # Should be 3.8+
```

## Usage Examples

### Example 1: View LLVM IR
```bash
cd sagco/compiler
python3 flamelang_compiler.py ir
cat ../artifacts/example.ll
```

### Example 2: Compile and Execute Native
```bash
python3 flamelang_compiler.py native
cd ../artifacts
clang example.o -o example
./example
echo $?  # Exit code 42 (placeholder)
```

### Example 3: Compile and Execute VM
```bash
python3 flamelang_compiler.py vm
cd ../vm
python3 sagco_cpu_vm.py --debug ../artifacts/example.bc
# Output: Result: 8, Stack: [8]
```

### Example 4: Monitor Daemon
```bash
# Terminal 1: Start daemon
cd sagco/vm
python3 sagco_cpu_vm.py --daemon --load-dir ../artifacts

# Terminal 2: Add bytecode
echo "01 0A 01 05 10 FF" | xxd -r -p > ../artifacts/test.bc
# Daemon automatically detects and executes (10 + 5 = 15)
```

## Testing

```bash
# Test compiler (VM mode)
cd sagco/compiler
python3 flamelang_compiler.py vm
ls ../artifacts/example.bc || echo "FAILED"

# Test VM execution
cd ../vm
python3 sagco_cpu_vm.py ../artifacts/example.bc | grep "Result: 8" && echo "PASSED"

# Test systemd service (if installed)
sudo systemctl status sagco-cpu.service
```

## Security

### Bytecode Verification
All bytecode is verified before execution:
- Valid opcode checking
- Hash verification (production: SHA-256 signatures)
- SBIP Stage 2 integration

### Systemd Hardening
The VM service runs with strict security:
- Dedicated `sagco` user (no login)
- No new privileges
- Protected system directories
- Memory and CPU limits
- Restricted namespaces

### Hash Manifests
```bash
# Generate hash
sha256sum artifacts/example.bc > artifacts/example.bc.sha256

# Verify (in sagco-init or manually)
sha256sum -c artifacts/example.bc.sha256
```

## Performance

| Mode   | Compilation | Startup | Runtime | Portability | Sandbox |
|--------|-------------|---------|---------|-------------|---------|
| Native | Slow        | Fast    | Fast    | Low         | No      |
| VM     | Fast        | Fast    | Moderate| High        | Yes     |

**Benchmarks (placeholder implementation):**
- Native: ~10-100x faster than VM mode
- VM: Sufficient for control plane, configuration, non-critical paths

## Roadmap

### Phase 1 (Current)
- ✅ Dual-mode compiler (native + VM)
- ✅ Stack-based VM interpreter
- ✅ SBIP integration scripts
- ✅ Systemd service definition
- ✅ Documentation suite

### Phase 2 (Future)
- 🔜 Real FlameLang parser (AST generation)
- 🔜 Extended bytecode instruction set
- 🔜 Function calls and stack frames
- 🔜 JIT compilation (hot path optimization)

### Phase 3 (Advanced)
- 🔮 Kernel module integration (optional)
- 🔮 Hardware acceleration (AVX, SIMD)
- 🔮 Distributed execution (swarm nodes)
- 🔮 Cryptographic signature verification

## Contributing

This is part of the Sovereignty Architecture project. See main repository for contribution guidelines.

## License

See [LICENSE](../LICENSE) file in the root directory.

## Related Projects

- **FlameLang**: Sovereignty programming language
- **SBIP**: Sovereignty Bootstrap Integration Protocol
- **Strategickhaos DAO**: Parent organization

## Documentation

📄 Full documentation available in [sagco/docs/](docs/):
- Implementation guide
- SBIP specification
- CPU layer architecture
- Attorney intake memo

## Contact

Part of the **Strategickhaos Sovereignty Architecture** project.

Repository: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

---

*SAGCO v1.0 - Ratio Ex Nihilo - Bootstrapping Sovereign Compute*
