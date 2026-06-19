# TRIG6 Material Simulations Archive

## Overview

The TRIG6 Material Simulations Archive contains 36 blueprint specifications for paper, binding, and material simulations using the OmniCalc .t6 format. This archive serves as a sister protocol companion to Chapter 16 and implements a comprehensive framework for evaluating material stability and fitness.

## Contents

### Documentation
- `TRIG6_MATERIAL_SIMULATIONS_ARCHIVE.md` - Complete archive with all 36 blueprints

### Scripts
- `scripts/trig6_engine.py` - Core TRIG6 simulation engine
- `scripts/potentiometer_proof.py` - Hardware integration for physical proof
- `scripts/arduino_potentiometer.ino` - Arduino sketch for potentiometer interface
- `scripts/demo_comprehensive.py` - Comprehensive demonstration of all features

### Blueprints (36 Total)

#### Section I: Paper Simulations (12)
1. BP-01: Classic Reed Papyrus
2. BP-02: Lime-Infused Papyrus
3. BP-03: Grass Adaptation
4. BP-04: Bamboo Hybrid
5. BP-05: Banana Stem
6. BP-06: Cotton Rag (HIGHEST FITNESS - f=0.63)
7. BP-07: Hemp Fiber
8. BP-08: Mulberry Bark
9. BP-09: Rice Straw
10. BP-10: Corn Husk
11. BP-11: Sugarcane Bagasse
12. BP-12: Recycled Fiber

#### Section II: Binding Simulations (12)
13. BP-13: Basic Coptic Sew
14. BP-14: Single-Needle Variant
15. BP-15: Double-Thread
16. BP-16: Nag Hammadi Replica
17. BP-17: Modern Coptic
18. BP-18: Exposed Spine
19. BP-19: Multi-Section (8 sig)
20. BP-20: Parchment Hybrid
21. BP-21: Scroll-Codex Fusion
22. BP-22: Reinforced (Tape)
23. BP-23: Decorative (Embroidered)
24. BP-24: Miniature

#### Section III: Material Simulations (12)
25. BP-25: Wheat Starch Glue
26. BP-26: Reed Gum
27. BP-27: Gelatin (Bone)
28. BP-28: Acacia Tannin ⚠️ DANGER
29. BP-29: Linen Stitching
30. BP-30: Hemp Thread
31. BP-31: Silk Fibroin
32. BP-32: Goat Leather (Alum)
33. BP-33: Veg-Tanned Leather
34. BP-34: Brain-Tanned ⚠️ DANGER
35. BP-35: Chrome-Tanned ⚠️ DANGER ZONE
36. BP-36: PVA Synthetic

## TRIG6 Engine Reference

The TRIG6 Engine evaluates material stability using the following parameters:

```
θ (theta):  Process phase (0 to 2π)
R:          Resonance/stability (0 to 1, high = stable)
D:          Drift/deviation (0 to 1, low = aligned)
N:          Noise/uncertainty (0 to 1, low = certain)
α (alpha):  Damping coefficient (controls convergence rate)
eq:         Equivalence factor (goal alignment)

Fitness: f = R × (1-D) × (1-N) × eq
Danger:  |tan θ| > 10 triggers instability flag
Threshold: f ≥ 0.5 = stable basin
```

## Quick Start

### 1. Run the Comprehensive Demo

```bash
cd archives/trig6/scripts
python3 demo_comprehensive.py
```

This showcases all TRIG6 features including:
- Basic evaluation
- Material comparison
- Danger zone detection
- Parameter optimization
- Fitness formula explanation

### 2. Run the TRIG6 Engine

```bash
cd archives/trig6/scripts
python3 trig6_engine.py
```

This will run example simulations for:
- BP-01: Classic Reed Papyrus
- BP-06: Cotton Rag (highest fitness)
- BP-35: Chrome-Tanned Leather (danger zone)

### 3. Test Potentiometer Integration

```bash
cd archives/trig6/scripts
python3 potentiometer_proof.py
```

Note: Hardware integration requires:
- Arduino Uno/Nano with potentiometer on A0
- pyserial library: `pip install pyserial`
- Script enters simulation mode if hardware not available

### 4. Upload Arduino Sketch

For hardware proof system:
1. Open `scripts/arduino_potentiometer.ino` in Arduino IDE
2. Connect Arduino via USB
3. Upload sketch to board
4. Run `potentiometer_proof.py` with matching serial port

## Archive Summary

| Category | Count | Stable (f≥0.5) | Danger Zones |
|----------|-------|----------------|--------------|
| Papers | 12 | 7 | 0 |
| Bindings | 12 | 4 | 0 |
| Materials | 12 | 5 | 3 |
| **TOTAL** | **36** | **16** | **3** |

### Danger Zone Materials
- **BP-28**: Acacia Tannin (θ=π/3, volatile fermentation)
- **BP-34**: Brain-Tanned (θ=π/3, enzyme instability)
- **BP-35**: Chrome-Tanned (θ=π/2, tan→∞) - NOT RECOMMENDED for archival binding

### Top Performers (f ≥ 0.55)
- **BP-06**: Cotton Rag Paper (f=0.63) - Museum-grade archival
- **BP-01**: Classic Reed Papyrus (f=0.59) - Evolved state
- **BP-02**: Lime-Infused Papyrus (f=0.59) - Pharaoh-grade
- **BP-25**: Wheat Starch Glue (f=0.59) - Archival standard
- **BP-07**: Hemp Fiber (f=0.58) - Durable industrial
- **BP-17**: Modern Coptic (f=0.55) - Contemporary binding
- **BP-26**: Reed Gum (f=0.55) - Natural adhesive

## Hardware Integration

### Potentiometer Mapping Modes

The potentiometer proof system supports multiple mapping modes:

```
MODE_NOISE:     N = pot_norm
MODE_THETA:     θ = pot_norm × 2π
MODE_ALPHA:     α = pot_norm
MODE_DRIFT:     D = pot_norm
```

### Arduino Setup

```cpp
// Simple Arduino sketch for potentiometer reading
void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A0);
  Serial.println(sensorValue);
  delay(100);
}
```

## Usage Examples

### Python API

```python
from trig6_engine import TRIG6Engine
import math

# Initialize engine
engine = TRIG6Engine(danger_threshold=10.0)

# Evaluate a material state
state = engine.evaluate(
    theta=math.pi/6,
    R=0.88,
    D=0.12,
    N=0.18,
    eq=1.0
)

print(f"Fitness: {state.fitness:.3f}")
print(f"Stable: {engine.is_stable(state)}")
print(f"Danger: {state.danger}")
```

### Optimize Theta

```python
# Find optimal theta for a recipe
optimal = engine.optimize_theta(
    theta_start=0,
    theta_end=math.pi/4,
    R=0.86,
    D=0.14,
    N=0.20,
    eq=0.98,
    steps=100
)

print(f"Optimal θ: {optimal.theta:.3f}")
print(f"Max fitness: {optimal.fitness:.3f}")
```

## Prior Art & Attribution

- **Document Hash**: SHA-256 pending
- **Prior Art Timestamp**: 2026-01-25T07:52:56.278Z
- **GPG Signature**: AE5519579584DEF5
- **Entity**: Strategickhaos DAO LLC (EIN: 39-2900295)
- **Inventor**: Domenic Gabriel Garza
- **Generated**: 2026-01-25

## License

See repository LICENSE file for details.

## References

- Sister Protocol | Chapter 16 Companion
- OmniCalc .t6 Format Specification
- TRIG6 Engine Mathematical Framework
