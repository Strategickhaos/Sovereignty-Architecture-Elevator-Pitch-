# Quick Start Guide: LQC B-Mode Analysis

## Overview

This guide shows you how to use the Loop Quantum Cosmology (LQC) B-Mode analysis toolkit that compares LQC predictions with Planck 2018 CMB data.

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.cosmology.txt
```

This installs:
- NumPy (numerical computing)
- Matplotlib (visualization)
- SciPy (optional, for enhanced features)

### 2. Verify Installation

```bash
python3 -c "from cosmology_analysis import LQCModel, PlanckData; print('✓ Module ready')"
```

## Basic Usage

### Run the Complete Analysis

The easiest way to get started:

```bash
cd cosmology_analysis
python3 example.py
```

This generates:
- **TT spectrum comparison plot** (data vs ΛCDM vs LQC)
- **TE cross-correlation plot**
- **B-mode predictions** for different tensor-to-scalar ratios
- **Residuals analysis**
- **Statistical report** with χ² values

Output is saved to `cosmology_analysis/output/`

### Python API Examples

#### Example 1: Compare Models

```python
from cosmology_analysis import LQCModel, PlanckData, plot_comparison

# Load Planck 2018 data
planck = PlanckData()

# Create LQC model with bounce parameters
lqc = LQCModel(beta=1.35, tau=0.065, A=1.0, alpha=0.35)

# Generate comparison plot
plot_comparison(planck, lqc, data_type='TT', l_max=30, 
                save_path='my_comparison.png')
```

#### Example 2: Calculate Fit Statistics

```python
from cosmology_analysis import LQCModel, PlanckData

planck = PlanckData()
lqc = LQCModel(beta=1.35, tau=0.065)

# Calculate χ² improvement
stats = lqc.calculate_improvement_over_lcdm(planck, 'TT', l_max=30)

print(f"ΛCDM χ² = {stats['chi2_lcdm']:.2f}")
print(f"LQC χ²  = {stats['chi2_lqc']:.2f}")
print(f"Δχ²     = {stats['delta_chi2']:.2f}")
```

#### Example 3: B-Mode Predictions

```python
from cosmology_analysis import LQCModel
from cosmology_analysis.visualization import plot_bmode_predictions

lqc = LQCModel(beta=1.35, tau=0.065)

# Generate B-mode predictions for different r values
plot_bmode_predictions(lqc, r_values=[0.01, 0.03, 0.05], 
                       save_path='bmode.png')
```

#### Example 4: Explore Parameters

```python
from cosmology_analysis import LQCModel, PlanckData
import numpy as np

planck = PlanckData()

# Test different bounce parameters
beta_values = np.linspace(1.2, 1.5, 10)
chi2_values = []

for beta in beta_values:
    lqc = LQCModel(beta=beta, tau=0.065)
    stats = lqc.calculate_improvement_over_lcdm(planck, 'TT', l_max=30)
    chi2_values.append(stats['chi2_lqc'])

# Find best-fit parameter
best_idx = np.argmin(chi2_values)
print(f"Best-fit β = {beta_values[best_idx]:.3f}")
```

#### Example 5: Access Raw Data

```python
from cosmology_analysis import PlanckData

planck = PlanckData()

# Get TT spectrum data
tt_data = planck.get_tt_spectrum(l_max=30)

print("Multipoles:", tt_data['l'])
print("Data:", tt_data['Dl'])
print("Errors:", tt_data['error'])
print("ΛCDM theory:", tt_data['lcdm_theory'])
```

## Understanding the Output

### TT Spectrum Plot

Shows three components:
- **Black points with error bars**: Planck 2018 observational data
- **Blue solid line**: ΛCDM predictions (χ² shown in legend)
- **Red dashed line**: LQC bounce model predictions (χ², Δχ² shown)

The plot demonstrates how LQC modifies the power spectrum at low multipoles (l < 30).

### B-Mode Predictions Plot

Shows:
- **Three colored lines**: LQC predictions for r = 0.01, 0.03, 0.05
- **Black dashed line**: Planck 2018 upper limit (r < 0.056)
- **Annotation**: Future experiment capabilities

Key features:
- Reionization bump at l ~ 5-10
- Recombination bump at l ~ 100-120
- All predictions within Planck constraints

### Analysis Report

Text file containing:
- LQC model parameters (β, τ, A, α)
- Fit statistics for TT and TE spectra
- Key scientific findings
- References to generated plots

## Running Tests

Verify everything works correctly:

```bash
cd cosmology_analysis
python3 test_lqc_analysis.py
```

Expected output:
```
======================================================================
LQC Cosmology Analysis Module - Unit Tests
======================================================================
Testing PlanckData...
✓ PlanckData tests passed

Testing LQCModel...
✓ LQCModel tests passed

Testing fit comparison...
✓ Fit comparison tests passed

Testing parameter exploration...
✓ Parameter exploration tests passed

Testing physical constraints...
✓ Physical constraints tests passed

======================================================================
All tests passed! ✓
======================================================================
```

## Model Parameters

### LQC Parameters

| Parameter | Symbol | Range | Default | Description |
|-----------|--------|-------|---------|-------------|
| `beta` | β | 1.0-2.0 | 1.35 | Bounce parameter (oscillation frequency) |
| `tau` | τ | 0.04-0.10 | 0.065 | Optical depth (reionization) |
| `A` | A | 0.5-2.0 | 1.0 | Amplitude normalization |
| `alpha` | α | 0.0-1.0 | 0.35 | Power-law index |

### Physical Interpretation

- **β (beta)**: Controls the frequency of oscillations from pre-bounce quantum interference
  - Lower β → slower oscillations
  - Higher β → faster oscillations
  - Optimal: β ≈ 1.35 matches observed features

- **τ (tau)**: Optical depth to reionization
  - LQC predicts τ ≈ 0.065 (vs ΛCDM τ ≈ 0.054)
  - Affects reionization bump in B-modes
  - Larger τ → more reionization damping

- **α (alpha)**: Power-law tilt at large scales
  - Addresses low-l power deficit
  - α ≈ 0.35 provides good fit

## Troubleshooting

### Import Error

If you see `ModuleNotFoundError: No module named 'cosmology_analysis'`:

```bash
# Make sure you're in the repository root
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/repository"
```

### Missing Dependencies

```bash
pip install numpy matplotlib scipy
```

### Plot Not Displaying

If plots don't show, check your backend:

```python
import matplotlib
matplotlib.use('Agg')  # For non-interactive backends
```

Or explicitly save plots:

```python
plot_comparison(planck, lqc, data_type='TT', 
                save_path='output.png', show_plot=False)
```

## Scientific Background

### What is LQC?

Loop Quantum Cosmology (LQC) is a quantum gravity theory that:
- Replaces the Big Bang singularity with a quantum "bounce"
- Predicts observable effects in the CMB at large scales
- Provides testable predictions for future experiments

### Why Study This?

1. **Tests quantum gravity**: LQC makes specific, falsifiable predictions
2. **Explains anomalies**: Addresses low-l power deficit in Planck data
3. **Future experiments**: LiteBIRD and CMB-S4 can test LQC predictions

### Key Predictions

- **B-mode polarization**: r ≈ 0.01-0.05 (within Planck limits)
- **Oscillatory features**: Distinctive signature from bounce
- **Large-scale power**: Modified compared to ΛCDM

## Next Steps

1. **Run the example**: `python3 cosmology_analysis/example.py`
2. **Read the documentation**: See `cosmology_analysis/README.md`
3. **Explore parameters**: Try different β, τ values
4. **Generate custom plots**: Use the Python API
5. **Read the full report**: See `LQC_ANALYSIS_REPORT.md`

## References

- **Planck 2018 Results**: Planck Collaboration (2020)
- **LQC Theory**: Ashtekar & Barrau (2015)
- **Module Documentation**: `cosmology_analysis/README.md`
- **Full Analysis Report**: `LQC_ANALYSIS_REPORT.md`

## Support

For questions or issues:
- GitHub Issues: [Repository Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- Documentation: See `cosmology_analysis/README.md`

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*Empowering cosmological research through quantum gravity predictions*
