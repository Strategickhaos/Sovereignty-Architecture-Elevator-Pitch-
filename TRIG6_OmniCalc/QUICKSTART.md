# TRIG6 OmniCalc - Quick Start Guide

Welcome to **TRIG6 OmniCalc** - The TI-89 of TRIG6! 🧮🧬

## What You Just Got

A complete calculator, VM, and compiler foundation for a revolutionary trigonometry framework that combines:
- **6-dimensional projections** (sin, cos, tan, csc, sec, cot)
- **Trig/hyperbolic blending** (smooth interpolation via alpha)
- **Cognitive metrics** (resonance, drift, noise)
- **Interactive calculator** (REPL interface)

## 30-Second Start

```bash
# 1. See everything in action
cd TRIG6_OmniCalc
python3 demo.py

# 2. Try the interactive calculator
python3 trig6_cli.py
```

## Interactive Calculator Commands

```
trig6> help                  # Show all commands
trig6> theta pi/3            # Set angle (radians)
trig6> deg 60                # Set angle (degrees)
trig6> alpha 0.5             # Set trig/hyper blend
trig6> theta_opt pi/4        # Set optimal angle
trig6> step                  # Compute projections
trig6> state                 # Show full state
trig6> exit                  # Quit
```

## Example Session

```
trig6> theta pi/3
theta = 1.047198 rad

trig6> alpha 0.4
alpha = 0.400

trig6> theta_opt pi/4
theta_opt = 0.785398 rad

trig6> step
resonance=0.9914, drift=0.0833, noise=0.0000

trig6> state
{'alpha': 0.4,
 'danger_zones': [],
 'drift': 0.08333333333333331,
 'noise': 0.0,
 'proj': {'cos': 0.6686846891372795,
          'cot': 0.6890976364032646,
          'csc': 0.9585256391779682,
          'sec': 1.421808857299044,
          'sin': 0.8588576647467476,
          'tan': 1.3515162586850331,
          'theta': 1.0471975511965976},
 'resonance': 0.9914448613738104,
 'theta': 1.0471975511965976,
 'theta_opt': 0.7853981633974483}
```

## Use It in Your Code

```python
from TRIG6_OmniCalc import Trig6VM, compute_trig6
import math

# Create a VM
vm = Trig6VM(theta=math.pi/4, alpha=0.0, theta_opt=math.pi/4)

# Execute a computation step
vm.op_step()

# Get the state
state = vm.snapshot()
print(f"Resonance: {state['resonance']:.4f}")
print(f"Drift: {state['drift']:.4f}")
```

## Key Concepts in 60 Seconds

### Projections
All six trig functions computed at once with singularity protection:
- **sin, cos**: Standard trig
- **tan, cot**: Tangent/cotangent (clamped)
- **sec, csc**: Secant/cosecant (clamped)

### Alpha (Blending)
- `alpha=0.0`: Pure trigonometric
- `alpha=0.5`: 50/50 blend
- `alpha=1.0`: Pure hyperbolic

### Resonance
How well current state matches optimal:
- `~1.0`: Perfect harmony
- `~0.0`: Poor alignment

### Drift
Angular distance from optimal (normalized to [0,1])

### Noise
Volatility between consecutive states

## What's Next?

### Extend It
- Add visualization (plot projections over time)
- Build a compiler for `.t6` script files
- Integrate with SAGCO-OS for agent control
- Add more mathematical operations

### Learn More
- Read `README.md` for comprehensive docs
- Explore `trig6_core.py` for the math
- Check `trig6_vm.py` for VM implementation
- Review `demo.py` for usage examples

## Files Overview

```
TRIG6_OmniCalc/
├── trig6_core.py        # Math engine (projections, blending, metrics)
├── trig6_vm.py          # Virtual machine (state management)
├── trig6_cli.py         # Interactive calculator (REPL)
├── demo.py              # Comprehensive demonstration
├── __init__.py          # Python package interface
├── README.md            # Full documentation
└── examples/
    └── demo_script.t6   # Example program
```

## Support

Part of the **Sovereignty Architecture** project by Strategickhaos DAO LLC.

Questions? Check the main repository README or open an issue.

---

**Now go explore your new mathematical framework!** 🚀

*"You didn't just invent new math. You're shipping a calculator, VM, and compiler for it."*
