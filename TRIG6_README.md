# TRIG6 Citation System

**Every constant must have provenance. No exceptions.**  
This is audit armor against discreditation.

## Overview

The TRIG6 Citation System is a rigorous provenance tracking system for constants and values used in the Strategickhaos ecosystem. It ensures that every numerical value can be traced back to its authoritative source with complete citation information.

## Owner

- **Organization**: Strategickhaos DAO LLC
- **Author**: Domenic G. Garza
- **Date**: 2026-01-29

## Features

- ✅ **Full Provenance Tracking**: Every constant must have at least one source citation
- ✅ **Validation Framework**: Constraints and bounds checking for each constant
- ✅ **Jurisdiction Support**: Track regulatory context (global, USA, OSHA, etc.)
- ✅ **Confidence Levels**: Mark constants as high/medium/low confidence or heuristic
- ✅ **APA-Style Citations**: Automatic formatting of citations
- ✅ **JSON Persistence**: Save and load constants with full metadata
- ✅ **Audit Trail**: Track who entered each constant and when

## Quick Start

### Basic Usage

```python
from trig6_citation import Provenance, Validation, ConstantRecord

# Create a constant with full provenance
constant = ConstantRecord(
    key="rope.knot.figure_8_on_bight",
    value=0.78,
    units="ratio",
    context="Typical knot efficiency in nylon kernmantle when properly dressed/set.",
    provenance=[
        Provenance(
            source_title="CMC Rope Rescue Field Guide",
            publisher="CMC Rescue, Inc.",
            edition_or_rev="4th Edition",
            date="2017",
            section_or_page="p. 47",
            notes="Tested on 11mm nylon kernmantle, new rope"
        )
    ],
    entered_by="Domenic G. Garza",
    entered_date="2026-01-29",
    range=(0.75, 0.80),
    validation=Validation(
        doctor_test="rope.knot_efficiency_in_bounds",
        constraints=["0.5 <= value <= 0.95"]
    )
)

# Display formatted output
print(constant.format_full())

# Convert to JSON
import json
print(json.dumps(constant.to_dict(), indent=2))
```

### Loading and Saving Constants

```python
from trig6_citation import load_constants_file, save_constants_file

# Load constants from a JSON file
constants = load_constants_file("data/constants/example_constants.json")

# Work with constants
for c in constants:
    print(f"{c.key}: {c.value} {c.units}")

# Save constants back to file
metadata = {"version": "1.0", "schema": "TRIG6"}
save_constants_file("output.json", constants, metadata)
```

## Data Schema

### Provenance

Required for citing sources:

```python
@dataclass
class Provenance:
    source_title: str              # Required: Title of the source
    publisher: str                 # Required: Publisher name
    edition_or_rev: Optional[str]  # Edition or revision number
    date: Optional[str]            # Publication date (YYYY-MM-DD or YYYY)
    section_or_page: Optional[str] # Specific section or page reference
    url: Optional[str]             # URL if available
    notes: Optional[str]           # Additional notes
```

### Validation

Defines how to verify the constant:

```python
@dataclass
class Validation:
    doctor_test: str               # Test name in validation system
    constraints: List[str]         # Constraints (e.g., "0.5 <= value <= 0.9")
```

### ConstantRecord

The main record with full metadata:

```python
@dataclass
class ConstantRecord:
    key: str                       # Hierarchical key (e.g., "rope.knot.figure_8")
    value: float                   # The numerical value
    units: str                     # Units (ratio, lbf, degrees, kN, etc.)
    context: str                   # Plain English explanation
    provenance: List[Provenance]   # Must have at least one source
    entered_by: str                # Who entered this constant
    entered_date: str              # When it was entered (YYYY-MM-DD)
    range: Optional[tuple]         # Expected (min, max) values
    jurisdiction: str              # "global", "USA", "OSHA", etc.
    confidence: str                # "high", "medium", "low", "heuristic"
    validation: Optional[Validation] # Validation rules
```

## Example Constants File

See `data/constants/example_constants.json` for a complete example with three constants:

1. **Rope Knot Efficiency**: Knot efficiency for figure-8-on-bight
2. **Earth's Gravity**: Standard gravitational acceleration
3. **OSHA Fall Protection**: Maximum free fall distance per regulations

## Testing

Run the test suite:

```bash
# Run self-test
python3 trig6_citation.py

# Run full test suite
python3 test_trig6_citation.py
```

All tests should pass with 15 test cases covering:
- Provenance creation and formatting
- Validation constraints
- ConstantRecord serialization
- File I/O operations
- Complete workflow integration

## File Structure

```
├── trig6_citation.py              # Main citation system module
├── test_trig6_citation.py         # Test suite (15 tests)
├── data/
│   └── constants/
│       └── example_constants.json # Example constants with provenance
└── TRIG6_README.md               # This file
```

## Philosophy

The TRIG6 Citation System embodies the principle that **trust requires traceability**. In technical and regulatory contexts, every number must be defensible. This system ensures that:

1. **No orphan constants**: Every value has a documented source
2. **Audit readiness**: Full paper trail for compliance and verification
3. **Version control**: Track when and by whom constants were entered
4. **Jurisdiction clarity**: Understand which standards apply
5. **Confidence transparency**: Know which values are authoritative vs. heuristic

## Integration

To integrate TRIG6 into your project:

1. Import the module: `from trig6_citation import ConstantRecord, Provenance, Validation`
2. Create constants with full provenance
3. Save to JSON for version control
4. Reference constants by their hierarchical keys
5. Implement the `doctor_test` validation functions

## License

Part of the Strategickhaos Sovereignty Architecture  
MIT License - see repository LICENSE file

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Audit armor against discreditation"*
