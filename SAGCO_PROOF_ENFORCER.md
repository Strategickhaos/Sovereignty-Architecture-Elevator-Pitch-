# SAGCO Proof Enforcer

**Kernel-side FlameIR admission gate that enforces 16 proofs before execution**

## Overview

The SAGCO Proof Enforcer is a critical security component that sits at the SAGCO syscall boundary. No FlameIR enters the execution domain without passing all invariants.

This transforms FlameLang proofs from "compiler checks" into **kernel law**.

## Architecture

### What This Gives You

- **Flame proofs become kernel law** - Not just compiler suggestions
- **FlameIR becomes a verifiable object** - Not just code
- **SAGCO becomes a proof-governed execution environment** - Not just a runtime

This is the line between:
- "a compiler that emits programs"
- **"an operating system that admits realities"**

## The 16 Proofs

### TIER 1 — KERNEL PROOFS
1. `fixed_point_convergence` - IR must contain expressions
2. `grounding_completeness` - IR must contain grounded operations
3. `genome_classification` - Codon lineage classification
4. `codon_bijection` - Codons must be in 6-bit range [0, 64)

### TIER 2 — PHYSICS PROOFS
5. `angle_boundedness` - Angles must be finite
6. `lipschitz_continuity` - Gradient/fanout limits
7. `wave_conservation` - Wave function integrity
8. `frequency_positivity` - Frequencies must be positive

### TIER 3 — TRANSFORM PROOFS
9. `hebrew_root_validity` - Root validity checks
10. `gematria_bounds` - Numeric bounds
11. `dna_encoding` - Genetic encoding validity
12. `rubik_god_number` - Permutations ≤ 20 (God's number)

### TIER 4 — SYSTEM PROOFS
13. `ir_acyclicity` - No forward/cyclic references
14. `type_safety` - Type system integrity
15. `resource_bounds` - Expression graph ≤ 65,536 nodes
16. `determinism` - No RNG, syscalls, or time sources

## Usage

### Basic Enforcement

```rust
use sagco_proof_enforcer::{FlameIR, FlameExpr, FlameType, FlameOp, enforce_all};

let ir = FlameIR {
    decls: vec![],
    exprs: vec![
        FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
        FlameExpr::Op { kind: FlameOp::Add, args: vec![0] },
    ],
};

match enforce_all(&ir) {
    Ok(()) => println!("IR admitted to execution"),
    Err(e) => println!("IR rejected: {}", e),
}
```

### Syscall Integration

```rust
use sagco_proof_enforcer::sagco_submit_ir;

pub fn handle_syscall(ir: FlameIR) -> Result<TaskId, ProofError> {
    // Enforces all proofs at boundary
    sagco_submit_ir(ir)
}
```

### What Happens on Failure

When any proof fails:
- ❌ IR is rejected
- ❌ Task is not scheduled
- ✅ Proof name + tier returned to caller
- ✅ Kernel remains uncontaminated

## Building

```bash
# Build the library
cargo build --release

# Run tests
cargo test

# Run the example
cargo run --example basic_enforcement
```

## Testing

The enforcer includes comprehensive tests for all proof violations:

```bash
# Run all tests
cargo test

# Run specific test
cargo test test_codon_out_of_range

# Run with output
cargo test -- --nocapture
```

## Integration Points

### At Syscall Boundary

```rust
pub fn sagco_submit_ir(ir: FlameIR) -> Result<TaskId, ProofError> {
    sagco_proof_enforcer::enforce_all(&ir)?;
    scheduler::admit(ir)
}
```

### Proof IDs (Stable ABI)

The `flame_proof_ids` module provides stable kernel ABI:

```rust
use sagco_proof_enforcer::ProofId;

let proof = ProofId::CodonBijection;
println!("Proof: {} (tier: {})", proof.name(), proof.tier_name());
```

## No-Std Support

For bare-metal or kernel environments:

```toml
[dependencies]
sagco-proof-enforcer = { version = "0.1", default-features = false }
```

The enforcer is designed to work in `no_std` environments with no heap allocation required.

## Examples

See `examples/basic_enforcement.rs` for a comprehensive demonstration of all proof scenarios.

## License

MIT

## Architecture Note

This enforcer implements the philosophical distinction between:
- Traditional OS: "Run this code"
- SAGCO: "Admit this reality"

FlameIR isn't executed - it's **admitted** after proving its nature aligns with universal invariants.
