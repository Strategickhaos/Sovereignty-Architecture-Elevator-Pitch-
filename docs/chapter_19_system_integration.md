# Chapter 19: System Integration

## Combining MA with Deviation

Real systems layer MA (force reduction) over deviations (tension amps). Friction/dynamics add, but start with geometry.

**Integrated Pull Formula:**
```
Integrated Pull = (Load / MA) × sec(θ/2)
```
*where θ = deviation angle; sec from TRIG6. For systems where the deviation applies to half the system, the effective pull per segment is this value divided by 2.*

### Example: 4:1 MA with 120° Deviation

**Given:**
- Mechanical Advantage: 4:1
- Load: 400 lbs
- Deviation angle: 120°

**Calculation:**
1. **Theoretical pull (no deviation):** 400 / 4 = 100 lbs
2. **Amplified pull (with deviation):** 100 × sec(120°/2) = 100 × sec(60°) = 100 × 2 = 200 lbs

**Field Application:** Calculate per segment—MA before deviation halves amp effect.

---

## Multi-Anchor Systems

Share loads for stability/redundancy. Resolve vectors: Break tensions into components, sum to zero horizontal, Load vertical.

### Vector Resolution Technique (2-3 Anchors)

**Steps:**
1. **Draw:** Load pointing down, anchors at angles θᵢ from vertical
2. **Set up equations:**
   - Horizontal balance: Σ Tᵢ sin(θᵢ) = 0
   - Vertical support: Σ Tᵢ cos(θᵢ) = Load
3. **Solve:** Assume symmetry or iterate (e.g., Python/SymPy for field app)

### Unequal Anchor Example

**Given:**
- Load: 300 lbs
- Anchor 1: 0° (straight up)
- Anchor 2: 45° from vertical (assume pulling at an angle, creating horizontal and vertical components)

**Note:** For a statically balanced system with one vertical anchor, the second anchor would need to provide only vertical support (no net horizontal force). In practice, this typically requires three anchors or the angled anchor must be part of a more complex geometry.

**Simplified two-anchor scenario (assuming minimal horizontal offset):**

**Equations:**
```
T₁ cos(0°) + T₂ cos(45°) = 300  (vertical balance)
T₁ sin(0°) = T₂ sin(45°)         (horizontal balance if symmetric opposing forces)
```

**TRIG6 Application:** Use tan(θ) for ratios—T_horizontal / T_vertical = tan(θ)

**For practical multi-anchor resolution:**
Use matrix methods or computational tools (Python/SymPy) to solve systems with more than 2 anchors at varying angles. Three-anchor systems provide better stability and clearer vector resolution.

---

## Tripod Vector Resolution

### Equilateral Configuration (60° legs)

**Setup:**
```
   A1  
  /  \  
A2   A3  
  \ /  
   Load
```

**Calculation:**
Each anchor tension: T = Load / (3 × cos(60°))

**Steps:**
1. Each leg at 60° from vertical
2. Vertical components: 3 × T × cos(60°) = 3 × T × 0.5 = Load
3. **Solve:** T = Load / 1.5 ≈ 0.667 × Load

**Example:** 300 lbs load → Each anchor: T = 300 / 1.5 = 200 lbs

**Component Analysis:**
- Horizontal components cancel (symmetry)
- Vertical sum: 3 × T × 0.5 = Load → T = Load / 1.5

---

## Redundancy Calculations

Backup against single failure. Design for N-1 redundancy.

### Dual Anchor System

**Requirements:**
- Primary + secondary
- Each rated ≥ Load × SF
- Safety Factors: 5:1 (static) / 10:1 (dynamic)

**Calculation:**
```
System WLL = Min(Primary, Secondary) after failure
```

**Example:** Dual 10 kN anchors
- Pre-failure: Shared load (5 kN each for 10 kN total system)
- Post-failure: Remaining anchor carries full 10 kN
- Must meet: Remaining ≥ Load × SF

### Tri-Redundant System (N=3)

**Configuration:** Equal load sharing
- Normal operation: Each carries Load/3
- Post-failure: Remaining 2 share Load

**Calculation:**
```
Post-failure tension per anchor: T_post = (Load / 2) / cos(θ)
```

**Example: 300 lbs, 3 anchors at 60°, SF=5 (static)**

**Pre-failure:**
- Load per leg: 300 / 3 = 100 lbs
- Actual tension: T = 100 / cos(60°) = 100 / 0.5 = 200 lbs
- Required rating: 200 × 5 = 1000 lbs per anchor (meets 1500 lbs rated)

**Post-failure (one anchor fails):**
- Remaining anchors: 2
- New load per anchor: 300 / 2 = 150 lbs
- Vector angle changes: 120° deviation between remaining anchors
- Recalculate with new geometry: T_post = 150 / cos(new_θ)

### Failure Modes to Consider

1. **Knot slip:** Efficiency drops → recalculate effective strength
2. **Anchor shift:** Angle θ changes → re-resolve vectors
3. **Dynamic shock load:** Apply impact factor

**TRIG6 Applications:**
- `csc(θ)` amplifies unequal loading
- `cot(θ)` helps rebalance post-failure

---

## Complete Picture: Integrated Analysis

### Step-by-Step Methodology

1. **Geometry:** Define angles, MA strands, anchor positions
2. **Vectors:** Resolve sin/cos components
3. **Multipliers:** Apply sec/csc for amplifications
4. **Redundancy:** Simulate failure, recalculate loads
5. **Dynamics:** Apply impact factor: × (1 + √(2 × FF))

### Case Study: Industrial Rigging

**Scenario:**
- 3:1 Mechanical Advantage
- 90° deviation angle
- Dual anchors at 30° from vertical
- Fall Factor 1 possible

**Static Analysis:**
1. Base pull: Load / 3 = 100 lbs (assume 300 lbs load)
2. Deviation amplification: 100 × sec(45°) = 100 × 1.41 = 141 lbs
3. Per anchor: 141 / 2 = 70.5 lbs
4. Anchor vector: 70.5 / cos(30°) = 70.5 / 0.866 = 81 lbs per anchor

**Dynamic Peak (FF=1):**
```
Impact = 141 × (1 + √(2 × 1)) = 141 × (1 + 1.414) = 141 × 2.414 ≈ 340 lbs
Per anchor: 340 / 2 = 170 lbs
Anchor vector: 170 / cos(30°) ≈ 196 lbs
```

**Safety Check:**
- Anchor rating with SF=10: Must be ≥ 196 × 10 = 1960 lbs
- System holds with proper anchor selection

---

## Field Pattern: "Vector Balance Check"

**Quick Validation:**
1. ✓ Do horizontal components sum to zero? → Stable
2. ✓ Do vertical components equal Load? → Supported
3. ✓ If failure shifts θ, recalculate amplifications
4. ✓ Use app/sketchpad for multi-anchor systems

**Pro Rule:** For complex systems (3+ anchors, unequal angles), use computational tools first, validate with field measurements.

---

## Disclaimer

**Educational Content:** This chapter presents theoretical calculations for understanding rope systems. Always verify against current industry standards (SPRAT, IRATA, NFPA) and consult qualified professionals for real-world applications. Field conditions introduce additional factors (friction, edge loading, environmental) not fully covered in these examples.

---

*Chapter 19 completes the integration of TRIG6 principles with practical multi-component systems. Use these techniques as a foundation, but always prioritize safety margins and professional oversight in critical applications.*
