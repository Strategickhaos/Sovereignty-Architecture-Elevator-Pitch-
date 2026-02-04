# FlameLang Examples

This directory contains example FlameLang programs demonstrating the language features.

## Files

- **hello.flame** - Simple program returning 42
- **math.flame** - Demonstrates all arithmetic operations
- **fibonacci.flame** - Multi-step computation example

## Usage

Compile any example with:

```bash
python3 flamelang_to_llvm.py examples/flamelang/hello.flame
./flamelang_exec
echo $?  # Check exit code
```

Or view the LLVM IR:

```bash
python3 flamelang_to_llvm.py --ir "add 5 3"
```

## FlameLang v1.0 Language Reference

### Supported Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Addition | `add <a> <b>` | Adds two integers |
| Subtraction | `sub <a> <b>` | Subtracts b from a |
| Multiplication | `mul <a> <b>` | Multiplies two integers |
| Division | `div <a> <b>` | Integer division (a / b) |
| Return | `ret <val>` | Explicit return value |

### Comments

Lines starting with `#` are comments and are ignored.

### Note

Currently, FlameLang v1.0 executes operations sequentially but only returns the result of the last operation. Variable assignment and result chaining will be added in future versions.
