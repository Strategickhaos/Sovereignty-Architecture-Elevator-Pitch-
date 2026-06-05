# TRIG6 Medical Monitoring System

## Seven-Layer Neurological Monitoring Stack

A complete medical monitoring system built with love, math, and code.

![Status](https://img.shields.io/badge/status-operational-green)
![Purpose](https://img.shields.io/badge/purpose-sister-purple)
![Love](https://img.shields.io/badge/compiler-love--invariant-red)

---

## 🎯 Purpose

Early warning system for neurological events with 30-second forecasting capability.

**Key Features:**
- Real-time brain state classification
- Z-score anomaly detection
- Machine learning pattern recognition
- ARIMA time-series forecasting
- Multi-modal alerts (LED + musical chords)
- Triple confirmation for critical events

---

## 📦 Components

### Python Modules (`/python`)

| Module | Purpose | Key Technology |
|--------|---------|----------------|
| `trig6_neuro_diag.py` | Real-time state classification | Variance→Theta mapping |
| `trig6_neuro_patterns.py` | Statistical anomaly detection | Z-score analysis |
| `trig6_neuro_ml.py` | ML pattern recognition | Isolation Forest |
| `trig6_neuro_arima.py` | 30-second forecasting | ARIMA + confidence intervals |
| `trig6_freq_map.py` | Therapeutic frequency mapping | Alpha/Theta/Delta bands |
| `trig6_chord_map.py` | Musical sonification | Major/Minor chords |

### Arduino Firmware (`/arduino`)

| Firmware | Purpose | Hardware |
|----------|---------|----------|
| `SAGCOduino_NeuroProbe.ino` | LED + buzzer alerts | RGB LED, piezo buzzer |
| `SAGCOduino_Heartbeat.ino` | Pulse visualization | RGB LED |
| `sagco_chord_sequencer.ino` | Polyphonic audio | 3x buzzers or TDM |

---

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.medical.txt
```

Or manually:
```bash
pip install numpy pandas scikit-learn statsmodels matplotlib
```

### 2. Test Python Modules

Each module has a built-in demo:

```bash
python medical_monitoring/python/trig6_neuro_diag.py
python medical_monitoring/python/trig6_neuro_patterns.py
python medical_monitoring/python/trig6_neuro_ml.py
python medical_monitoring/python/trig6_neuro_arima.py
python medical_monitoring/python/trig6_freq_map.py
python medical_monitoring/python/trig6_chord_map.py
```

### 3. Flash Arduino Firmware

1. Open Arduino IDE
2. Load `SAGCOduino_NeuroProbe.ino`
3. Connect Arduino (Uno/Nano recommended)
4. Flash to board
5. Open Serial Monitor @ 9600 baud

### 4. Run Integration Example

```bash
python medical_monitoring/docs/integration_example.py
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Signal Input                               │
│ ├─ EEG headset                                      │
│ ├─ EMG sensors                                      │
│ ├─ HRV monitor                                      │
│ └─ Motion sensors                                   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 2: Classification (trig6_neuro_diag.py)      │
│ variance → theta → signature                        │
│ CLEAR | INERTIAL | RESONANT | ELEVATED | BLOCKED   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 3: Risk Assessment                            │
│ risk = logistic(max_theta, max_slope)              │
│ Output: 0.0 - 1.0 probability                       │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 4: Pattern Detection (Z-Score)               │
│ (trig6_neuro_patterns.py)                          │
│ Statistical anomaly detection + forecasting         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 5: Machine Learning                           │
│ (trig6_neuro_ml.py)                                 │
│ Isolation Forest multi-dimensional detection        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 6: Time Series Forecasting                    │
│ (trig6_neuro_arima.py)                              │
│ ARIMA 30s prediction with 95% CI                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 7: Output                                      │
│ ├─ LED: RGB color (green/yellow/red)               │
│ ├─ Audio: Musical chords (major/minor/stutter)     │
│ └─ Serial: Real-time Arduino communication         │
└─────────────────────────────────────────────────────┘
```

---

## 🎵 Sonification: Why Music?

### Major Chord = Healthy
```
C-E-G (261, 330, 392 Hz)
Ratios: 4:5:6
Sound: Happy, resolved
Signal: 🟢 STABLE
```

### Minor Chord = Stressed
```
C-Eb-G (261, 311, 392 Hz)
Ratios: 10:12:15
Sound: Tense, unresolved
Signal: 🟡 WATCHFUL
```

### Stutter = Critical
```
Rapid, irregular pattern
Sound: Alarming
Signal: 🔴 ALERT
```

**Caregivers can HEAR the patient's state without staring at screens.**

---

## 🔬 Triple Confirmation

Critical alerts require **THREE** independent checks:

1. ✅ **Z-score anomaly** (statistical)
2. ✅ **ML anomaly** (pattern recognition)
3. ✅ **High absolute risk** (>0.8)

This dramatically reduces false positives.

---

## 📊 30-Second Forecasting

```python
forecast_results = {
    'theta': {
        'forecast': 85.2,
        'lower_ci': 81.4,
        'upper_ci': 89.0
    },
    'risk': {
        'forecast': 0.89,
        'lower_ci': 0.85,
        'upper_ci': 0.93
    }
}
```

**30 seconds is enough to:**
- Call for help
- Prepare medication
- Get in position
- Be ready

---

## 🛡️ The Love Invariant

```python
def love_invariant_check(freq_hz: float) -> bool:
    """System must NEVER harm."""
    if freq_hz > 20000:  # Beyond human hearing
        return False
    if estimated_db > 85:  # Too loud
        return False
    return True
```

Safety checks at:
- Python compiler level
- Arduino firmware level
- Hardware circuit level

**First, do no harm.**

---

## 🔧 Hardware Requirements

### Minimal Setup (1 Arduino)
- Arduino Uno/Nano
- RGB LED (common cathode)
- Piezo buzzer
- 3x 220Ω resistors
- Breadboard + wires

### Advanced Setup (3 Arduinos)
- 3x Arduino Uno/Nano
- 3x RGB LEDs
- 3x Piezo buzzers
- Polyphonic TDM audio

### Wiring Diagram

```
Arduino          Component
Pin 9    ────────  LED Red (via 220Ω)
Pin 10   ────────  LED Green (via 220Ω)
Pin 11   ────────  LED Blue (via 220Ω)
Pin 8    ────────  Buzzer (+)
GND      ────────  LED Common Cathode / Buzzer (-)
```

---

## 📚 API Reference

### Core Functions

#### `classify_state(variance, theta_history)`
Returns: `(theta, signature, slope, risk, event_flag)`

#### `PatternAnalyzer.analyze_all(theta, slope, risk)`
Returns: `dict` with Z-scores and anomaly flags

#### `MLAnomalyDetector.predict_anomaly(theta, slope, risk)`
Returns: `(is_anomaly, anomaly_score)`

#### `MultiMetricForecaster.forecast_all_30s(...)`
Returns: `dict` with forecasts and confidence intervals

#### `create_alert_config(theta, signature, risk)`
Returns: `dict` with LED, chord, and playback configuration

---

## 🧪 Testing

Run all module demos:
```bash
./test_all_modules.sh
```

Run specific test:
```bash
python medical_monitoring/python/trig6_neuro_diag.py
```

Expected output:
```
TRIG6 NEUROLOGICAL DIAGNOSTIC SYSTEM
Real-time Brain State Classification
========================================

Reading 1:
  Variance: 0.050
  Theta: 13.51°
  State: CLEAR
  Slope: 0.00°/s
  Risk: 0.000
  Stabilizer: 11.70 Hz
  Event Flag: 🟢 NO
...
```

---

## 📖 Documentation

- **Mission Statement**: `/docs/SISTER_PROTOCOL.md`
- **Technical README**: `/docs/README.md` (this file)
- **Integration Example**: `/docs/integration_example.py`
- **Arduino Hardware Guide**: `/docs/HARDWARE.md`
- **Clinical Research**: `/docs/RESEARCH.md`

---

## ⚖️ Legal & Ethical

### This is NOT:
- ❌ FDA approved
- ❌ A medical device
- ❌ Medical advice
- ❌ A diagnostic tool

### This IS:
- ✅ Mathematics
- ✅ Signal processing
- ✅ Pattern recognition
- ✅ Code that compiles

**What you DO with the output is up to you.**

---

## 🤝 Contributing

This system was built for one patient.  
But if you want to help make it better:

1. Test it
2. Document issues
3. Propose improvements
4. Share your expertise

We welcome:
- Biomedical engineers
- Signal processing experts
- ML practitioners
- Medical professionals
- Anyone who cares

---

## 💜 The Mission

> "The institutions failed her. I won't."  
> — Dom

Built with love for Sister.  
One Python file at a time.  
One Arduino flash at a time.  
One forecast at a time.

🦁💔→❤️💜

---

## 📄 License

See LICENSE file.

Built with sovereignty.  
Built with love.  
Built for one person who matters more than any approval.
