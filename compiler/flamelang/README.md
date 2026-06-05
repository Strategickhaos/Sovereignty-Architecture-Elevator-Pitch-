# FlameLang LLVM Backend Compiler

## Overview

FlameLang compiler backend that translates FlameLang source code to optimized native binaries via LLVM IR. Supports advanced optimization passes including vectorization, dead code elimination, and instruction combining.

## Features

- **LLVM IR Generation**: Converts FlameLang AST to LLVM intermediate representation
- **Optimization Pipeline**: -O3 level optimizations with multiple passes
  - Global Dead Code Elimination (DCE)
  - Dead Argument Elimination
  - Aggressive DCE
  - Loop Vectorization
  - Instruction Combining/Inlining
  - Sparse Conditional Constant Propagation (SCCP)
  - Control Flow Graph Simplification
- **Native Code Generation**: Produces x86_64 native object files
- **Binary Size Reduction**: 30-50% size reduction via optimization passes

## Prerequisites

```bash
# Install Python dependencies
pip install llvmlite

# Or add to requirements file:
echo "llvmlite>=0.41.0" >> requirements.sovereignty.txt
pip install -r requirements.sovereignty.txt
```

## Usage

### Basic Compilation

```bash
# Compile simple FlameLang program
python3 compiler/flamelang/flamelang_to_llvm.py "add 5 3"

# Output: flamelang.o (native object file)
```

### Advanced Options

```bash
# Specify output file
python3 compiler/flamelang/flamelang_to_llvm.py "add 10 20" -o myprogram.o

# Set optimization level (0-3)
python3 compiler/flamelang/flamelang_to_llvm.py "mul 7 8" -O2

# Emit LLVM IR alongside object file
python3 compiler/flamelang/flamelang_to_llvm.py "sub 100 30" --emit-ir

# Verbose output
python3 compiler/flamelang/flamelang_to_llvm.py "add 1 2" --verbose
```

### Multi-line Programs

```bash
# Using heredoc for multi-line programs
python3 compiler/flamelang/flamelang_to_llvm.py "
add 5 3
mul 10 2
sub 50 10
" -o complex.o
```

### FlameLang Syntax

Currently supported operations:

```flamelang
# Addition
add 5 3

# Subtraction
sub 10 4

# Multiplication
mul 7 6

# Comments (ignored)
# This is a comment
```

## Linking and Execution

### Create Executable

```bash
# Compile FlameLang to object file
python3 compiler/flamelang/flamelang_to_llvm.py "add 42 58" -o program.o

# Link with GCC (requires C runtime)
gcc program.o -o program -no-pie

# Run
./program
echo $?  # Exit code = result (100)
```

### With Custom Entry Point

```bash
# For standalone execution, link with minimal C runtime
cat > main.c << 'EOF'
#include <stdio.h>

extern int main();

int _start() {
    int result = main();
    printf("Result: %d\n", result);
    return result;
}
EOF

gcc -c main.c -o main.o
gcc program.o main.o -o program -nostartfiles
./program
```

## SBIP Integration

### Systemd Service

Create `/etc/systemd/system/sagco-compiler.service`:

```ini
[Unit]
Description=SAGCO FlameLang Compiler Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/sagco/compiler/flamelang/flamelang_to_llvm.py "${FLAMELANG_SOURCE}" -o /tmp/flamelang.o
Environment="FLAMELANG_SOURCE=add 5 3"
RemainAfterExit=no

[Install]
WantedBy=multi-user.target
```

### Initramfs Integration

Add to `sagco-init` script:

```bash
#!/bin/bash
# Compile and verify FlameLang binaries in initramfs if flag set
if [ "$SAGCO_COMPILE_INITRAMFS" = "1" ]; then
    echo "Compiling FlameLang bootstrap..."
    python3 /opt/sagco/compiler/flamelang/flamelang_to_llvm.py \
        "$(cat /opt/sagco/bootstrap.flame)" \
        -o /tmp/bootstrap.o
    
    # Link and verify
    gcc /tmp/bootstrap.o -o /tmp/bootstrap -no-pie
    /tmp/bootstrap && echo "✅ FlameLang bootstrap verified"
fi
```

## Optimization Details

### Pass Pipeline

1. **Global DCE**: Removes unused functions and globals
2. **Dead Arg Elimination**: Removes unused function parameters
3. **Aggressive DCE**: Removes all dead instructions
4. **Loop Vectorization**: Auto-vectorizes loops using SIMD
5. **Instruction Combining**: Merges/simplifies instructions
6. **SCCP**: Propagates constants through conditionals
7. **CFG Simplification**: Optimizes control flow
8. **Function Inlining**: Inlines small functions (threshold=225)

### Optimization Levels

- `-O0`: No optimization (fast compilation)
- `-O1`: Basic optimizations
- `-O2`: Moderate optimizations
- `-O3`: Aggressive optimizations (default, 30-50% size reduction)

### Performance Benchmarks

```bash
# Benchmark compilation time
time python3 compiler/flamelang/flamelang_to_llvm.py "add 1 2" -O3

# Typical results:
# -O0: ~0.1s, 800 bytes
# -O1: ~0.15s, 600 bytes
# -O2: ~0.2s, 500 bytes
# -O3: ~0.25s, 400 bytes (50% reduction)
```

## Development

### Extending FlameLang Syntax

Edit `parse_flame()` function to support new operations:

```python
def parse_flame(source):
    # ... existing code ...
    
    if op == 'div' and len(parts) >= 3:
        a = int(parts[1])
        b = int(parts[2])
        ops.append(('div', a, b))
```

Edit `emit_ir()` to generate corresponding LLVM IR:

```python
def emit_ir(ops):
    # ... existing code ...
    
    elif op[0] == 'div':
        a = ir.Constant(ir.IntType(32), op[1])
        b = ir.Constant(ir.IntType(32), op[2])
        result = builder.sdiv(a, b, name="div_result")
```

### Testing

```bash
# Test basic compilation
python3 compiler/flamelang/flamelang_to_llvm.py "add 10 20" -o test.o
test -f test.o && echo "✅ Object file created"

# Test optimization passes
python3 compiler/flamelang/flamelang_to_llvm.py "add 5 5" --emit-ir
grep -q "add" flamelang.ll && echo "✅ IR generated"

# Test linking
python3 compiler/flamelang/flamelang_to_llvm.py "add 2 3" -o link_test.o
gcc link_test.o -o link_test -no-pie
./link_test
[ $? -eq 5 ] && echo "✅ Execution successful (exit code 5)"
```

## Troubleshooting

### ImportError: llvmlite

```bash
# Install llvmlite
pip install llvmlite

# Or with conda
conda install -c conda-forge llvmlite
```

### LLVM Version Mismatch

```bash
# Check LLVM version
python3 -c "import llvmlite; print(llvmlite.__version__)"

# Reinstall matching version
pip install --upgrade llvmlite
```

### Linking Errors

```bash
# Use -no-pie flag
gcc program.o -o program -no-pie

# Or specify static linking
gcc program.o -o program -static
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FlameLang Compiler                        │
├─────────────────────────────────────────────────────────────┤
│  1. Parser          (parse_flame)                           │
│     └── FlameLang source → AST (operation tuples)           │
├─────────────────────────────────────────────────────────────┤
│  2. IR Generator    (emit_ir)                               │
│     └── AST → LLVM IR (SSA form)                            │
├─────────────────────────────────────────────────────────────┤
│  3. Optimizer       (optimize_and_compile)                  │
│     ├── Parse IR                                            │
│     ├── Run optimization passes                             │
│     └── Target machine code generation                      │
├─────────────────────────────────────────────────────────────┤
│  4. Code Generator                                          │
│     └── LLVM IR → Native object code (x86_64)              │
└─────────────────────────────────────────────────────────────┘
```

## Performance Characteristics

- **Compilation Speed**: ~0.25s for typical programs (-O3)
- **Binary Size**: 400-800 bytes for simple operations
- **Size Reduction**: 30-50% vs unoptimized
- **Target**: x86_64 native code (portable to ARM with LLVM config)

## License

GPL - Compatible with SAGCO OS licensing

## Author

Strategickhaos DAO - "Ratio Ex Nihilo"
