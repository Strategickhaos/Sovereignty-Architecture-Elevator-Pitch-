# TRIG6 OmniCalc - Quick Reference

## Installation & Setup
```bash
cd TRIG6_OmniCalc
python3 trig6_cli.py        # Start interactive REPL
python3 trig6_cli.py file.t6  # Run script file
```

## Common Commands

### Interactive REPL
```
theta pi/4      # Set angle to π/4 radians
deg 45          # Set angle to 45 degrees
alpha 0.5       # Set blend factor to 0.5
theta_opt pi/3  # Set optimal angle
step            # Compute projections and metrics
state           # Show detailed state
snapshot        # Show JSON state
help            # Show all commands
exit            # Quit
```

## .t6 Script Examples

### Basic Computation
```
theta pi/4
alpha 0.5
step
state
```

### Using Variables
```
set my_angle pi/6
set threshold 0.8
theta my_angle
alpha 0.5
step
```

### Conditionals
```
# Correct if resonance too low
if resonance < 0.8 then theta pi/4

# Adjust based on noise
if noise > 0.5 then alpha 0.2

# Use variables
set min_res 0.9
if resonance < min_res then theta_opt pi/3
```

### Complete Example
```
# Optimization script
set target 0.95

# Initial configuration
theta 0
alpha 0.3
theta_opt pi/4
step

# Optimize
if resonance < target then theta pi/6
step

if resonance < target then theta pi/4
step

# Final result
state
```

## Key Metrics

- **Resonance**: [0, 1] - Higher = better alignment to optimal angle
- **Drift**: [0, 1] - How far from optimal (0 = perfect)
- **Noise**: [0, 1] - Proximity to danger zones (0 = safe)

## Danger Zones

| Angle | Issue | Severity |
|-------|-------|----------|
| 0, 2π | cot singularity | Critical |
| π/2, 3π/2 | tan/cot singularity | Critical |
| π | Phase flip boundary | Warning |

## Python Integration

```python
from trig6_vm import Trig6VM

# Create VM
vm = Trig6VM()

# Set parameters
vm.op_set_theta(3.14159/4)  # π/4
vm.op_set_alpha(0.5)

# Compute
vm.op_step()

# Access results
print(f"sin(θ) = {vm.state.sin}")
print(f"Resonance = {vm.state.resonance}")

# Get JSON
json_state = vm.snapshot()
```

## Tips

1. Always call `step` after changing theta or alpha
2. Use `state` to see computed metrics
3. Check for danger warnings in output
4. Variables are evaluated at runtime
5. Conditionals check VM state metrics

## Common Patterns

### Safety Check
```
theta pi/2
step
if noise > 0.5 then theta pi/4
step
```

### Optimization Loop
```
set target 0.9
theta 0
step

if resonance < target then theta pi/6
step

if resonance < target then theta pi/4
step
```

### Blend Exploration
```
theta pi/4
blend off
step
state

blend on
step
state
```

---

For full documentation, see README.md
