# TRIG6 Constants Pack

This directory contains the default TRIG6 constants pack configuration and domain-specific constants for industrial and technical applications.

## Structure

```
trig6-pack.json          # Main pack configuration
domains/                 # Domain-specific constants
├── rope/
│   └── constants.json   # Rope access and rescue (SPRAT/IRATA)
├── rigging/
│   └── constants.json   # Industrial rigging (ASME B30)
├── pipe/
│   └── constants.json   # Pipefitting (ASME/API)
├── ndt/
│   └── constants.json   # NDT/Radiography (GATED)
└── khaos/
    └── constants.json   # KHAOS symbolic constants
```

## Pack Configuration

The main `trig6-pack.json` file defines:

- **Metadata**: Pack name, version, owner, and dates
- **Domains**: Five technical domains with enable/disable flags
- **Settings**: System-wide behavior flags

## Domains

### Enabled Domains

1. **Rope** - Rope access and rescue constants (SPRAT/IRATA standards)
2. **Rigging** - Industrial rigging constants (ASME B30 standards)
3. **Pipe** - Pipefitting constants (ASME/API standards)
4. **KHAOS** - Symbolic constants and glyph mappings for the Strategickhaos ecosystem

### Gated Domains

5. **NDT** - Non-Destructive Testing and Radiography (**DISABLED BY DEFAULT**)
   - **Gate Reason**: Exposure calculations require RAD certification
   - **Unlock Flag**: `--enable-ndt`
   - **Requirements**: RAD license and proper certifications

## Settings

The pack enforces:

- **strict_provenance**: Tracks data source and verification
- **require_entered_by**: Requires attribution for all constants
- **fail_on_missing_citation**: Enforces citation requirements
- **doctor_on_load**: Validates pack integrity on load
- **output_format**: JSON format for all outputs

## Usage

### Loading the Pack

```javascript
const pack = require('./trig6-pack.json');

// Check if a domain is enabled
if (pack.domains.rope.enabled) {
  const ropeConstants = require(pack.domains.rope.constants_file);
  // Use constants...
}
```

### Enabling Gated Domains

The NDT domain is gated and requires explicit enabling:

```bash
# Command-line flag
./your-tool --enable-ndt

# Or in code with proper license verification
if (hasValidRADLicense()) {
  enableDomain('ndt');
}
```

## Domain Details

### Rope Access
- Safety factors for static/dynamic lines
- Rope strength specifications
- Working load limits
- Inspection intervals

### Industrial Rigging
- Sling angle load factors
- Safety factors by material type
- D/d ratios for sheaves
- Rejection criteria for equipment

### Pipefitting
- Pipe schedules and ratings
- Allowable stress tables by material and temperature
- Weld joint efficiencies
- Flange pressure ratings
- Corrosion allowances

### NDT/Radiography (Gated)
- Radiation dose limits
- Source activity specifications
- Film density requirements
- Penetrameter (IQI) standards
- **WARNING**: Requires proper certification and licensing

### KHAOS
- Glyph mappings and Unicode symbols
- Color codes for visual representation
- Symbolic constants (φ, ℏ, κ)
- System state codes
- Ritual sequences for state transitions

## Provenance

All constants include provenance metadata:
- `entered_by`: Who entered the data
- `verified_by`: Authority that verified the constants
- `last_updated`: Last modification date

## Standards References

- **SPRAT/IRATA**: Rope access standards
- **ASME B30.x**: Rigging and lifting standards
- **ASME B31.x**: Piping standards
- **API 570**: Piping inspection
- **ASNT SNT-TC-1A**: NDT personnel qualification
- **ISO 9712**: NDT qualification and certification

## Version

- **Pack Name**: default
- **Version**: 1.0.0
- **Owner**: Strategickhaos DAO LLC
- **Created**: 2026-01-29
- **Last Updated**: 2026-01-29

## License

Copyright © 2026 Strategickhaos DAO LLC. All rights reserved.
