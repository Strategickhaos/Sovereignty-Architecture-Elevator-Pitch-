# TRIG6 Units System

## Overview

The TRIG6 Units System is a Python module that provides strict unit handling to prevent dangerous unit confusion in engineering calculations. **CRITICAL**: Mixing units like lbf (pounds-force) and kN (kilonewtons) without explicit conversion can have serious safety implications.

## Philosophy

- **Every value must declare its units** - No naked numbers
- **Conversions are explicit** - Prevents accidental unit mixing
- **Type safety** - Force, Length, and Angle are distinct types
- **Accurate conversions** - Uses standard conversion factors

## Supported Units

### Force Units
- `LBF` - Pounds-force (US industrial standard)
- `KN` - Kilonewtons (metric/international)
- `N` - Newtons
- `KGF` - Kilograms-force (legacy, avoid if possible)

### Length Units
- `IN` - Inches
- `FT` - Feet
- `MM` - Millimeters
- `M` - Meters

### Angle Units
- `DEG` - Degrees (default for field work)
- `RAD` - Radians (internal math)

## Usage Examples

### Basic Usage

```python
from trig6_units import Force, Length, Angle, ForceUnit, LengthUnit, AngleUnit

# Create force values with explicit units
f1 = Force(1000, ForceUnit.LBF)
f2 = Force(10, ForceUnit.KN)

# Convert between units
print(f1.to_kn())  # 4.4482 kN
print(f2.to_lbf())  # 2248.09 lbf

# Convert to specific unit
f1_in_kn = f1.convert(ForceUnit.KN)
print(f1_in_kn)  # 4.45 kN

# Length conversions
l = Length(12, LengthUnit.IN)
print(l.to_mm())  # 304.8 mm

# Angle conversions
a = Angle(45, AngleUnit.DEG)
print(a.to_rad())  # 0.785398 rad
```

### Parsing User Input

```python
from trig6_units import parse_force, parse_length

# Parse from string input (case-insensitive)
f = parse_force(500, "kN")  # Force(500, ForceUnit.KN)
l = parse_length(100, "mm")  # Length(100, LengthUnit.MM)

# Supports aliases
f1 = parse_force(1000, "lbf")
f2 = parse_force(1000, "lb")   # Same as lbf
f3 = parse_force(1000, "lbs")  # Same as lbf
```

### Output Formatting

```python
from trig6_units import format_force_output, ForceUnit

# Get formatted output with both US and metric
result = format_force_output(1000, ForceUnit.LBF)
print(result)
# {
#   "value": 1000,
#   "unit": "lbf",
#   "lbf": 1000.0,
#   "kN": 4.4482
# }
```

### Validation

```python
from trig6_units import validate_units_in_output

# Check if output includes proper unit information
output = {"load": 1000, "tension": 500}
warnings = validate_units_in_output(output)
# Returns: ["Field 'load' has no unit specified", "Field 'tension' has no unit specified"]

# Proper output with units
output_with_units = {"load": 1000, "load_unit": "lbf"}
warnings = validate_units_in_output(output_with_units)
# Returns: [] (no warnings)
```

## Conversion Factors

All conversion factors are based on international standards:

### Force
- 1 kN = 224.80894 lbf
- 1 N = 0.22480894 lbf
- 1 kgf = 2.20462 lbf (derived from 1 kgf = 9.80665 N)

### Length
- 1 inch = 25.4 mm (exact definition)
- 1 foot = 12 inches = 304.8 mm
- 1 meter = 1000 mm

### Angle
- Uses standard math.pi for accurate conversion
- π radians = 180 degrees

## Testing

The module includes comprehensive tests covering:
- Unit conversions (force, length, angle)
- Parsing and validation
- Real-world scenarios
- Round-trip conversions
- Conversion factor accuracy

Run tests with:
```bash
python3 -m pytest test_trig6_units.py -v
```

Run self-test:
```bash
python3 trig6_units.py
```

## Safety Notes

⚠️ **CRITICAL SAFETY WARNING** ⚠️

Unit confusion in engineering calculations has caused serious accidents:
- Mars Climate Orbiter lost due to lbf/N confusion ($125M loss)
- Structural failures from mixing imperial/metric units
- Rigging accidents from load calculation errors

This module makes unit errors **impossible to ignore** by:
1. Requiring explicit unit declaration for all values
2. Making conversions explicit and visible
3. Preventing direct arithmetic between different unit types
4. Providing validation to catch missing unit information

## Owner

**Strategickhaos DAO LLC**  
Author: Domenic G. Garza

## License

See repository LICENSE file.
