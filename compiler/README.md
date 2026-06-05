# FlameLang Compiler

LLVM-native compiler for the FlameLang symbolic language.

## Features

- LLVM IR generation from FlameLang source
- Portable linking using clang (handles CRT, libc, dynamic loader)
- Optimization: -O3 for ~50% binary size reduction
- Auto-detection of LLVM tools (supports versioned binaries)

## Usage

```bash
python3 flamelang_to_llvm.py <source_file> [output_file]
```

### Example

```bash
# Compile a FlameLang program
echo "# Test program" > hello.flame
python3 flamelang_to_llvm.py hello.flame hello_exec

# Run the executable
./hello_exec
```

## Requirements

- Python 3.8+
- LLVM toolchain (llvm-as, llc)
- Clang compiler

### Install on Debian/Ubuntu

```bash
sudo apt-get install llvm clang python3
```

## Technical Details

### Compilation Pipeline

1. **Parse FlameLang source** → Generate LLVM IR
2. **LLVM IR → Bitcode** (llvm-as)
3. **Bitcode → Object file** (llc)
4. **Link with clang** (clang -O3) ✅ **FIXED: No longer uses brittle `ld`**

### Why Clang for Linking?

The previous approach used `ld` directly, which caused issues:
- Missing C runtime (CRT) initialization
- Distribution-specific differences in library paths
- Manual handling of libc linkage

Using `clang` for linking solves these issues:
- Automatically handles CRT setup
- Portable across distributions
- Proper dynamic loader configuration
- Consistent with LLVM-native approach

## See Also

- [SBIP Specification](../SBIP_SPEC_v1.0.md)
- [FlameLang Specification](../FLAMELANG_SPECIFICATION.md)
