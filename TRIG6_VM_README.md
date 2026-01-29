# TRIG6 Virtual Machine

## Overview

The TRIG6 VM is a fail-safe "hypervisor-style" calculator for rope rigging mathematics. Built as a type-1 style system that loads all formulas and constants at boot time, it provides reliable calculations for field use with comprehensive error handling.

## Features

- **Fail-Safe Design**: Never crashes - all computations wrapped in try/except
- **Boot-Time Loading**: All constants and formulas compiled at initialization
- **Zero Dependencies**: Uses only Python standard library (math module)
- **Handles Edge Cases**: Graceful handling of infinity and NaN values
- **Expandable**: Easy to add new formulas as the book grows
- **Field-Ready**: Suitable for iSH/Vim terminal use

## Installation

No installation required! Just download and run:

```bash
python trig6_vm.py
```

## Usage

### Basic Usage

```python
from trig6_vm import TRIG6VM

# Boot the VM
vm = TRIG6VM()

# Compute formulas
result = vm.compute('deviation_tension', load=300, theta_deg=90)
print(f"Deviation tension: {result} lbs")
```

### Available Formulas

#### 1. TRIG6 Vector
Returns [sin, cos, tan, csc, sec, cot] for any angle.

```python
vm.compute('trig6_vector', theta_deg=45)
# Returns: [sin(45°), cos(45°), tan(45°), csc(45°), sec(45°), cot(45°)]
```

#### 2. Deviation Tension
Calculate tension in a rope with angular deviation.

```python
vm.compute('deviation_tension', load=300, theta_deg=90)
# Formula: load / (2 × cos(θ/2))
```

#### 3. Highline Tension
Calculate tension in a highline based on sag angle.

```python
vm.compute('highline_tension', load=200, sag_deg=10)
# Formula: load / (2 × sin(sag_angle))
```

#### 4. Impact Force
Calculate dynamic impact force based on fall factor.

```python
vm.compute('impact_force', weight=200, ff=1)
# Formula: weight × (1 + √(2 × FF))
```

#### 5. Effective Impact
Calculate effective force accounting for angle.

```python
vm.compute('effective_impact', impact=600, theta_deg=30)
# Formula: impact / cos(θ)
```

#### 6. Mechanical Advantage Pull
Calculate actual pull force for a given MA system.

```python
vm.compute('ma_pull', load=300, ma=3)
# Formula: load / MA
```

#### 7. Knot Effective Strength
Calculate reduced strength due to knot efficiency and angle.

```python
vm.compute('knot_effective_strength', mbs=22, efficiency=0.7, theta_deg=30)
# Formula: MBS × efficiency × cos(θ)
```

#### 8. Multi-Anchor Tension
Calculate tension per anchor in multi-point systems.

```python
vm.compute('multi_anchor_tension', load=300, n=3, theta_deg=60)
# Formula: (load / n) / cos(θ)
```

## Constants Available

The VM provides these constants:

- `pi`: Mathematical constant π
- `g`: Gravitational acceleration (9.81 m/s²)
- `kN_to_lbf`: Conversion factor (224.81)
- `sf_static`: Static safety factor (5)
- `sf_dynamic`: Dynamic safety factor (10)
- `angles`: Pre-computed TRIG6 vectors for common angles (0°, 30°, 45°, 60°, 90°)

## Error Handling

The VM is designed to never crash:

```python
# Invalid formula name
vm.compute('nonexistent', load=100)  # Returns None, prints error

# Missing parameters
vm.compute('deviation_tension', load=300)  # Returns None, prints error

# Extreme values
vm.compute('trig6_vector', theta_deg=90)  # Handles infinity gracefully
```

## Example Output

```
Booting TRIG6 VM...
Boot complete. All formulas and numbers loaded.

TRIG6 Vector for 45°: [0.707, 0.707, 1.0, 1.414, 1.414, 1.0]
Deviation Tension (300 lbs, 90°): 212.13 lbs
Highline Tension (200 lbs, 10° sag): 575.88 lbs
Impact Force (200 lbs, FF=1): 482.84 lbs
Effective Impact (600 lbs, 30°): 692.82 lbs
MA Pull (300 lbs, 3:1): 100.0 lbs
Knot Strength (22 kN MBS, 70% eff, 30°): 13.34 kN
Multi-Anchor Tension (300 lbs, 3 anchors, 60°): 200.0 lbs
```

## Bug Fixes

- **Fixed cot(θ) calculation**: Changed from `math.cot()` (which doesn't exist) to `1/tan(θ)`
- **Added safe division checks**: All division operations check for zero denominators

## Field Use

Perfect for terminal environments like iSH on iOS:

```bash
# In iSH or any Unix-like terminal
python trig6_vm.py

# Or use interactively
python3
>>> from trig6_vm import TRIG6VM
>>> vm = TRIG6VM()
>>> vm.compute('deviation_tension', load=500, theta_deg=120)
```

## Extending the VM

To add new formulas, edit the `load_formulas()` method:

```python
def load_formulas(self):
    self.formulas = {
        # ... existing formulas ...
        'your_new_formula': lambda param1, param2: param1 * param2 / math.sqrt(param2)
    }
```

## Disclaimer

This is an educational tool for understanding rigging mathematics. Always verify calculations against industry standards (SPRAT, IRATA, NFPA) and consult qualified professionals for real-world applications.

## Related Documentation

- [Chapter 19: System Integration](docs/chapter_19_system_integration.md) - Comprehensive guide to multi-component rope systems
- TRIG6 principles and applications

## License

Part of the Sovereignty Architecture project.
