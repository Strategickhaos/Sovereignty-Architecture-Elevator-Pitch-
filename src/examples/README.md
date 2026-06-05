# Caveman Logic System - Quick Start

This directory contains the implementation and examples of the Caveman Logic System.

## Running the Examples

### Option 1: Using TypeScript (tsx)
```bash
npx tsx src/examples/caveman-logic-examples.ts
```

### Option 2: Using compiled JavaScript
```bash
npm run build
node dist/examples/caveman-logic-examples.js
```

## Using in Your Code

### TypeScript
```typescript
import { CavemanLogic, PhysicsGate, TRIG6 } from './caveman-logic';

// Quick check
const itComputes = CavemanLogic.doesItCompute(
  false, // No free energy
  true,  // Effect after cause
  true,  // Can be bounded
  true,  // Reproducible
  true   // Fails safely
);

// Full evaluation
const result = CavemanLogic.evaluate({
  name: "My feature",
  requiresFreeEnergy: false,
  effectAfterCause: true,
  canBeBounded: true,
  isReproducible: true,
  failsSafely: true
});

console.log(result.decision); // "accept", "investigate", or "reject"
console.log(result.recommendation);
```

### JavaScript (ES Modules)
```javascript
import { CavemanLogic } from './dist/caveman-logic.js';

const result = CavemanLogic.evaluate({
  name: "My feature",
  requiresFreeEnergy: false,
  effectAfterCause: true,
  canBeBounded: true,
  isReproducible: true,
  failsSafely: true
});

console.log(result.decision);
```

## Documentation

Full documentation available at [docs/CAVEMAN_LOGIC.md](../docs/CAVEMAN_LOGIC.md)

## Core Principle

> "Does this shit compute?"
> - If no → fuck 'em (discard/sandbox)
> - If maybe → TRIG6 it
> - If yes → keep building

That's it. That's the whole operating system.
