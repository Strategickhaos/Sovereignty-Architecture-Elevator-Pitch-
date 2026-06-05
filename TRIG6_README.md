# TRIG6 - Trigonometric Intermediate Representation (6-function)

A physics compiler with regulatory citations. It boots, it compiles, it returns deterministic output.

**Owner:** Strategickhaos DAO LLC  
**Author:** Domenic G. Garza  
**License:** Proprietary - All Rights Reserved

## Overview

TRIG6 is a command-line physics calculator that provides:
- Core trigonometric functions (all 6: sin, cos, tan, csc, sec, cot)
- Physics models for rigging, climbing, and rope rescue calculations
- Constants registry with full regulatory citations and provenance tracking
- Deterministic, zero-dependency calculations (pure Python math)

## Installation

The script requires Python 3.6+ with no external dependencies.

```bash
chmod +x trig6
./trig6 doctor  # Run self-tests
```

## Quick Start

```bash
# Run self-tests
./trig6 doctor

# Calculate all 6 trig functions for an angle
./trig6 vector --theta 45

# Calculate two-leg bridle tension
./trig6 bridle --load 300 --theta 120

# Look up a constant with citations
./trig6 cite rope.knot.figure_8_on_bight

# Get JSON output
./trig6 --json vector --theta 30
```

## Commands

### Core Math
- `vector --theta <degrees>` - Compute all 6 trig functions for an angle

### Physics Models
- `bridle --load <lbs> --theta <deg>` - Two-leg bridle leg tension
- `highline --load <lbs> --sag <deg>` - Symmetric highline tension
- `impact --weight <lbs> --ff <factor>` - Impact force estimate
- `amplify --force <lbs> --theta <deg>` - Force amplification by angle
- `ma --load <lbs> --ma <ratio>` - Mechanical advantage pull force
- `multileg --load <lbs> --n <count> --theta <deg>` - Multi-leg equal share

### Constants & Citations
- `constant <key>` - Look up a constant value (JSON output)
- `cite <key>` - Get full citation with sources
- `list [--prefix <text>]` - List all available constants

### Utilities
- `doctor` - Run all self-tests
- `--json` - Force JSON output for any command
- `--pack <name>` - Use a different constants pack (default: "default")

## Examples

### Vector Calculation
```bash
$ ./trig6 vector --theta 45
model: trig6_vector
theta_deg: 45.0
sin: 0.7071067811865475
cos: 0.7071067811865476
tan: 0.9999999999999999
csc: 1.4142135623730951
sec: 1.414213562373095
cot: 1.0000000000000002
```

### Bridle Tension
```bash
$ ./trig6 bridle --load 300 --theta 120
model: bridle_two_leg_equal_angle
load: 300.0
included_angle_deg: 120.0
leg_tension: 299.99999999999994
citation: ITI Rigging Engineering Basics, Sling Angle Chart
```

### Constant Lookup with Citation
```bash
$ ./trig6 cite rope.knot.figure_8_on_bight
KEY: rope.knot.figure_8_on_bight
VALUE: 0.75 efficiency_ratio
CONTEXT: Figure-8 on a bight knot strength efficiency relative to unknotted rope
CONFIDENCE: high

SOURCES:
  - On Rope: North American Vertical Rope Techniques - National Speleological Society (2nd Edition) @ Chapter 3: Knots
  - Knots for Climbers - Falcon Guides (2nd Edition) @ pp. 45-48

ENTERED BY: Domenic G. Garza
```

## Constants System

TRIG6 uses a modular constants system:

- **Packs**: Top-level collections of domain-specific constants
- **Domains**: Thematic groupings (e.g., rope, carabiners, regulations)
- **Constants**: Individual values with full provenance tracking

Each constant includes:
- Key (hierarchical dot notation)
- Value and units
- Context description
- Confidence level
- Multiple source citations
- Entry metadata

### Available Constants

Current default pack includes rope domain:
- `rope.knot.figure_8_on_bight` - Figure-8 knot efficiency (0.75)
- `rope.knot.bowline` - Bowline knot efficiency (0.70)
- `rope.knot.double_fisherman` - Double fisherman's efficiency (0.65)
- `rope.safety_factor.working` - OSHA/ASME working safety factor (5.0)
- `rope.breaking_strength.static_11mm` - Typical 11mm static rope (28 kN)

## Physics Models

### Bridle Leg Tension
Two-leg bridle with equal legs and symmetric angle.
```
T = W / (2 * cos(θ/2))
```
Where θ is the included angle between legs.

### Highline Tension
Center-loaded symmetric highline.
```
T = W / (2 * sin(θ))
```
Where θ is the sag angle from horizontal.

### Impact Force
Field estimate for dynamic rope systems.
```
F = W * (1 + sqrt(2 * FF))
```
Where FF is the fall factor (fall distance / rope length).

### Angle Amplification
Force amplification due to angle from vertical.
```
F_amplified = F / cos(θ)
```

### Mechanical Advantage
Ideal mechanical advantage (no friction).
```
Pull = Load / MA
```

### Multi-leg Equal Share
Multiple legs with equal load sharing and identical angles.
```
T_per_leg = (Load / n) / cos(θ)
```
Where n is number of legs, θ is angle from vertical.

## Assumptions

All models include explicit assumptions in their output:
- Static loads (not dynamic)
- No friction (ideal systems)
- Symmetric configurations
- Equal load sharing

Always verify assumptions match your use case.

## Self-Tests

The `doctor` command runs comprehensive self-tests:
- Trigonometric identities (sin²+cos²=1)
- Specific angle verification
- Physics model validation
- Constants system integrity

All tests must pass for reliable operation.

## Safety Notice

⚠️ **CRITICAL SAFETY INFORMATION**

This tool is for **educational and planning purposes only**. 

- Always consult qualified professionals for real-world applications
- Verify all calculations independently
- Follow applicable regulations and standards (OSHA, ASME, NFPA, etc.)
- Use appropriate safety factors for your application
- Real-world conditions may differ from model assumptions

**Human life is at stake. Double-check everything.**

## Architecture

TRIG6 follows these principles:
1. **Zero dependencies** - Pure Python 3 standard library only
2. **Deterministic output** - Same inputs always produce same outputs
3. **Citability** - Full provenance for every constant
4. **Transparency** - All assumptions stated explicitly
5. **Verifiability** - Self-tests validate core functionality

## License

Proprietary - All Rights Reserved  
© 2026 Strategickhaos DAO LLC

## Contact

For licensing inquiries: Strategickhaos DAO LLC
