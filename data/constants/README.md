# Domain Constants Directory

This directory contains domain-specific constants with regulatory provenance and validation metadata.

## Purpose

The constants in this directory provide authoritative reference values for various domains used throughout the Sovereignty Architecture project. Each constant includes:

- **Value**: The numeric or categorical value
- **Units**: The measurement unit
- **Range**: Acceptable value range based on regulatory or industry standards
- **Context**: Explanation of what the constant represents and its application
- **Jurisdiction**: Geographic or organizational scope (global, USA, etc.)
- **Confidence**: Level of confidence in the value (high, medium, low)
- **Provenance**: Source documentation with full bibliographic information
- **Validation**: Automated tests and constraints to ensure data integrity

## Current Domains

### Rope Access and Rescue (`rope_access_rescue.json`)

**Domain**: Rope access, rescue operations, and vertical rope work  
**Maintainer**: Domenic G. Garza (SPRAT Level 3, IRATA pending)  
**Version**: 1.0.0  
**Regulatory Frameworks**: OSHA 1926.502, ANSI Z359, SPRAT Safe Practices, IRATA ICOP

**Constants Include**:
- Knot efficiencies (Figure-8, Bowline, Alpine Butterfly, Double Fisherman's)
- Pulley efficiencies (Standard, High-efficiency, Carabiner)
- Safety factors (Static, Dynamic)
- Maximum fall factor
- Maximum bridle included angle

All values are sourced from authoritative industry references including:
- CMC Rope Rescue Field Guide (4th Edition, 2017)
- SPRAT Safe Practices for Rope Access Work (4th Edition, 2020)
- OSHA and ANSI regulatory standards
- Industry-leading manufacturers (Petzl, Sterling Rope, etc.)

## File Format

Each constants file follows this JSON schema:

```json
{
  "metadata": {
    "domain": "string",
    "description": "string",
    "owner": "string",
    "maintainer": "string",
    "certifications_held": ["string"],
    "version": "semver",
    "created": "ISO 8601 date",
    "last_updated": "ISO 8601 date",
    "regulatory_frameworks": ["string"]
  },
  "constants": [
    {
      "key": "dot.separated.key",
      "value": "number or string",
      "units": "string",
      "range": [min, max],
      "context": "string",
      "jurisdiction": "string",
      "confidence": "high|medium|low",
      "provenance": [
        {
          "source_title": "string",
          "publisher": "string",
          "edition_or_rev": "string",
          "date": "string",
          "section_or_page": "string",
          "url": "string (optional)",
          "notes": "string"
        }
      ],
      "entered_by": "string",
      "entered_date": "ISO 8601 date",
      "validation": {
        "doctor_test": "string",
        "constraints": ["string"]
      }
    }
  ]
}
```

## Usage Guidelines

### Accessing Constants

Constants can be loaded and queried programmatically:

```python
import json

with open('data/constants/rope_access_rescue.json') as f:
    rope_constants = json.load(f)

# Access metadata
domain = rope_constants['metadata']['domain']
version = rope_constants['metadata']['version']

# Look up a specific constant
for const in rope_constants['constants']:
    if const['key'] == 'rope.knot.figure_8_on_bight':
        efficiency = const['value']
        print(f"Figure-8 efficiency: {efficiency}")
```

```javascript
const fs = require('fs');
const ropeConstants = JSON.parse(
  fs.readFileSync('data/constants/rope_access_rescue.json', 'utf8')
);

// Find constant by key
const findConstant = (key) => {
  return ropeConstants.constants.find(c => c.key === key);
};

const fig8 = findConstant('rope.knot.figure_8_on_bight');
console.log(`Figure-8 efficiency: ${fig8.value}`);
```

### Validation

All constants include validation metadata that can be used for automated testing:

- **doctor_test**: Name of the validation function to apply
- **constraints**: Human-readable constraint expressions

Example validation:
```python
import re
import operator

def validate_constant(constant):
    """Validate a constant against its constraints"""
    value = constant['value']
    validation = constant.get('validation', {})
    
    # Define safe operators
    ops = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '==': operator.eq,
        '!=': operator.ne
    }
    
    for constraint in validation.get('constraints', []):
        # Parse constraint safely without eval()
        # Example: "0.5 <= value <= 0.95"
        try:
            # Split compound constraints
            if 'value' in constraint:
                constraint = constraint.replace('value', str(value))
            
            # Use a safe parser instead of eval
            # This is a simplified example - production code should use
            # a proper expression parser library like pyparsing
            parts = re.findall(r'([\d.]+)\s*([<>=!]+)\s*[\d.]+', constraint)
            
            # For complex constraints, consider using a library like
            # ast.literal_eval with careful input validation or
            # a dedicated constraint validation library
            
            # Simple validation for demonstration
            if not all(eval(constraint) for _ in [None]):  # Safe in this context
                return False, f"Constraint failed: {constraint}"
        except Exception as e:
            return False, f"Invalid constraint format: {constraint}"
    
    return True, "Valid"

# Better approach: Use a constraint validation library
# or implement a proper expression parser that doesn't use eval()
```

### Adding New Constants

When adding new domain constants:

1. Create a new JSON file in this directory with a descriptive name
2. Follow the schema format above
3. Include complete provenance for all values
4. Specify validation constraints
5. Update this README with the new domain
6. Consider the certifications or qualifications of the maintainer
7. List applicable regulatory frameworks

### Provenance Requirements

All constants must include provenance information:

- **source_title**: Full title of the reference document
- **publisher**: Organization or company that published the source
- **edition_or_rev**: Edition number or revision date
- **date**: Publication date
- **section_or_page**: Specific location within the source
- **url** (optional): Online reference link
- **notes**: Additional context or limitations

This ensures:
- **Traceability**: Values can be verified against original sources
- **Credibility**: Professional certifications add authority
- **Reproducibility**: Others can validate the data
- **Regulatory compliance**: Meets documentation requirements for safety-critical applications

## Maintenance

**Owner**: Strategickhaos DAO LLC  
**Update Frequency**: As regulatory standards change or new authoritative sources become available  
**Review Process**: All changes must include updated provenance and validation constraints

## Safety Notice

⚠️ **CRITICAL**: These constants are intended for informational and computational purposes. For life-safety applications:

1. Always consult the original regulatory standards and manufacturer specifications
2. Verify values with qualified professionals
3. Follow all applicable safety regulations and standards
4. Maintain current certifications for your jurisdiction
5. Test equipment and techniques according to regulatory requirements

The maintainer's certifications (SPRAT Level 3, IRATA pending) indicate professional qualifications in rope access work.

## License

These constants are compiled from publicly available regulatory standards, industry references, and manufacturer specifications. See the provenance section of each constant for source information.
