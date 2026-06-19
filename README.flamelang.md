# 🔥 FlameLang Compiler

A revolutionary compiler that enforces physics at compile time through multi-layer transformations.

## Overview

FlameLang is a language that validates mathematical invariants during compilation, ensuring that your code respects fundamental physical laws. The compiler transforms code through multiple layers:

1. **Layer 1**: Linguistic (English → Hebrew)
2. **Layer 2**: Numeric (Unicode → Gematria)
3. **Layer 3**: Wave (c=2πr → Hz)
4. **Layer 4**: DNA (Freq → Codon)
5. **Layer 5**: LLVM IR Generation
6. **Proof Validation**: 16 mathematical theorems

## Installation

### Prerequisites

- Rust 1.70 or later

### Building from Source

```bash
cargo build --release
```

The compiler binary will be available at `target/release/flamec`.

## Usage

### Basic Compilation

```bash
flamec input.flame              # Compile to binary
```

### Custom Output

```bash
flamec input.flame -o output    # Specify output file
```

### Advanced Options

```bash
flamec input.flame --emit=llvm  # Emit LLVM IR only
flamec input.flame --validate   # Run proofs only, no codegen
```

### Help

```bash
flamec --help     # Show usage information
flamec --version  # Show version information
```

## Example Programs

See the `examples/flamelang/` directory for sample programs:

- `hello.flame` - Hello World example
- `physics.flame` - Physics transformation example
- `simple.flm` - Minimal program

### Running Examples

```bash
flamec examples/flamelang/hello.flame
./examples/flamelang/hello
```

## Proof Validation

The FlameLang compiler validates the following mathematical invariants:

- ✓ Fixed-point convergence
- ✓ Grounding completeness (M/F/B)
- ✓ Codon bijection (64 ↔ 64)
- ✓ Pipe bend closure (Σθ = 360°)
- ✓ Rubik bound (≤ 20 moves)
- ✓ Setback identity (arc = r × θ)

If your code violates any of these invariants, compilation will fail with a detailed error message.

## File Extensions

- `.flame` - Standard FlameLang source files
- `.flm` - Abbreviated FlameLang source files

## Testing

Run the test suite:

```bash
cargo test
```

## Development

### Project Structure

```
.
├── Cargo.toml              # Rust project configuration
├── src/
│   ├── lib.rs              # Compiler library
│   └── bin/
│       └── flamec.rs       # CLI binary
├── examples/
│   └── flamelang/          # Example programs
└── README.flamelang.md     # This file
```

## License

© 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

## Philosophy

> FlameLang enforces physics at compile time.  
> Illegal physics = compilation error.

Traditional compilers check syntax and types. FlameLang goes further by validating that your code respects fundamental mathematical and physical laws. This ensures correctness at a deeper level than conventional languages.

## Specification

For detailed information about the FlameLang language design, see `FLAMELANG_SPECIFICATION.md`.
