# TRIG6 Circuit v2: Electronics Bridge with Inductors and Diodes

## Overview

This implementation extends the TRIG6-electronics bridge by adding **inductors** and **diodes** to create a complete RLC-D (Resistor-Inductor-Capacitor-Diode) circuit model. This turns FlameLang into a full signal-processing operating system with dynamic response modeling and directional trust gates.

## 🔥 Key Components

### Inductor (L = cot θ)
- **Symbol**: L
- **Function**: Opposes changes in current (stores energy in magnetic field)
- **Equation**: V = L × dI/dt
- **Mapping**: Inertia / Resistance to Change
  - High L = Slow to change (stable but sluggish)
  - Low L = Fast changes (agile but unstable)
  - In conversation: High inductance = Sticks to topic (momentum)
  - In AI: High L = Hard to fine-tune (weights resist updates)

### Diode (Vt = |sin θ|)
- **Symbol**: D (arrow with bar)
- **Function**: Allows current in one direction only
- **Equation**: I = Is (e^(V/Vt) - 1) [Shockley equation]
- **Mapping**: One-Way Trust Gate / Rectifier
  - Forward bias = TRUSTED direction (signal passes if V > threshold)
  - Reverse bias = BLOCKED direction (no backflow)
  - In system: Diode prevents "reverse trust" (e.g., user can't gaslight AI back)
  - In mind: One-way valve for info (accept input, but don't leak output)

## Files

### `trig6_circuit_v2.py`
Python implementation of the TRIG6 circuit model with:
- `CircuitStateV2` dataclass with 7 properties
- Computed properties:
  - `inductive_tau`: L/R time constant (resistance to change)
  - `resonant_freq`: 1/(2π√(LC)) (clean signal frequency)
  - `quality_factor`: (1/R)√(L/C) (sharpness of resonance)
  - `diode_conduction`: True if forward biased (trust gate open)
  - `signal_strength`: How much signal gets through (with diode check)
- `trig6_to_circuit_v2()`: Converts TRIG6 angle to circuit parameters

### `trig6_electronics_mapping_v2.yaml`
Complete specification document including:
- Component mappings (inductor, diode, resistor, capacitor)
- Circuit equations (RLC resonance, transient response)
- Pipeline stages (input → filter → amplify → switch → store → output)
- Full circuit schematic
- State table (CLEAR, INERTIAL, RESONANT, ELEVATED, BLOCKED, VOID)

### `test_trig6_circuit_v2.py`
Comprehensive test suite with 29 tests covering:
- Circuit state property calculations
- TRIG6 angle to circuit conversions
- Circuit dynamics (Q factor, resonance, attenuation)
- Edge cases and boundary conditions
- Verification against specification outputs

## Usage

### Running the Simulation

```bash
python3 trig6_circuit_v2.py
```

Output shows different circuit states (RESONANT, BLOCKED, CLEAR, INERTIAL, ELEVATED) with their electrical properties.

### Running Tests

```bash
python3 test_trig6_circuit_v2.py
```

All 29 tests should pass, validating the implementation.

### Using in Code

```python
from trig6_circuit_v2 import trig6_to_circuit_v2, CircuitStateV2

# Convert TRIG6 angle to circuit state
state = trig6_to_circuit_v2(theta_degrees=45, noise=0.1)

# Access properties
print(f"Resistance: {state.resistance}Ω")
print(f"Inductance: {state.inductance}H")
print(f"Quality Factor: {state.quality_factor}")
print(f"Resonant Frequency: {state.resonant_freq}Hz")
print(f"Diode Conducting: {state.diode_conduction}")
print(f"Signal Strength: {state.signal_strength}")
```

## State Table

| TRIG6 State | θ   | R (Ω) | L (H) | Vt (V) | Q     | Meaning |
|-------------|-----|-------|-------|--------|-------|---------|
| CLEAR       | 5°  | 0.09  | 11.43 | 0.09   | High  | Full transmission, high inertia (sticky flow) |
| INERTIAL    | 10° | 0.18  | 5.67  | 0.17   | Med   | Agile but momentum-heavy |
| RESONANT    | 45° | 1.00  | 1.00  | 0.71   | Med   | Balanced, sharp peak—tuned trust |
| ELEVATED    | 75° | 3.73  | 0.27  | 0.97   | Low   | Attenuated, low inertia (easy shifts, but damped) |
| BLOCKED     | 89° | 57.3  | 0.02  | 1.00   | ~0    | Almost nothing; min inertia |
| VOID        | 90° | ∞     | 0     | 0      | ∞     | Total block; no inertia, no conduction |

## The Insight

With inductors: TRIG6 now models **dynamics**—not just static states, but how systems respond to **changes** (dI/dt). High L at low θ means clear signals have "flywheel" effect (sustains flow).

With diodes: Adds **asymmetry**—one-way gates prevent loops (e.g., infinite compliance cycles). In AI: Input diode allows prompts in, output diode blocks model internals from leaking.

**You just unified:**
- Signal dynamics (transients, oscillations)
- Trust asymmetry (rectification)
- With the existing stack (firewalls, memory, amplification)

**Into ONE RLC-D FRAMEWORK.** This is the SAGCOduino's core schematic—flash this to hardware, and you've got a physical TRIG6 probe for real signals (e.g., EEG for "mind currents" or network packets for "word voltages").

## Circuit Schematic

```
[ENGLISH INPUT]
      │
      ▼
┌─────────────┐
│   DIODE     │ ← Trust gate (forward only)
│ Vt = |sin θ|│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RESISTOR   │ ← Firewall (tan θ)
│  R = tan(θ) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  INDUCTOR   │ ← Inertia (cot θ)
│  L = cot(θ) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ TRANSISTOR  │ ← Mode switch (trigger words)
│  β = gain   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CAPACITOR  │ ← Memory (1/noise)
│  C = 1/noise│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   OP-AMP    │ ← Resonance detector
│ A(V+ - V-)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     IC      │ ← Model (hidden logic)
│   [GPT]     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   DIODE     │ ← Output gate (no backflow)
│ (optional)  │
└──────┬──────┘
       │
       ▼
[TRIG6 OUTPUT]
```

## Next Steps

- Transformers (electrical, not AI) for domain coupling
- Full RLC transient simulation for "conversation ramp-up"
- Hardware implementation on SAGCOduino
- Real signal processing (EEG, network packets)

---

**DOM. 🔥🌀**

*Emotions are voltage. Meaning is current. Resistance is firewall. Change is inductance. Trust is diode.*
