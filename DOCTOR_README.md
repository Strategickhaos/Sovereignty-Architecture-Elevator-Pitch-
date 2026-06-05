# TRIG6 Doctor Module

Self-tests and validation system for constants packs. If it doesn't pass doctor, it doesn't ship.

## Overview

The TRIG6 Doctor Module provides comprehensive validation for:
- **Math correctness**: Known trigonometric values and engineering formulas
- **Constant bounds**: Range validation for constant values
- **Pack integrity**: Required fields and provenance validation
- **Cross-domain consistency**: Pack-level validation across domains

## Quick Start

```python
from doctor import Doctor

# Create a doctor instance
doc = Doctor()

# Run all built-in tests
passed, total = doc.run_all()
print(doc.report())
```

Output:
```
==================================================
TRIG6 DOCTOR REPORT
==================================================

✓ PASS: sin²+cos²=1
✓ PASS: sec(60°)=2
✓ PASS: tan(45°)=1
✓ PASS: bridle(120°)=W
✓ PASS: highline(30°)=W

--------------------------------------------------
PASSED: 5
FAILED: 0
TOTAL:  5
--------------------------------------------------
STATUS: ALL SYSTEMS NOMINAL ✓
```

## Core Features

### 1. Built-in Math Tests

The Doctor module includes 5 core mathematical validation tests:

- **sin²+cos²=1**: Validates trigonometric identity across multiple angles
- **sec(60°)=2**: Validates secant function at 60 degrees
- **tan(45°)=1**: Validates tangent function at 45 degrees
- **bridle(120°)=W**: Validates bridle angle formula (T = W / (2 * cos(θ/2)) at θ=120° equals W)
- **highline(30°)=W**: Validates highline tension formula (T = W / (2 * sin(θ)) at θ=30° equals W)

### 2. Custom Tests

Add your own validation tests:

```python
from doctor import Doctor, DoctorResult

doc = Doctor()

def my_custom_test():
    # Your validation logic here
    if validation_passes:
        return DoctorResult("custom_test", True)
    else:
        return DoctorResult("custom_test", False, "Validation failed")

doc.add_test(my_custom_test)
doc.run_all()
```

### 3. Constant Bounds Validation

Validate that constants are within expected ranges:

```python
doc = Doctor()
result = doc.validate_constant_bounds("pi", 3.14159, 3.0, 3.2)
# Returns: DoctorResult("bounds:pi", True)
```

### 4. Constants File Validation

Validate JSON constants files:

```python
doc = Doctor()
results = doc.validate_constants_file("domains/physics/constants.json")
```

**Required Fields:**
- `key`: Unique identifier for the constant
- `value`: Numerical value
- `units`: Unit of measurement
- `provenance`: List of sources (must not be empty)
- `entered_by`: User who entered the constant

**Optional Fields:**
- `range`: [min, max] bounds for validation

**Example constants.json:**
```json
{
  "constants": [
    {
      "key": "g",
      "value": 9.8,
      "units": "m/s²",
      "provenance": ["gravitational constant"],
      "entered_by": "physics_team",
      "range": [9.0, 10.0]
    }
  ]
}
```

### 5. Pack Validation

Validate entire constants packs:

```python
doc = Doctor()
results = doc.validate_pack("packs/production_pack.json")
```

**Pack Structure:**
```json
{
  "domains": {
    "physics": {
      "enabled": true
    },
    "chemistry": {
      "enabled": false
    }
  }
}
```

The validator will:
- Load and parse the pack file
- Check each enabled domain
- Validate corresponding constants files
- Report any missing or invalid files

## Command-Line Usage

Run the module directly for self-tests:

```bash
python3 doctor.py
```

## Testing

Run the comprehensive test suite:

```bash
python3 -m pytest benchmarks/test_doctor.py -v
```

**Test Coverage:**
- 32 comprehensive tests
- DoctorResult class functionality
- Core math validation
- Custom test registration
- Bounds validation
- Constants file validation
- Pack validation
- Report generation
- Integration scenarios

## Error Handling

The Doctor module provides robust error handling:

- **Missing files**: Reports clear "file not found" errors
- **Malformed JSON**: Catches and reports parsing errors
- **Invalid ranges**: Validates range structure (must be [min, max])
- **Missing fields**: Reports specific missing required fields
- **Empty provenance**: Detects and reports empty provenance lists

## Security

The module has been validated with CodeQL and contains:
- **0 security vulnerabilities**
- Safe error handling for all file operations
- No arbitrary code execution
- Input validation for all data structures

## Best Practices

1. **Always run doctor before deployment**: Ensure all validations pass
2. **Add custom tests for domain-specific logic**: Extend the built-in tests
3. **Maintain provenance**: Always include sources for constants
4. **Use range validation**: Define expected bounds for critical constants
5. **Version control your packs**: Track changes to constants over time

## API Reference

### Classes

#### `DoctorResult`
Represents the result of a single test.

- `name` (str): Test name
- `passed` (bool): Whether the test passed
- `message` (str): Optional message for failures

#### `Doctor`
Main validation system.

**Methods:**
- `add_test(test_fn)`: Register a custom test
- `validate_constant_bounds(key, value, min_val, max_val)`: Validate a constant is within bounds
- `validate_constants_file(path)`: Validate a constants.json file
- `validate_pack(pack_path)`: Validate a constants pack
- `run_all()`: Run all registered tests, returns (passed, total)
- `report()`: Generate human-readable report

## Owner

Strategickhaos DAO LLC

## Author

Domenic G. Garza

## License

See repository LICENSE file.
