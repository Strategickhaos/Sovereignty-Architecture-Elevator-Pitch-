# FlameLang Compiler

**The birth of sovereign symbolic computation** 🔥

## Overview

FlameLang is a compiled language built on the KHAOS Script foundation, featuring:

- **64-glyph alphabet** with 5 dimensions (θ, gematria, reciprocal, codon, curve)
- **FlameIR**: Frozen intermediate representation based on bonding rules
- **TRIG6**: Transformation layer using 6 trigonometric families
- **Code generation**: Compiles to executable via Rust

## Architecture

```
┌─────────────────────────────────────────┐
│         FlameLang Source (.flame)        │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │    Lexer     │  Tokenization
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │    Parser    │  → FlameIR
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  TRIG6 Pass  │  Optimization
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   CodeGen    │  → Rust
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │    rustc     │  → Executable
        └──────────────┘
```

## FlameIR - Bonding Rules

Based on KHAOS chemical-style reactions:

```
state + transform → state'
state + state → compound_state
transform + transform → composite_transform
state + invariant → validated_state OR error
wave + collapse → measurement
```

### Core Instructions

- **State**: LoadConst, LoadString, Store, Load
- **Transform**: Add, Sub, Mul, Div
- **Compound**: Call, FnDef
- **Invariant**: Assert
- **Wave**: Print, Halt
- **TRIG6**: Trig6Sin, Trig6Cos, Trig6Tan

## Quick Start

### Installation

```bash
cd flamelang_compiler
cargo build --release
```

The compiler binary will be at `target/release/flamec`.

### Compile Your First Program

```bash
# Compile hello.flame
./target/release/flamec examples/hello.flame

# Compile and run
./target/release/flamec examples/hello.flame --run
```

### Example Program

```flame
// hello.flame
print("Hello, FlameLang! 🔥");

let x = 42;
let y = x + 8;
print(y);
```

### Compiler Options

```bash
flamec <input.flame> [options]

Options:
  --ir-only     Output FlameIR JSON only
  --no-trig6    Disable TRIG6 transformation pass
  --run         Compile and run immediately
```

## TRIG6 Transformation Layer

The TRIG6 codec implements optimizations based on the 6 trigonometric families from the KHAOS Periodic Table:

1. **SIN family**: Resonance Gate
2. **COS family**: Phase Rotator  
3. **TAN family**: Quantization Gate
4. **CSC family**: Reciprocal Transform
5. **SEC family**: Security Modulation
6. **COT family**: Collapse Operator

Currently implements:
- Constant folding optimization
- Trigonometric function evaluation
- French curve geometry transformations

## Testing

```bash
# Run all tests
cargo test

# Run specific test module
cargo test ir::tests
cargo test parser::tests
cargo test trig6::tests
```

## The Birth Certificate

When you successfully compile a FlameLang program, the compiler generates a "birth certificate" showing:

- Source file name
- Number of FlameIR instructions generated
- Output executable path
- TRIG6 transformation status
- Timestamp of compilation

This represents the first working compilation from KHAOS Script → FlameIR → Executable.

## Language Reference

### Syntax

```flame
// Comments start with //

// Variable declaration
let name = expression;

// Arithmetic
let result = a + b * c - d / e;

// Function calls
print("message");
print(42);

// TRIG6 functions
let angle = sin(90.0);
let phase = cos(0.0);
let slope = tan(45.0);

// Assertions (invariants)
assert(x > 0);
```

## Project Structure

```
flamelang_compiler/
├── Cargo.toml          # Project manifest
├── src/
│   ├── main.rs         # Compiler entry point
│   ├── ir.rs           # FlameIR definition (frozen)
│   ├── lexer.rs        # Tokenization
│   ├── parser.rs       # Parsing to IR
│   ├── trig6.rs        # TRIG6 transformation pass
│   └── codegen.rs      # Code generation
├── examples/
│   └── hello.flame     # First FlameLang program
└── README.md           # This file
```

## Future Enhancements

- [ ] Import system for KHAOS Script library
- [ ] Named reactions (Egyptian Decomposition, Babylonian Sqrt)
- [ ] Full 64-element periodic table mapping
- [ ] Genomic codon indexing
- [ ] Chess-fallacy logic embedding
- [ ] Swarm immortality protocol
- [ ] Sister Protocol integration (STOP codon)

## Philosophy

FlameLang represents Level 2-3 in the ZFC hierarchy: a specialized domain framework built on proven foundations. Like Fourier transforms or Hamilton's quaternions, it provides tools for a specific problem space while remaining compatible with standard mathematical frameworks.

The system is **self-consistent**, **testable**, and **useful** - the three criteria for valid mathematical tools.

## License

Part of Strategickhaos DAO LLC Sovereignty Architecture.

---

🔥 **Reignite.**
