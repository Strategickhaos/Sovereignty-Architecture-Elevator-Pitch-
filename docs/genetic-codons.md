# Genetic Codons Dataset

This module provides access to a comprehensive dataset of 64 genetic codon triplets, each mapped to unique properties including physics characteristics, Hebrew letter associations, and symbolic glyphs.

## Overview

The genetic codon system represents a complete 64-element mapping inspired by DNA/RNA codons (AAA through TTT), with each triplet containing:

- **Atomic Number**: Sequential identifier (1-64)
- **Angular Position**: Degrees around a circle (0-360°)
- **Hebrew Letter**: Associated letter from the Hebrew alphabet
- **Glyph**: Unicode symbolic representation
- **Family**: Trigonometric classification (SIN, COS, TAN, CSC, SEC, COT)
- **Norm Squared**: Magnitude measure (numeric or "inf")
- **Schwarzschild Classification**: Black hole physics region
- **Xi Critical**: Critical xi value
- **Fragility**: Stability level (MAX, HIGH, MEDIUM, LOW)

## Data Structure

### Codon Families

The 64 codons are distributed across six trigonometric families:

- **SIN (White)**: 11 codons
- **COS (Yellow)**: 11 codons
- **TAN (Orange)**: 10 codons
- **CSC (Red)**: 11 codons
- **SEC (Blue)**: 11 codons
- **COT (Green)**: 10 codons

### Schwarzschild Classifications

Based on black hole physics:

- **Event Horizon**: 4 codons (infinite norm_sq)
- **Near Horizon**: 16 codons
- **Exterior**: 24 codons
- **ISCO (stable)**: 20 codons

### Fragility Levels

- **MAX**: 4 codons (at Event Horizon)
- **HIGH**: 16 codons
- **MEDIUM**: 24 codons
- **LOW**: 20 codons

## Usage

### Loading the Dataset

```typescript
import { loadGeneticCodons } from './src/genetic-codons.js';

const dataset = loadGeneticCodons();
console.log(`Loaded ${Object.keys(dataset).length} codons`);
```

### Getting a Specific Codon

```typescript
import { getCodon } from './src/genetic-codons.js';

const aaa = getCodon('AAA');
console.log(`${aaa.hebrew} (${aaa.glyph}) - ${aaa.family}`);
// Output: Aleph (⟋) - SIN (White)
```

### Querying Codons

```typescript
import { queryCodons } from './src/genetic-codons.js';

// Get all HIGH fragility codons in the SIN family
const results = queryCodons({
  family: 'SIN (White)',
  fragility: 'HIGH'
});

// Get codons in a specific angle range
const firstQuadrant = queryCodons({
  minAngle: 0,
  maxAngle: 90
});
```

### Finding Event Horizon Codons

```typescript
import { getEventHorizonCodons } from './src/genetic-codons.js';

const eventHorizonCodons = getEventHorizonCodons();
// Returns: AAA (0°), CAA (90°), GAA (180°), TAA (270°)
```

### Getting by Atomic Number

```typescript
import { getCodonByAtomic } from './src/genetic-codons.js';

const [triplet, properties] = getCodonByAtomic(32);
console.log(`Atomic 32: ${triplet}`); // CTT
```

### Dataset Statistics

```typescript
import { getDatasetStats } from './src/genetic-codons.js';

const stats = getDatasetStats();
console.log(stats.familyDistribution);
console.log(stats.fragilityDistribution);
```

## Testing

Run the test script to verify functionality:

```bash
npx tsx src/test-genetic-codons.ts
```

## Files

- `data/genetic_codons.json` - Raw dataset (64 codons)
- `src/types/genetic-codons.ts` - TypeScript type definitions
- `src/genetic-codons.ts` - Utility functions for loading and querying
- `src/test-genetic-codons.ts` - Test/demo script

## Examples

### Find All Maximum Fragility Codons

```typescript
import { queryCodons } from './src/genetic-codons.js';

const maxFragility = queryCodons({ fragility: 'MAX' });
// Returns 4 codons: AAA, CAA, GAA, TAA (all at Event Horizon)
```

### Get All Codons in a Family

```typescript
import { getCodonsByFamily } from './src/genetic-codons.js';

const cosCodons = getCodonsByFamily('COS (Yellow)');
console.log(`COS family has ${cosCodons.length} codons`);
```

### Filter by Multiple Criteria

```typescript
import { queryCodons } from './src/genetic-codons.js';

const results = queryCodons({
  schwarzschild: 'ISCO (stable)',
  minAtomic: 8,
  maxAtomic: 42
});
```

## Integration

This dataset can be integrated into:

- Quantum DNA splicer systems
- Symbolic language processors (FlameLang)
- Physics simulation engines
- Genetic algorithm implementations
- Sacred geometry visualizations
- Hebrew letter mapping systems

## License

Part of the Sovereignty Architecture project.
