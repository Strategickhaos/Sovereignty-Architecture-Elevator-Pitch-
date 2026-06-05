# TRIG6 OmniCalc

Calculator/VM/compiler for the TRIG6 mathematical framework - your "TI-89 for TRIG6".

## Overview

TRIG6 OmniCalc is a complete computational environment for working with TRIG6 mathematics, featuring:

- **Core Math Engine** (`trig6_core.py`): Raw/blended projections, resonance/drift/noise metrics, danger zone detection
- **Virtual Machine** (`trig6_vm.py`): Stateful execution environment with operations for angle manipulation
- **Compiler** (`trig6_compiler.py`): Parser and compiler for .t6 micro-language scripts
- **Interactive REPL** (`trig6_cli.py`): Command-line interface with script loading capability

## Requirements

- Python 3.10+ (tested with Python 3.12)
- Standard library only (math, dataclasses, typing, json)

## Installation

No installation required! Simply clone the repository and run:

```bash
cd TRIG6_OmniCalc
python3 trig6_cli.py
```

## Quick Start

### Interactive REPL

Start the interactive calculator:

```bash
python3 trig6_cli.py
```

Example session:

```
trig6> theta pi/4
Set theta = 0.785398 rad (45.00°)

trig6> alpha 0.5
Set alpha = 0.500000

trig6> step
Step executed. Use 'state' to view results.

trig6> state
============================================================
TRIG6 VM STATE
============================================================
θ (theta):     0.785398 rad (45.00°)
α (alpha):     0.500000
θ_opt:         0.785398 rad (45.00°)

--- Projections ---
sin(θ):        0.707107
cos(θ):        0.707107
tan(θ):        1.000000
csc(θ):        1.414214
sec(θ):        1.414214
cot(θ):        1.000000
blended:       0.868671

--- Metrics ---
Resonance:     0.700000
Drift:         0.000000
Noise:         0.100000
============================================================
```

### Running Scripts

Execute a .t6 script file:

```bash
python3 trig6_cli.py examples/demo_script.t6
```

Or load from within the REPL:

```
trig6> load examples/demo_script.t6
```

## .t6 Micro-Language

The .t6 micro-language is a simple, line-based DSL for programming TRIG6 operations.

### Syntax

- **Commands**: One per line, space-separated arguments
- **Expressions**: Support `pi`, basic arithmetic (`+`, `-`, `*`, `/`)
- **Comments**: `#` to end of line
- **Variables**: `set <var> <expr>` for assignment

### Commands

#### Angle Operations
```
theta <expr>          # Set theta in radians (e.g., theta pi/4)
deg <degrees>         # Set theta in degrees (e.g., deg 45)
theta_opt <expr>      # Set optimal theta
```

#### Blend Operations
```
alpha <expr>          # Set alpha [0,1] (e.g., alpha 0.5)
blend on|off          # Toggle full hyperbolic (alpha=1/0)
```

#### Computation
```
step                  # Compute projections and metrics
state                 # Print current state
```

#### Variables and Conditionals
```
set <var> <expr>      # Assign variable (e.g., set low_res 0.5)
if <var|metric> <op> <expr> then <cmd>
                      # Conditional execution
                      # metric: resonance, drift, noise
                      # op: <, >, =, <=, >=
```

#### Control Flow
```
exit                  # Exit script
```

### Example Script

```
# Demo: Drift correction
set low_res 0.5

theta pi/2
alpha 0.2
theta_opt pi/4

step
state

if resonance < low_res then theta pi/3

step
state
```

## Architecture

### Components

1. **trig6_core.py** - Core TRIG6 mathematics
   - Raw projections (sin, cos, tan, csc, sec, cot)
   - Blended projections (circular + hyperbolic)
   - Metrics (resonance, drift, noise)
   - Danger zone detection

2. **trig6_vm.py** - Virtual Machine
   - State management (theta, alpha, theta_opt)
   - Operations (set_theta, set_alpha, step)
   - State inspection (snapshot, print_state)

3. **trig6_compiler.py** - Compiler
   - Parser for .t6 syntax
   - Compiler to VM operations
   - Variable management
   - Conditional execution

4. **trig6_cli.py** - REPL
   - Interactive command interface
   - Script loading (.t6 files)
   - Command-line execution

### Data Flow

```
.t6 script → Compiler → VM Operations → VM State → Metrics
     ↓                                       ↓
  REPL commands → Direct VM ops ──────────→ State
```

## Integration with SAGCO-OS

TRIG6 OmniCalc is designed to integrate with SAGCO-OS:

- **Hypervisor Integration**: Call `Trig6VM.op_step()` in hypervisor ticks for agent weight calculations (e.g., `w_i = sin θ`)
- **Swarm Simulations**: Emit .t6 scripts from hypervisor for distributed computation
- **State Synchronization**: Use `snapshot()` for state logging and correlation

Example integration:

```python
from trig6_vm import Trig6VM

# In SAGCO hypervisor
vm = Trig6VM()
vm.op_set_theta(agent_angle)
vm.op_step()
agent_weight = vm.state.sin  # Use sin(θ) as weight
```

## Development

### Running Examples

Test the compiler:
```bash
python3 trig6_compiler.py
```

Test the VM:
```bash
python3 trig6_vm.py
```

Test the core math:
```bash
python3 trig6_core.py
```

### Extending

To add new operations:

1. Add core math to `trig6_core.py`
2. Add VM operation to `trig6_vm.py`
3. Add compiler command to `trig6_compiler.py`
4. Add CLI command to `trig6_cli.py`

Example: Adding a new metric

```python
# In trig6_core.py
def compute_harmony(self, theta: float) -> float:
    return math.cos(theta) * math.sin(theta)

# In trig6_vm.py
def op_step(self):
    # ... existing code ...
    self.state.harmony = self.core.compute_harmony(self.state.theta)

# In trig6_compiler.py
# Harmony automatically available in conditionals as 'harmony'
```

## Patent Reference

This implementation serves as a reference for TRIG6 mathematical theorems and computational framework.

## License

See repository LICENSE file.

## Authors

Created for the Sovereignty Architecture project.

---

**Dom—play, evolve, ship. This is your math alive. 🧮🧬**
