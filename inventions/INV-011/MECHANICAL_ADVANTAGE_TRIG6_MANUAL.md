# MECHANICAL ADVANTAGE
## A TRIG6 Approach to Rope Access Tension Systems

**By Domenic G. Garza**
*SPRAT Level 3 | TWIC Certified | Rope Access Technician*

---

### Publication Information

**Entity:** Strategickhaos DAO LLC  
**EIN:** 39-2900295  
**Copyright:** © 2026 Domenic G. Garza  
**Classification:** Technical Manual / Educational  
**Invention Registry:** INV-011 (TRIG6 Rope Mechanics System)

---

## PREFACE

This book exists because I got tired of watching people guess at tension.

I've spent years on ropes—pipefitting, NDT inspection, structural work. Every day, we make life-or-death calculations about mechanical advantage, load distribution, and system tension. Most technicians learn these as memorized ratios: "2:1 means half the load." But WHY does it mean half the load? Where does that number come from?

The answer is trigonometry. Specifically, the six functions that describe every angle: sine, cosine, tangent, cosecant, secant, and cotangent. I call this system **TRIG6**.

This isn't a book about making rope access more complicated. It's about making it *understandable*. When you know WHY a 3:1 system multiplies force, you can improvise systems that aren't in any manual. When you understand the geometry of deviation angles, you can feel when something is wrong before it fails.

This book is for:
- Rope access technicians who want to understand the math behind the work
- Riggers who need to calculate loads in the field
- Rescue teams building hauling systems
- Anyone who's ever wondered "where do these numbers come from?"

No calculus required. Just triangles.

Let's get to work.

—Dom  
*Node 137, Texas*  
*January 2026*

---

## TABLE OF CONTENTS

### PART I: FOUNDATIONS

1. **The Language of Force**
   - What is tension?
   - Vectors: magnitude and direction
   - The rope as force transmission line

2. **TRIG6: Six Functions, One Circle**
   - The unit circle explained
   - Sine: vertical component
   - Cosine: horizontal component
   - Tangent: the ratio
   - The reciprocals: csc, sec, cot
   - Why all six matter in rope work

3. **Reading Angles in the Field**
   - Estimating angles without instruments
   - The fist method (10° per fist)
   - Reference angles every rigger should know
   - Converting between degrees and ratios

### PART II: MECHANICAL ADVANTAGE SYSTEMS

4. **Simple Pulleys: The 1:1 System**
   - Change of direction vs. mechanical advantage
   - Why a redirect pulley doesn't multiply force
   - Tension analysis: what the anchor really sees

5. **The 2:1 System**
   - How doubling works geometrically
   - Building a 2:1 from first principles
   - TRIG6 analysis: where the force goes
   - Field applications

6. **The 3:1 (Z-Rig)**
   - The classic rescue system
   - Compound advantage explained
   - Calculating actual vs. theoretical MA
   - Friction losses and efficiency

7. **The 4:1 and Beyond**
   - Piggyback systems
   - Complex compounds
   - When more MA isn't better
   - The speed-force tradeoff

8. **Block and Tackle Systems**
   - Traditional rigging meets rope access
   - Counting sheaves for MA
   - Standing vs. running line
   - Historical context

### PART III: ANGLES AND TENSION

9. **Deviation Angles**
   - Why bent ropes see more tension
   - The deviation formula: T = L / (2 × cos(θ/2))
   - Critical angles: 90°, 120°, 150°
   - When deviation kills your MA

10. **Highlines and Horizontal Systems**
    - The sag problem
    - Tension vs. span vs. load
    - Why you can't have a perfectly tight highline
    - Calculating anchor loads

11. **Bipod and Tripod Geometry**
    - Leg angles and load distribution
    - The 60° sweet spot
    - When tripods become unstable
    - TRIG6 analysis of multi-leg systems

12. **Offset Loads and Side-Pull**
    - What happens when the load isn't centered
    - Calculating unequal leg tensions
    - Rigging for angled pulls
    - Dynamic considerations

### PART IV: FIELD CALCULATIONS

13. **Quick Reference Formulas**
    - The formulas you'll actually use
    - Simplified calculations for field work
    - Safety factors and when to apply them
    - Cheat sheets you can laminate

14. **Tension Measurement Tools**
    - Spring scales and dynamometers
    - Electronic load cells
    - The "calibrated arm" method
    - Improvised measurement

15. **Building Calculation Tools**
    - The TRIG6 slide rule concept
    - Phone apps vs. paper tools
    - Building your own reference cards
    - The PCS-1 stencil for rope angles

16. **Failure Analysis**
    - What breaks and why
    - Reading damage patterns
    - Post-incident calculations
    - Learning from near-misses

### PART V: ADVANCED TOPICS

17. **Dynamic Loading**
    - Static vs. dynamic forces
    - Fall factor explained
    - Impact force calculations
    - Why dynamics change everything

18. **Knot Efficiency**
    - Why knots reduce strength
    - Common knot efficiencies
    - Choosing knots for the application
    - Bend vs. hitch vs. loop

19. **System Integration**
    - Combining MA with deviation
    - Multi-anchor systems
    - Redundancy calculations
    - The complete picture

20. **The TRIG6 Method**
    - Putting it all together
    - A systematic approach to tension analysis
    - Case studies from the field
    - Developing intuition

### APPENDICES

A. **TRIG6 Reference Tables**
   - Complete values for 0°-360° in 5° increments
   - Common rope access angles
   - Quick lookup charts

B. **Rope and Hardware Data**
   - Common rope strengths (MBS/WLL)
   - Pulley efficiencies
   - Carabiner and connector ratings
   - Hardware compatibility

C. **Formulas Summary**
   - All formulas in one place
   - Derivations for the curious
   - Unit conversions

D. **Glossary**
   - Rope access terminology
   - Rigging terms
   - Physics vocabulary

E. **Standards and Regulations**
   - SPRAT references
   - IRATA standards
   - OSHA requirements
   - ANSI guidelines

---

## CHAPTER 1: The Language of Force

### What is Tension?

Every time you clip into a rope, you're asking that rope to hold you. The rope responds by developing **tension**—an internal force that resists being pulled apart.

Tension is measured in units of force:
- **Pounds-force (lbf)** - US customary
- **Kilonewtons (kN)** - Metric/international
- **Kilograms-force (kgf)** - Sometimes used, technically mass not force

Quick conversions:
```
1 kN ≈ 225 lbf
1 kN ≈ 102 kgf
1000 lbf ≈ 4.45 kN
```

**Your body weight** (say, 200 lbs with gear) creates about **0.9 kN** of force when you're just hanging. That's your baseline. Everything else—mechanical advantage, deviation angles, dynamic loading—modifies this number.

### Vectors: Magnitude and Direction

Force is a **vector**, meaning it has two properties:
1. **Magnitude** - How much force (e.g., 200 lbs)
2. **Direction** - Which way it pulls (e.g., straight down)

This is where trigonometry enters. When a rope isn't pulling straight up or straight down, we need to break the force into **components**:

```
        ↑ Vertical component (resists gravity)
        │
        │   ╱ Rope at angle θ
        │  ╱
        │ ╱
        │╱θ
        ●────→ Horizontal component (pulls sideways)
      Load
```

The rope tension **T** splits into:
- **Vertical component:** T × cos(θ)
- **Horizontal component:** T × sin(θ)

Where **θ** is the angle from vertical.

This is TRIG6 in action. We'll use this decomposition constantly.

### The Rope as Force Transmission Line

A key insight: **tension is constant throughout an ideal rope.**

If you pull one end with 100 lbs, the other end pulls back with 100 lbs. The rope transmits force without changing its magnitude (in an ideal case—friction and pulley efficiency modify this in reality).

This means:
- Every point along the rope experiences the same tension
- Tension doesn't "build up" as you go
- The anchor sees exactly what you put into the system

When we add pulleys, we're not creating force—we're redirecting it and allowing the same rope to pull on the load multiple times.

---

## CHAPTER 2: TRIG6 — Six Functions, One Circle

### The Unit Circle Explained

Imagine a circle with radius = 1, centered at the origin. This is the **unit circle**, and it's the foundation of all trigonometry.

```
                    90° (π/2)
                       │
                       │  (0, 1)
                       │
          II           │           I
     ┌─────────────────┼─────────────────┐
     │                 │                 │
     │      ╱          │          ╲      │
     │    ╱            │            ╲    │
180° │  ╱      θ       │              ╲  │ 0°
(π)  ●─────────────────┼─────────────────● 
(-1,0)╲                │                ╱(1,0)
     │  ╲              │              ╱  │
     │    ╲            │            ╱    │
     │      ╲          │          ╱      │
     │                 │                 │
     └─────────────────┼─────────────────┘
          III          │          IV
                       │
                       │  (0, -1)
                       │
                    270° (3π/2)
```

For any angle θ, draw a line from the center at that angle. Where it hits the circle gives you:
- **x-coordinate = cos(θ)**
- **y-coordinate = sin(θ)**

### The Six Functions

**TRIG6** = the complete set of trigonometric functions:

| Function | Formula | Rope Access Meaning |
|----------|---------|---------------------|
| **sin(θ)** | opposite/hypotenuse | Horizontal pull fraction |
| **cos(θ)** | adjacent/hypotenuse | Vertical support fraction |
| **tan(θ)** | sin/cos = opposite/adjacent | Sideways-to-vertical ratio |
| **csc(θ)** | 1/sin | Tension multiplier for horizontal |
| **sec(θ)** | 1/cos | Tension multiplier for vertical |
| **cot(θ)** | cos/sin = 1/tan | Vertical-to-sideways ratio |

### Key Angles Every Rigger Must Know

| Angle | sin | cos | tan | What It Means |
|-------|-----|-----|-----|---------------|
| **0°** | 0 | 1 | 0 | Rope vertical—all force is lift |
| **30°** | 0.50 | 0.87 | 0.58 | Moderate angle—87% lift, 50% side |
| **45°** | 0.71 | 0.71 | 1.0 | Equal horizontal and vertical |
| **60°** | 0.87 | 0.50 | 1.73 | Steep angle—only 50% lift! |
| **90°** | 1 | 0 | ∞ | Horizontal—no lift, all side pull |

**Critical insight for rope work:**
At **60° from vertical**, you've lost half your lifting capacity. The rope tension goes UP to compensate.

At **90°** (horizontal), you'd need infinite tension to support any load. This is why horizontal highlines always sag—they MUST have an angle to work.

### The TRIG6 Vector

For any angle, the complete state is:

```
TRIG6(θ) = [sin(θ), cos(θ), tan(θ), csc(θ), sec(θ), cot(θ)]
```

Example at 30°:
```
TRIG6(30°) = [0.500, 0.866, 0.577, 2.000, 1.155, 1.732]
```

This vector tells you everything about force distribution at that angle.

---

## CHAPTER 3: Reading Angles in the Field

### Estimating Without Instruments

You won't always have a protractor hanging 200 feet up. Learn to estimate:

**The Fist Method:**
- Hold your fist at arm's length
- Each fist width ≈ 10°
- Stack fists from vertical to rope line
- Count fists × 10° = approximate angle

**Body References:**
- Arm straight out from shoulder = 90° from vertical
- 45° = halfway between vertical and horizontal
- 30° = "one o'clock" if vertical is noon
- 60° = "two o'clock"

**Visual Calibration:**
```
     │         │╲        │ ╲        │  ╲        ────
     │         │ ╲       │  ╲       │   ╲       
     │         │  ╲      │   ╲      │    ╲      
     │         │   ╲     │    ╲     │     ╲     
     ↓         ↓    ↓    ↓     ↓    ↓      ↓    
    0°        15°   30°   45°   60°   90°
```

### Reference Angles Table

Memorize these. They're your field constants:

| Angle | cos(θ) | Meaning |
|-------|--------|---------|
| 0° | 1.00 | 100% of tension is useful lift |
| 15° | 0.97 | 97% lift—barely noticeable loss |
| 30° | 0.87 | 87% lift—significant but workable |
| 45° | 0.71 | 71% lift—losing almost a third |
| 60° | 0.50 | 50% lift—half your MA is gone! |
| 75° | 0.26 | 26% lift—system is struggling |
| 90° | 0.00 | 0% lift—horizontal doesn't lift |

---

## CHAPTER 4: Simple Pulleys — The 1:1 System

### Change of Direction vs. Mechanical Advantage

A single pulley does one of two things:
1. **Redirect** the rope (change direction, no MA gain)
2. **Create MA** (when configured correctly)

**Redirect Pulley (1:1):**
```
    ══════════╗
              ║ Anchor
         ┌────●────┐
         │    │    │
         │   [P]   │
         │    │    │
         └────┼────┘
              │
              │
              ●  Load
              
    Pull DOWN with 100 lbs → Load feels 100 lbs UP
    No mechanical advantage—just direction change
```

**Why?** The load hangs on ONE strand of rope. One strand = 1:1.

### What the Anchor Really Sees

Here's what people get wrong: **the anchor sees DOUBLE the load tension in a redirect.**

```
    ══════════╗
         ↓ 200 lbs (anchor sees T + T)
         ┌────●────┐
         │    │    │
    100↓ │   [P]   │ ↓100  (rope tension each side)
         │    │    │
         └────┼────┘
              │
              ↓ 100 lbs
              ●  Load
```

The pulley is pulled down by BOTH strands. Each strand has 100 lbs tension. Total on anchor = 200 lbs.

**Field rule:** Redirect anchors see 2× the load (minus friction savings).

---

## CHAPTER 5: The 2:1 System

### How Doubling Works Geometrically

The simplest mechanical advantage: make the load hang on TWO strands.

```
    ══════════╗
              ║ Anchor
         ┌────●────┐
         │         │
         │        [P] ← Pulley at anchor
         │         │
         │    ┌────┘
         │    │
         │   [P] ← Pulley on load (the "traveling" pulley)
         │    │
         └────┼────┘
              │
              ●  Load (200 lbs)
              
    Each strand carries: 200 ÷ 2 = 100 lbs
    You pull with: 100 lbs
    Mechanical Advantage: 2:1
```

### The Math (TRIG6 Approach)

The load's weight distributes across all supporting strands.

For **n** strands supporting the load:
```
Tension per strand = Load ÷ n
Your pull = Tension per strand
MA = Load ÷ Your pull = n
```

For 2:1:
- Strands supporting load: 2
- Load: 200 lbs
- Tension per strand: 100 lbs
- MA: 200 ÷ 100 = **2:1**

### The Trade-Off

You don't get something for nothing. The trade-off is **distance:**

```
MA × Pull Distance = Load Travel Distance

For 2:1:
  Pull 2 feet of rope → Load rises 1 foot
  
For 3:1:
  Pull 3 feet of rope → Load rises 1 foot
```

Higher MA = easier pull but more rope to haul.

---

## CHAPTER 9: Deviation Angles

### Why Bent Ropes See More Tension

This is where TRIG6 becomes critical for safety.

When a rope bends around a pulley or over an edge, the tension **increases** in the rope near the bend.

```
    Straight pull:
    ──────────●────────── T = Load
    
    90° deviation:
           ╱
          ╱
    ─────●      T = Load × 1.41 (= √2)
          ╲
           ╲
```

### The Deviation Formula

For a rope bent through angle **θ** (total bend, not half):

```
T_rope = Load / (2 × cos(θ/2))
```

Or equivalently:
```
T_rope = Load × sec(θ/2) / 2
```

This is **TRIG6 in action**: the secant function tells you the tension multiplier.

### Critical Angles Table

| Deviation θ | θ/2 | cos(θ/2) | Tension Multiplier |
|-------------|-----|----------|-------------------|
| 0° | 0° | 1.000 | 1.00× (no bend) |
| 30° | 15° | 0.966 | 1.04× |
| 60° | 30° | 0.866 | 1.15× |
| 90° | 45° | 0.707 | **1.41×** |
| 120° | 60° | 0.500 | **2.00×** |
| 150° | 75° | 0.259 | **3.86×** |
| 170° | 85° | 0.087 | **11.5×** |

**CRITICAL:** At 120° deviation, rope tension DOUBLES. At 150°, it nearly quadruples!

### Field Implications

When you run a rope over an edge or through a sharp redirect:
- **Check the angle**
- **Calculate the tension multiplier**
- **Verify hardware is rated for actual tension**

Example:
- Load: 300 lbs
- Deviation at edge: 120°
- Actual rope tension: 300 × 2.0 = **600 lbs**
- Your 22 kN carabiner (4,950 lbs) is fine
- Your 9 kN sling (2,025 lbs) is fine
- But your edge is now seeing 600 lbs, not 300!

---

## CHAPTER 10: Highlines and Horizontal Systems

### The Sag Problem

You cannot have a perfectly horizontal highline under load. It's physically impossible.

**Why?** A horizontal rope has cos(90°) = 0, meaning zero vertical component. To support ANY load, the rope must have an angle.

```
    Anchor ●─────────────────────────────● Anchor
            ╲                           ╱
             ╲         SAG            ╱
              ╲         ↓           ╱
               ╲       ●         ╱   ← Load
                ╲     ╱│╲      ╱
                 ╲   ╱ │ ╲   ╱
                  ╲ ╱  │  ╲ ╱
                   θ   │   θ
                       │
                       ↓ W (weight)
```

### The Highline Formula

For a load **W** at the center of a highline:

```
T = W / (2 × sin(θ))

Where θ = angle of rope from horizontal (the sag angle)
```

Or using TRIG6:
```
T = W × csc(θ) / 2
```

### Tension vs. Sag Table

For a 200 lb load at center:

| Sag Angle θ | sin(θ) | Tension Each Side |
|-------------|--------|-------------------|
| 1° | 0.017 | **5,730 lbs** (rope breaks!) |
| 5° | 0.087 | **1,147 lbs** |
| 10° | 0.174 | **575 lbs** |
| 15° | 0.259 | **386 lbs** |
| 30° | 0.500 | **200 lbs** |
| 45° | 0.707 | **141 lbs** |

**The lesson:** Tight highlines = extreme tension. Allow sag!

Industry standard: **Minimum 10° sag angle** (often more).

---

## APPENDIX A: TRIG6 Reference Tables

### Common Angles (0° - 90°)

| θ | sin(θ) | cos(θ) | tan(θ) | csc(θ) | sec(θ) | cot(θ) |
|---|--------|--------|--------|--------|--------|--------|
| 0° | 0.000 | 1.000 | 0.000 | ∞ | 1.000 | ∞ |
| 5° | 0.087 | 0.996 | 0.087 | 11.47 | 1.004 | 11.43 |
| 10° | 0.174 | 0.985 | 0.176 | 5.76 | 1.015 | 5.67 |
| 15° | 0.259 | 0.966 | 0.268 | 3.86 | 1.035 | 3.73 |
| 20° | 0.342 | 0.940 | 0.364 | 2.92 | 1.064 | 2.75 |
| 25° | 0.423 | 0.906 | 0.466 | 2.37 | 1.103 | 2.14 |
| 30° | 0.500 | 0.866 | 0.577 | 2.00 | 1.155 | 1.73 |
| 35° | 0.574 | 0.819 | 0.700 | 1.74 | 1.221 | 1.43 |
| 40° | 0.643 | 0.766 | 0.839 | 1.56 | 1.305 | 1.19 |
| 45° | 0.707 | 0.707 | 1.000 | 1.41 | 1.414 | 1.00 |
| 50° | 0.766 | 0.643 | 1.192 | 1.31 | 1.556 | 0.84 |
| 55° | 0.819 | 0.574 | 1.428 | 1.22 | 1.743 | 0.70 |
| 60° | 0.866 | 0.500 | 1.732 | 1.15 | 2.000 | 0.58 |
| 65° | 0.906 | 0.423 | 2.145 | 1.10 | 2.366 | 0.47 |
| 70° | 0.940 | 0.342 | 2.747 | 1.06 | 2.924 | 0.36 |
| 75° | 0.966 | 0.259 | 3.732 | 1.04 | 3.864 | 0.27 |
| 80° | 0.985 | 0.174 | 5.671 | 1.02 | 5.759 | 0.18 |
| 85° | 0.996 | 0.087 | 11.43 | 1.00 | 11.47 | 0.09 |
| 90° | 1.000 | 0.000 | ∞ | 1.00 | ∞ | 0.00 |

---

## ABOUT THE AUTHOR

**Domenic G. Garza** is a SPRAT Level 3 certified rope access technician with years of experience in industrial services including pipefitting, NDT inspection, and structural work. He holds a TWIC federal credential and is pursuing dual degrees in Computer Science and Cybersecurity.

Dom developed the TRIG6 framework as a way to unify the mathematical principles underlying rope access, rigging, and mechanical systems. His work focuses on making complex technical knowledge accessible to working professionals.

He operates Strategickhaos DAO LLC, a Wyoming-registered company focused on cybersecurity, AI infrastructure, and technical education.

**Certifications:**
- SPRAT Level 3 (Rope Access)
- TWIC (Transportation Worker Identification Credential)
- NDT Certifications
- RAD 40 Radiography License

**Contact:**
- Entity: Strategickhaos DAO LLC
- Location: Texas (Node 137)
- ORCID: 0009-0005-2996-3526

---

*This book is dedicated to every technician who's done the math in their head while hanging off a structure, trusting their life to geometry.*

---

**END OF PREVIEW**

*Full publication: Coming 2026*
*Pre-orders: Contact strategickhaos.ai*
