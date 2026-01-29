# TRIG6 Pipe Template Generator

## Overview

The TRIG6 Pipe Template Generator is a Python tool that generates saddle curves for pipe wye/tee fabrication using trigonometric projection mathematics.

**Entity:** Strategickhaos DAO LLC  
**Invention:** TRIG6 Projection Curve System  
**Patent:** Pending assignment (Physical Tool category)

## What is a Saddle Curve?

A saddle curve is the intersection of two cylinders at an angle. In pipe fabrication, this represents the cut line needed when joining two pipes at a branch angle (wye or tee connection).

The mathematical formula for a true wye with equal-diameter pipes:

```
h(θ) = (D/2) × tan(α) × cos(θ)
```

Where:
- `D` = pipe diameter
- `α` = branch angle
- `θ` = position around circumference (0 to 2π)

## Installation

No external dependencies are required. The script uses only Python standard library modules:
- `math`
- `argparse`
- `dataclasses`
- `typing`

Simply ensure you have Python 3.7+ installed:

```bash
python3 --version
```

## Usage

### Basic Usage

Generate a 30° wye template for a 10-inch diameter pipe:

```bash
python3 trig6_pipe_template.py --diameter 10 --angle 30
```

This creates an SVG file: `wye_30deg_d10.svg`

### Custom Output File

```bash
python3 trig6_pipe_template.py --diameter 10 --angle 30 --output my_template.svg
```

### With Data Table

Display the calculated points in an ASCII table:

```bash
python3 trig6_pipe_template.py --diameter 6 --angle 45 --table
```

Output:
```
┌─────────┬───────────┬────────────┬────────────┐
│ Segment │  θ (deg)  │  X (in)    │  Y (in)    │
├─────────┼───────────┼────────────┼────────────┤
│       0 │      0.00 │      0.000 │     +3.000 │
│       1 │     45.00 │      2.356 │     +2.121 │
│       2 │     90.00 │      4.712 │     +0.000 │
...
```

### With TRIG6 Analysis

Show complete trigonometric analysis of the branch angle:

```bash
python3 trig6_pipe_template.py --diameter 10 --angle 45 --analyze
```

Output includes:
- All six trigonometric functions (sin, cos, tan, csc, sec, cot)
- Quadrant information
- Amplitude factor

### Advanced Options

Control the precision of the curve with more segments:

```bash
python3 trig6_pipe_template.py --diameter 8 --angle 60 --segments 24
```

More segments = smoother curve (default: 12)

## Command-Line Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--diameter` | `-d` | float | 10.0 | Pipe diameter in inches |
| `--angle` | `-a` | float | 30.0 | Branch angle in degrees (0-90) |
| `--segments` | `-s` | int | 12 | Number of segments for curve |
| `--output` | `-o` | string | auto | Output SVG file path |
| `--table` | | flag | false | Print point table to stdout |
| `--analyze` | | flag | false | Show TRIG6 analysis |

## Input Validation

The script validates all inputs:

- **Diameter:** Must be positive (> 0)
- **Angle:** Must be between 0 and 90 degrees
- **Segments:** Must be positive (> 0)

Invalid inputs will display an error message and exit.

## Output Format

### SVG Template

The generated SVG includes:
- **Saddle curve path** (purple line)
- **Centerline reference** (dashed gray line)
- **Projection points** (purple dots)
- **Scale bar** (10-inch reference)
- **Title and metadata** (pipe diameter, angle, TRIG6-PCS designation)

The SVG is sized in inches for easy printing at 1:1 scale.

### File Naming Convention

When no output file is specified, the script auto-generates a filename:

```
wye_{angle}deg_d{diameter}.svg
```

Examples:
- `wye_30deg_d10.svg` - 30° angle, 10" diameter
- `wye_45deg_d6.svg` - 45° angle, 6" diameter

## Examples

### Example 1: Standard 45° Wye

```bash
python3 trig6_pipe_template.py --diameter 10 --angle 45
```

Creates a template for a 45-degree wye branch on 10-inch pipe.

### Example 2: Tight 30° Branch with High Precision

```bash
python3 trig6_pipe_template.py --diameter 8 --angle 30 --segments 24 --output tight_branch.svg
```

Creates a highly detailed template with 24 segments.

### Example 3: Analysis Mode

```bash
python3 trig6_pipe_template.py --diameter 6 --angle 60 --table --analyze
```

Shows both the point table and trigonometric analysis without saving a file.

## TRIG6 Vector System

The TRIG6 system computes all six trigonometric functions simultaneously:

1. **sin(θ)** - Sine
2. **cos(θ)** - Cosine
3. **tan(θ)** - Tangent
4. **csc(θ)** - Cosecant (1/sin)
5. **sec(θ)** - Secant (1/cos)
6. **cot(θ)** - Cotangent (1/tan)

This complete trigonometric state enables precise geometric calculations for pipe fabrication.

## Practical Applications

### Pipe Fabrication

1. Generate the SVG template
2. Print at 1:1 scale (check scale bar = 10 inches)
3. Cut out the template
4. Wrap around pipe and mark the cut line
5. Cut along the saddle curve
6. Join to branch pipe at specified angle

### Quality Control

- The template includes measurement references
- Scale bar ensures proper printing
- Segment markers allow verification of curve accuracy

### Engineering Analysis

- Use `--table` to get precise coordinates
- Use `--analyze` to verify trigonometric calculations
- Adjustable segments allow testing different tolerances

## Technical Details

### Coordinate System

- **X-axis:** Linear unwrap of pipe circumference (0 to πD)
- **Y-axis:** Height offset from centerline (±amplitude)
- **Origin:** Start of unwrapped circumference at maximum height

### Mathematical Properties

- **Amplitude:** `(D/2) × tan(α)` - Maximum height deviation
- **Circumference:** `π × D` - Total unwrapped length
- **Period:** 2π - Full rotation around pipe
- **Symmetry:** Mirror symmetry at 180°

### Edge Cases

The script handles edge cases safely:
- Division by zero in reciprocal functions → infinity
- 90° angle → infinite amplitude (validation prevents this)
- 0° angle → zero amplitude (validation prevents this)

## Error Handling

The script provides clear error messages:

```bash
# Invalid diameter
$ python3 trig6_pipe_template.py --diameter -5 --angle 30
trig6_pipe_template.py: error: Diameter must be positive

# Invalid angle
$ python3 trig6_pipe_template.py --diameter 10 --angle 95
trig6_pipe_template.py: error: Branch angle must be between 0 and 90 degrees

# File permission error
$ python3 trig6_pipe_template.py --diameter 10 --angle 30 --output /root/test.svg
❌ Error saving SVG: [Errno 13] Permission denied: '/root/test.svg'
```

## Contributing

This tool is part of the Strategickhaos DAO LLC sovereignty architecture. For questions, improvements, or bug reports, please contact the development team.

## License

See the repository LICENSE file for terms and conditions.

## Version History

- **v1.0** (2025-01-29): Initial release
  - TRIG6 vector system
  - Saddle curve generation
  - SVG template output
  - Input validation and error handling
  - ASCII table output
  - Trigonometric analysis mode
