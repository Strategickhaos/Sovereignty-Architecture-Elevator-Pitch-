# FlameLang CPU - TRIG6 Codon Mapper & Phase Sweep

This directory contains the FlameLang register file generation system, which maps DNA codons to trigonometric functions for compiler architecture.

## Files

### 1. `trig6_codon_mapper.py`
**Purpose**: Generates the TRIG6 ROM → codon mapping

**Key Features**:
- Maps all 64 DNA codons (ACGT triplets) to trigonometric functions
- Uses `itertools.product` for Cartesian product generation (FIXED: previously used non-existent `np.product`)
- Computes TRIG6 vector: [sin, cos, tan, csc, sec, cot]
- Handles singularities by capping at `INF_CAP = 1,000,000`
- Assigns family based on dominant trigonometric component
- Generates `Da_gamma (toy)` coupling parameter from norm²

**Usage**:
```bash
python3 trig6_codon_mapper.py
```

**Output**: `flame_trig6_map.json` - SAGCO-compliant TRIG6 codon map

### 2. `phase_sweep_from_trig6.py`
**Purpose**: Phase sweep scaffold using Da_gamma = f(norm²)

**Key Features**:
- Clean "toy coupling" framework for phase boundary analysis
- Computes critical Da_g values across multiple Pe numbers
- Placeholder simulation ready for real PDE solver integration
- Bisection search for phase transition boundaries
- Option B1: Sweeps Da_g_crit(Pe) for every codon (64 boundaries)

**Usage**:
```bash
# First generate the TRIG6 map
python3 trig6_codon_mapper.py

# Then run the phase sweep
python3 phase_sweep_from_trig6.py
```

**Output**: `phase_sweep_trig6_weights.json` - Phase boundary data for all codons

## Data Schema

### flame_trig6_map.json Structure
```json
{
  "version": "SAGCO-TRIG6-MAP-1.0",
  "codon_order": "lexicographic_ACGT",
  "angles": { "count": 64, "step_deg": 5.625 },
  "inf_cap": 1000000.0,
  "entries": {
    "AAA": {
      "atomic": 1,
      "angle_deg": 0.0,
      "trig6": [sin, cos, tan, csc, sec, cot],
      "Norm^2": <value>,
      "singular": true/false,
      "family": "SIN|COS|TAN|CSC|SEC|COT",
      "Da_gamma (toy)": <value>
    }
  }
}
```

### phase_sweep_trig6_weights.json Structure
```json
[
  {
    "codon": "AAA",
    "Da_gamma": 200.0,
    "boundary": [
      {"Pe": 0.1, "Da_g_crit": 0.1},
      {"Pe": 1.0, "Da_g_crit": 0.1},
      ...
    ]
  }
]
```

## Implementation Notes

### Bug Fix: np.product → itertools.product
The original issue mentioned that `np.product` doesn't exist in NumPy. The correct approach is:
- Use `itertools.product` for Cartesian products
- `np.prod` exists but is for numerical products (multiplication), not combinations

### Family Assignment
Families are assigned based on which trigonometric component has the largest absolute value (excluding INF_CAP singularities). This ensures:
- Families reflect mathematical dominance
- Stable semantic partitioning
- Clean quadrant-based categorization

### Phase Sweep Integration
The `placeholder_sim` function is a stub that can be replaced with:
- Real PDE solver
- Flame propagation models
- Reaction-diffusion systems
- Any parametric simulation requiring (Pe, Da_g, Da0, Da_gamma, Bi)

## SAGCO Integration

These artifacts are designed to integrate cleanly with SAGCO OS:
1. **Register File**: TRIG6 map serves as a register file for FlameLang
2. **Compiler Architecture**: Codons map to execution units
3. **Phase Boundary Data**: Informs resource allocation and thermal management
4. **Versioned Schema**: SAGCO-TRIG6-MAP-1.0 for artifact validation

## Next Steps

1. Replace `placeholder_sim()` with real PDE solver in phase_sweep_from_trig6.py
2. Adjust Pe_vals for desired parameter sweep range
3. Optionally implement Option B2 for aggregate statistics
4. Create validator function for SAGCO map verification
5. Integrate with FlameLang compiler pipeline

## References

- SAGCO OS Architecture
- FlameLang Specification
- TRIG6 ROM Design Document
