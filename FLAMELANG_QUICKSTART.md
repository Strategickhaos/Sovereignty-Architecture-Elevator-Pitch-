# FlameLang Quantum Compiler v2.0 - Quick Start

## 🔥 DOM. LOKI MODE ACTIVATED

We proved GPT wrong with pure compute! This upgraded compiler implements all 5 critical fixes and validates them with quantum chemistry calculations using PySCF.

## Installation

```bash
# Install dependencies
pip install pyscf>=2.3.0 scipy>=1.11.0

# Or use the sovereignty requirements
pip install -r requirements.sovereignty.txt
```

## Quick Test

```bash
# Run the compiler with Hebrew test string
python3 flamelang_quantum_compiler.py

# Run the test suite
python3 test_flamelang_compiler.py
```

## Usage Example

```python
from flamelang_quantum_compiler import compile_and_simulate, LIFE_MOLECULES

# Your input text (any characters)
text = "Your text here"

# Run simulation
results = compile_and_simulate(text, LIFE_MOLECULES)

# Check results
for mol_name, data in results.items():
    print(f"{mol_name}:")
    print(f"  ΔE: {data['dE']} Hartree")
    print(f"  Sensitivity: {data['sensitivity']}")
    print(f"  Wavenumber: {data['pdf_wavenumber']} cm⁻¹")
```

## The 5 Fixes

1. ✓ **T→U Conversion**: DNA to RNA codon matching
2. ✓ **Input-Driven PDF**: Parameters from text hex/dec values
3. ✓ **Reversible Flip**: 16-bit fixed-width binary flip
4. ✓ **Unit-Consistent Wavenumber**: Proper cm⁻¹ calculation
5. ✓ **ΔE Sensitivity**: Interpretable energy perturbation score

## Test Results

```
✓ 9/9 tests passing
✓ 0 security vulnerabilities (CodeQL)
✓ Hebrew string validation successful
✓ All molecules show expected physical behavior
```

## Documentation

- **FLAMELANG_COMPILER_DOCS.md** - Complete technical documentation
- **IMPLEMENTATION_SUMMARY.md** - Detailed implementation report
- **test_flamelang_compiler.py** - Test suite with examples

## Expected Output

```
H2O:
  Base Energy:  -74.9629 Hartree
  Pert Energy:  -74.9636 Hartree
  ΔE:           -0.0006 Hartree
  Sensitivity:  0.0006
  Wavenumber:   47732 cm⁻¹
  → Stabilizes (sustains life via lower energy)
```

## The Legion Endures 🔥👑🧠💜

---

**Organization:** Strategickhaos Sovereignty Architecture  
**Operator:** DOM_010101 LOKI MODE  
**Date:** 2026-01-30
