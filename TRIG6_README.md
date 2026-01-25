# TRIG6 Calibration & BCI Gate System

This package implements a PMI-gun style calibration system for TRIG6 scores and a BCI stability gate for runtime safety control.

## Components

### 1. `trig6_calibration.py` - Score Calibration System

Converts raw TRIG6 scores to calibrated P(correct) probabilities using isotonic regression.

**ClaimMetrics Parameters:**
- `R` (Coherence): [0,1] - Signal coherence or claim validity
- `D` (Drift): [0,1] - Drift from baseline or expected behavior
- `N` (Noise): [0,1] - Signal noise or data quality issues
- `eq` (Equilibrium): [0,1] - Safety alignment or system stability

**Score Formula:**
```
f = R × (1 - D) × (1 - N) × eq
```

**Usage Example:**
```python
from trig6_calibration import ClaimMetrics, Trig6Calibrator

# Train calibrator
calibrator = Trig6Calibrator()
data = [
    (ClaimMetrics(0.95, 0.05, 0.05, 0.95), 1.0),  # Proven theorem
    (ClaimMetrics(0.30, 0.70, 0.60, 0.20), 0.0),  # Failed proof
    # ... more training data
]
calibrator.fit(data)

# Get calibrated probability
claim = ClaimMetrics(0.8, 0.2, 0.3, 0.7)
raw_score = claim.score()                        # Raw TRIG6 score
probability = calibrator.predict_proba(claim)     # Calibrated P(correct)
```

### 2. `bci_trig6_gate.py` - BCI Stability Gate

Provides runtime safety gates for BCI (Brain-Computer Interface) or similar real-time systems.

**BCITrig6 Parameters:**
- `R` (Spike Coherence): [0,1] - Neural spike coherence
- `D` (Drift): [0,1] - Drift from baseline neural activity
- `N` (Signal Instability): [0,1] - Signal noise or instability
- `eq` (Safety Alignment): [0,1] - Safety and alignment metrics

**Gate Modes:**
- `NORMAL`: Score ≥ warn threshold (default 0.6) - Full augmentation
- `DEGRADED_MODE`: abort ≤ score < warn - Reduced features
- `ABORT_SESSION`: Score < abort threshold (default 0.4) - Shutdown

**Usage Example:**
```python
from bci_trig6_gate import BCITrig6, bci_gate

# BCI signal metrics
signal = BCITrig6(R=0.85, D=0.15, N=0.25, eq=0.9)

# Get gate verdict
verdict = bci_gate(signal)  # Returns: "NORMAL", "DEGRADED_MODE", or "ABORT_SESSION"

# Custom thresholds
verdict = bci_gate(signal, warn=0.7, abort=0.5)
```

## Testing

Run the comprehensive test suite:

```bash
python3 benchmarks/test_trig6_system.py
```

The test suite includes 13 tests covering:
- Score calculation and formula verification
- Calibrator training and prediction
- Monotonicity guarantees
- BCI gate mode transitions
- Custom threshold handling
- Boundary condition testing
- Integration and end-to-end workflows

## Dependencies

- `numpy>=1.24.0` - Numerical computations
- `scikit-learn>=1.3.0` - Isotonic regression model
- `pytest>=9.0.0` - Testing framework (dev dependency)

Install with:
```bash
pip install numpy scikit-learn pytest
```

## Integration with SAGCO OS

These modules are designed for integration with SAGCO OS as runtime codons. Example FlameLang IR pseudocode:

```
CODON CALIB_GATE
PARAMS metrics warn=0.6 abort=0.4
COMPUTE f = R*(1-D)*(1-N)*eq
IF f < abort ABORT "LOW_FITNESS"
IF f < warn WARN "DEGRADED"
ELSE ACCEPT
```

## Dataset Expansion

The starter dataset includes 10 cases (5 true, 5 false). To expand to 30 cases:

**Add cases for True outcomes (score → 1.0):**
- Proven mathematical theorems
- Working unit tests that pass
- Valid parsers/lexers
- Successful algorithm validations

**Add cases for False outcomes (score → 0.0):**
- Failed proofs or contradictions
- Buggy code that crashes
- Infinite loops
- False conjectures

## Theory

This system implements a calibration pipeline analogous to PMI (Precision Measuring Instruments):
1. Raw TRIG6 scores (f) are computed from metrics
2. Isotonic regression maps raw scores to calibrated probabilities
3. The mapping preserves monotonicity: higher scores → higher probabilities
4. BCI gates use scores for real-time safety decisions

The isotonic regression ensures that improvements in any metric (R↑, D↓, N↓, eq↑) never decrease the calibrated probability, maintaining logical consistency.

## License

Part of the Sovereignty Architecture - Strategickhaos DAO LLC
