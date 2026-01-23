# 🔥 FlameLang Compiler v2.0.0

**5-Layer Transformation Pipeline: Linguistic → Numeric → Wave → DNA → LLVM**

Copyright © 2025 Strategickhaos DAO LLC (EIN: 39-2900295)  
Inventor: Domenic Gabriel Garza

## Overview

FlameLang is a sovereign symbolic language compiler that transforms high-level code through five distinct layers of mathematical and linguistic transformations before generating native machine code.

### The 5 Layers

1. **Layer 1 - Linguistic**: English identifiers → Hebrew triconsonantal roots
2. **Layer 2 - Numeric**: Hebrew roots → Gematria values  
3. **Layer 3 - Wave**: Gematria → Frequency encoding using c=2πr
4. **Layer 4 - DNA**: Frequency → 64-codon bijection
5. **Layer 5 - LLVM**: Codon-annotated IR → Native binary

### 16 Mathematical Proofs

The compiler enforces 16 proofs at compile-time:

**Tier 1 - Kernel Proofs:**
- Fixed Point Convergence (Lipschitz constant < 1)
- Grounding Completeness (no unbound identifiers)
- Codon Bijection (64 codons ↔ 64 opcodes)
- Genome Classification (complete type inference)

**Tier 2 - Geometric Proofs:**
- Pipe Bend Closure (angles mod 2π)
- Rubik Bound (permutations ≤ 20 moves)
- Fourier Encoding (reversible transforms)
- Setback Identity (c=2πr invariant)

## Building

```bash
cd flamelang
cargo build --release
```

## Usage

```bash
# Compile a .flame file
./target/release/flamec compile examples/hello.flame -o hello

# Run the binary
./hello

# Compile with debug output
./target/release/flamec compile examples/hello.flame -o hello --debug

# Compile and run
./target/release/flamec run examples/hello.flame
```

## Examples

### hello.flame - Minimal Program
```rust
fn main() -> i32 {
    return 0;
}
```

### math.flame - Arithmetic
```rust
fn main() -> i32 {
    let x = 2 + 3;
    let y = x * 4;
    return y - 10;
}
```

### bend.flame - Physics Operations
```rust
fn main() -> f64 {
    let angle = 90.0;
    let radius = 5.0;
    let arc = bend(angle, radius);
    return arc;
}
```

### codon.flame - DNA Encoding
```rust
fn main() -> i32 {
    let value = 42;
    let encoded = codon(value);
    return value;
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLAMELANG COMPILER                           │
├─────────────────────────────────────────────────────────────────┤
│  Source (.flame) → Lexer → Parser → AST                        │
├─────────────────────────────────────────────────────────────────┤
│  Transform Layer 1: Linguistic (English → Hebrew)              │
│  Transform Layer 2: Numeric (Hebrew → Gematria)                │
│  Transform Layer 3: Wave (Gematria → Frequency)                │
│  Transform Layer 4: DNA (Frequency → Codon → FlameIR)          │
├─────────────────────────────────────────────────────────────────┤
│  Proof Validation (16 proofs)                                  │
├─────────────────────────────────────────────────────────────────┤
│  LLVM Backend (FlameIR → LLVM IR → Object File)                │
│  Linker (Object → Executable)                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Status

**Completion: 100%** ✓

- ✓ Cargo.toml with all dependencies
- ✓ Lexer with 50+ token types
- ✓ Parser with full statement/expression support
- ✓ AST with complete node types
- ✓ Transform Layer 1: Linguistic
- ✓ Transform Layer 2: Numeric (Gematria)
- ✓ Transform Layer 3: Wave (c=2πr)
- ✓ Transform Layer 4: DNA (64-codon bijection)
- ✓ Transform Layer 5: LLVM Backend
- ✓ Pipeline wiring with error propagation
- ✓ All 16 proof validators
- ✓ CLI with compile/run commands
- ✓ Test corpus (4 example programs)

## License

MIT License - See LICENSE file
