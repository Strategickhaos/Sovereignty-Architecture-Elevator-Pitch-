# Chapter 17: Dynamic Loading

## Introduction

When a falling mass is stopped by a rope system, the peak force experienced can be many times greater than the static weight. Understanding dynamic loading is critical for safe rigging, fall protection systems, and rescue operations.

This chapter presents field-appropriate models for estimating impact forces and introduces TRIG6 angle amplification effects in dynamic systems.

## Impact Force Model

### Simplified Impact Estimate

For field use, we can estimate peak impact force using:

**Impact ≈ W × (1 + √(2 × FF))**

Where:
- **W** = weight of falling mass
- **FF** = fall factor (fall distance / rope length)

**This model assumes a dynamic rope with sufficient elongation; low-stretch or static systems will experience higher peak forces.**

This approach is appropriate for field-facing applications because:
- It assumes elastic rope behavior
- It intentionally avoids calculus and energy integrals
- It produces conservative but realistic peak values
- It matches the intuition techs already have: "Fall factor matters more than weight"

### Fall Factor Explained

Fall factor is the ratio of how far you fall to how much rope is available to absorb the energy:

**FF = Fall Distance / Rope Length**

Examples:
- Fall 2m on 10m of rope: FF = 0.2 (mild impact)
- Fall 5m on 5m of rope: FF = 1.0 (severe impact)
- Fall 4m on 2m of rope: FF = 2.0 (maximum possible, extremely severe)

**FIELD PATTERN — FF Cliff at 1**

- **What it is:** Fall factors above FF = 1.0 create exponentially higher forces
- **What it does:** System loads can exceed rope or anchor ratings, causing failure
- **What to do about it:** Shorten exposed rope length; position protection points to keep FF < 0.5

### Impact Force Examples

Using W = 100 kg (roughly 1000 N static load):

| Fall Factor | Impact Force | Peak Load |
|-------------|--------------|-----------|
| 0.1 | 100 × (1 + √0.2) = 145 kg | ~1.5× static |
| 0.5 | 100 × (1 + √1.0) = 200 kg | ~2.0× static |
| 1.0 | 100 × (1 + √2.0) = 241 kg | ~2.4× static |
| 2.0 | 100 × (1 + √4.0) = 300 kg | ~3.0× static |

Note how impact increases non-linearly. A fall factor of 2.0 creates roughly double the force of FF = 0.5, even though the fall factor itself only increased by 4×.

## TRIG6 Angle Amplification

When dynamic loading occurs in a system with deviation or angles, the effective force on anchor points is amplified by the secant of the deviation angle.

### The Secant Multiplier

**Effective Impact = Impact Force × sec(θ)**

Where:
- **θ** = angle of deviation from vertical
- **sec(θ)** = 1 / cos(θ) = secant function

This is not "new physics"—it's the correct application of component resolution. When force must resolve against a non-vertical line, secant becomes the tension multiplier.

### Why Secant Matters

In a vertical system, the rope carries the full load. When the rope is at an angle θ from vertical:

- The rope must carry **more** tension to support the same vertical load
- That additional tension is exactly **sec(θ)** times the vertical force
- At small angles, this effect is minor
- At large angles, this effect dominates

### Angle Amplification Examples

Consider a 200 kg impact force (from FF = 0.5 example above):

| Deviation Angle | sec(θ) | Effective Impact | Notes |
|-----------------|--------|------------------|-------|
| 0° (vertical) | 1.00 | 200 kg | No amplification |
| 15° | 1.04 | 208 kg | Minimal effect |
| 30° | 1.15 | 230 kg | **15% increase** |
| 45° | 1.41 | 282 kg | 41% increase |
| 60° | 2.00 | 400 kg | **Load doubles** |

**The 30° and 60° cases are pedagogically powerful** because they show how quickly angle effects compound with dynamic loading.

### Field Applications

#### Highlines
When a load falls on a tensioned highline, the angle from vertical at the attachment point determines the force amplification. A loaded highline already has high tension; adding dynamic loading with angle amplification can exceed system capacity.

#### Deviation Anchors
If a climber falls and the rope runs through a deviation at an angle, that deviation anchor sees the amplified force. Protection points must account for both impact force AND angular amplification.

#### Traverse Systems
Angled rope segments in traverse systems experience higher tensions during dynamic events. The shallower the angle (closer to horizontal), the higher the amplification.

## Combining Fall Factor and Angle Effects

In real systems, both fall factor and angle amplification occur together:

**Total System Force = W × (1 + √(2 × FF)) × sec(θ)**

Example: 100 kg person, FF = 1.0, deviation angle = 30°
- Base impact: 100 × (1 + √2) = 241 kg
- With angle: 241 × sec(30°) = 241 × 1.15 = **277 kg**

That's 2.77× the static load, compared to 2.41× without considering the angle.

## Practical Risk Management

### Keep Fall Factors Low
- Position protection frequently
- Minimize slack in the system
- Use dynamic rope where appropriate
- Target FF < 0.5 for normal operations

### Minimize Deviation Angles
- Route ropes as vertically as possible
- Use directional anchors to maintain alignment
- Be aware of rope angles under all loading conditions
- Design systems to minimize geometric amplification

### Design for Dynamic Loading
- Never rely on static calculations alone
- Build safety margins into anchor strength
- Use dynamic components (rope stretch, energy absorbers) strategically
- Test critical systems under controlled conditions

### Understand System Behavior
- Know your rope's dynamic properties
- Recognize high-risk configurations
- Train for fall scenarios
- Have rescue plans that account for dynamic loading

## Interactive Figures

Static figures showing impact force curves, fall factor relationships, and angle amplification effects are included in this chapter.

**Interactive versions of Figures 17-1 through 17-3 are available at:**
**strategickhaos.ai/trig6/interactive**

These interactive tools allow you to:
- Adjust fall factor and see impact force change in real-time
- Explore angle amplification at any deviation angle
- Combine effects to understand total system loading
- Visualize force vectors in dynamic scenarios

## Summary

Dynamic loading introduces forces significantly higher than static weights. The key principles are:

1. **Fall factor** is the primary driver of impact force
2. **Impact force scales with √(2 × FF)**, not linearly with fall distance
3. **Angle amplification** multiplies impact forces by sec(θ)
4. **Combined effects** can create dangerous loading conditions
5. **Risk management** focuses on minimizing both fall factors and deviation angles

Understanding these relationships allows technicians to:
- Design safer rope systems
- Predict failure modes before they occur
- Make informed decisions about anchor placement and rope routing
- Respond appropriately to dynamic loading events

This foundation in dynamic loading, combined with the geometric principles from Chapter 9, prepares us for integrated system analysis in Chapter 19.

---

*Next: Chapter 19 — System Integration*
