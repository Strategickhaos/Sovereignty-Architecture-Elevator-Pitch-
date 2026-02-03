# Caveman Logic System

> "Does this shit compute?"

A clean, safe decision-making framework based on fundamental physics constraints and multi-angle testing methodology.

## Core Philosophy

**Belief is optional. Constraints aren't.**

The Caveman Logic System provides a disciplined approach to evaluating ideas, features, and decisions without relying on intuition, politics, or wishful thinking. It's based on three fundamental questions:

1. **Does it compute?** → If no, discard/sandbox
2. **Maybe?** → TRIG6 it (test from 6 angles)
3. **Yes?** → Keep building

This isn't arrogance. It's tool discipline.

---

## The Three Components

### 1. Main Decision Gate

The entry point for any concept, idea, or decision:

```typescript
import { CavemanLogic, Decision } from './caveman-logic';

const result = CavemanLogic.evaluate({
  name: "New feature X",
  requiresFreeEnergy: false,
  effectAfterCause: true,
  canBeBounded: true,
  isReproducible: true,
  failsSafely: true
});

// result.decision will be: REJECT, INVESTIGATE, or ACCEPT
// result.recommendation provides human-readable guidance
```

### 2. Caveman Physics Gate

Five fundamental checks based on physics constraints:

#### 1. **Energy**
Does it require free energy?
- If yes → **NOPE** (violates thermodynamics)
- If no → Continue

#### 2. **Causality**
Does effect come after cause?
- If no → **NOPE** (violates causality)
- If yes → Continue

#### 3. **Constraints**
Can I bound it (limits, caps, thresholds)?
- If no → **SANDBOX** (unbounded systems are dangerous)
- If yes → Continue

#### 4. **Reproducibility**
Can I make it happen again?
- If no → **LOG + IGNORE** (one-offs aren't reliable)
- If yes → Continue

#### 5. **Failure Mode**
When it fails, does it fail loud and safe?
- If no → **FIX OR TOSS** (silent failures are deadly)
- If yes → Continue

```typescript
import { PhysicsGate } from './caveman-logic';

const result = PhysicsGate.validate({
  requiresFreeEnergy: false,
  effectAfterCause: true,
  canBeBounded: true,
  isReproducible: true,
  failsSafely: true
});

console.log(result.passed); // true/false
console.log(result.details); // Array of human-readable checks
```

### 3. TRIG6 Testing

When something is fuzzy but interesting, test it from 6 angles:

1. **Change scale assumptions** (larger/smaller)
2. **Change time assumptions** (faster/slower)
3. **Change resource assumptions** (more/less)
4. **Change environmental assumptions** (different context)
5. **Change interaction assumptions** (isolated/connected)
6. **Change boundary assumptions** (open/closed system)

**Outcomes:**
- If it **blows up** at any angle → Reject with love ❌
- If it **stays bounded** across angles → Keep ✅
- If it **resonates** (works only in narrow band) → Handle gently ⚠️

```typescript
import { TRIG6, createSimpleAngleTester } from './caveman-logic';

// Create a test function that checks if concept stays bounded at each angle
const angleTester = createSimpleAngleTester((angle) => {
  // Your test logic here
  // Return true if concept stays bounded, false if it blows up
  return true;
});

const result = TRIG6.test("My fuzzy concept", angleTester);

console.log(result.outcome); // "reject", "keep", or "handle_gently"
console.log(result.bounded); // true/false
console.log(result.resonance); // true if works in narrow band
```

---

## Why This Keeps You Sane

1. **No special treatment**: Nothing gets a pass. Not even your own ideas.
2. **Emotion is data**: Feelings are logged, but decisions wait for tests.
3. **Constraints over belief**: Physics doesn't care about your opinions.
4. **Fail safe, fail loud**: When things break, we know immediately.
5. **Multi-angle validation**: Truth reveals itself under different assumptions.

---

## Usage Examples

### Example 1: Evaluating a New API Endpoint

```typescript
import { CavemanLogic } from './caveman-logic';

const evaluation = CavemanLogic.evaluate({
  name: "New batch processing API",
  requiresFreeEnergy: false,        // Uses normal compute resources
  effectAfterCause: true,           // Request → Processing → Response
  canBeBounded: true,               // We can set rate limits and timeouts
  isReproducible: true,             // Same input → same output
  failsSafely: true                 // Returns error codes, doesn't crash
});

console.log(evaluation.decision);      // Decision.ACCEPT
console.log(evaluation.recommendation); // "✅ ACCEPT: Passes physics gate..."
```

### Example 2: Evaluating a Questionable Feature

```typescript
import { CavemanLogic, createSimpleAngleTester } from './caveman-logic';

// Feature that might not scale well
const evaluation = CavemanLogic.evaluate(
  {
    name: "Real-time sync for all users",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
  },
  // Test under different assumptions
  createSimpleAngleTester((angle) => {
    switch(angle) {
      case 1: return false; // Blows up at large scale
      case 2: return true;  // OK at normal speed
      case 3: return false; // Requires too many resources
      case 4: return true;  // Works in stable environment
      case 5: return true;  // OK when isolated
      case 6: return true;  // Works in closed system
    }
    return false;
  })
);

// Result: Decision.REJECT
// "❌ REJECT WITH LOVE: Passes physics but blows up under different assumptions"
```

### Example 3: Quick Sanity Check

```typescript
import { CavemanLogic } from './caveman-logic';

// Quick boolean check
const itComputes = CavemanLogic.doesItCompute(
  false, // No free energy
  true,  // Effect after cause
  true,  // Can be bounded
  true,  // Reproducible
  true   // Fails safely
);

if (!itComputes) {
  console.log("Fuck 'em - doesn't compute");
}
```

---

## Integration with Existing Systems

The Caveman Logic System can be integrated into:

- **Code Review Process**: Evaluate PRs against physics constraints
- **Architecture Decisions**: Validate new system designs
- **Feature Planning**: Gate new features before implementation
- **Incident Response**: Analyze failure modes and reproducibility
- **API Design**: Ensure endpoints are bounded and fail safely

---

## Design Principles

### No Belief Required

You don't have to "believe" in an idea. You test it against constraints.

### Angles, Not Identity

If an idea fails TRIG6, it's not personal. It just doesn't work under those assumptions.

### Constraints Are Reality

Energy, causality, boundaries - these aren't negotiable. They're physics.

### Emotion as Data

Excitement about an idea? Log it. But test the idea anyway.

### Fail Loud, Fail Safe

Silent failures kill systems. Loud failures teach lessons.

---

## Command-Line Interface (Future)

```bash
# Evaluate a concept
caveman-logic eval --concept "my-feature" --config feature.yaml

# Run physics gate only
caveman-logic physics --requiresFreeEnergy false --canBeBounded true ...

# Run TRIG6 test
caveman-logic trig6 --concept "my-feature" --angles 6 --test-script test.js
```

---

## Testing Your Own Concepts

1. **Define the concept** clearly
2. **Answer the 5 physics questions** honestly
3. **Run TRIG6** if it passes physics but seems fuzzy
4. **Accept the result** without emotion
5. **Iterate or discard** based on the outcome

---

## Philosophy

> "That's not arrogance. That's tool discipline."

The Caveman Logic System doesn't make you smarter. It makes you more disciplined. It removes ego from the equation and lets constraints do the talking.

**Does it compute?**
- If not → fuck 'em.
- If maybe → TRIG6 that shit.
- If yes → ship.

That's it. That's the whole operating system.

---

## Contributing

To add new gate types or testing methodologies:

1. Follow the existing pattern in `caveman-logic.ts`
2. Add comprehensive tests
3. Update this documentation
4. Submit a PR with your rationale

Remember: New gates must themselves pass the Caveman Logic System.

---

## License

Part of the Sovereignty Architecture - MIT License

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"No belief. No identity. Just angles."*
