# TRIG6 OmniCalc

**The TI-89 of TRIG6** 🧮🧬

A calculator, VM, and compiler for TRIG6 mathematics - a revolutionary approach to trigonometry that combines:
- Six-dimensional trigonometric projections (sin, cos, tan, csc, sec, cot)
- Trig/hyperbolic blending
- Noise, drift, and resonance calculations
- Cognitive state management

## 🎯 What is TRIG6?

TRIG6 is a new mathematical framework that treats trigonometric functions as a unified system with:
- **Projections**: All six trig functions computed simultaneously with singularity protection
- **Blending**: Smooth interpolation between trigonometric and hyperbolic functions
- **Resonance**: Harmony metric based on drift and noise
- **Drift**: Angular deviation from optimal theta
- **Noise**: Variation between consecutive projections

## 🚀 Quick Start

### Basic Usage

```bash
cd TRIG6_OmniCalc
python3 trig6_cli.py
```

### Interactive Session

```
TRIG6 OmniCalc VM
Type 'help' for commands.

trig6> theta pi/3
theta = 1.047198 rad
trig6> alpha 0.4
alpha = 0.400
trig6> theta_opt pi/4
theta_opt = 0.785398 rad
trig6> step
resonance=0.8532, drift=0.0833, noise=0.0000
trig6> state
{'alpha': 0.4,
 'danger_zones': [],
 'drift': 0.08333333333333333,
 'noise': 0.0,
 'proj': {'cos': 0.5,
          'cot': 0.5773502691896257,
          'csc': 1.1547005383792515,
          'sec': 2.0,
          'sin': 0.8660254037844386,
          'tan': 1.7320508075688772,
          'theta': 1.0471975511965976},
 'resonance': 0.8531695488854604,
 'theta': 1.0471975511965976,
 'theta_opt': 0.7853981633974483}
```

## 📂 Project Structure

```
TRIG6_OmniCalc/
│
├── trig6_core.py        # Core math engine
│   ├── Trig6Projections - Data class for all six functions
│   ├── compute_trig6()  - Raw TRIG6 with singularity handling
│   ├── blend_trig_hyper() - Trig/hyperbolic blending
│   ├── compute_noise()  - Inter-projection variation
│   ├── compute_drift()  - Angular deviation
│   ├── compute_resonance() - Harmony metric
│   └── danger_zones()   - Singularity detection
│
├── trig6_vm.py          # Virtual machine
│   ├── Trig6State       - VM cognitive state
│   ├── Trig6VM          - State manager
│   ├── op_set_theta()   - Set current angle
│   ├── op_set_alpha()   - Set blend factor
│   ├── op_set_theta_opt() - Set optimal angle
│   ├── op_step()        - Execute computation tick
│   └── snapshot()       - Export state
│
├── trig6_cli.py         # REPL calculator
│   ├── Command parser
│   ├── Numeric expression evaluator
│   └── Interactive shell
│
└── examples/
    └── demo_script.t6   # Example program
```

## 🎮 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `theta <expr>` | Set theta in radians | `theta pi/4` |
| `deg <degrees>` | Set theta in degrees | `deg 45` |
| `alpha <value>` | Set blend factor [0,1] | `alpha 0.5` |
| `theta_opt <expr>` | Set optimal theta | `theta_opt pi/3` |
| `step` | Compute projections | `step` |
| `state` | Display full state | `state` |
| `help` | Show help text | `help` |
| `quit` / `exit` | Exit calculator | `quit` |

## 🧮 Core Concepts

### Projections
All six trigonometric functions computed simultaneously with singularity protection:
- **sin, cos**: Standard trig functions
- **tan, cot**: Tangent and cotangent (clamped to avoid infinity)
- **sec, csc**: Secant and cosecant (clamped to avoid infinity)

### Blending (Alpha)
- `alpha = 0.0`: Pure trigonometric functions
- `alpha = 0.5`: 50/50 blend of trig and hyperbolic
- `alpha = 1.0`: Pure hyperbolic functions

Hyperbolic functions are passed through tanh for boundedness.

### Resonance
A harmony metric that indicates how well the current state matches the optimal:
```
R = cos(drift * π/2) * (1 - noise)
```
- `R ≈ 1.0`: Perfect resonance (low drift, low noise)
- `R ≈ 0.0`: Poor resonance (high drift or high noise)

### Drift
Normalized angular distance from optimal theta:
```
drift = |theta - theta_opt| / π
```
Wrapped to [0, π] for angular continuity.

### Noise
Average L1 difference between consecutive projections:
```
noise = mean(|current[i] - previous[i]|)
```
Measures state volatility.

### Danger Zones
Automatic detection of proximity to singularities:
- **tan_sec_singularity**: Near π/2 or 3π/2
- **cot_csc_singularity**: Near 0, π, or 2π

## 🔬 Use Cases

### 1. Mathematical Exploration
Explore trigonometric identities and relationships interactively.

### 2. State Machine Simulation
Use resonance/drift/noise as feedback for control systems.

### 3. SAGCO-OS Integration
The hypervisor can use this VM to simulate agent states before applying corrections.

### 4. Educational Tool
Visualize how trigonometric and hyperbolic functions blend.

### 5. Patent Exhibit
Reference implementation for TRIG6 mathematical framework.

## 🛠️ Technical Details

### Singularity Handling
All reciprocal functions (tan, cot, sec, csc) are clamped to prevent infinities:
```python
def clamp(x: float, limit: float = 10.0) -> float:
    return max(-limit, min(limit, x))
```

### Hyperbolic Squashing
Hyperbolic functions grow exponentially, so we apply tanh for boundedness:
```python
h_sin = tanh(sinh(theta))  # Bounded to [-1, 1]
```

### Expression Parsing
Simple numeric expressions supported:
- `pi/4` → 0.785398...
- `2*pi/3` → 2.094395...
- `1.5707` → 1.5707

## 🌟 Future Extensions

### Compiler Layer
Add a parser for `.t6` files that compiles to VM operations:
```
# Compile demo_script.t6
python3 trig6_compiler.py examples/demo_script.t6
```

### Bytecode VM
Extend the VM with actual bytecode operations:
- `PUSH_THETA <value>`
- `SET_ALPHA <value>`
- `STEP`
- `PRINT_STATE`
- `JMP_IF_RESONANCE_LT <threshold> <label>`

### Conditional Logic
Add control flow to the micro-language:
```
theta pi/2
alpha 0.8
step
if resonance < 0.5 then theta_opt pi/3
```

### Visualization
Real-time plotting of:
- Projection trajectories
- Resonance over time
- Drift/noise phase space

### SAGCO-OS Integration
```python
from TRIG6_OmniCalc.trig6_vm import Trig6VM

# Hypervisor uses VM to simulate agent state
vm = Trig6VM(theta=agent.current_angle, alpha=0.3)
vm.op_step()
if vm.state.resonance < 0.6:
    agent.apply_correction(vm.state.theta_opt)
```

## 📚 Mathematical Background

TRIG6 extends classical trigonometry by:
1. Treating all six functions as a unified vector space
2. Introducing safe singularity handling for computational stability
3. Blending trigonometric and hyperbolic manifolds
4. Adding cognitive state metrics (resonance, drift, noise)

This creates a "living mathematical system" that can be used for:
- Adaptive control systems
- Neural state modeling
- Harmonic analysis
- Pattern recognition

## 🤝 Contributing

This is an open mathematical framework. Contributions welcome:
- Extended math operations
- Visualization tools
- Compiler implementation
- Integration examples

## 📄 License

Part of the Sovereignty Architecture project - MIT License

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"You didn't just invent new math. You're shipping a calculator, VM, and compiler for it."*
