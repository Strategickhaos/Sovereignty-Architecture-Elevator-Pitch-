# Execution Kernel (INV-098)

## Overview

The **Strategickhaos Execution Kernel v1.0** is a sophisticated fixed-point iteration system that implements a feedback loop between three specialized calculators:

```
pipe_bend → dna_codon → rubik_solver → pipe_bend (loop)
```

This kernel demonstrates convergence behavior in multi-domain systems and includes full provenance tracking for reproducibility.

## Architecture

### 1. Type & Unit System

**TypedValue**: Prevents unit errors by attaching units to all numeric values
- Supports automatic conversion between compatible units (e.g., degrees ↔ radians)
- Example: `TypedValue(90.0, "degrees")`

**UnitGuard**: Enforces type/unit compatibility across the system
- Compatible unit categories: angle, length, energy, count, binary
- Validates unit correctness before calculations

### 2. Calculator Nodes

**PipeBendCalculator** (INV-097)
- Implements Dom's hand-drawn pipe bend formulas
- Input: radius (length), angle (degrees/radians)
- Output: setback, arc_length, angle_out
- Formula: `arc_length = radius × angle_radians`

**DnaCodonCalculator**
- Maps arc length to DNA sequences and amino acid properties
- Translates codons using standard genetic code
- Calculates total bend angle from amino acid composition
- Output: sequence length, amino acid count, total bend angle

**RubikSolverCalculator**
- Treats system state as Rubik's Cube complexity
- Maps bend angle to move count (max 20 = God's Number)
- Calculates health score (100% = solved, 0% = maximally scrambled)
- Output: move_count, angle_sum, health_score, complexity

### 3. Execution Graph

Manages calculator connections and execution order:
- Defines edges between calculator outputs and inputs
- Handles topological sorting (cycle-safe via iteration)
- Maintains state for each calculator node

### 4. Fixed-Point Convergence Engine

**Algorithm 5**: Iterative fixed-point finder with damping

Key features:
- Runs calculators in sequence each iteration
- Applies feedback with configurable damping (default: 0.3)
- Detects convergence using epsilon threshold (default: 0.001)
- Maximum iterations: 100 (configurable)

Convergence criteria:
```python
delta = abs(health_score[i] - health_score[i-1])
if delta < epsilon:
    CONVERGED
```

### 5. Provenance & Lineage Tracker

**Algorithm 8**: Hash-chained provenance for reproducibility

Creates:
- `spec.yaml`: Input specification
- `final.yaml`: Final convergence state
- `lineage.json`: Hash chain of all iterations

Hash chain format:
```
GENESIS → hash(GENESIS:state₀) → hash(hash₀:state₁) → ...
```

### 6. Grounding Checks (Demystifier Integration)

**INV-091**: Validates all outputs are grounded

Three criteria:
1. **Measurable**: Has numeric value
2. **Bounded**: Within defined limits
3. **Falsifiable**: Has defined unit

Bounds:
- angle: 0-360 degrees
- radius: 0.1-1000 inches
- move_count: 0-20 moves (God's Number)
- health_score: 0-100 percent

## Usage

### Basic Usage

```python
from execution_kernel import ExecutionKernel, TypedValue

# Create kernel
kernel = ExecutionKernel()

# Run with default initial state
metrics = kernel.run()

# Run with custom initial state
custom_state = {
    "radius": TypedValue(10.0, "inches"),
    "angle": TypedValue(180.0, "degrees"),
}
metrics = kernel.run(custom_state)
```

### Command Line

```bash
# Run default simulation
python3 execution_kernel.py

# Output includes:
# - Convergence status
# - Final state values
# - Grounding check results
# - Provenance directory path
```

### Running Tests

```bash
# Run all unit tests
python3 test_execution_kernel.py

# Test output shows 21 tests covering all components
```

## Example Output

### Converged Run
```
============================================================
STRATEGICKHAOS EXECUTION KERNEL v1.0
============================================================
Initial state: {'radius': 5.0000 inches, 'angle': 90.0000 degrees}
Loop: pipe_bend → dna_codon → rubik_solver → pipe_bend
------------------------------------------------------------
✅ CONVERGED in 17 iterations
   ε = 0.000000

Final state:
   radius: 39.6256
   angle: 90.0000
   health_score: 16.6667
   ...

Grounding check: PASSED ✓
Provenance saved to: runs/2026-01-19T18-49-59
```

### Forensic Detection
```
FORENSIC SIMULATION: High network traffic detected
------------------------------------------------------------
❌ DID NOT CONVERGE after 100 iterations
health_score: 4.1667

🚨 ALERT: System health below 50% - Potential infection detected!
```

## Provenance Files

### final.yaml
```yaml
converged: true
iterations: 17
epsilon: 0.000000
final_state:
  radius: 39.6256
  health_score: 16.6667
  ...
```

### lineage.json
```json
[
  {
    "iteration": 0,
    "hash": "80b6161ece22007f",
    "prev_hash": "GENESIS"
  },
  {
    "iteration": 1,
    "hash": "70e186312db2df81",
    "prev_hash": "80b6161ece22007f"
  },
  ...
]
```

## Dependencies

- Python 3.8+
- PyYAML (for spec and output files)
- Standard library: math, hashlib, json, datetime, pathlib, dataclasses, typing

## Security

✅ CodeQL Analysis: **0 alerts**
- No security vulnerabilities detected
- Proper error handling for file operations
- Type-safe unit conversions
- Bounded value checks

## Files

- `execution_kernel.py` - Main implementation (650+ lines)
- `test_execution_kernel.py` - Unit tests (21 tests)
- `EXECUTION_KERNEL_README.md` - This documentation
- `runs/` - Provenance output directory (gitignored)

## References

- INV-097: Pipe Bend Calculator
- INV-091: Demystifier Integration
- INV-098: Execution Kernel

## Authors

**Strategickhaos DAO LLC**
- Architecture: Dominic Sears
- Implementation: 2026-01-19

## License

See main repository LICENSE file.
