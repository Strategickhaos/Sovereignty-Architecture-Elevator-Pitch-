# FlameLang Compiler

This directory contains the FlameLang to LLVM compiler implementation.

## Overview

FlameLang is compiled to native x86_64 binaries via an LLVM backend. The compiler performs aggressive optimizations including:

- Dead code elimination (DCE)
- Loop vectorization
- Instruction combining
- Native CPU feature targeting (AVX2 when available)
- -O3 optimization level

## Files

### flamelang_to_llvm.py
Main compiler implementation that:
1. Parses FlameLang source code
2. Generates LLVM IR
3. Optimizes IR with multiple passes
4. Emits native x86_64 object code
5. Links to executable binary

## Usage

```bash
# Basic compilation
./flamelang_to_llvm.py source.flame output_binary

# Example with simple operations
echo "add 5 3" > test.flame
./flamelang_to_llvm.py test.flame test_exec
./test_exec
echo $?  # Should print result
```

## Dependencies

The compiler requires:
- Python 3.7+
- llvmlite (Python LLVM bindings)
- ld (GNU linker)

Install dependencies:
```bash
pip install llvmlite
```

## FlameLang Syntax (Stub)

Current implementation supports basic arithmetic operations:
```
add <num1> <num2>
sub <num1> <num2>
mul <num1> <num2>
```

This is a stub parser. Extend based on the full FlameLang specification.

## Integration with SAGCO Services

The compiler can be run as a daemon via the `sagco-compiler.service` systemd service, which watches for source files and automatically compiles them.

## See Also

- [SBIP Specification](../../docs/SBIP_SPEC_v1.0.md) - Complete SBIP v1.0 documentation
- [FlameLang Specification](../../FLAMELANG_SPECIFICATION.md) - Language specification
- [Services](../../services/) - systemd service files
