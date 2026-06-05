# TRIG6 - Trigonometric Intermediate Representation

A physics compiler with regulatory citations for rope rescue and rigging applications.

## Overview

TRIG6 is a command-line tool that provides deterministic physics calculations with full regulatory citations. It's designed for rope rescue, rigging, and climbing professionals who need accurate calculations backed by industry standards (NFPA, UIAA, etc.).

## Installation

No installation required - just ensure Python 3 is available:

```bash
chmod +x trig6
./trig6 doctor  # Run self-tests
```

## Usage

### Basic Commands

```bash
# Run self-tests
./trig6 doctor

# Calculate all 6 trigonometric functions
./trig6 vector --theta 45

# Calculate bridle leg tension
./trig6 bridle --load 300 --theta 120

# Calculate highline tension
./trig6 highline --load 200 --sag 30

# Estimate impact force
./trig6 impact --weight 180 --ff 1.5

# Calculate angle amplification
./trig6 amplify --force 100 --theta 30

# Calculate mechanical advantage
./trig6 ma --load 300 --ma 3

# Calculate multi-leg tension
./trig6 multileg --load 600 --n 3 --theta 15
```

### Constants and Citations

```bash
# Look up a constant
./trig6 constant rope.knot.figure_8_on_bight

# Get full citation
./trig6 cite rope.knot.figure_8_on_bight

# List all constants
./trig6 list

# List constants by prefix
./trig6 list --prefix rope.knot
```

### Model Documentation

```bash
# List all computational models
./trig6 models

# Get detailed explanation of a model
./trig6 explain bridle_two_leg_equal_angle
```

### JSON Output

Add `--json` flag before the command for JSON output:

```bash
./trig6 --json doctor
./trig6 --json vector --theta 45
```

## Features

### Computational Models

1. **trig6_vector** - All six trigonometric functions
2. **bridle_two_leg_equal_angle** - Two-leg bridle tension
3. **highline_center_symmetric** - Symmetric highline tension
4. **impact_field_estimate** - Impact force estimation
5. **angle_amplification_sec** - Force amplification by angle
6. **mechanical_advantage_ideal** - Ideal mechanical advantage
7. **multi_leg_equal_share_equal_angle** - Multi-leg anchor tension

### Constants Registry

The system includes a comprehensive constants registry with:
- Knot efficiency factors (figure 8, bowline, etc.)
- Rope properties (dynamic/static elongation)
- Safety factors (NFPA 15:1)
- Equipment strength ratings (carabiners, etc.)

All constants include full regulatory citations from:
- NFPA 1983 (Standard on Life Safety Rope)
- UIAA standards (Mountaineering equipment)
- Industry references (CMC, On Rope, etc.)

### Safety Features

- Input validation (prevents division by zero, negative values)
- Warning messages for dangerous configurations
- Regulatory citation tracking
- Deterministic output for auditing

## Architecture

```
trig6                      # Main executable
├── core/
│   ├── __init__.py
│   └── model_registry.py  # Model documentation system
└── packs/
    ├── default_pack.json  # Pack configuration
    └── rope.json          # Rope/rigging constants with citations
```

## Examples

### Safe vs Dangerous Angles

```bash
# Safe bridle angle
./trig6 bridle --load 300 --theta 90
# leg_tension: 212.13 lbf

# Dangerous bridle angle (>120°)
./trig6 bridle --load 300 --theta 150
# leg_tension: 600 lbf
# warning: DANGER: Angle > 120° means leg tension exceeds load
```

### Impact Force Calculation

```bash
./trig6 impact --weight 180 --ff 1.5
# impact_force: 491.77 lbf
# warning: This is a field estimate. Use manufacturer data for critical applications.
```

### Constants with Citations

```bash
./trig6 cite rope.knot.figure_8_on_bight

# Output:
# KEY: rope.knot.figure_8_on_bight
# VALUE: 0.75 dimensionless (strength retention)
# CONTEXT: Figure 8 on a bight knot retains approximately 75% of rope strength
# CONFIDENCE: high
#
# SOURCES:
#   - NFPA 1983: Standard on Life Safety Rope - National Fire Protection Association (2017 Edition) @ Section 4.3
#   - On Rope: North American Vertical Rope Techniques - National Speleological Society (2nd Edition) @ Chapter 3
#
# ENTERED BY: Domenic G. Garza
```

## Testing

Run the self-test suite:

```bash
./trig6 doctor
```

This verifies:
- Mathematical correctness (sin²+cos²=1, etc.)
- Physics model accuracy
- Constants pack loading
- Data integrity

## License

Proprietary - All Rights Reserved  
Owner: Strategickhaos DAO LLC  
Author: Domenic G. Garza

## Safety Notice

⚠️ **IMPORTANT**: This tool provides field estimates and calculations based on industry standards. Always:
- Verify calculations independently
- Use manufacturer-specific data when available
- Follow applicable regulations and standards
- Seek professional training before working at height
- Never rely solely on software for life-safety decisions

TRIG6 is a computational tool - not a substitute for proper training, equipment, or professional judgment.
