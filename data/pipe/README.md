# Pipefitting Constants with ASME/API Provenance

## Overview

This system provides industry-standard pipefitting constants with full provenance tracking from authoritative sources including ASME (American Society of Mechanical Engineers), API (American Petroleum Institute), and AWS (American Welding Society) standards.

## Maintainer

**Domenic G. Garza**  
Certifications: Pipefitter Journeyman, Turner Industries

Owner: Strategickhaos DAO LLC

## Regulatory Frameworks

All constants are sourced from recognized industry standards:

- **ASME B31.1** - Power Piping
- **ASME B31.3** - Process Piping
- **ASME B36.10M** - Welded and Seamless Wrought Steel Pipe
- **ASME B16.9** - Factory-Made Wrought Buttwelding Fittings
- **API 570** - Piping Inspection Code
- **AWS D1.1** - Structural Welding Code

## Constants Included

### Thermal Expansion Coefficients
- **Carbon Steel** (A106, A53): 6.5×10⁻⁶ in/in/°F
  - Source: ASME B31.1 Power Piping (2020 Edition), Table C-3
  - Mean coefficient from 70°F to 400°F
  
- **304 Stainless Steel**: 9.6×10⁻⁶ in/in/°F
  - Source: ASME B31.3 Process Piping (2022 Edition), Table C-3
  - Mean coefficient for austenitic stainless

### Wall Thickness (2" NPS)
- **Schedule 40**: 0.154 inches
  - Source: ASME B36.10M (2018), Table 1
  - Standard weight, OD = 2.375"
  
- **Schedule 80**: 0.218 inches
  - Source: ASME B36.10M (2018), Table 1
  - Extra strong, OD = 2.375"

### Fitting Takeouts (2" NPS, Long Radius)
- **90° Elbow**: 3.0 inches
  - Source: ASME B16.9 (2018), Table 1
  - Center-to-face dimension
  
- **45° Elbow**: 1.5 inches
  - Source: ASME B16.9 (2018), Table 1
  - Center-to-face dimension

### Welding
- **Standard Root Gap**: 0.09375 inches (3/32")
  - Source: AWS D1.1 (2020), Figure 3.4
  - Typical root opening; verify with applicable WPS

### Mathematical Constants
- **Pi (π)**: 3.14159
  - For circumference calculations: C = π × D

## Usage

### Python Module

```python
from pipefitting_constants import PipefittingConstants

# Initialize the constants loader
constants = PipefittingConstants()

# Get a specific value
thermal_exp = constants.get_value('pipe.thermal_expansion.carbon_steel')
print(f"Carbon steel thermal expansion: {thermal_exp} in/in/°F")

# Search for constants
results = constants.search_constants('thermal_expansion')
for result in results:
    print(f"{result['key']}: {result['value']} {result['units']}")

# Get full information with provenance
print(constants.format_constant('pipe.schedule.40.wall_thickness.2inch'))

# Validate all constants
validation_results = constants.validate_all()
all_valid = all(result[0] for result in validation_results.values())
print(f"All constants valid: {all_valid}")
```

### Direct JSON Access

The constants are stored in `data/pipe/pipefitting_constants.json` and can be accessed directly:

```python
import json

with open('data/pipe/pipefitting_constants.json') as f:
    data = json.load(f)

# Access metadata
print(data['metadata']['maintainer'])

# Access constants
for constant in data['constants']:
    print(f"{constant['key']}: {constant['value']} {constant['units']}")
```

## Data Structure

Each constant includes:

- **key**: Unique identifier (e.g., `pipe.thermal_expansion.carbon_steel`)
- **value**: Numeric value
- **units**: Engineering units
- **range**: Acceptable range for the value
- **context**: Description and usage notes
- **jurisdiction**: Applicability (global, US, etc.)
- **confidence**: Confidence level (high, medium, low)
- **provenance**: Array of source citations
  - source_title
  - publisher
  - edition_or_rev
  - date
  - section_or_page
  - notes
- **entered_by**: Person who entered the data
- **entered_date**: Date of entry
- **validation**: Validation rules
  - doctor_test: Test function name
  - constraints: List of validation expressions

## Validation

All constants include validation rules ("doctor tests") to ensure data integrity:

```python
# Run all validations
validation_results = constants.validate_all()

# Validate a specific constant
is_valid, messages = constants.validate_constant('pipe.weld_gap.standard')
if is_valid:
    print("Constant passes all validations")
else:
    for message in messages:
        print(f"Validation issue: {message}")
```

## Testing

Run the test suite to verify all constants:

```bash
python3 test_pipefitting_constants.py
```

The test suite validates:
- Data loading and structure
- Constant retrieval and search
- Value accuracy
- Provenance tracking
- Constraint validation
- Range checking

## Demo

Run the demo to see the system in action:

```bash
python3 pipefitting_constants.py
```

This displays:
- Metadata and maintainer information
- List of all available constants
- Detailed example with provenance
- Validation results for all constants

## Professional Credentials

This constants database is maintained by **Domenic G. Garza**, a certified Pipefitter Journeyman with credentials from Turner Industries. All values are sourced from authoritative industry standards and include complete provenance tracking for professional verification.

## License

Part of the Strategickhaos Sovereignty Architecture  
© 2026 Strategickhaos DAO LLC

## Version

**Version 1.0.0**  
Created: 2026-01-29  
Last Updated: 2026-01-29
