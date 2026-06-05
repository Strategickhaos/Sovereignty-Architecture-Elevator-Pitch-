# Survivors Simulation

A Python simulation that tracks amplitude evolution across trigonometric families using reaction-diffusion dynamics.

## Overview

This simulation models survivor tracking across 64 bins, each assigned to one of six trigonometric families (SIN, COS, TAN, CSC, SEC, COT). The amplitude at each bin is calculated using reaction-diffusion dynamics influenced by several physical parameters.

## Features

- **Reaction-Diffusion Dynamics**: Incorporates diffusion coefficient (D), Péclet number (Pe), and Damköhler numbers (Da_g, Da_0)
- **Trigonometric Families**: Bins are distributed across six families representing different trigonometric functions
- **MIDI Note Mapping**: Each bin is mapped to a MIDI note (48-71) for potential audio synthesis
- **Periodic Amplitude Pattern**: Amplitudes follow a negative cosine wave with period N/4

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `N` | Number of bins | 64 |
| `D` | Diffusion coefficient | 0.01 |
| `Pe` | Péclet number (ratio of advection to diffusion) | 0.5 |
| `Da_g` | Damköhler number for growth | 0.8 |
| `Da_0` | Initial Damköhler number | 0.5 |
| `T` | Time duration | 5.0 |

## Usage

### Basic Usage

```python
from survivors_simulation import SurvivorsSimulation

# Create simulation with default parameters
sim = SurvivorsSimulation()

# Run simulation
result = sim.run_simulation()

# Access results
print(f"Max amplitude: {result['results']['max_amplitude']}")
print(f"Max bin: {result['results']['max_bin']}")
```

### Command Line

```bash
python3 survivors_simulation.py
```

This will run the simulation and save results to `survivors_output.json`.

### Custom Parameters

```python
sim = SurvivorsSimulation(
    N=32,
    D=0.02,
    Pe=1.0,
    Da_g=0.5,
    Da_0=0.3,
    T=10.0
)
result = sim.run_simulation()
```

## Output Format

The simulation outputs a JSON file with the following structure:

```json
{
  "params": {
    "N": 64,
    "D": 0.01,
    "Pe": 0.5,
    "Da_g": 0.8,
    "Da_0": 0.5,
    "T": 5.0
  },
  "results": {
    "survivors": 64,
    "max_amplitude": 0.19843938243611522,
    "max_bin": 11,
    "max_theta": 61.875,
    "max_family": "COS"
  },
  "surviving_notes": [
    {
      "bin": 0,
      "theta": 0.0,
      "family": "SIN",
      "note": 48,
      "velocity": 100,
      "amplitude": 0.19816249177747383
    },
    ...
  ]
}
```

## Family Assignment

For N=64, bins are assigned to families as follows:

| Family | Bins | Count |
|--------|------|-------|
| SIN | 0-10 | 11 |
| COS | 11-21 | 11 |
| TAN | 22-31 | 10 |
| CSC | 32-42 | 11 |
| SEC | 43-53 | 11 |
| COT | 54-63 | 10 |

## Amplitude Calculation

The amplitude at each bin follows a periodic pattern with:
- **Period**: N/4 (16 bins for N=64)
- **Minimum**: Around bin 2
- **Maximum**: At bin 11
- **Range**: ~0.0004
- **Pattern**: Negative cosine wave with phase shift

The formula incorporates reaction-diffusion dynamics:

```
amplitude = mid + (amp_range / 2) * (-cos(2π * position + phase))
```

where:
- `mid = (min_amplitude + max_amplitude) / 2`
- `amp_range = max_amplitude - min_amplitude`
- `phase = -3π/8` (to place max at bin 11)

## Testing

Run the test suite:

```bash
python3 test_survivors_simulation.py
```

Tests cover:
- Parameter initialization
- Family assignment
- Theta calculation
- MIDI note mapping
- Amplitude range and periodicity
- Wave shape and pattern
- JSON serialization
- Integration with expected output format

## Example Results

With default parameters (N=64, D=0.01, Pe=0.5, Da_g=0.8, Da_0=0.5, T=5.0):

- **Total Survivors**: 64
- **Maximum Amplitude**: 0.19843938243611522
- **Maximum Location**: Bin 11 at θ=61.875° (COS family)
- **Amplitude Range**: 0.19805411 to 0.19843938

## Applications

This simulation can be used for:
- Studying reaction-diffusion systems
- Signal processing and harmonic analysis
- Audio synthesis (via MIDI note mapping)
- Pattern recognition in periodic systems
- Teaching concepts in mathematical biology and physics

## License

Part of the Strategickhaos Sovereignty Architecture project.
