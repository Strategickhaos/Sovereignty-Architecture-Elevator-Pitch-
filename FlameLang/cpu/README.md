# FlameLang CPU: Trig PDE Sweep

## Overview

This directory contains the `trig_pde_sweep.py` script that simulates a Partial Differential Equation (PDE) on a 64-bin trigonometric/MIDI grid. The script implements a hymn-PDE symphony that maps resonance patterns to MIDI notes.

## Script: trig_pde_sweep.py

### Description

The script simulates a PDE system with the following characteristics:

- **Spatial bins**: 64 bins (i = 0..63) with θ_i = i × 360/64
- **PDE equation**: ∂_t A = [ξ² (1 + S cos(6 Re t))] A_xx - Pe A_x + (Da_g - Da_0) A - Da_sat A²
- **Output**: Maps final amplitude A(i,T) to MIDI notes (60+i) with velocity proportional to A(i,T)

### Features

- **Explicit Euler integration** with positivity clamp for stability
- **Periodic boundary conditions** for cycle vibes
- **CFL stability check** for diffusion/advection timestep
- **Trig modulation** on diffusion coefficient D using ξ² term
- **Initial condition boosting** at bins i=8 and i=32 (resonance/dual points)
- **MIDI output** with surviving bins as a chord (4-beat hold)
- **Text output** of final amplitude profile

### Installation

Install required dependencies:

```bash
pip install -r requirements.sovereignty.txt
```

Or install specific packages:

```bash
pip install numpy mido
```

### Usage

Run the script from the FlameLang/cpu directory:

```bash
cd FlameLang/cpu
python3 trig_pde_sweep.py
```

### Output Files

The script generates two output files:

1. **trig_pde_sweep.mid** - MIDI file with resonance patterns as musical notes
2. **trig_pde_sweep_final_A.txt** - Text file with final amplitude values for each bin

**Note**: These output files are excluded from git commits via `.gitignore`.

### Parameters

The script uses the following default parameters:

- `N = 64` - Number of spatial bins
- `D = 1.0` - Base diffusion coefficient
- `Pe = 2.0` - Péclet number (advection strength)
- `Da_g = 1.0` - Growth Damköhler number
- `Da_0 = 0.5` - Base Damköhler number
- `Da_sat = 1.0` - Saturation Damköhler number
- `S = 0.1` - Modulation strength
- `Re = 1.0` - Resonance frequency parameter
- `T_final = 10.0` - Final simulation time
- `BASE_NOTE = 60` - MIDI base note (Middle C)

### Implementation Details

- **Stability**: Uses CFL condition: dt = min(0.5 × dx²/D, dx/Pe) / 2
- **Discretization**: Central difference for diffusion, upwind for advection
- **Boundary**: Periodic boundaries using numpy.roll()
- **Time integration**: Explicit forward Euler with positivity preservation
- **MIDI mapping**: Notes 60-108 (C4 to C8), velocity scaled by amplitude

### Next Steps

Potential enhancements:

- Integration with SAGCO validator
- Full BVP (Boundary Value Problem) implementation
- Parameter sweep capabilities
- Real-time visualization
- JSON export for SAGCO compatibility

---

*Part of the Strategickhaos Sovereignty Architecture - FlameLang System*
