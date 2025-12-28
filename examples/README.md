# 🔥 FlameLang Physics Examples

This directory contains example scripts demonstrating the FlameLang Physics module with Hebrew root operators for quantum gravity and CMB modeling.

## Available Examples

### cmb_analysis.py
Comprehensive demonstration of FlameLang Physics capabilities:
- Display all 20 Hebrew root operators
- Natural language intent compilation
- Planck 2018 TT power spectrum analysis
- Power law and LQG bounce model fitting
- Complete FlameLang physics workflow
- Model comparison

**Usage:**
```bash
python3 examples/cmb_analysis.py
```

## Quick Start

```python
from flamelang_physics import flamelang_physics_compile, CMBDataAnalyzer

# Compile a physics intent
model = flamelang_physics_compile("Bounce suppress low-l radiation")
print(model.operators)       # ['BOUNCE', 'SUPPRESS', 'RADIATE']
print(model.hebrew_roots)    # ['דחה', 'כבש', 'אור']

# Analyze CMB data
analyzer = CMBDataAnalyzer()
l_data, D_l_data = analyzer.generate_planck_low_l_sample()
A, alpha = analyzer.fit_power_law(l_data, D_l_data)
print(f"Power law: A={A:.2f}, α={alpha:.2f}")
```

## Hebrew Root Operators

### Core Operators
- **CREATE** (ברא) - Particle creation/annihilation
- **SEPARATE** (בדל) - Measurement/collapse/decoherence
- **CONNECT** (חבר) - Entanglement/correlations
- **TRANSFORM** (הפך) - State evolution/wave transforms
- **CONSTRAIN** (גבל) - Conservation laws/boundaries
- **OBSERVE** (ראה) - Observation/measurement problem
- **RADIATE** (אור) - Photon emission/blackbody radiation
- **EXPAND** (רחב) - Cosmic expansion/inflation
- **SUPPRESS** (כבש) - Power suppression/damping
- **BOUNCE** (דחה) - Repulsion/quantum bounce
- **HARMONIZE** (שוה) - Balance/unification of scales
- **FLUCTUATE** (נוע) - Vacuum fluctuations/quantum noise
- **UNIFY** (אחד) - Oneness/quantum-gravity unification

### CMB/Quantum Gravity Extensions
- **ANOMALIZE** (פלא) - Wonder/anomaly generation
- **LENSE** (עדש) - Lens/distort (gravitational lensing)
- **POLARIZE** (קוטב) - Polarize (B-modes, E-modes)
- **SCALE** (מדד) - Measure/scale invariance
- **PERTURB** (הפר) - Disturb/perturbations
- **ASYMMETRIZE** (שני) - Two/duality/asymmetry
- **VIOLATE** (חלל) - Profane/violation (parity/CP)

## Physics Models

### Power Law Model
Simple baseline for CMB analysis:
```
D_l ≈ A * l^α
```

### LQG Bounce Model
Loop Quantum Gravity model with pre-bounce effects:
```
D_l ≈ A * l^α * (1 + sin(bounce_param*l) * exp(-l/10))
```

## Dependencies

```bash
pip install numpy scipy
```

Optional for visualization:
```bash
pip install matplotlib seaborn
```

## Further Reading

- `../flamelang_physics.py` - Main module implementation
- `../test_flamelang_physics.py` - Comprehensive test suite
- `../FLAMELANG_SPECIFICATION.md` - Complete specification

🔥 Reignite.
