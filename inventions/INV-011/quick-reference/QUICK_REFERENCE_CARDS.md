# TRIG6 Quick Reference Cards
## Field-Ready Calculation Tools

---

## Card 1: Mechanical Advantage

```
┌─────────────────────────────────────────┐
│     MECHANICAL ADVANTAGE QUICK REF      │
├─────────────────────────────────────────┤
│  Count strands supporting the load      │
│  That's your theoretical MA             │
│                                         │
│  1:1 = redirect only (no advantage)     │
│  2:1 = half the pull, 2× the rope       │
│  3:1 = third the pull, 3× the rope      │
│  4:1 = quarter pull, 4× the rope        │
│                                         │
│  Actual MA = Theoretical × Efficiency   │
│  Typical pulley efficiency: 85-95%      │
│                                         │
│  5:1 system with 90% pulleys:           │
│  Actual MA ≈ 5 × 0.9 × 0.9 = 4.05      │
└─────────────────────────────────────────┘
```

---

## Card 2: Deviation Angles

```
┌─────────────────────────────────────────┐
│      DEVIATION TENSION MULTIPLIER       │
├─────────────────────────────────────────┤
│  T = Load / (2 × cos(θ/2))              │
│                                         │
│  Deviation │ Multiplier │ 100 lb load   │
│  ──────────┼────────────┼─────────────  │
│     30°    │   1.04×    │   104 lbs     │
│     60°    │   1.15×    │   115 lbs     │
│     90°    │   1.41×    │   141 lbs     │
│    120°    │   2.00×    │   200 lbs     │
│    150°    │   3.86×    │   386 lbs     │
│                                         │
│  ⚠️  120°+ deviation = DOUBLE+ tension  │
└─────────────────────────────────────────┘
```

---

## Card 3: Highline Tensions

```
┌─────────────────────────────────────────┐
│         HIGHLINE TENSION (CENTER)       │
├─────────────────────────────────────────┤
│  T = Load / (2 × sin(sag angle))        │
│                                         │
│  Sag Angle │ Multiplier │ 200 lb load   │
│  ──────────┼────────────┼─────────────  │
│     5°     │   5.74×    │  1,147 lbs    │
│    10°     │   2.88×    │    575 lbs    │
│    15°     │   1.93×    │    386 lbs    │
│    30°     │   1.00×    │    200 lbs    │
│    45°     │   0.71×    │    141 lbs    │
│                                         │
│  ⚠️  NEVER rig tighter than 10° sag!    │
└─────────────────────────────────────────┘
```

---

## Card 4: Critical Angles

```
┌─────────────────────────────────────────┐
│      CRITICAL ANGLES - MEMORIZE         │
├─────────────────────────────────────────┤
│  Angle │ sin   │ cos   │ What It Means  │
│  ──────┼───────┼───────┼─────────────── │
│   0°   │ 0.00  │ 1.00  │ All lift       │
│  30°   │ 0.50  │ 0.87  │ 87% lift       │
│  45°   │ 0.71  │ 0.71  │ Equal H/V      │
│  60°   │ 0.87  │ 0.50  │ 50% lift!      │
│  90°   │ 1.00  │ 0.00  │ No lift        │
│                                         │
│  At 60° from vertical, you've lost      │
│  HALF your lifting capacity!            │
└─────────────────────────────────────────┘
```

---

## Card 5: Unit Conversions

```
┌─────────────────────────────────────────┐
│         FORCE UNIT CONVERSIONS          │
├─────────────────────────────────────────┤
│  1 kN ≈ 225 lbf                         │
│  1 kN ≈ 102 kgf                         │
│  1000 lbf ≈ 4.45 kN                     │
│                                         │
│  Quick estimates:                       │
│  • 200 lb person ≈ 0.9 kN               │
│  • 1 ton = 2000 lbs ≈ 9 kN              │
│  • 22 kN carabiner ≈ 5000 lbs           │
│  • 9 kN sling ≈ 2000 lbs                │
│                                         │
│  Always work in same units!             │
└─────────────────────────────────────────┘
```

---

## Card 6: Safety Factors

```
┌─────────────────────────────────────────┐
│          SAFETY FACTORS (SF)            │
├─────────────────────────────────────────┤
│  Working Load Limit (WLL):              │
│    WLL = MBS / Safety Factor            │
│                                         │
│  Typical Safety Factors:                │
│  • SPRAT/IRATA: 10:1 (life safety)     │
│  • OSHA rigging: 5:1 minimum            │
│  • Rescue: 15:1 (conservative)          │
│  • Dynamic loads: 2× static SF          │
│                                         │
│  Example:                               │
│  22 kN rope (MBS) ÷ 10 = 2.2 kN WLL    │
│  = ~500 lbs working load                │
└─────────────────────────────────────────┘
```

---

## Card 7: Rope Angle Estimation

```
┌─────────────────────────────────────────┐
│       FIELD ANGLE ESTIMATION            │
├─────────────────────────────────────────┤
│  THE FIST METHOD:                       │
│  • Hold fist at arm's length            │
│  • Each fist ≈ 10°                      │
│  • Stack from vertical to rope          │
│  • Count × 10 = angle                   │
│                                         │
│  CLOCK METHOD (vertical = 12):          │
│  • 1 o'clock ≈ 30°                      │
│  • 2 o'clock ≈ 60°                      │
│  • 3 o'clock = 90°                      │
│                                         │
│  BODY REFERENCE:                        │
│  Arm straight out = 90° from vertical   │
└─────────────────────────────────────────┘
```

---

## Card 8: TRIG6 Functions

```
┌─────────────────────────────────────────┐
│         TRIG6 FUNCTION SUMMARY          │
├─────────────────────────────────────────┤
│  Function │ Formula │ Rope Meaning      │
│  ─────────┼─────────┼─────────────────  │
│  sin(θ)   │ opp/hyp │ Horizontal pull   │
│  cos(θ)   │ adj/hyp │ Vertical support  │
│  tan(θ)   │ sin/cos │ Side-to-vert ratio│
│  csc(θ)   │ 1/sin   │ Horiz multiplier  │
│  sec(θ)   │ 1/cos   │ Vert multiplier   │
│  cot(θ)   │ cos/sin │ Vert-to-side ratio│
│                                         │
│  All six functions matter in            │
│  complex rigging scenarios!             │
└─────────────────────────────────────────┘
```

---

## Card 9: Pre-Flight Checklist

```
┌─────────────────────────────────────────┐
│         RIGGING PRE-FLIGHT              │
├─────────────────────────────────────────┤
│  □ Anchor rated for 2× load minimum    │
│  □ All hardware properly rated          │
│  □ Deviation angles < 120°              │
│  □ Highline sag ≥ 10°                   │
│  □ MA system efficiency calculated      │
│  □ Safety factor ≥ 10:1                 │
│  □ Edge protection in place             │
│  □ Backup/redundancy verified           │
│  □ Communication plan established       │
│  □ Rescue plan in place                 │
│                                         │
│  When in doubt, ADD SLINGS!             │
└─────────────────────────────────────────┘
```

---

## Card 10: Emergency Quick Refs

```
┌─────────────────────────────────────────┐
│         EMERGENCY CALCULATIONS          │
├─────────────────────────────────────────┤
│  WORST CASE SCENARIOS:                  │
│                                         │
│  Max person + gear: 300 lbs (1.35 kN)  │
│  × 2 (dynamic) = 600 lbs (2.7 kN)      │
│  × 10 (SF) = 6000 lbs (27 kN) MBS     │
│                                         │
│  120° deviation doubles tension!        │
│  Tight highline = rope failure          │
│  No edge pro = cut rope                 │
│                                         │
│  IF IT LOOKS WRONG, IT IS WRONG.        │
│  Trust your gut. Add redundancy.        │
└─────────────────────────────────────────┘
```

---

## Usage Instructions

### Lamination
Print these cards on waterproof paper or laminate them for field use. Recommended size: 4" × 6" (index card size).

### Organization
- Punch hole in corner
- Attach with carabiner to gear loop
- Keep one set in rescue kit
- One set in rigging bag

### Practice
Review these cards:
- Before every job
- During safety briefings
- In training sessions
- After any incident

### Customization
Add your own notes on the back:
- Site-specific data
- Local equipment ratings
- Team contact info
- Common configurations

---

**Remember: These are quick references, not replacements for proper training. When in doubt, consult a qualified rigger or engineer.**

---

*Part of the TRIG6 Rope Mechanics System (INV-011)*  
*© 2026 Domenic G. Garza / Strategickhaos DAO LLC*
