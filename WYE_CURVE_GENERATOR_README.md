# Wye Curve Template Generator

A precision tool for generating branch-end cutting templates for true wye pipe intersections.

## Overview

This generator produces accurate miter line templates for cutting branch pipes in wye configurations. It uses the corrected formula for equal-diameter true wye intersections:

**h(φ) = r·tan(α/2)·cos(φ)**

Where:
- **r** = pipe radius (D/2)
- **α** = wye angle (e.g., 30° for a 30° wye)
- **φ** = angular position around the circumference

## Features

- ✅ **Mathematically correct** amplitude formula
- ✅ **Digitized point data** for any diameter and angle
- ✅ **Smooth SVG curves** using Catmull-Rom to cubic Bézier conversion
- ✅ **Laser/CNC ready** output format
- ✅ **Scalable** to any pipe size and wye angle

## Installation

No installation required! Just ensure Python 3.6+ is installed.

```bash
# Make the script executable
chmod +x wye_curve_generator.py
```

## Usage

### Basic Example

Generate a 30° wye curve for 10" diameter pipe with 12 points:

```bash
python3 wye_curve_generator.py --diameter 10 --angle 30 --points 12
```

### Command-Line Options

```
-d, --diameter  Pipe diameter in inches (required)
-a, --angle     Wye angle in degrees (required)
-n, --points    Number of points around circumference (default: 12)
-o, --output    Output SVG filename (default: wye_<D>in_<angle>deg.svg)
--no-table      Suppress point table output
```

### Examples

```bash
# 30° wye for 10" pipe (standard example)
python3 wye_curve_generator.py -d 10 -a 30 -n 12 -o PCS-1_30deg_wye_curve.svg

# 45° wye for 6" pipe with 16 points
python3 wye_curve_generator.py -d 6 -a 45 -n 16

# Quick generation without point table
python3 wye_curve_generator.py -d 8 -a 30 -n 12 --no-table
```

## Output

The generator produces:

1. **Point table** - Digitized x, h coordinates
2. **SVG file** - Ready for laser cutting or CNC machining
3. **Scaling rules** - Mathematical formulas for reference

### Example Output for D=10", α=30°, N=12

```
Digitized Point Data:
n    x (in)    h (in)
0    0.000     1.340
1    2.618     1.160
2    5.236     0.670
3    7.854     0.000
4    10.472   -0.670
5    13.090   -1.160
6    15.708   -1.340
7    18.326   -1.160
8    20.944   -0.670
9    23.562    0.000
10   26.180    0.670
11   28.798    1.160
12   31.416    1.340

Peak amplitude: ±1.339746 inches
```

## Theory

### The Corrected Formula

For an equal-diameter true wye intersection at angle α, the height of the miter line at angular position φ is:

**h(φ) = r·tan(α/2)·cos(φ)**

For D=10", α=30°:
- r = 5 inches
- tan(15°) = 0.267949
- **A = 5 × 0.267949 = 1.339746 inches** ✅

This gives the correct peak height of ±1.339746" (not ±1.443").

### Scaling Rules

For any pipe diameter D and wye angle α:

1. **Radius**: r = D/2
2. **Unwrap length**: L = π·D
3. **Step** (for N points): Δx = π·D/N
4. **Amplitude**: A = r·tan(α/2)
5. **Height** at point n: h(φₙ) = A·cos(2π·n/N)
6. **SVG Y-shift**: +A (to make Y non-negative)

## Template Type

**This template is for the branch end (wrap around branch).**

Use this to mark the cut line around the circumference of the branch pipe. When wrapped around the branch, it will create the saddle curve needed for a perfect wye intersection.

### Not included in this tool:
- Main pipe opening template (fishmouth on the main) - requires different parameterization

## Use Cases

- HVAC ductwork fabrication
- Industrial piping systems
- Custom exhaust manifolds
- Precision metalworking
- Educational demonstrations of pipe geometry

## Technical Notes

- The SVG uses Catmull-Rom spline interpolation converted to cubic Bézier curves for smooth, continuous curves
- Y coordinates are shifted upward by amplitude A so the curve lives in [0, 2A] for easy cutting/printing
- Stroke width is set to 0.03 for precision cutting
- Output dimensions are in inches

## Verification

The output has been verified against the theoretical formula:

✅ D=10", α=30° gives peak amplitude = 1.339746" (matches theory)
✅ Unwrap length = πD = 31.415927" (matches circumference)
✅ Point spacing = L/N = 2.618" for N=12 (matches equal spacing)

## Future Enhancements

Potential additions:
- Main pipe opening (fishmouth) template generator
- DXF output format
- Grid lines and alignment marks
- Multiple branch angles in one file
- Unequal diameter branches

## License

Part of the Sovereignty Architecture project. See repository LICENSE file.

## Author

Generated as part of the Strategic Khaos DAO engineering toolkit.

---

**⚓ Helm locked. Ready for fabrication.**
