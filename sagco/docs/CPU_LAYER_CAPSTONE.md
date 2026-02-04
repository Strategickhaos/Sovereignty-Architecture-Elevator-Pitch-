# SAGCO CPU Layer - Capstone Documentation

## Overview

SAGCO (Sovereignty Architecture Guaranteed Compute Overlay) targets standard hardware ISAs (e.g., x86_64) via an LLVM backend. The 'CPU layer' refers to the compilation target architecture and its execution environment.

## Architecture

### Primary Execution Path: Native Compilation

FlameLang source code is compiled through the following pipeline:

```
FlameLang Source → AST → LLVM IR → Native Machine Code → CPU Execution
```

**Key Components:**
- **FlameLang Compiler** (`flamelang_compiler.py`): Parses source and generates LLVM IR
- **LLVM Backend**: Handles optimization and native code generation
- **Target ISA**: x86_64 (extensible to ARM, RISC-V, etc.)

### Optional Execution Path: VM Interpreter

For portability and sandboxing, an optional VM execution layer ('SAGCO-CPU') can interpret FlameLang bytecode:

```
FlameLang Source → AST → SAGCO Bytecode → VM Interpreter → Result
```

**Key Components:**
- **Bytecode Compiler**: Emits stack-based bytecode from AST
- **SAGCO CPU VM** (`sagco_cpu_vm.py`): Interprets bytecode in userspace
- **Execution Model**: Stack-based (similar to Python bytecode, Lua)

## CPU Layer Definition

The CPU layer encompasses:

1. **Hardware Target**: x86_64 architecture (primary), with LLVM providing portability
2. **Execution Model**: Direct CPU execution of compiled native code
3. **Performance**: No interpretation overhead in native mode
4. **Security**: Sandboxed execution available via VM mode

## Future Work

An optional VM execution layer ('SAGCO-CPU') provides:
- **Portability**: Bytecode runs on any platform with the VM interpreter
- **Sandboxing**: Restricted execution environment for untrusted code
- **Debugging**: Easier introspection and step-through debugging
- **Hot-reload**: Dynamic code updates without recompilation

## Implementation Details

### File Structure
```
sagco/
├── compiler/
│   └── flamelang_compiler.py    # Compiler with LLVM/bytecode backends
├── vm/
│   └── sagco_cpu_vm.py          # VM interpreter
├── sbip/
│   ├── sagco-init               # Boot integration script
│   └── sagco-cpu.service        # Systemd service file
└── docs/
    └── (this file)
```

### Compilation Modes

**Native Mode:**
```bash
python3 flamelang_compiler.py native source.flame
# Produces: example.ll (LLVM IR), example.o (object file)
# Link with: clang example.o -o executable
```

**VM Mode:**
```bash
python3 flamelang_compiler.py vm source.flame
# Produces: example.bc (bytecode)
# Execute with: python3 sagco_cpu_vm.py example.bc
```

### Bytecode Format

SAGCO bytecode uses a simple stack machine with the following opcodes:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x01 | PUSH | Push value onto stack |
| 0x02 | POP | Pop and output value |
| 0x10 | ADD | Add top two stack values |
| 0x11 | SUB | Subtract top two stack values |
| 0x12 | MUL | Multiply top two stack values |
| 0x13 | DIV | Divide top two stack values |
| 0x20 | CALL | Function call (future) |
| 0x21 | RET | Return from function (future) |
| 0xFF | HALT | Stop execution |

Example bytecode (push 5, push 3, add, halt):
```
01 05 01 03 10 FF
```

## Dependencies

**For Native Compilation:**
- LLVM toolchain (llvm, clang)
- llvmlite Python library (optional, for IR generation)

**For VM Execution:**
- Python 3.8+
- No external dependencies

## Integration with SBIP

The CPU layer integrates with the Sovereignty Bootstrap Integration Protocol (SBIP):

1. **Stage 1 (initramfs)**: Identity splash and verification
2. **Stage 2 (sagco-init)**: Artifact verification, optional VM execution
3. **Stage 3 (systemd)**: Start VM daemon service if enabled

## Distinction from Other Approaches

**Not Kernel-Module Based**: SAGCO runs entirely in userspace, avoiding kernel-level complexity and security risks.

**Not Emulated**: Native mode compiles to actual CPU instructions, not emulated bytecode.

**Not VM-Only**: Unlike pure VM languages (Java, Python), native mode provides zero-overhead execution.

## Performance Characteristics

**Native Mode:**
- Performance: Native CPU speed (same as C/C++)
- Startup: Fast (no interpreter loading)
- Memory: Minimal overhead
- Use case: Production workloads

**VM Mode:**
- Performance: ~10-50x slower than native (typical for interpreters)
- Startup: Very fast (just load bytecode)
- Memory: Interpreter + bytecode + stack
- Use case: Development, sandboxing, portability

---

*This documentation describes the SAGCO CPU layer as implemented in the Sovereignty Architecture Elevator Pitch repository.*
