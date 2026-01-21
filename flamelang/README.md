# 🔥 FlameLang v2.0.0

Sovereign 5-Layer Transformation Pipeline

## Overview

FlameLang is a symbolic programming language that transforms source code through five distinct layers:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: LINGUISTIC    English → Hebrew → Glyph                            │
│  LAYER 2: NUMERIC       Unicode → Decimal → Hex                             │
│  LAYER 3: WAVE          Decimal → c=2πr → Hz/BPS                            │
│  LAYER 4: DNA           Freq → Codon → ACGT Sequence                        │
│  LAYER 5: LLVM          Codon → Opcode → Native Binary                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Mathematical Foundations (16 Proofs)

- **Tier 1 (Kernel)**: Fixed-point convergence, grounding, genome, bijection
- **Tier 2 (Geometric)**: Pipe closure, Rubik bound, Fourier, setback identity
- **Tier 3 (Adversarial)**: Fallacy detection, jujitsu, RLHF, chess isomorphism
- **Tier 4 (Distribution)**: Torrent, hash chain, DNA durability, swarm immortality

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
flamelang = "2.0.0"
```

## Usage

```rust
use flamelang::compile;

let source = r#"
    let r: float = 5.0;
    let theta: angle = 90deg;
    bend theta radius r;
"#;

let binary = compile(source)?;
```

## Example

Run the hello world example:

```bash
cd flamelang
cargo run --example hello_flame
```

## Compilation Targets

FlameLang supports multiple compilation targets:

- `Target::Hebrew` - Stop after Layer 1 (Hebrew roots)
- `Target::Numeric` - Stop after Layer 2 (Numeric/Gematria)
- `Target::Wave` - Stop after Layer 3 (Wave/Frequency)
- `Target::Dna` - Stop after Layer 4 (DNA/Codon)
- `Target::LlvmIr` - Emit LLVM IR
- `Target::Native` - Full native binary (default)

## Testing

```bash
cargo test
```

## Architecture

### Layer 1: Linguistic Transformation
Tokenizes source code and performs lexical analysis.

### Layer 2: Numeric Transformation
Converts tokens to numeric representations (Unicode → Decimal → Hex).

### Layer 3: Wave Transformation
Applies wave mathematics using the formula c = 2πr to generate frequencies.

### Layer 4: DNA Transformation
Maps frequencies to DNA codons and ACGT sequences.

### Layer 5: LLVM Code Generation
Generates LLVM IR and compiles to native binary.

## License

MIT License

## Copyright

© 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo
