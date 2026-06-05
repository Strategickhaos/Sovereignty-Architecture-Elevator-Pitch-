# TRIG6 - Trigonometric and Engineering Constants Library

**A self-validating constants management system with provenance tracking and mathematical verification.**

Owner: Strategickhaos DAO LLC  
Author: Domenic G. Garza

## Overview

TRIG6 provides a robust system for managing mathematical and engineering constants with:
- **Self-validation**: Built-in mathematical tests verify correctness
- **Provenance tracking**: Track sources and citations for all constants
- **Pack-based organization**: Group constants by domain with flexible validation rules
- **Doctor module**: Comprehensive validation and reporting system

## Features

### Core Mathematical Tests

The Doctor module includes built-in tests that verify fundamental mathematical truths:

- **Trigonometric Identity**: sin²θ + cos²θ = 1 (verified at multiple angles)
- **Secant at 60°**: sec(60°) = 2
- **Tangent at 45°**: tan(45°) = 1
- **Bridle Angle Formula**: Validates rigging calculations
- **Highline Sag Formula**: Validates tension calculations

### Validation Features

- **Required Fields**: Ensures all constants have key, value, and units
- **Range Checking**: Validates constants are within expected bounds
- **Provenance Validation**: Enforces citation and source documentation
- **Pack Settings**: Flexible validation rules per pack
- **Comprehensive Reporting**: Human-readable validation reports

## Quick Start

### Basic Usage

```python
from trig6 import Doctor

# Create a doctor instance
doc = Doctor()

# Run all core mathematical tests
passed, total = doc.run_all()
print(doc.report())
```

### Validate a Constants File

```python
from trig6 import Doctor

doc = Doctor()
results = doc.validate_constants_file(
    "domains/trigonometry/constants.json",
    strict_provenance=True
)

for result in results:
    print(result)
```

### Validate a Complete Pack

```python
from trig6 import Doctor

doc = Doctor()
results = doc.validate_pack("packs/standard.json")

# Generate report
passed = sum(1 for r in results if r.passed)
total = len(results)
print(f"Pack Validation: {passed}/{total} tests passed")
```

## Directory Structure

```
trig6/
├── __init__.py           # Package initialization
├── doctor.py             # Core validation system
├── domains/              # Domain-specific constants
│   ├── trigonometry/
│   │   └── constants.json
│   └── mechanics/
│       └── constants.json
├── packs/                # Pack configurations
│   ├── standard.json     # Standard pack (lenient)
│   └── strict.json       # Strict pack (full provenance)
└── tests/
    └── test_doctor.py    # Comprehensive test suite
```

## Constants File Format

```json
{
  "domain": "trigonometry",
  "version": "1.0.0",
  "constants": [
    {
      "key": "pi",
      "value": 3.141592653589793,
      "units": "radians",
      "description": "The ratio of a circle's circumference to its diameter",
      "range": [3.14, 3.15],
      "provenance": [
        {
          "source_title": "Mathematical Constants",
          "author": "Various",
          "year": 2024
        }
      ],
      "entered_by": "Domenic G. Garza"
    }
  ]
}
```

## Pack Configuration

```json
{
  "pack_name": "standard",
  "version": "1.0.0",
  "description": "Standard TRIG6 constants pack",
  "settings": {
    "strict_provenance": false,
    "require_entered_by": false,
    "fail_on_missing_citation": false
  },
  "domains": {
    "trigonometry": {
      "enabled": true,
      "constants_file": "domains/trigonometry/constants.json"
    }
  }
}
```

### Pack Settings

- **strict_provenance**: Require provenance for all constants
- **require_entered_by**: Require entered_by field for all constants
- **fail_on_missing_citation**: Fail validation if citations are missing

## Running Tests

```bash
# Run all tests
python3 -m unittest trig6/tests/test_doctor.py -v

# Run a specific test class
python3 -m unittest trig6.tests.test_doctor.TestDoctorCoreMath -v

# Run the doctor module directly (self-test)
python3 trig6/doctor.py
```

## Test Coverage

The test suite includes 27 comprehensive tests covering:

- ✅ DoctorResult class functionality
- ✅ Core mathematical validation tests
- ✅ Bounds validation
- ✅ Constants file validation
- ✅ Pack validation
- ✅ Custom test registration
- ✅ Report generation
- ✅ Error handling

## Adding Custom Tests

```python
from trig6 import Doctor, DoctorResult

doc = Doctor()

def my_custom_test():
    # Your validation logic here
    if some_condition:
        return DoctorResult("my_test", True)
    else:
        return DoctorResult("my_test", False, "Reason for failure")

doc.add_test(my_custom_test)
passed, total = doc.run_all()
print(doc.report())
```

## Philosophy

**If it doesn't pass doctor, it doesn't ship.**

The TRIG6 Doctor module ensures that all constants are:
1. Mathematically correct
2. Properly documented
3. Within expected ranges
4. Traceable to authoritative sources

This approach provides confidence in the accuracy and reliability of the constants used in engineering calculations.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass: `python3 -m unittest trig6/tests/test_doctor.py`
2. New constants include proper provenance
3. Mathematical constants are verified against authoritative sources
4. Documentation is updated for new features

## Credits

Owner: Strategickhaos DAO LLC  
Author: Domenic G. Garza

Built with precision and care for the engineering community.
