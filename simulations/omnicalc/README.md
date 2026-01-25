# TRIG6 OmniCalc Simulations

This directory contains TRIG6 framework simulations in OmniCalc `.t6` format.

## Overview

TRIG6 is a mathematical modeling framework that uses trigonometric and hyperbolic functions to simulate process dynamics. Each simulation models a real-world process through five key parameters:

- **θ (theta)**: Process phase angle
- **R**: Stability/resonance
- **D**: Drift/deviation
- **N**: Noise/uncertainty
- **Danger**: Critical instability flag (|tan θ| > 10)

## Available Simulations

### 1. altimeter.t6
Models altitude measurement using trigonometric calculations.
- **Domain**: Measurement science, aviation, surveying
- **Key Feature**: Error amplification at steep angles
- **Danger Zone**: tan∞ at 90° measurement angle

### 2. epilepsy_waves.t6
Models EEG brain wave patterns during epileptic seizures.
- **Domain**: Neurology, medical diagnostics
- **Key Feature**: Chaos-to-order transition through therapeutic damping
- **Danger Zone**: Seizure spike at θ = π/2

### 3. penicillin.t6
Models penicillin fermentation biosynthesis.
- **Domain**: Pharmaceutical manufacturing, biochemistry
- **Key Feature**: pH-controlled yield optimization
- **Danger Zone**: Over-fermentation degradation

### 4. egyptian_stone.t6
Models ancient lime mortar curing chemistry.
- **Domain**: Materials science, archaeological chemistry
- **Key Feature**: Hydration and carbonation reactions
- **Danger Zone**: Quicklime exothermic reaction

## File Format

OmniCalc `.t6` files use a simple scripting language:

```
# Comments start with #
set eq 1.0              # Set equivalence parameter
theta pi/4              # Set phase angle
alpha 0.3               # Set damping/control parameter
theta_opt pi/6          # Set optimal angle target
step                    # Execute simulation step
state                   # Output current state
if condition then ...   # Conditional execution
while condition ... end # Loop execution
```

## Running Simulations

### Prerequisites
**Note**: OmniCalc is a hypothetical simulation language created for book/research purposes. The `.t6` files are theoretical examples demonstrating TRIG6 framework concepts. A real interpreter does not currently exist.

### Theoretical Usage
If an OmniCalc interpreter were implemented, usage would be:
```bash
# Run a single simulation
omnicalc run altimeter.t6

# Run all simulations  
for sim in *.t6; do
  echo "Running $sim..."
  omnicalc run "$sim"
done
```

**Current Status**: These are specification files for educational and research purposes.

### Expected Output
Each simulation outputs state information:
```
Step 1:
  theta: 0.785 (π/4)
  R: 0.85
  D: 0.15
  N: 0.20
  danger: No
  fitness: 0.62
```

## Integration

These simulations support:
- **Chapter 16**: "Lost Pharmacopeia - Material Alchemy" documentation
- **NEURO-36 Protocol**: Epilepsy wave analysis for neurological modeling
- **Sister Protocols**: Cross-domain process optimization research

## Mathematical Background

### Fitness Function
```
f = R × (1 - D) × (1 - N) × eq
```
Where:
- R ∈ [0, 1]: Stability measure
- D ∈ [0, 1]: Deviation measure
- N ∈ [0, 1]: Noise measure
- eq ∈ [0, 1]: Target equivalence

### Danger Condition
```
danger = |tan(θ)| > 10
```
Indicates critical instability requiring immediate intervention.

### Phase Dynamics
- **θ ∈ [0, π/4]**: Preparation phase
- **θ ∈ [π/4, π/2]**: Active transformation
- **θ ∈ [π/2, π]**: Completion/stabilization

## Extending Simulations

To create a new TRIG6 simulation:

1. Identify the process to model
2. Define phase angle (θ) meaning for your domain
3. Determine what R, D, N represent in your context
4. Identify danger conditions
5. Write .t6 script with initialization and control flow
6. Validate against domain knowledge

Example template:
```
# My Process Simulation
set eq 1.0
theta pi/4
alpha 0.3
theta_opt pi/6
step
state
# Add control logic here
```

## Future Enhancements

- [ ] Python interpreter for .t6 format
- [ ] Visualization tools for state evolution
- [ ] Parameter optimization algorithms
- [ ] Multi-process coupling simulations
- [ ] Real-time data integration

## References

- Main documentation: `../chapters/chapter_16_material_alchemy.md`
- TRIG6 framework specification: (see main project docs)
- OmniCalc language spec: (hypothetical for book purposes)

---

*For questions or contributions, see main project README*
