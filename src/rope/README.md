# Rope Access Constants Module

**Professional rope access and rescue constants with full regulatory provenance**

## Overview

This module provides type-safe access to rope access and rescue constants derived from industry standards and certified sources. All constants include full regulatory provenance, allowing engineers and safety professionals to trace values back to authoritative sources.

## Features

- **Regulatory Provenance**: Every constant is backed by citations from industry standards (OSHA, ANSI, SPRAT, IRATA)
- **Type Safety**: Full TypeScript type definitions for all constants and metadata
- **Validation**: Built-in constraint validation and "doctor tests" for safety-critical values
- **Search & Query**: Find constants by category, jurisdiction, confidence level, or text search
- **Professional Certification**: Maintained by SPRAT Level 3 certified professional

## Installation

The module is part of the Sovereignty Architecture project. Import it in your TypeScript code:

```typescript
import { getRopeConstants, RopeConstant } from './src/rope/index.js';
```

## Usage

### Basic Access

```typescript
import { getRopeConstants } from './src/rope/index.js';

const rope = getRopeConstants();

// Get a specific constant
const figure8 = rope.getConstant('rope.knot.figure_8_on_bight');
console.log(`Figure-8 on bight efficiency: ${figure8?.value}`);
// Output: Figure-8 on bight efficiency: 0.78

// Get all knot efficiency constants
const knots = rope.getConstantsByCategory('knot');
knots.forEach(k => {
  console.log(`${k.key}: ${k.value} (${k.units})`);
});
```

### Search and Query

```typescript
// Search for constants containing "pulley"
const pulleys = rope.searchConstants('pulley');
pulleys.forEach(result => {
  console.log(`Found in: ${result.matches.join(', ')}`);
  console.log(`  ${result.constant.key}: ${result.constant.value}`);
});

// Get constants by jurisdiction
const usaConstants = rope.getConstantsByJurisdiction('USA');
const globalConstants = rope.getConstantsByJurisdiction('global');

// Filter by confidence level
const highConfidence = rope.getConstantsByConfidence('high');
```

### Validation

```typescript
// Validate a single constant
const validation = rope.validateConstant('rope.knot.figure_8_on_bight');
if (!validation.valid) {
  console.error(`Validation errors: ${validation.errors.join(', ')}`);
}
if (validation.warnings.length > 0) {
  console.warn(`Warnings: ${validation.warnings.join(', ')}`);
}

// Validate all constants
const allValidations = rope.validateAll();
const failed = allValidations.filter(v => !v.valid);
if (failed.length > 0) {
  console.error(`${failed.length} constants failed validation`);
}
```

### Provenance Access

```typescript
const constant = rope.getConstant('rope.design_factor.lifesafety_pfas');
if (constant) {
  console.log(`\nConstant: ${constant.key}`);
  console.log(`Value: ${constant.value} ${constant.units}`);
  console.log(`Context: ${constant.context}`);
  console.log(`\nProvenance:`);
  
  constant.provenance.forEach(prov => {
    console.log(`  - ${prov.source_title}`);
    console.log(`    Publisher: ${prov.publisher}`);
    console.log(`    Edition: ${prov.edition_or_rev}`);
    console.log(`    Section: ${prov.section_or_page}`);
    if (prov.url) {
      console.log(`    URL: ${prov.url}`);
    }
    console.log(`    Notes: ${prov.notes}`);
  });
}
```

## Available Constants

### Knot Efficiency
- `rope.knot.figure_8_on_bight` - 0.78 (Figure-8 on a bight)
- `rope.knot.bowline` - 0.70 (Bowline)
- `rope.knot.alpine_butterfly` - 0.75 (Alpine butterfly loop)
- `rope.knot.double_fishermans` - 0.65 (Double fisherman's bend)

### Pulley Efficiency
- `rope.pulley.efficiency.standard` - 0.90 (Standard bushing bearing)
- `rope.pulley.efficiency.high_efficiency` - 0.95 (Ball bearing)
- `rope.pulley.efficiency.carabiner` - 0.50 (Carabiner as improvised pulley)

### Design Factors
- `rope.design_factor.lifesafety_pfas` - 10.0 (OSHA PFAS minimum)
- `rope.design_factor.training_heuristic` - 5.0 (Training heuristic)

### Safety Parameters
- `rope.max_fall_factor` - 2.0 (Maximum theoretical fall factor)
- `rope.angle.max_bridle_included` - 120.0 degrees (Maximum bridle angle)

## Data Structure

Constants are stored in JSON format at `data/rope/constants.json` with the following structure:

```json
{
  "metadata": {
    "domain": "rope",
    "description": "Rope access and rescue constants with regulatory provenance",
    "owner": "Strategickhaos DAO LLC",
    "maintainer": "Domenic G. Garza",
    "certifications_held": ["SPRAT Level 3", "IRATA (pending)"],
    "version": "1.0.0",
    "regulatory_frameworks": ["OSHA 1926.502", "ANSI Z359", "SPRAT Safe Practices", "IRATA ICOP"]
  },
  "constants": [
    {
      "key": "rope.knot.figure_8_on_bight",
      "value": 0.78,
      "units": "ratio",
      "range": [0.75, 0.80],
      "context": "Knot efficiency for figure-8...",
      "jurisdiction": "global",
      "confidence": "high",
      "provenance": [
        {
          "source_title": "CMC Rope Rescue Field Guide",
          "publisher": "CMC Rescue, Inc.",
          "edition_or_rev": "4th Edition",
          "date": "2017",
          "section_or_page": "p. 47",
          "notes": "Tested on 11mm static kernmantle..."
        }
      ],
      "entered_by": "Domenic G. Garza",
      "entered_date": "2026-01-29",
      "validation": {
        "doctor_test": "rope.knot_efficiency_in_bounds",
        "constraints": ["0.5 <= value <= 0.95"]
      }
    }
  ]
}
```

## Safety Considerations

⚠️ **CRITICAL SAFETY NOTICE** ⚠️

These constants are provided for informational and educational purposes. When working with life-safety systems:

1. **Always verify** values with manufacturer specifications for your specific equipment
2. **Follow applicable regulations** for your jurisdiction (OSHA, ANSI, SPRAT, IRATA, etc.)
3. **Use proper training** - rope access work requires professional certification
4. **Consider environmental factors** - age, wear, contamination affect all values
5. **Maintain equipment** per manufacturer guidelines
6. **Get professional inspection** - have systems inspected by qualified personnel

The maintainer holds SPRAT Level 3 certification but this does not constitute professional advice. Consult with certified rope access professionals and follow all applicable safety standards.

## Regulatory Frameworks

This module references the following regulatory frameworks:

- **OSHA 1926.502** - Fall Protection Standards (USA)
- **ANSI Z359** - Fall Protection and Arrest Equipment (USA)
- **SPRAT Safe Practices** - Society of Professional Rope Access Technicians
- **IRATA ICOP** - Industrial Rope Access Trade Association Code of Practice

## Contributing

To add new constants:

1. Ensure you have proper source documentation
2. Add the constant to `data/rope/constants.json`
3. Include full provenance with source citations
4. Add appropriate validation constraints
5. Run validation tests to ensure data integrity

## License

Part of the Sovereignty Architecture project - see root LICENSE file.

## Maintainer

**Domenic G. Garza**  
Strategickhaos DAO LLC  
Certifications: SPRAT Level 3, IRATA (pending)

---

*"Measure twice, tie once, check thrice."*
