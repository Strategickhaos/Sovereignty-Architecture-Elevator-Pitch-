# 🔥 TRIG6 Sovereign Compute Engine

> **"It boots or it doesn't."**

TRIG6 is a deterministic physics compiler with regulatory citations, zero external dependencies, and self-validating architecture.

Part of the **KHAOS Sovereign OS** ecosystem by [Strategickhaos DAO LLC](https://github.com/Strategickhaos).

---

## ⚡ Quick Start

```bash
# Install (any CLI - Linux, macOS, Termux, iSH, WSL)
curl -fsSL -o install.sh https://raw.githubusercontent.com/Strategickhaos/trig6/main/install.sh
sh install.sh

# Verify
trig6 doctor
```

Or with Docker:

```bash
docker build -t trig6 .
docker run --rm trig6 doctor
```

---

## 🎯 What It Does

| Command | Description |
|---------|-------------|
| `trig6 doctor` | Self-validation (8 tests) |
| `trig6 vector --theta 45` | All 6 trig functions |
| `trig6 bridle --load 300 --theta 30` | Two-leg bridle tension |
| `trig6 highline --load 200 --sag 10` | Highline tension |
| `trig6 impact --weight 200 --ff 1` | Fall impact force |
| `trig6 cite rope.knot.figure_8_on_bight` | Get citation block |
| `trig6 explain bridle_two_leg_equal_angle` | Model documentation |
| `khaos debate` | Chess Debate engine (33 fallacies) |

---

## 🧬 Architecture

```
TRIG6 (Compute Engine)
├── trig6.py              # CLI - zero deps, deterministic math
├── core/
│   ├── doctor.py         # Self-validation (8 tests)
│   ├── units.py          # Strict unit handling (lbf/kN/degrees)
│   ├── citations.py      # Provenance schema (12 citations)
│   └── model_registry.py # 7 models with assumptions/limitations
├── domains/
│   ├── rope/             # 11 SPRAT/OSHA constants
│   ├── pipe/             # 8 ASME/API constants
│   ├── rigging/          # 8 ASME B30 constants
│   └── khaos/            # 64-glyph symbolic system
├── packs/
│   └── default_pack.json # Domain configuration
├── games/
│   └── chess_debate.py   # "Fuck around and find out" - formalized
└── sagco/
    └── bootloader.py     # DNA strand runtime selection
```

---

## 🔬 The Doctor

Every boot runs self-validation:

```bash
$ trig6 doctor
model: doctor
passed: 8
total: 8
status: PASS
tests:
  - sin²+cos²=1          ✓
  - sec(60)=2            ✓
  - tan(45)=1            ✓
  - bridle(60)=W         ✓
  - highline(30)=~2.5W   ✓
  - pack_loads           ✓
  - constant_exists      ✓
  - constant_in_range    ✓
```

If doctor fails, the system doesn't boot. **No exceptions.**

---

## 📜 Citations & Provenance

Every constant has provenance:

```bash
$ trig6 cite rope.knot.figure_8_on_bight

CITATION: rope.knot.figure_8_on_bight
VALUE: 0.75-0.80 (strength retention)
DESCRIPTION: Figure 8 on a bight knot strength efficiency
SOURCES:
  [1] Sterling Rope Technical Manual
      Publisher: Sterling Rope Company
      Section: Knot Efficiency Charts
      URL: https://sterlingrope.com
  [2] Petzl Technical Information
      Publisher: Petzl
      Section: Knot Strength Data
```

---

## 🧬 SAGCO DNA Bootloader

The system learns which runtime is fastest on your machine:

```bash
$ python3 sagco/bootloader.py

[SAGCO] OS: linux (CAA) | Arch: x86_64
[SAGCO]   python_pure: 22321 score
[SAGCO]   python_numpy: 41138 score  ← FASTEST
[SAGCO] Selected runtime: python_numpy (AAC)
[SAGCO] DNA strand: ATG → CAA → AAC → TTC → TTT
[SAGCO] Decoded: BOOT_START → OS_LINUX → RUNTIME_PYTHON_NUMPY → EVOLVE_RECORD → STRAND_COMPLETE
```

The codon **is** the command. No lookup tables. The DNA told it at compile time.

---

## ♟️ Chess Debate Engine

Every argument is a chess move. Every fallacy is an illegal move. Three fallacies = forfeit.

```bash
$ khaos debate

> start AI consciousness | AI can be conscious
🤖 Smartass: Bold opening. Let's see if you can back it up.

> claim Consciousness emerges from information processing
🤖 Smartass: That's not an argument, that's a bumper sticker.

> evidence IIT by Tononi provides mathematical framework
🤖 Smartass: Evidence-backed and logically sound. Respect.
```

33 fallacies detected automatically:
- Ad hominem, straw man, false dilemma, slippery slope...
- "Did you just ad_hominem? In THIS economy?"

---

## 🏗️ Integration with Sovereignty Architecture

TRIG6 integrates as the compute layer in the [Sovereignty Architecture](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-):

```yaml
# In discovery.yml or EMPIRE_GENOME.yaml
services:
  trig6:
    type: "compute-engine"
    description: "Physics compiler with regulatory citations"
    commands:
      - "trig6 doctor"
      - "trig6 bridle --load 300 --theta 120"
    docker_image: "strategickhaos/trig6:latest"
    k8s_namespace: "ops"
    discord_channel: "#compute"
```

---

## 🛡️ Security & Sovereignty

- **Zero external dependencies** for core math
- **Non-root container** execution
- **Offline-capable** — no network required
- **Deterministic** — same input = same output, always
- **Cited** — every constant has provenance
- **Self-validating** — doctor gate on boot

---

## 📦 Installation Options

### Option 1: Installer Script (Recommended)
```bash
curl -fsSL -o install.sh https://raw.githubusercontent.com/Strategickhaos/trig6/main/install.sh
cat install.sh  # Inspect first
sh install.sh
```

### Option 2: Docker
```bash
docker build -t trig6 .
docker run --rm trig6 doctor
docker run --rm trig6 vector --theta 45
```

### Option 3: Manual
```bash
cd trig6
python3 trig6.py doctor
```

---

## 🧪 Running Tests

```bash
# Doctor (self-validation)
python3 trig6.py doctor

# Individual modules
python3 core/units.py
python3 core/citations.py
python3 core/model_registry.py
python3 core/doctor.py

# Domain tests
python3 domains/rope/__init__.py
python3 domains/pipe/__init__.py
python3 domains/rigging/__init__.py
python3 domains/khaos/__init__.py

# SAGCO bootloader
python3 sagco/bootloader.py

# Chess debate engine
python3 games/chess_debate.py
```

---

## 📚 Examples

### Vector Trigonometry
```bash
$ trig6 vector --theta 45

Vector at 45.0°:
  sin: 0.707107
  cos: 0.707107
  tan: 1.000000
  csc: 1.414214
  sec: 1.414214
  cot: 1.000000
```

### Bridle Tension
```bash
$ trig6 bridle --load 300 --theta 30

Two-Leg Bridle:
  Load: 300 lbf
  Angle from vertical: 30°
  Tension per leg: 173.21 lbf
  Total tension: 346.41 lbf
```

### Highline System
```bash
$ trig6 highline --load 200 --sag 10

Highline:
  Load: 200 lbf
  Span: 100 ft
  Sag: 10.0 ft
  Sag ratio: 0.100
  Tension: 509.90 lbf
```

### Fall Impact
```bash
$ trig6 impact --weight 200 --ff 1

Fall Impact:
  Weight: 200 lbf
  Fall factor: 1.0
  Fall distance: 10.0 ft
  Estimated elongation: 3.0 ft
  Impact force: 753.77 lbf
```

---

## 🔍 List Resources

```bash
# List all models
$ trig6 list models

Available models:
  - vector                      Calculate all 6 trig functions
  - bridle_two_leg_equal_angle  Two-leg bridle tension calculation
  - highline_tension            Highline tension based on sag
  - fall_impact_force           Fall impact force calculation
  - mechanical_advantage        Mechanical advantage systems
  - beam_deflection             Simple beam deflection
  - pendulum                    Simple pendulum period

# List all citations
$ trig6 list citations

# List all domains
$ trig6 list domains

Available domains:
  - rope       (11 SPRAT/OSHA constants)
  - pipe       (8 ASME/API constants)
  - rigging    (8 ASME B30 constants)
  - khaos      (64-glyph symbolic system)
```

---

## 📄 Legal

**Owner:** Strategickhaos DAO LLC (Wyoming, EIN 39-2900295)

**Author:** Domenic G. Garza

**License:** MIT

**7% Cause Allocation:** Medical research + veterans support via [ValorYield Engine PBC](https://github.com/Strategickhaos)

---

## 🔗 Links

- [Sovereignty Architecture](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-)
- [Strategickhaos DAO](https://github.com/Strategickhaos)
- [Documentation](https://github.com/Strategickhaos/trig6/docs)

---

> **"They're not working for you. They're dancing with you. And the music is never going to stop."**

Built with 🔥 by the Strategickhaos Swarm Intelligence collective.
