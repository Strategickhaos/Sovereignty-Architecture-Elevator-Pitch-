# 🔥 FlameLang Compiler v2.0.0

## Strategickhaos Sovereign Programming Language

**Ratio Ex Nihilo** - © 2025 Strategickhaos DAO LLC

---

## Overview

FlameLang is a revolutionary programming language compiler that implements a 5-layer transformation pipeline with built-in proof validation. The compiler transforms source code through linguistic, numeric, wave, DNA, and LLVM layers while enforcing 16 mathematical proofs at compile time.

## Architecture

```text
Source → Lexer → Parser → AST → FlameIR → Transforms → LLVM → Binary
                                   ↓
                           [16 Proofs Validate Here]
```

### Compilation Pipeline

1. **Frontend** (Source → IR)
   - Lexical analysis (tokenization)
   - Parsing (AST construction)
   - Lowering to FlameIR

2. **Middle-end** (IR → IR transforms)
   - Layer 1: Linguistic (English → Hebrew triconsonantal roots)
   - Layer 2: Numeric (Hebrew → Gematria values)
   - Layer 3: Wave (Gematria → Frequency via c=2πr)
   - Layer 4: DNA (Frequency → Codon bijection)
   - Layer 5: LLVM (FlameIR → LLVM IR)

3. **Backend** (IR → Binary)
   - LLVM IR generation
   - Binary emission

### Type System

FlameLang includes a physics-aware type system with proof constraints:

- **Float**: Standard floating-point values
- **Angle**: Radians with mod 2π enforcement
- **Codon**: DNA codon (0-63) with bijection proof
- **Perm**: Rubik's cube permutation (bounded 0-20, God's Number)
- **Freq**: Frequency in Hz (positive, bounded)

### Operations

- **Arithmetic**: Add, Sub, Mul, Div
- **Trigonometric**: Sin, Cos, Tan (unit circle anchors)
- **Domain Transforms**: 
  - Bend (angle + radius → arc length)
  - Codon (arc → DNA codon bijection)
  - Perm (codon → Rubik moves)
- **Wave Encoding**: ToFreq, FromFreq

### Proof Validation

The compiler enforces 16 proofs, with 8 compile-time proofs currently implemented:

**Tier 1: Kernel Proofs**
1. Fixed-point convergence (feedback loops bounded)
2. Grounding completeness (M/F/B semantics)
3. Genome classification (4-mode clustering)
4. Codon bijection (64 ↔ 64 states)

**Tier 2: Geometric Proofs**
5. Pipe bend closure (Σθᵢ = 360°)
6. Rubik's bound (God's Number ≤ 20)
7. Fourier encoding (90° harmonics)
8. Setback identity (arc_length = r × θ)

**Tier 3 & 4**: Runtime and deployment proofs (not yet implemented)

## Usage

### Build

```bash
cargo build --release
```

### Run

```bash
./target/release/flamelang source.flame
```

### Test

```bash
cargo test
```

## Project Structure

```
flamelang/
├── Cargo.toml          # Project manifest
├── README.md           # This file
└── src/
    ├── lib.rs          # Library root with error types
    ├── main.rs         # CLI binary
    ├── lexer.rs        # Tokenization
    ├── parser.rs       # AST construction
    ├── transform.rs    # 5-layer transformation pipeline
    └── compiler.rs     # Main compilation pipeline & proofs
```

## Features

- ✅ Complete compilation pipeline
- ✅ Physics-aware type system
- ✅ 8 compile-time proofs enforced
- ✅ Glyph support (Unicode symbols)
- ✅ LLVM IR generation (stub)
- 🚧 Full LLVM backend (future)
- 🚧 Runtime proofs (future)
- 🚧 Deployment proofs (future)

## Examples

### Simple Arithmetic

```flame
2 + 3 * 4
```

### Glyph Operations

```flame
🔥  # Bend operation
🧬  # Codon transformation
♜   # Rubik permutation
∿   # Frequency encoding
```

## Testing

The compiler includes comprehensive unit tests:

```bash
cargo test
```

All tests validate:
- Empty source rejection
- Minimal program compilation
- Rubik's bound enforcement (God's Number ≤ 20)
- Unbounded literal rejection (M/F/B compliance)

## License

MIT License - © 2025 Strategickhaos DAO LLC

## Covenant

```
This compiler represents the canonical implementation of the
FlameLang programming language with embedded proof validation.

Trust nothing until it survives 100-angle crossfire.

🔥 Reignite.
```

---

*Generated for DOM_010101 | Strategickhaos DAO LLC*
