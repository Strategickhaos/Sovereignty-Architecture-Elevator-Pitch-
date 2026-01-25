# TRIG6 Alchemy Visualization Guide

## Understanding Basin Plots and θ-Space Representations

This guide explains how to visualize and interpret TRIG6 encodings of historical alchemy recipes.

---

## 1. Basic θ-Space Plot

### What is θ-Space?

θ-space is a 2D projection of the chemical process parameter space, where:
- **θ** (horizontal axis): Process phase from 0 to 2π
- **R, D, or N** (vertical axis): Resonance, Drift, or Noise values [0-1]

### Example: Lampblack Ink (Zosimos)

```
Process Timeline:
├─────────────┼─────────────────────┼───────────┤
0.0          0.2                  0.6         1.0
(prep)       (mix & grind)        (test)      (done)
θ=0          θ=0.4π               θ=1.2π      θ=2π
```

**θ vs. R (Resonance) Plot:**

```
R (Resonance)
1.0 │
    │           ╱▔▔▔▔▔╲
0.7 │═════════╱        ╲═══════  ← Stable basin
    │        ╱          ╲
0.4 │       ╱            ╲
    │      ╱              ╲
0.0 ├─────┴────────────────┴────
    0    π/4   π/2  3π/4   π   2π
         θ (process phase)

Legend:
═══ = Target resonance (R = 0.7)
╱╲  = Basin boundaries
```

**Interpretation:**
- Process stays in stable basin (R > 0.6) from θ = π/4 to θ = π
- Outside this range, quality degrades (too watery or too thick)
- No catastrophic failures (no danger zones)

---

## 2. Multi-Parameter Comparison

### Comparing R, D, N for a Single Recipe

**Example: Mercury Fixation (Hermes)**

```
Value
1.0 │                    D ▲
    │                     ╱│╲
0.8 │                    ╱ │ ╲
    │        N ▲        ╱  │  ╲
0.6 │         ╱│╲      ╱   │   ╲
    │        ╱ │ ╲    ╱    │    ╲
0.4 │   R  ╱  │  ╲  ╱     │     ╲
    │   ═══   │   ══      │
0.2 │         │           │
    │         │           │
0.0 ├─────────┼───────────┼──────
    0        π/2         π      2π
             θ (process phase)

R (solid) = Resonance (low, ~0.4)
D (dashed) = Drift/toxicity (high, ~0.6)
N (dotted) = Noise (moderate, ~0.5)
```

**Interpretation:**
- Low resonance (R = 0.4): Process doesn't work well
- High drift (D = 0.6): Produces toxic byproducts
- Moderate noise (N = 0.5): Results somewhat variable
- **Conclusion:** Unsafe and ineffective recipe

---

## 3. Danger Zone Visualization

### Unstable θ Regimes

Recipes near θ = π/2, 3π/4, etc. enter **unstable regimes** where |tan(θ)| → ∞.

```
|tan(θ)|
  ∞ │    X           X           X
    │    │           │           │
 10 ├────┼───────────┼───────────┼────
    │   ╱│╲         ╱│╲         ╱│╲
    │  ╱ │ ╲       ╱ │ ╲       ╱ │ ╲
  0 ├─┘  │  └─────┘  │  └─────┘  │  └
    0   π/2   π    3π/2  2π    5π/2  3π
        θ (process phase)

X = Danger zone (|tan(θ)| > 10)
```

**What This Means:**
- Tiny changes in parameters → huge changes in outcome
- Historically: explosions, poisonings, complete failures
- Modern equivalent: Systems approaching critical points

### Example: Aqua Regia (Jabir)

```
θ = 3π/4 (near critical point)

Parameter Sensitivity:
  Small change          Large change
  in temp/time    →     in outcome
       ↓                    ↓
    +5% heat          SAFE ACID
                         or
                    TOXIC FUMES + EXPLOSION
```

---

## 4. Basin Landscape View

### 2D Parameter Space

**Example: Ink Recipe (Pigment vs. Binder Ratio)**

```
Binder
Ratio
 1.0 │ ░░░░░░░░░░░░░░░░░░░░
     │ ░░░░░░░░░░░░░░░░░░░░  ← Too thick (clogs)
 0.8 │ ░░░░░░░░░░░░░░░░░░░░
     │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
 0.6 │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← Optimal basin
     │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
 0.4 │ ░░░░░░░░░░░░░░░░░░░░
     │ ░░░░░░░░░░░░░░░░░░░░  ← Too watery
 0.2 │ ░░░░░░░░░░░░░░░░░░░░
     │
 0.0 ├─────────────────────
     0.2  0.4  0.6  0.8  1.0
          Pigment Ratio

Legend:
▓▓ = Stable basin (f > 0.5)
░░ = Unstable region (f < 0.3)
```

**Fitness Landscape:**

```
f (fitness)
 1.0 │
     │       ╱▔▔▔▔╲
 0.7 │      ╱      ╲      ← Peak of basin
     │     ╱        ╲
 0.4 │    ╱          ╲
     │   ╱            ╲
 0.0 ├──┘              └──
     Low    Optimal    High
        Pigment:Binder
```

---

## 5. Comparative House Analysis

### Success Rate by Tradition

```
Success Rate (% safe recipes)

100% │
     │ ░
  80%│ ░
     │ ░
  60%│ ░  ▓  ▓  ▓
     │ ░  ▓  ▓  ▓
  40%│ ░  ▓  ▓  ▓
     │ ░  ▓  ▓  ▓
  20%│ ░  ▓  ▓  ▓
     │ ░  ▓  ▓  ▓
   0%├─┴──┴──┴──┴─
     H  Z  J  P

H = Hermes (0%)
Z = Zosimos (44%)
J = Jabir (44%)
P = Paracelsus (44%)

░ = Dangerous recipes
▓ = Safe recipes
```

### Average R, D, N by House

```
Value
1.0 │
    │              N
0.8 │             ╱│╲
    │       D    ╱ │ ╲
0.6 │      ╱│╲  ╱  │  ╲    D
    │     ╱ │ ╲╱   │   ╲  ╱│╲
0.4 │    ╱  │  │   │    ╲╱ │ ╲
    │   ╱   │  │   │     │  │  ╲
0.2 │  R    R  R   R     │  │   │
    │  ══   ══ ══  ══    │  │   │
0.0 ├──┴────┴──┴───┴─────┴──┴───┴──
    Hermes Zosimos Jabir Paracelsus

R (═) = Resonance (efficacy)
D (/) = Drift (toxicity)
N (^) = Noise (uncertainty)
```

**Key Insights:**
- Hermes: High D & N, low R → Failed recipes
- Zosimos: Balanced, low D & N → Practical success
- Jabir: Moderate across all → Mixed results
- Paracelsus: High D for some → Medical risks

---

## 6. θ-Class Distribution

### Histogram of θ Values

```
Count
  9 │     ▓
    │     ▓
  8 │     ▓  ▓
    │     ▓  ▓
  6 │     ▓  ▓  ▓
    │     ▓  ▓  ▓
  5 │     ▓  ▓  ▓  ░
    │     ▓  ▓  ▓  ░
  4 │     ▓  ▓  ▓  ░  ░
    │     ▓  ▓  ▓  ░  ░
  2 │  ░  ▓  ▓  ▓  ░  ░  ░  ░
    │  ░  ▓  ▓  ▓  ░  ░  ░  ░
  0 ├──┴──┴──┴──┴──┴──┴──┴──┴──
    π/8 π/6 π/4 π/3 π/2 2π/3 3π/4 5π/6
         θ-class

▓ = Stable regime
░ = Unstable regime (danger zones)
```

**Interpretation:**
- Most recipes cluster in stable regions (π/6 to π/3)
- Dangerous recipes appear near critical points (π/2, 3π/4)
- Very few at extremes (π/8, 5π/6)

---

## 7. Fitness Distribution

### Histogram of Overall Fitness

```
Count
 12 │        ▓
    │        ▓
  9 │        ▓  ▓
    │        ▓  ▓
  8 │        ▓  ▓  ▓
    │        ▓  ▓  ▓
  7 │  ░     ▓  ▓  ▓
    │  ░     ▓  ▓  ▓
    │  ░     ▓  ▓  ▓  ░
    │  ░     ▓  ▓  ▓  ░
  0 ├──┴─────┴──┴──┴──┴──
    ≤0.2  0.2-0.3  0.3-0.5  >0.5
       f (fitness)

░ = Failed recipes
▓ = Successful recipes
```

**Categories:**
- f > 0.5: Excellent (8 recipes) - modern standard
- 0.3 < f ≤ 0.5: Good (12 recipes) - historically successful
- 0.2 < f ≤ 0.3: Marginal (9 recipes) - inconsistent
- f ≤ 0.2: Poor (7 recipes) - failures

---

## 8. NEURO-36 Cross-Mapping Network

### Recipe → Disease Connections

```
Historical Recipes              Disease Codons
                               
CORAL CALX ════════════════════════ GI-012 (antacid)
                               
SPAGYRIC ───────────────────────── INF-008 (inflammation)
                               
MELISSA ────────────────────────── ANX-005 (anxiety)
                               
VERDIGRIS ──────────────────────── INF-011 (antimicrobial)
                               
ANTIMONY ╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳ EPI-032 (seizures)
(UNSAFE)

Legend:
════ = Validated connection (safe & effective)
──── = Hypothesis (safe, needs study)
╳╳╳╳ = Historical only (unsafe)
```

---

## 9. How to Create Your Own Visualizations

### Tools and Libraries

**Python (Matplotlib/Seaborn):**
```python
import matplotlib.pyplot as plt
import numpy as np

# Load recipe data
theta = np.linspace(0, 2*np.pi, 100)
R = lambda t: 0.7 * np.exp(-(t - np.pi)**2 / 0.5)

# Plot basin
plt.plot(theta, R(theta))
plt.xlabel('θ (process phase)')
plt.ylabel('R (resonance)')
plt.title('Lampblack Ink Basin')
plt.axhline(y=0.6, color='r', linestyle='--', label='threshold')
plt.show()
```

**R (ggplot2):**
```r
library(ggplot2)

# Load data
df <- read_csv("TRIG6_ALCHEMICAL_INDEX.yaml")

# Plot house comparison
ggplot(df, aes(x=house, y=R, fill=danger)) +
  geom_boxplot() +
  labs(title="Resonance by House",
       x="Alchemical House",
       y="R (Resonance)")
```

**ASCII/Text Art (for documentation):**
- Use Unicode box-drawing characters: ─│┌┐└┘
- Use block characters: █▓▒░
- Use symbols: ═╱╲▲▼
- Keep plots simple and readable

### Data Sources

1. Parse YAML files directly
2. Use provided summary statistics
3. Calculate fitness: f = R × (1 - D) × (1 - N)
4. Group by house, hazard, or θ-class

---

## 10. Interpretation Guide

### Reading Basin Plots

**Stable Basin:**
- Wide, flat peak
- Gradual slopes
- f > 0.5 over broad range
- **Example:** Bronze alloy (Zosimos)

**Unstable Basin:**
- Narrow, sharp peak
- Steep slopes
- f > 0.5 only in tiny range
- **Example:** Aqua regia (Jabir)

**No Basin (Failure):**
- No peak above threshold
- Low R throughout
- High D or N
- **Example:** Alkahest (Hermes)

### Color Coding Standards

**Hazard Levels:**
- 🟢 GREEN: LOW (safe for study)
- 🟡 YELLOW: MEDIUM (caution required)
- 🟠 ORANGE: HIGH (dangerous)
- 🔴 RED: EXTREME (deadly)

**Fitness Levels:**
- 🟢 GREEN: f > 0.5 (excellent)
- 🟡 YELLOW: 0.3 < f ≤ 0.5 (good)
- 🟠 ORANGE: 0.2 < f ≤ 0.3 (marginal)
- 🔴 RED: f ≤ 0.2 (poor)

---

## Conclusion

These visualizations transform abstract TRIG6 parameters into intuitive geometric representations. Key principles:

1. **θ-space plots** show process evolution over time
2. **Basin landscapes** reveal stable operating regions
3. **Danger zones** highlight unstable regimes
4. **Comparative charts** show patterns across traditions
5. **Network diagrams** connect ancient recipes to modern diseases

Use these tools to explore the dataset and understand which alchemical recipes represent genuine chemical insights versus dead ends.

**Remember:** All visualizations are for educational modeling only. Never use them as guides for practical chemistry.
