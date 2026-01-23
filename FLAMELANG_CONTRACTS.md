# 🔥 FlameLang Contract Documentation

## Overview

This directory contains the **canonical contracts** extracted from the FlameLang v2.0.0 compiler source code. These contracts define the formal specification that all FlameLang tools and implementations must adhere to.

## Contract Files

### 1. `flame_ir.contract.yaml`

**Purpose**: Defines the canonical Intermediate Representation (IR) used by the FlameLang compiler.

**Contents**:
- **Type System**: 5 core types with proof constraints
  - `Float`: Standard floating-point values
  - `Angle`: Radians with mod 2π enforcement
  - `Codon`: DNA codon states (0-63)
  - `Perm`: Rubik's Cube permutations (0-20)
  - `Freq`: Frequency in Hertz (positive)

- **Operations**: 15+ operations across 4 categories
  - Arithmetic: `Add`, `Sub`, `Mul`, `Div`
  - Trigonometric: `Sin`, `Cos`, `Tan`
  - Domain Transforms: `Bend`, `Codon`, `Perm` (your physics kernel)
  - Wave Encoding: `ToFreq`, `FromFreq`

- **IR Structure**: The canonical data structures
  - `FlameIR`: Top-level container (decls + exprs)
  - `FlameDecl`: Variable/function declarations
  - `FlameExpr`: Expression nodes (Lit, Var, Op, Return)

- **Examples**: Concrete IR representations
  - Hello World: `42 * 2 + 10`
  - Arc to Codon: `🔥(angle, radius) → 🧬`

**Key Insight**: This is the **single source of truth** for what valid FlameLang IR looks like. All compiler passes transform source code into this representation.

---

### 2. `sagco_syscalls.contract.yaml`

**Purpose**: Defines the execution model and system calls for the SAGCO (Sovereign Architecture General Computing Operations) runtime.

**Contents**:
- **Execution Model**: 5-layer transformation pipeline
  - Frontend: Lexer → Parser → AST → IR
  - Middle-end: 4 semantic transformation layers
  - Backend: LLVM IR → Binary

- **Syscalls**: 28+ system operations across 5 categories
  - **Frontend** (3 syscalls): tokenize, parse, lower
  - **Transforms** (4 syscalls): linguistic, numeric, wave, DNA layers
  - **Proof Validation** (16 syscalls): theorem checking organized in 4 tiers
  - **Backend** (2 syscalls): LLVM codegen, binary emission
  - **I/O** (2 syscalls): read source, write binary

- **16 Proof Theorems**:
  - **Tier 1 - Kernel**: Fixed-point convergence, grounding, genome, codon bijection
  - **Tier 2 - Physics**: Angle bounds, Lipschitz continuity, wave conservation, frequency positivity
  - **Tier 3 - Transforms**: Hebrew roots, gematria, DNA encoding, Rubik's God Number
  - **Tier 4 - System**: IR acyclicity, type safety, resource bounds, determinism

- **Syscall Sequences**: Standard execution flows
  - Full compilation: 12-step sequence (28 total syscalls)
  - AST-only: Fast syntax checking
  - IR transform: Middle-end only

**Key Insight**: This defines **HOW** FlameLang programs execute. Every compilation follows these exact syscall sequences.

---

## Extraction Methodology

These contracts were **extracted directly from actual source code**, not imagined:

1. **Source Analysis**: Examined `src/pipeline.rs`, `src/lib.rs`, and parser/lexer modules
2. **Structure Mapping**: Identified IR structs (`FlameType`, `FlameOp`, `FlameExpr`, `FlameDecl`)
3. **Flow Tracing**: Followed `compile()` function through all stages
4. **Proof Enumeration**: Catalogued all 16 `validate_*` proof functions
5. **Contract Synthesis**: Formalized discovered patterns into YAML specifications

## Usage

### For Compiler Developers
Use these contracts as the specification when implementing FlameLang features:
```bash
# Before implementing a new operation:
grep -A 10 "operations:" flame_ir.contract.yaml

# Before adding a transformation pass:
grep -A 20 "transforms:" sagco_syscalls.contract.yaml
```

### For Verification Engineers
These contracts define the proof obligations:
```bash
# List all required proofs:
grep "proof_required:" flame_ir.contract.yaml

# See proof validation syscalls:
grep "sys_validate_" sagco_syscalls.contract.yaml
```

### For Tool Builders
Parse these contracts to generate bindings:
```python
import yaml

# Load IR contract
with open('flame_ir.contract.yaml') as f:
    ir_spec = yaml.safe_load(f)
    
# Generate type definitions
for type_name, type_spec in ir_spec['types'].items():
    print(f"Type: {type_name}")
    print(f"  Representation: {type_spec['representation']}")
    print(f"  Constraints: {type_spec['constraints']}")
```

## Verification Status

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | ✅ Implemented | Lexer, parser, AST lowering working |
| Transforms | ⚠️ Stubs | Pass-through implementations (TODO) |
| Proofs | ⚠️ Stubs | All return `Ok()` (TODO) |
| Backend | 🔄 Partial | LLVM IR generation only (no inkwell yet) |

## Contract Compliance

To be **FlameLang-compliant**, an implementation must:

1. ✅ Accept source that lexes/parses per the grammar
2. ✅ Lower to `FlameIR` with exact structure in `flame_ir.contract.yaml`
3. ✅ Execute syscall sequences as defined in `sagco_syscalls.contract.yaml`
4. ✅ Validate all 16 proof theorems before code generation
5. ✅ Generate semantically equivalent output

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-23 | Initial extraction from compiler source |

## References

- **FlameLang Specification**: `FLAMELANG_SPECIFICATION.md`
- **Compiler Source**: Not currently in this repo (extracted from build sessions)
- **Build ID**: `ratio-ex-nihilo`
- **Copyright**: © 2025 Strategickhaos DAO LLC

## License

MIT License - Same as FlameLang compiler

---

## Quick Reference

### Type System (5 types)
```
Float → Angle → Freq → Codon → Perm
  ↓      ↓       ↓       ↓      ↓
 f64   [0,2π)   >0Hz  [0,63]  [0,20]
```

### Transformation Pipeline (5 layers)
```
English → Hebrew → Gematria → Wave → DNA → LLVM
Layer 1   Layer 2   Layer 3   Layer 4  Layer 5
```

### Proof Tiers (16 theorems)
```
Tier 1: Kernel (4)    → Mathematical foundations
Tier 2: Physics (4)   → Physical constraints
Tier 3: Transform (4) → Encoding correctness
Tier 4: System (4)    → Runtime guarantees
```

---

**Generated**: 2026-01-23  
**Build**: ratio-ex-nihilo  
**Maintainer**: dom@strategickhaos.ai
