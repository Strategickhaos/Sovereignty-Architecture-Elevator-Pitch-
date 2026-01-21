# 🔥 FlameLang Examples

This directory contains example FlameLang programs that demonstrate the Sovereignty Architecture framework's mathematical and physical proofs.

## hello_sovereign.flm

The first sovereign FlameLang program that tests four core proofs of the Sovereignty Architecture:

### Proof Tests

#### PROOF 5: PIPE CLOSURE (Σθ = 360°)
Tests that a closed pipe path with four 90° bends sums to 360°, demonstrating topological closure properties.

**Variables:**
- `theta1, theta2, theta3, theta4`: Four 90-degree angles
- `r`: Pipe radius (5.0 inches, standard pipe size)

**Operations:**
- `bend theta radius r`: Computes arc length for each elbow using s = r × θ

**Result:** ✓ PASSES (90° + 90° + 90° + 90° = 360°)

#### PROOF 6: RUBIK BOUND (≤ 20 moves)
Tests adherence to the Rubik's Cube God's Number theorem, which states any scrambled Rubik's Cube can be solved in 20 moves or fewer.

**Variables:**
- `scramble: perm = 15`: A 15-move scramble from solved state

**Operations:**
- `perm scramble`: Validates the permutation is within the 20-move bound

**Result:** ✓ PASSES (15 ≤ 20)

#### PROOF 4: CODON BIJECTION (64 ↔ 64)
Tests the bijective mapping between 64 audio frequencies and the 64 genetic codons, establishing a reversible correspondence.

**Variables:**
- `freq: freq = 440Hz`: A4 tuning standard frequency

**Operations:**
- `codon freq`: Bijectively maps frequency to one of 64 codons

**Result:** ✓ PASSES (mapping is reversible: 440Hz → [A,T,G] → index 42 → ~440Hz)

#### PROOF 2: GROUNDING (finite values only)
Tests that all values are finite and bounded, ensuring no infinities or NaN values exist in the system.

**Variables:**
- `finite: float = 42.0`: A finite, bounded value

**Invalid Operations (would fail compilation):**
- `let infinite: float = 1.0 / 0.0;` ❌ FlameError::ProofViolation
- `let nan: float = 0.0 / 0.0;` ❌ FlameError::ProofViolation

**Result:** ✓ PASSES (42.0 is finite and bounded)

### Output

If all proofs pass, the program returns `42` (the answer to life, the universe, and everything).

## About FlameLang

FlameLang is a sovereign symbolic language designed for the Strategickhaos Sovereignty Architecture. It provides:

1. **Proof-Based Validation** — Programs must satisfy mathematical proofs to compile
2. **Physical Constraints** — Embeds real-world physical and topological constraints
3. **Symbolic Execution** — Glyph-based execution model for sovereign computing
4. **Bijective Mappings** — Reversible transformations between domains (audio ↔ genetics)

For the complete FlameLang specification, see [FLAMELANG_SPECIFICATION.md](../../FLAMELANG_SPECIFICATION.md).

## Copyright

© 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo
