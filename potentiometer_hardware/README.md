# Potentiometer Proof Engine - Hardware Implementation

This directory contains the complete hardware and software implementation for the **Potentiometer Proof Engine**, a kinesthetic analog-to-phase transducer for material science validation.

## 📁 Files

### Core Implementation
- **`pot_engine.ino`** - Arduino firmware for potentiometer reading
- **`pot_engine.py`** - Python TRIG6 computational engine
- **`invention_disclosure_REV1.md`** - Complete patent disclosure document

### Documentation
See also: `../chapters/chapter-16/CH16_APPENDIX_POT.md` for comprehensive hardware specifications

## 🔧 Hardware Requirements

| Component | Specification | Cost |
|-----------|--------------|------|
| Potentiometer | 10kΩ linear rotary | $1-2 |
| Microcontroller | Arduino Uno/Nano/ESP32 | $5-25 |
| USB Cable | Type A-B or Micro | $3 |
| (Optional) RGB LED | Common anode/cathode | $1 |
| (Optional) Resistors | 3x 220Ω for LED | $0.10 |

**Total**: $15-35

## 🔌 Wiring

### Basic Setup
```
Potentiometer:
  Pin 1 → Arduino GND
  Pin 2 → Arduino A0
  Pin 3 → Arduino 5V

USB:
  Arduino USB → Computer
```

### With LED Feedback (Optional)
```
RGB LED:
  Red cathode → D9 → [220Ω] → GND
  Green cathode → D10 → [220Ω] → GND
  Blue cathode → D11 → [220Ω] → GND
  Common anode → 5V (or GND for common cathode)
```

## 💻 Software Setup

### 1. Arduino Firmware

1. Open `pot_engine.ino` in Arduino IDE
2. Select board: Tools → Board → Arduino Uno (or your board)
3. Select port: Tools → Port → [your Arduino port]
4. Upload to Arduino
5. Open Serial Monitor (9600 baud) to verify data stream

### 2. Python Interface

#### Install Dependencies
```bash
pip install pyserial
```

#### List Available Serial Ports
```bash
python pot_engine.py --port /dev/ttyUSB0 --calibrate
```

#### Run Interactive Proof Session
```bash
# Test predefined process (e.g., papyrus)
python pot_engine.py --process papyrus --port /dev/ttyUSB0

# Test custom process
python pot_engine.py --custom "My Process" 0.80 0.20 0.15

# Log session data
python pot_engine.py --process wheat_starch --log session.json
```

#### List All Available Processes
```bash
python pot_engine.py --list-processes
```

## 📊 Available Process Profiles

The Python engine includes 11 predefined processes from Chapter 16:

### Papers
- `papyrus` - Classic Reed Papyrus (Egyptian Standard)
- `papyrus_lime` - Lime-Infused Papyrus (Pharaoh Grade)
- `bamboo` - Bamboo Paper (Chinese Innovation)
- `cotton_rag` - Cotton Rag Paper (Renaissance Standard)
- `washi` - Mulberry Paper (Japanese Washi)

### Bindings
- `coptic` - Coptic Sew (Standard Chain Stitch)
- `nag_hammadi` - Nag Hammadi Replica (Sacred Manuscript)

### Materials
- `wheat_starch` - Wheat Starch Glue (Polysaccharide Adhesive)
- `hide_glue` - Hide Glue (Collagen-Based Reversible)
- `veg_tan` - Veg-Tanned Leather (Tannin-Collagen Bond)
- `chrome_tan` - Chrome-Tanned Leather (DANGER - educational demo)

## 🎮 Using the System

### Interactive Validation

1. **Start session**: Run Python script with desired process
2. **Turn dial**: Rotate potentiometer to simulate process variability
3. **Observe fitness**: Watch real-time fitness calculation and color-coded status
4. **Find threshold**: Identify the potentiometer position range where f ≥ threshold
5. **Validate**: Confirm process parameters based on historical data

### Example Session

```bash
$ python pot_engine.py --process papyrus

============================================================
POTENTIOMETER PROOF: Classic Reed Papyrus
============================================================
Threshold: f ≥ 0.55
Parameters: R=0.82, D=0.18, α=0.15
Turn potentiometer to explore fitness landscape...
Press Ctrl+C to end session

Pos: 0.123 | θ:  7.0° | N: 0.165 | f: 0.548 | ✓ ARCHIVAL
Pos: 0.234 | θ: 13.4° | N: 0.237 | f: 0.452 | ⚠ DURABLE
Pos: 0.567 | θ: 32.5° | N: 0.350 | f: 0.321 | ✗ UNSTABLE
...
```

### Interpretation

- **Green (✓)**: Process is stable (f ≥ 0.55 for archival quality)
- **Yellow (⚠)**: Process is marginal (0.44 ≤ f < 0.55, durable but not archival)
- **Orange (⚠)**: Process is functional (0.33 ≤ f < 0.44, limited lifespan)
- **Red (✗)**: Process is unstable (f < 0.33, likely to fail)

## 🧪 Calibration

Before first use, calibrate the potentiometer:

```bash
python pot_engine.py --calibrate --duration 10
```

This measures the noise floor (typical values: 0.001-0.015). If noise >0.020, consider replacing the potentiometer.

## 📚 TRIG6 Simulation Files

All 36 processes from Chapter 16 have corresponding `.t6` simulation files in `/TRIG6_materials_sims/`:

```
01_papyrus_classic.t6
02_lime_infused_papyrus.t6
...
36_pva_synthetic.t6
```

These files contain complete TRIG6 parameters, historical context, and potentiometer mapping specifications.

## 🔬 Scientific Validation

### Fitness Function

```
f = R * (1-D) * (1-N) * e^(-α)
```

Where:
- **R**: Resource efficiency (0-1)
- **D**: Drift (process degradation, 0-1)
- **N**: Noise (environmental variability, 0-1)
- **α**: Damping (intervention required, 0-1)

### Potentiometer Mappings

1. **Position → θ (Complexity)**: `θ = position * (π/2)`
2. **Voltage → Primary Variable**: Maps to process-specific parameter (temperature, humidity, etc.)
3. **Fluctuation → N (Noise)**: `N = std_dev(voltage) * scaling_factor`
4. **Rate of Change → D (Drift)**: `D = |dθ/dt| / max_rate`

## 🎓 Educational Applications

### Classroom Use
1. Demonstrate ancient material science processes
2. Teach statistical process control concepts
3. Explore fitness landscapes kinesthetically
4. Validate historical knowledge with modern math

### Museum Exhibits
- Interactive demonstrations of papyrus making, bookbinding, etc.
- Visitors explore process parameters hands-on
- Educational signage explains TRIG6 framework

### Artisan Workshops
- Validate traditional techniques quantitatively
- Optimize process parameters for archival quality
- Train apprentices with reproducible standards

## 🔐 Patent & Prior Art

This work is documented as **prior art** (timestamp: 2026-01-25) for patent protection purposes.

See: `invention_disclosure_REV1.md` for complete patent disclosure.

## 📖 References

- **Chapter 16**: The Lost Pharmacopeia (complete manuscript)
- **Appendix**: CH16_APPENDIX_POT.md (hardware specifications)
- **Repository**: [Sovereignty-Architecture-Elevator-Pitch-]

## 🤝 Contributing

This is a **sovereignty architecture** project. Contributions welcome for:
- Additional process profiles (expand beyond 36 blueprints)
- Hardware variations (ESP32 IoT, VR integration, etc.)
- Experimental validation data
- Educational curriculum development

## 📄 License

[To be determined - likely dual licensing: Educational/Non-commercial (open source) + Commercial (royalty-based)]

## ✉️ Contact

**Author**: Dominic Thibodeau (StrategicKhaos)  
**Repository**: Sovereignty-Architecture-Elevator-Pitch-  
**Date**: 2026-01-25

---

**"Ancient materials become computable. Computable materials become provable. Potentiometer → TRIG6 → Proof."**
