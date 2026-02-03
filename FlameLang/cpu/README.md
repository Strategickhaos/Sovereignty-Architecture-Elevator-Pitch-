# Caveman Physics Gate

A pure Python constraint-based evaluation system that uses **TRIG6** (6 independent perspectives) to validate claims.

## Overview

The Caveman Physics Gate is a **constraint-only** evaluation system. No belief. No identity. Just constraints.

**Philosophy**: 
- Does it compute? → Ship it.
- Maybe? → TRIG6 it (evaluate from 6 independent viewpoints).
- Nope? → Reject it.

## Features

- ✅ **Pure Python** - No NumPy or external dependencies
- ✅ **TRIG6 Evaluation** - Six independent perspectives (not random hash selection)
- ✅ **Structured Claims** - Dataclass-based claim packets with boolean signals
- ✅ **Clear Verdicts** - NOPE / SANDBOX / FIX+TOSS / SHIP

## The Six Perspectives (TRIG6)

1. **Energy** - Free energy / conservation (violates_energy)
2. **Causality** - Cause→effect order (violates_causality)
3. **Bounds** - Limits / caps / thresholds (has_bounds)
4. **Reproducibility** - Repeatability (reproducible)
5. **Fail-Safe** - Failure mode safety (fails_safe)
6. **Adversary** - What breaks under hostile conditions (confidence-based)

## Usage

```python
from FlameLang.cpu import Claim, CavemanPhysicsGate

gate = CavemanPhysicsGate()

# Create a claim with explicit constraints
claim = Claim(
    text="Energy is conserved in closed systems.",
    violates_energy=False,
    violates_causality=False,
    has_bounds=True,
    reproducible=True,
    fails_safe=True,
    confidence=0.95
)

# Evaluate the claim
result = gate.evaluate(claim)

print(f"Verdict: {result['verdict']}")
print(f"Reason: {result['reason']}")
print(f"Caveman: {result['caveman']}")
```

## Verdict Logic

### NOPE (Hard Reject)
- Violates energy conservation
- Violates causality

**Caveman**: "fuck 'em"

### FIX+TOSS
- Fails unsafe (failsafe = False)
- Must be corrected or discarded

**Caveman**: "fix or toss"

### SANDBOX
- Unbounded (has_bounds = False)
- Not reproducible (reproducible = False)
- Too many unknowns (≥2 perspectives are None)

**Caveman**: "MAYBE → sandbox"

### SHIP
- Passes all constraints
- Bounded, repeatable, safe enough

**Caveman**: "YES → ship"

## Running the Examples

```bash
python3 FlameLang/cpu/caveman_physics_gate.py
```

This will run three example claims:

1. **Magic crystals** - Violates energy & causality → NOPE
2. **Energy conservation** - All constraints pass → SHIP
3. **Fuzzy PDE boundary** - Too many unknowns → SANDBOX

## Design Notes

- **No random angles**: Unlike the previous implementation, this uses actual independent heuristics, not `hash(claim)` for random angle selection.
- **No NumPy**: Pure Python only, uses built-in `dataclasses`.
- **Real evaluation**: The "5 rocks" checks are actual boolean evaluations, not keyword matching.
- **Confidence matters**: The adversary perspective requires high confidence (≥0.85) to pass, keeping the gate honest about threat modeling.

## The "5 Rocks" Signals

When you don't know a constraint value, leave it as `None`. The gate will default to SANDBOX for too many unknowns, which is the safe choice.

If you want to turn this into a real "physics gate", feed it structured claim packets with actual constraint evaluations, not just keyword matches.
