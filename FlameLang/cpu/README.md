# FlameLang CPU Phase Sweep Module

This module implements phase sweep calculations for FlameLang's trigonometric weight system.

## Files

- **phase_sweep_trig6_weights.py** - Main script for performing phase boundary sweeps across 64 genetic codons
- **flame_trig6_map.json** - Sample input file mapping codons to atomic elements with norm² values
- **phase_sweep_trig6_weights.json** - Sample output showing SAGCO-formatted phase boundaries

## Usage

```bash
# Make sure scipy is installed
pip install scipy numpy

# Run the phase sweep
python phase_sweep_trig6_weights.py
```

## Configuration

The script uses the following default parameters (editable in the script):

- `Pe_vals`: Peclet numbers (logarithmic scale from 0.1 to 100)
- `Da0`: Base Damköhler number (0.1)
- `Bi`: Biot number (1.0)
- `Da_min`, `Da_max`: Search range for critical Damköhler (0.01 to 50.0)
- `tol`: Bisection tolerance (1e-3)
- `NORM_CAP`: Maximum norm² value (200.0)

## Input Format

The input JSON file (`flame_trig6_map.json`) should contain 64 codon entries with:
- `Atomic #`: Element atomic number
- `Symbol`: Element symbol (optional)
- `Norm^2`: L2 norm squared value (used for Da_gamma calculation)

Example:
```json
{
  "AAA": {
    "Atomic #": 1,
    "Symbol": "H",
    "Norm^2": 12.5,
    "L2_weight": 0.85
  }
}
```

## Output Format (SAGCO-Ready)

The output follows the SAGCO-TRIG6-PHASE-1.0 schema:

```json
{
  "version": "SAGCO-TRIG6-PHASE-1.0",
  "generated_at": "2026-02-03T11:48:00CST",
  "params": {
    "Da0": 0.1,
    "Bi": 1.0,
    "Pe_vals": [0.1, ...],
    "tol": 0.001
  },
  "entries": [
    {
      "codon": "AAA",
      "atomic_num": 1,
      "Da_gamma": 12.5,
      "boundary": [
        {"Pe": 0.1, "Da_g_crit": 0.099246...},
        ...
      ]
    }
  ]
}
```

## Validator

The script includes a `validate_sagco_phase()` function that checks:
- Version compatibility
- 64 codon entries present
- Correct entry structure

## Implementation Notes

- **Placeholder Simulation**: Currently uses `placeholder_sim()` which is a toy model. Replace with actual BVP/LSODA solver when ready.
- **Da_gamma Calculation**: Derived from input norm² values, capped at `NORM_CAP` to prevent overflow
- **Bisection Search**: Uses scipy's bisect to find critical Da_g values for survival boundaries
- **Parallelization**: Can be parallelized per codon for production use

## Next Steps

1. Replace `placeholder_sim()` with full PDE/BVP solver
2. Add aggregate statistics (B2 option from original specification)
3. Integrate with SAGCO OS core kernel
4. Scale Pe_vals to 10+ points for production
