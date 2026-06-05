# CPU Module - Caveman Physics Gate

This directory contains kernel-level modules for the Sovereignty Architecture, including the Caveman Physics Gate for validating claims against physical constraints.

## Caveman Physics Gate

### Overview

The **Caveman Physics Gate** is a validation system that checks claims against fundamental physics principles using the "5 rocks gate" approach and TRIG6 angle analysis for fuzzy/uncertain claims.

### Philosophy

"Does this shit compute?"
- If **no** → reject (discard / sandbox)
- If **maybe** → TRIG6 it (test from more angles)
- If **yes** → keep building / ship

**No belief. No identity. Just angles.**

### Features

1. **5 Rocks Gate**: Basic validation against fundamental principles
   - Energy conservation
   - Causality
   - Constraints (bounded behavior)
   - Reproducibility
   - Safe failure modes

2. **TRIG6 Analysis**: Tests fuzzy/uncertain claims from 6 angles using trigonometric functions
   - Computes norms at 6 evenly spaced angles (0°, 60°, 120°, 180°, 240°, 300°)
   - Classifies based on norm values:
     - **BLOWS UP** (norm > 1e5): Reject with love
     - **UNBOUNDED** (norm > 50): Fuck em
     - **RESONATES NARROW** (6 < norm < 8): Handle gently
     - **BOUNDED** (norm ≤ 6): Keep building / ship

3. **Deterministic**: Uses MD5 hashing for reproducible results across sessions

### Usage

#### As a script

```bash
cd /path/to/repo
python3 cpu/caveman_physics_gate.py
```

#### As a module

```python
from caveman_physics_gate import CavemanPhysicsGate

# Create gate instance
gate = CavemanPhysicsGate()

# Check a claim
verdict = gate.check_claim("Energy is conserved in closed systems.")
print(verdict)  # Output: YES → SHIP

# Check a fuzzy claim
verdict = gate.check_claim("Maybe this PDE boundary is fuzzy.")
print(verdict)  # Output: MAYBE → TRIG6: BOUNDED → KEEP → SHIP

# Check an invalid claim
verdict = gate.check_claim("Magic crystals heal everything.")
print(verdict)  # Output: If yes → nope.
```

### Example Output

```
Claim: "Magic crystals heal everything instantly."
If yes → nope.

Claim: "Energy is conserved in closed systems."
YES → SHIP

Claim: "Pipe offsets compute consciousness."
YES → SHIP

Claim: "Maybe this PDE boundary is fuzzy."
MAYBE → TRIG6: BOUNDED → KEEP → SHIP
```

### Dependencies

- **numpy** (>=1.24.0): For trigonometric computations
- **hashlib**: For deterministic claim hashing (standard library)
- **math**: For basic trigonometric functions (standard library)

### Installation

Ensure numpy is installed:

```bash
pip3 install numpy>=1.24.0
```

Or install all sovereignty requirements:

```bash
pip3 install -r requirements.sovereignty.txt
```

### Technical Details

#### TRIG6 Computation

For each of the 6 angles (θ), the gate computes a 6-dimensional vector:
- sin(θ)
- cos(θ)
- tan(θ) = sin(θ)/cos(θ)
- csc(θ) = 1/sin(θ)
- sec(θ) = 1/cos(θ)
- cot(θ) = cos(θ)/sin(θ)

The norm is computed as: `√(sin²(θ) + cos²(θ) + tan²(θ) + csc²(θ) + sec²(θ) + cot²(θ))`

Values are capped at 10⁶ to prevent overflow for angles where denominators approach zero.

#### Claim Mapping

Claims are mapped to one of the 6 angles using MD5 hashing:
```python
claim_hash = int(hashlib.md5(claim.encode()).hexdigest(), 16)
idx = claim_hash % 6
```

This ensures deterministic, reproducible results across Python sessions.

### Testing

Run the included validation tests:

```bash
python3 /tmp/test_caveman_gate.py
```

Expected output:
```
✓ Test 1 passed: Magic claim rejected
✓ Test 2 passed: Valid physics claim shipped
✓ Test 3 passed: Fuzzy claim triggers TRIG6
✓ Test 4 passed: Free energy claim rejected
✓ Test 5 passed: TRIG6 correctly computed 6 angles

✅ All tests passed!
```

### Security

This module has been validated with CodeQL and found no security vulnerabilities.

### Future Enhancements

- Legion query integration for distributed claim validation
- PDE boundary tie for mathematical consistency checking
- More sophisticated 5 rocks gate checks beyond keyword matching
- Integration with observability stack for claim tracking

---

**Part of the Strategickhaos Sovereignty Architecture**  
"Caveman style: Straight reject with 'fuck em' if unbounded." 🦁😈💜
