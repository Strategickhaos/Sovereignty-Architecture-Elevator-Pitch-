# 🔥 FlameLang Compiler

**A sovereign symbolic language that enforces physics at compile time.**

FlameLang compiles through multiple transformation layers, validating mathematical invariants at each step. Illegal physics = compilation error.

## Features

- **Multi-layer Transformation Pipeline**
  - Layer 1: Linguistic (English → Hebrew)
  - Layer 2: Numeric (Unicode → Gematria)
  - Layer 3: Wave (c=2πr → Hz)
  - Layer 4: DNA (Freq → Codon)
  - Layer 5: LLVM IR Generation

- **Proof Validation** - 16 mathematical theorems enforced at compile time:
  - Fixed-point convergence
  - Grounding completeness (M/F/B)
  - Codon bijection (64 ↔ 64)
  - Pipe bend closure (Σθ = 360°)
  - Rubik bound (≤ 20 moves)
  - Setback identity (arc = r × θ)

## Installation

Build from source using Cargo:

```bash
cargo build --release
```

The compiler binary will be located at `target/release/flamec`.

## Usage

```bash
# Compile to binary
flamec input.flame

# Specify output file
flamec input.flame -o output

# Show help
flamec --help

# Show version
flamec --version
```

## Example

Create a simple FlameLang program (`hello.flame`):

```flame
// Hello World in FlameLang
main {
    return 0;
}
```

Compile it:

```bash
flamec hello.flame
```

Output:

```
🔥 FlameLang Compiler v1.0.0
   Ratio Ex Nihilo - Genesis Build

📄 Compiling: hello.flame

   Pipeline:
   ├── Layer 1: Linguistic (English → Hebrew)
   ├── Layer 2: Numeric (Unicode → Gematria)
   ├── Layer 3: Wave (c=2πr → Hz)
   ├── Layer 4: DNA (Freq → Codon)
   ├── Layer 5: LLVM IR Generation
   └── Proof Validation (16 theorems)

✅ Compiled successfully!
   Output: hello (62 bytes)

   Proofs validated:
   ├── ✓ Fixed-point convergence
   ├── ✓ Grounding completeness (M/F/B)
   ├── ✓ Codon bijection (64 ↔ 64)
   ├── ✓ Pipe bend closure (Σθ = 360°)
   ├── ✓ Rubik bound (≤ 20 moves)
   └── ✓ Setback identity (arc = r × θ)
```

## Project Structure

```
.
├── Cargo.toml          # Workspace configuration
├── flamelang/          # FlameLang compiler library
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs      # Core compilation logic
├── flamec/             # CLI binary
│   ├── Cargo.toml
│   └── src/
│       └── main.rs     # Command-line interface
└── examples/
    └── flamelang/      # Example FlameLang programs
        └── hello.flame
```

## Development

### Running Tests

```bash
cargo test
```

### Building Release Version

```bash
cargo build --release
```

### Running Examples

```bash
./target/release/flamec examples/flamelang/hello.flame
```

## License

MIT License

© 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo
