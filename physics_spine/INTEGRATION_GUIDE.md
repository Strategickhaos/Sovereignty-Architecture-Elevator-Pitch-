# Physics Spine Integration Guide

## Overview

This guide provides instructions for integrating the Physics Spine multi-regime BB spectrum model with standard CMB analysis tools (CLASS, CAMB) and running production-level analyses.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Integration with CLASS](#integration-with-class)
3. [Integration with CAMB](#integration-with-camb)
4. [Production Workflow](#production-workflow)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

```bash
# 1. Install Physics Spine
cd /path/to/repository
pip install -r physics_spine/requirements.txt

# 2. (Optional) Install CLASS for production use
pip install classy

# 3. (Optional) Install CAMB for production use
pip install camb
```

### Basic Usage

```python
from physics_spine import UnifiedModel, ModelParameters

# Create model
model = UnifiedModel(l_max=1000, grid_points=10)

# Define parameters
params = ModelParameters(
    beta=1.45,      # LQC bounce scale
    mu_G2=3.2e-7,   # String tension
    r=0.028,        # Tensor-to-scalar ratio
    f_mu=0.052,     # String fraction
    tau=0.065,      # Optical depth
    A_lens=1.0      # Lensing normalization
)

# Compute spectrum
spectrum = model.compute_spectrum(params)
```

## Integration with CLASS

### Step 1: Install CLASS

```bash
# Clone CLASS
git clone https://github.com/lesgourg/class_public.git
cd class_public

# Compile with Python wrapper
make
cd python
python setup.py install
```

### Step 2: Modify Initial Power Spectrum

Create a custom CLASS module to incorporate LQC bounce effects:

```python
from classy import Class
import numpy as np
from physics_spine import ModelParameters

def setup_class_with_bounce(params: ModelParameters):
    """
    Configure CLASS with bounce-modified initial conditions.
    """
    cosmo = Class()
    
    # Base cosmological parameters
    cosmo.set({
        'output': 'tCl,pCl,lCl',
        'modes': 's,t',  # Scalar and tensor modes
        'lensing': 'yes',
        'r': params.r,
        'tau_reio': params.tau,
        
        # Standard ΛCDM parameters
        'h': 0.675,
        'omega_b': 0.02237,
        'omega_cdm': 0.120,
        'A_s': 2.1e-9,
        'n_s': 0.965,
        
        # Tensor spectral index
        'n_t': 0.0,  # Standard inflation prediction
        
        # Output precision
        'l_max_scalars': 2500,
        'l_max_tensors': 1000,
    })
    
    return cosmo

def apply_bounce_modification(Cl_tensor, params, l_array):
    """
    Apply LQC bounce modifications to CLASS tensor output.
    """
    # Get bounce suppression factor
    k = l_array / 14000.0  # Approximate k-l relation
    
    # Bounce suppression
    suppression = np.exp(-params.beta / k)
    
    # Apply to tensor Cl
    Cl_modified = Cl_tensor * suppression**2
    
    return Cl_modified

# Usage
params = ModelParameters(
    beta=1.45, mu_G2=3.2e-7, r=0.028, 
    f_mu=0.052, tau=0.065, A_lens=1.0
)

cosmo = setup_class_with_bounce(params)
cosmo.compute()

# Extract tensor Cl
l_max = 1000
l_array = np.arange(2, l_max + 1)
Cl_tensor = cosmo.lensed_cl(l_max)['tt'][:l_max-1]

# Apply bounce modifications
Cl_bounce = apply_bounce_modification(Cl_tensor, params, l_array)

cosmo.struct_cleanup()
```

### Step 3: Add String Defect Contributions

```python
from physics_spine.core import BBSpectrumCalculator

def add_string_contributions(Cl_base, params, l_array):
    """
    Add cosmic string vector mode contributions.
    """
    calc = BBSpectrumCalculator(l_max=len(l_array) + 1)
    
    # Calculate string contribution
    k = l_array / 14000.0
    Delta_V2 = calc.string_vector_power(k, params.mu_G2, l_array)
    V_l = calc.transfer_function(k, l_array, regime='vector')
    
    # String B-mode power
    Cl_string = params.f_mu * Delta_V2 * V_l**2
    
    # Apply mid-l damping
    damping = calc.calculate_regime_damping(l_array)
    Cl_string *= damping['mid_l']
    
    # Add to base
    Cl_total = Cl_base + Cl_string
    
    return Cl_total, Cl_string
```

### Full CLASS Pipeline

```python
def full_class_pipeline(params: ModelParameters):
    """
    Complete CLASS + Physics Spine pipeline.
    """
    # 1. Run CLASS
    cosmo = setup_class_with_bounce(params)
    cosmo.compute()
    
    # 2. Extract base spectrum
    l_max = 1000
    l_array = np.arange(2, l_max + 1)
    
    # Get lensed Cl (includes primordial + lensing)
    cl_dict = cosmo.lensed_cl(l_max)
    Cl_BB_base = cl_dict['bb'][:l_max-1]  # B-mode
    
    # 3. Apply bounce modifications
    Cl_BB_bounce = apply_bounce_modification(Cl_BB_base, params, l_array)
    
    # 4. Add string contributions
    Cl_BB_total, Cl_string = add_string_contributions(
        Cl_BB_bounce, params, l_array
    )
    
    cosmo.struct_cleanup()
    
    return {
        'l': l_array,
        'Cl_BB_total': Cl_BB_total,
        'Cl_BB_bounce': Cl_BB_bounce,
        'Cl_string': Cl_string,
    }
```

## Integration with CAMB

### Step 1: Install CAMB

```bash
pip install camb
```

### Step 2: Setup CAMB with Physics Spine

```python
import camb
from camb import model
import numpy as np
from physics_spine import ModelParameters

def setup_camb_with_bounce(params: ModelParameters):
    """
    Configure CAMB with unified model parameters.
    """
    pars = camb.CAMBparams()
    
    # Cosmological parameters
    pars.set_cosmology(
        H0=67.5,
        ombh2=0.02237,
        omch2=0.120,
        tau=params.tau,
    )
    
    # Initial power spectrum
    pars.InitPower.set_params(
        As=2.1e-9,
        ns=0.965,
        r=params.r,
        nt=0.0,  # Tensor spectral index
    )
    
    # Enable tensors
    pars.WantTensors = True
    
    # Set accuracy
    pars.set_accuracy(AccuracyBoost=2.0, lAccuracyBoost=2.0)
    
    # Maximum l
    pars.set_for_lmax(2500, lens_potential_accuracy=2)
    
    return pars

def run_camb_unified(params: ModelParameters):
    """
    Run CAMB with Physics Spine modifications.
    """
    # Setup
    pars = setup_camb_with_bounce(params)
    
    # Compute
    results = camb.get_results(pars)
    
    # Get tensor power spectra
    powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')
    totCL = powers['total']
    unlensedCL = powers['unlensed_scalar']
    
    # Extract BB
    l_array = np.arange(totCL.shape[0])
    Cl_BB_base = totCL[:, 2]  # BB is index 2
    
    # Apply Physics Spine modifications
    from physics_spine.core import BBSpectrumCalculator
    
    calc = BBSpectrumCalculator(l_max=len(l_array) - 1)
    k = l_array[2:] / 14000.0
    
    # Bounce modification
    suppression = np.exp(-params.beta / k)
    Cl_BB_bounce = Cl_BB_base[2:] * suppression**2
    
    # String contribution
    Delta_V2 = calc.string_vector_power(k, params.mu_G2, l_array[2:])
    V_l = calc.transfer_function(k, l_array[2:], regime='vector')
    damping = calc.calculate_regime_damping(l_array[2:])
    
    Cl_string = params.f_mu * Delta_V2 * V_l**2 * damping['mid_l']
    
    # Total
    Cl_BB_total = Cl_BB_bounce + Cl_string
    
    return {
        'l': l_array[2:],
        'Cl_BB_total': Cl_BB_total,
        'Cl_BB_bounce': Cl_BB_bounce,
        'Cl_string': Cl_string,
    }
```

## Production Workflow

### 1. Data Preparation

```python
from physics_spine import PlanckData
import numpy as np

# Load real Planck 2018 data
def load_planck_2018_bb():
    """
    Load actual Planck 2018 BB spectrum.
    Replace with real data loading.
    """
    # This is a placeholder - replace with actual data file loading
    data_file = "path/to/planck_2018_BB_binned.fits"
    
    # Load using astropy or similar
    # For now, use mock data
    return PlanckData.load_mock_data(l_max=1000)

data = load_planck_2018_bb()
```

### 2. Parameter Estimation with MCMC

```python
from physics_spine import BayesianPipeline, UnifiedModel
import emcee
import corner

def log_probability(theta, model, data):
    """
    Log probability for MCMC sampling.
    """
    beta, log_mu, r, f_mu, tau, A_lens = theta
    
    # Unpack
    mu_G2 = 10**log_mu
    
    # Prior bounds
    if not (1.0 <= beta <= 2.0):
        return -np.inf
    if not (-8 <= log_mu <= -6):
        return -np.inf
    if not (0.0 <= r <= 0.05):
        return -np.inf
    if not (0.01 <= f_mu <= 0.1):
        return -np.inf
    if not (0.05 <= tau <= 0.08):
        return -np.inf
    if not (0.8 <= A_lens <= 1.2):
        return -np.inf
    
    # Create parameters
    try:
        params = ModelParameters(
            beta=beta,
            mu_G2=mu_G2,
            r=r,
            f_mu=f_mu,
            tau=tau,
            A_lens=A_lens,
        )
    except:
        return -np.inf
    
    # Compute spectrum
    try:
        spectrum = model.compute_spectrum(params, apply_selection=True)
        model_interp = np.interp(data.l, spectrum['l'], spectrum['C_BB_total'])
        
        # Likelihood
        chi2 = np.sum(((data.C_BB - model_interp) / data.sigma)**2)
        log_like = -0.5 * chi2
        
        return log_like
    except:
        return -np.inf

# Run MCMC
model = UnifiedModel(l_max=1000, grid_points=10)
data = load_planck_2018_bb()

# Initial position
ndim = 6
nwalkers = 32
p0 = [
    [1.5, -6.5, 0.03, 0.05, 0.065, 1.0] + 0.01*np.random.randn(ndim)
    for _ in range(nwalkers)
]

# Sample
sampler = emcee.EnsembleSampler(
    nwalkers, ndim, log_probability, 
    args=(model, data)
)

print("Running MCMC...")
sampler.run_mcmc(p0, 5000, progress=True)

# Extract samples
samples = sampler.get_chain(discard=1000, thin=15, flat=True)

# Plot corner
fig = corner.corner(
    samples,
    labels=['β', 'log₁₀(μG²)', 'r', 'f_μ', 'τ', 'A_lens'],
    truths=[1.45, -6.5, 0.028, 0.052, 0.065, 1.0],
)
fig.savefig('mcmc_corner.png')

print("MCMC complete!")
print(f"Mean parameters: {np.mean(samples, axis=0)}")
print(f"Std parameters: {np.std(samples, axis=0)}")
```

### 3. Model Comparison

```python
from physics_spine import compute_bayes_factor

# Compute evidence using nested sampling (requires dynesty or similar)
try:
    import dynesty
    
    def prior_transform(u):
        """Transform unit cube to prior space"""
        theta = np.zeros(6)
        theta[0] = 1.0 + u[0] * 1.0  # beta [1, 2]
        theta[1] = -8.0 + u[1] * 2.0  # log_mu [-8, -6]
        theta[2] = u[2] * 0.05  # r [0, 0.05]
        theta[3] = 0.01 + u[3] * 0.09  # f_mu [0.01, 0.1]
        theta[4] = 0.05 + u[4] * 0.03  # tau [0.05, 0.08]
        theta[5] = 0.8 + u[5] * 0.4  # A_lens [0.8, 1.2]
        return theta
    
    def log_likelihood(theta):
        return log_probability(theta, model, data)
    
    # Run nested sampling
    sampler = dynesty.NestedSampler(
        log_likelihood, prior_transform, ndim=6
    )
    sampler.run_nested()
    
    results = sampler.results
    log_Z_unified = results.logz[-1]
    
    print(f"Log evidence (unified): {log_Z_unified:.2f}")
    
except ImportError:
    print("Install dynesty for nested sampling: pip install dynesty")
```

## Advanced Usage

### Custom Regime Transitions

```python
from physics_spine.core import BBSpectrumCalculator

# Modify damping functions
calc = BBSpectrumCalculator(l_max=1000)

def custom_damping(l, transition_scale=50):
    """Custom exponential damping"""
    return {
        'low_l': np.exp(-(l / transition_scale)**2),
        'transition': np.exp(-((l - transition_scale) / transition_scale)**2),
        'mid_l': 1 - np.exp(-(l / transition_scale)**2),
    }

# Apply in spectrum calculation
# (Requires modifying core.py or creating derived class)
```

### Systematic Error Analysis

```python
# Add systematic uncertainties
def add_systematics(spectrum, systematic_errors):
    """
    Add systematic errors to model prediction.
    
    Args:
        spectrum: Model spectrum dict
        systematic_errors: Dict with error sources
    """
    l = spectrum['l']
    C_BB = spectrum['C_BB_total']
    
    # Beam uncertainty
    if 'beam_error' in systematic_errors:
        beam_err = systematic_errors['beam_error']
        C_BB *= (1 + beam_err * np.random.randn(len(l)))
    
    # Foreground contamination
    if 'foreground_level' in systematic_errors:
        fg_level = systematic_errors['foreground_level']
        C_BB += fg_level * (l / 80)**(-0.5)  # Dust-like
    
    # Calibration uncertainty
    if 'calibration_error' in systematic_errors:
        cal_err = systematic_errors['calibration_error']
        C_BB *= (1 + cal_err)
    
    return C_BB
```

## Troubleshooting

### Common Issues

**1. Import Error: Cannot import physics_spine**

```bash
# Add to PYTHONPATH
export PYTHONPATH=/path/to/repository:$PYTHONPATH
```

**2. Numerical Instability**

```python
# Increase numerical precision
import numpy as np
np.seterr(all='raise')  # Catch numerical errors

# Or use higher precision
from mpmath import mp
mp.dps = 50  # 50 decimal places
```

**3. Slow MCMC Convergence**

```python
# Use better proposal distribution
# Tune step size
# Increase number of walkers
# Use parallel tempering
```

**4. CLASS/CAMB Integration Issues**

```bash
# Ensure correct versions
pip install --upgrade classy camb

# Check compatibility
python -c "import classy; print(classy.__version__)"
python -c "import camb; print(camb.__version__)"
```

## Performance Optimization

### Vectorization

```python
# Use numpy vectorization for batch computations
params_batch = [
    ModelParameters(beta=b, mu_G2=m, r=0.03, f_mu=0.05, tau=0.065, A_lens=1.0)
    for b in np.linspace(1.0, 2.0, 10)
    for m in np.logspace(-8, -6, 10)
]

# Compute in parallel
from multiprocessing import Pool

def compute_single(params):
    return model.compute_spectrum(params)

with Pool(4) as p:
    results = p.map(compute_single, params_batch)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_spectrum(beta, mu_G2, r, f_mu, tau, A_lens):
    params = ModelParameters(beta, mu_G2, r, f_mu, tau, A_lens)
    return model.compute_spectrum(params)
```

## References

- CLASS documentation: https://lesgourg.github.io/class_public/
- CAMB documentation: https://camb.readthedocs.io/
- emcee documentation: https://emcee.readthedocs.io/
- dynesty documentation: https://dynesty.readthedocs.io/

---

**Last Updated**: 2025-12-28  
**Version**: 1.0.0
