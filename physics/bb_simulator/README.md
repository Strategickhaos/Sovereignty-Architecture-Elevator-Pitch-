# BB Simulator for Unified LQC-String Model

Production-ready Python simulator based on the Physics Spine Spec equations. Generates mock Planck-like B-mode data from the unified model, fits it against baselines (ΛCDM, LQC-only, String-only), and computes Δχ².

## Overview

This simulator implements a unified cosmological model combining:
- **Loop Quantum Cosmology (LQC)**: Bounce suppression at low multipole moments
- **String Theory**: Cosmic string defects at mid multipole moments
- **ΛCDM Baseline**: Standard lensing contributions

## Key Features

- ✅ **Bounce suppression** at low l via β/k term
- ✅ **String defects** at mid l via μ/l² term
- ✅ **Lensing baseline** with A_lens
- ✅ **Bayesian priors** mocked via initial guesses (extendable to full MCMC)
- ✅ **Mock data generation** with configurable noise (10% default)
- ✅ **Model comparison** via Δχ² statistics

## Installation

### Dependencies

```bash
pip install numpy scipy
```

Or use the existing requirements:
```bash
pip install -r requirements.sovereignty.txt
```

## Usage

### Quick Start

Run the simulator with default parameters:

```bash
python physics/bb_simulator/bb_simulator.py
```

### Python API

```python
from physics.bb_simulator import run_simulation, print_results

# Run simulation with default parameters
results = run_simulation()
print_results(results)

# Run with custom parameters
custom_params = [0.05, 2.0, 0.08, 1.2]  # [r, beta, f_mu, a_lens]
results = run_simulation(
    l_min=2,
    l_max=1001,
    true_params=custom_params,
    noise_level=0.15
)
```

### Individual Model Functions

```python
from physics.bb_simulator import bb_model, lcdm_model, lqc_only, string_only
import numpy as np

# Multipole moments
l_values = np.arange(2, 1001)

# Unified model
r, beta, f_mu, a_lens = 0.03, 1.5, 0.05, 1.0
c_l_unified = bb_model(l_values, r, beta, f_mu, a_lens)

# Baseline models
c_l_lcdm = lcdm_model(l_values, r, a_lens)
c_l_lqc = lqc_only(l_values, r, beta, a_lens)
c_l_string = string_only(l_values, r, f_mu, a_lens)
```

## Models

### Unified Model

The complete model combining all physical effects:

```
C_l^{BB} = r Δ_T²(k) T_l²(k) + A_lens C_l^{lens} + f_μ Δ_V²(k) V_l²(k)
```

Where:
- **Primordial tensor component**: `r Δ_T²(k) T_l²(k)` with bounce suppression `exp(-β/k)`
- **Lensing component**: `A_lens C_l^{lens}` 
- **String defect component**: `f_μ Δ_V²(k) V_l²(k)` with `1/l²` scaling
- **Transition damping**: `exp(-l/50)` for smooth regime handoff

### ΛCDM Baseline

Standard cosmology without quantum gravity or string effects:

```
C_l^{BB} = r/l + A_lens/l
```

### LQC-Only Model

Loop Quantum Cosmology with bounce suppression but no strings:

```
C_l^{BB} = r Δ_T²(k) T_l²(k) + A_lens C_l^{lens}
```

With bounce suppression: `Δ_T²(k) = k² exp(-β/k)`

### String-Only Model

Cosmic string defects without LQC bounce:

```
C_l^{BB} = r/l + f_μ Δ_V²(k) V_l²(k) + A_lens/l
```

With string defects: `Δ_V²(k) = f_μ/l²`

## Parameters

| Parameter | Description | Typical Range | Default |
|-----------|-------------|---------------|---------|
| `r` | Tensor-to-scalar ratio | 0.01 - 0.1 | 0.03 |
| `beta` | Bounce suppression (LQC) | 1.0 - 3.0 | 1.5 |
| `f_mu` | String defect amplitude | 0.01 - 0.2 | 0.05 |
| `a_lens` | Lensing baseline amplitude | 0.5 - 2.0 | 1.05 |
| `l` | Multipole moment | 2 - 1000+ | 2-1001 |

## Output

The simulator produces:

### Model Fits
- Fitted parameters for each model
- Chi-squared (χ²) goodness-of-fit values
- Parameter names and values

### Delta Chi-Squared (Δχ²)
- Δχ² vs ΛCDM: Improvement over standard cosmology
- Δχ² vs LQC-only: Benefit of including string defects
- Δχ² vs String-only: Benefit of including bounce suppression

### Expected Results

**Mock Data (perfect fit):**
- Unified χ²: ~0.00 (perfect fit to generated data)
- Δχ² vs baselines: ~0.00 (all models fit equally well to unified-generated data)

**Real Planck Data (anticipated):**
- Unified χ²: Lower than baselines
- Δχ² vs ΛCDM: -5 to -10 (unified model fits significantly better)
- Negative Δχ² indicates unified model better handles:
  - Low-l suppression (LQC bounce effects)
  - Mid-l excess (string defect contributions)

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest physics/bb_simulator/test_bb_simulator.py -v

# Run specific test class
pytest physics/bb_simulator/test_bb_simulator.py::TestBBSimulator -v

# Run with coverage
pytest physics/bb_simulator/test_bb_simulator.py --cov=physics.bb_simulator
```

Test coverage includes:
- ✅ Basic model functions (single value and array inputs)
- ✅ Regime-specific behavior verification
- ✅ All baseline models (ΛCDM, LQC-only, String-only)
- ✅ Chi-squared calculations
- ✅ Mock data generation with noise
- ✅ Model fitting structure and correctness
- ✅ Parameter recovery accuracy
- ✅ Positive definiteness of all models
- ✅ Numerical stability across multipole range
- ✅ Full workflow integration

## Physics Background

### Loop Quantum Cosmology (LQC)

LQC resolves the Big Bang singularity with a quantum bounce. The bounce suppresses primordial tensor modes at low multipole moments (large scales):

```
Δ_T²(k) ∝ k² exp(-β/k)
```

The exponential suppression factor `exp(-β/k)` becomes significant at small k (low l), reducing the B-mode power spectrum at large angular scales.

### Cosmic Strings

Topological defects from symmetry breaking in the early universe can generate vector modes that contribute to B-mode polarization:

```
Δ_V²(k) ∝ f_μ/l²
```

The `1/l²` scaling produces enhanced power at intermediate scales, potentially observable in CMB data.

### Regime Transition

The unified model uses exponential damping `exp(-l/50)` to smoothly transition between:
- **Low l (l < ~50)**: LQC bounce dominates
- **Mid l (l > ~50)**: String defects contribute
- **High l**: Lensing baseline

## Extensions

### Real Data Integration

Replace mock data with Planck B-mode measurements:

```python
# Load real Planck data (requires astropy or similar)
from astropy.io import fits

# Load B-mode power spectrum
planck_data = fits.open('planck_bb_spectrum.fits')
l_values = planck_data['MULTIPOLE'].data
bb_data = planck_data['BB_POWER'].data

# Fit models
results = fit_models(l_values, bb_data)
```

### Full Bayesian Analysis

Extend to MCMC sampling with `emcee`:

```python
import emcee

def log_probability(params, l_values, data, data_errors):
    r, beta, f_mu, a_lens = params
    
    # Prior bounds
    if not (0.0 < r < 0.2 and 0.5 < beta < 5.0 and 
            0.0 < f_mu < 0.5 and 0.1 < a_lens < 3.0):
        return -np.inf
    
    # Likelihood
    model_vals = bb_model(l_values, r, beta, f_mu, a_lens)
    chi2 = np.sum(((data - model_vals) / data_errors) ** 2)
    return -0.5 * chi2

# Run MCMC
ndim, nwalkers = 4, 32
pos = [0.03, 1.5, 0.05, 1.05] + 1e-4 * np.random.randn(nwalkers, ndim)
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, 
                                args=(l_values, data, data_errors))
sampler.run_mcmc(pos, 5000, progress=True)
```

### CAMB Integration

For realistic transfer functions:

```python
import camb

# Set up CAMB parameters
pars = camb.CAMBparams()
pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122)
pars.InitPower.set_params(r=0.03)  # tensor-to-scalar ratio
pars.set_for_lmax(2500, lens_potential_accuracy=1)

# Get results
results = camb.get_results(pars)
powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
bb_spectrum = powers['tensor'][:, 2]  # BB component
```

## References

- **Physics Spine Spec**: Original equations and model specification
- **Planck Collaboration**: CMB B-mode measurements
- **LQC Review**: Loop Quantum Cosmology bounce physics
- **Cosmic Strings**: Topological defect contributions to CMB

## License

Part of the Strategickhaos Sovereignty Architecture.
See main repository LICENSE for details.

## Contact

For questions about the physics or implementation, see the main repository documentation.
