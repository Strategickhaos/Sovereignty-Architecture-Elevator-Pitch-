# Chapter 5: TRIG6 as Risk Geometry

**How TRIG6 Models Failures**

---

## Overview

TRIG6 is more than trigonometry—it's a **geometric framework for mapping risks**. Every failure, threat, or uncertainty can be encoded as a point in TRIG6 space, allowing mathematical analysis of:

- **Phase (θ)**: Where are we in the failure lifecycle?
- **Resonance (R)**: How strong are our mitigations?
- **Drift (D)**: How far have we deviated from optimal?
- **Noise (N)**: How uncertain is the situation?
- **Danger Zones**: Are we approaching catastrophic thresholds?

This chapter explains the geometry, the mathematics, and the practical application of TRIG6 to risk mapping.

---

## The Geometry of Risk

### Traditional Risk Matrices

**Classic Approach:**
```
      Low │ Medium │ High
Risk: ────┼────────┼─────
      Green │ Yellow │ Red
```

**Problems:**
- Binary categories (no nuance)
- Static assessment (no dynamics)
- No mathematical framework (can't optimize)
- Ignores phase dependencies (early ≠ late failures)

### TRIG6 Risk Space

**Enhanced Approach:**
Every risk is a 4D vector in phase space:

```
Risk = (θ, R, D, N)

θ ∈ [0, 2π]      - Phase angle (failure lifecycle)
R ∈ [0, 1]       - Resonance (mitigation strength)
D ∈ [0, 1]       - Drift (deviation from ideal)
N ∈ [0, 1]       - Noise (uncertainty level)
```

**Advantages:**
- Continuous values (full nuance)
- Dynamic tracking (θ evolves over time)
- Mathematical optimization (maximize R, minimize D, N)
- Phase-aware (tan θ reveals critical thresholds)

---

## The Four Dimensions Explained

### Dimension 1: Theta (θ) - Phase of Failure

**Concept:** Where are we in the failure lifecycle?

**Geometric Interpretation:**
- θ is an **angle** on the unit circle
- One complete rotation (2π) = full failure cycle
- Different phases have different risk profiles

**Phase Mapping:**

```
θ ∈ [0, π/2):         Early Phase
  - Problem emerging
  - Preventable with modest intervention
  - tan(θ) is small, manageable slope

θ = π/2:              Critical Inflection
  - Tipping point reached
  - tan(θ) → ∞ (vertical asymptote)
  - DANGER ZONE: immediate action required

θ ∈ (π/2, π]:         Mid Phase
  - Failure progressing
  - tan(θ) negative (inverse relationship)
  - Mitigation costs increasing

θ ∈ (π, 3π/2]:        Late Phase
  - Severe degradation
  - tan(θ) large positive again
  - Approaching catastrophe

θ ∈ (3π/2, 2π]:       Catastrophic
  - System failure imminent
  - tan(θ) → -∞ as approaches 2π ≡ 0
  - Rebuild required
```

**Example:**

```python
# Revenue allocation failure (SP-01)
theta_values = {
    "newly_discovered": math.pi/8,      # θ = 0.39, tan = 0.41
    "under_review": math.pi/4,          # θ = 0.79, tan = 1.0
    "critical_meeting": 1.57,           # θ ≈ π/2, tan → ∞
    "post_incident": 3*math.pi/4,       # θ = 2.36, tan = -1.0
}
```

### Dimension 2: Resonance (R) - Mitigation Stability

**Concept:** How strong are our defenses against this failure?

**Geometric Interpretation:**
- R is **amplitude** of the protective wave
- High R = strong, stable mitigations
- Low R = weak, fragile controls

**Resonance Scale:**

```
R ∈ [0.8, 1.0]:   Excellent
  - Multiple redundant mitigations
  - Tested under stress
  - Low probability of failure

R ∈ [0.5, 0.8):   Good
  - Primary mitigation in place
  - Some backup controls
  - Moderate risk remains

R ∈ [0.3, 0.5):   Weak
  - Minimal mitigations
  - Single point of failure
  - High vulnerability

R ∈ [0.0, 0.3]:   Critical
  - No effective controls
  - Failure likely
  - Urgent intervention needed
```

**Example:**

```python
# GPG signature forgery (SP-04)
resonance_evolution = {
    "no_signatures": 0.1,              # Terrible
    "manual_verification": 0.4,        # Weak
    "automated_checks": 0.7,           # Good
    "blockchain_provenance": 0.9,      # Excellent
}
```

### Dimension 3: Drift (D) - Deviation from Optimal

**Concept:** How far have we strayed from the ideal state?

**Geometric Interpretation:**
- D is **displacement** from center
- High D = major deviation, off course
- Low D = minor variance, on track

**Drift Scale:**

```
D ∈ [0.0, 0.2]:   Nominal
  - Within normal operating parameters
  - Minor course corrections suffice

D ∈ (0.2, 0.5]:   Concerning
  - Noticeable deviation
  - Trending toward danger
  - Active monitoring required

D ∈ (0.5, 0.8]:   Severe
  - Major deviation from spec
  - Urgent corrective action needed
  - Mission at risk

D ∈ (0.8, 1.0]:   Catastrophic
  - Complete departure from mission
  - Fundamental restructuring required
  - Existential threat
```

**Example:**

```python
# Mission drift to profit (SP-03)
drift_scenarios = {
    "7%_enforced": 0.1,                # Nominal
    "5%_allocated": 0.3,               # Concerning (30% deviation)
    "2%_allocated": 0.7,               # Severe (70% deviation)
    "0%_allocated": 1.0,               # Catastrophic
}
```

### Dimension 4: Noise (N) - Uncertainty Entropy

**Concept:** How unpredictable is the situation?

**Geometric Interpretation:**
- N is **entropy** or information uncertainty
- High N = chaotic, hard to predict
- Low N = deterministic, well-understood

**Noise Scale:**

```
N ∈ [0.0, 0.2]:   Predictable
  - Clear cause-effect relationships
  - Historical data available
  - Confident forecasting possible

N ∈ (0.2, 0.5]:   Moderate
  - Some unknown factors
  - Patterns exist but noisy
  - Probabilistic planning needed

N ∈ (0.5, 0.8]:   High
  - Many unknowns
  - Weak signal-to-noise ratio
  - Scenario planning required

N ∈ (0.8, 1.0]:   Chaotic
  - Completely unpredictable
  - Black swan territory
  - Robust system design essential
```

**Example:**

```python
# AI ratification failure (SP-07)
noise_sources = {
    "single_ai_agent": 0.9,            # Chaotic (unknown biases)
    "3_diverse_agents": 0.6,           # High (some disagreement)
    "5_agents_behavioral_dna": 0.3,    # Moderate (fingerprinted)
    "10_agents_cross_validated": 0.1,  # Predictable
}
```

---

## Danger Zone Detection

### The Tangent Threshold

**Key Insight:** tan(θ) reveals proximity to catastrophe.

**Why Tangent?**
- sin and cos are bounded [-1, 1]
- **tan has vertical asymptotes** at θ = π/2 + nπ
- As θ → π/2, tan(θ) → ∞ (explosion)
- Small changes in θ cause huge changes in tan

**Danger Zone Definition:**

```python
def check_danger_zone(theta, threshold=10):
    """
    Returns True if failure is in critical region.
    
    threshold=10 means tan(θ) must exceed 10
    For θ in [0, 2π], this occurs near:
      - θ ≈ 1.47 to 1.67 (around π/2 ≈ 1.57)
      - θ ≈ 4.61 to 4.81 (around 3π/2 ≈ 4.71)
    """
    try:
        tangent = math.tan(theta)
        return abs(tangent) > threshold
    except:
        # Exactly at π/2: tan is undefined (infinite)
        return True
```

**Example:**

```
θ = 0.79 (π/4):       tan = 1.0      → Safe
θ = 1.27 (0.8π):      tan = 3.08     → Safe
θ = 1.47:             tan = 10.98    → DANGER
θ = 1.57 (π/2):       tan = ∞        → CRITICAL
θ = 1.67:             tan = -10.98   → DANGER
θ = 2.36 (3π/4):      tan = -1.0     → Safe
```

### Composite Danger Score

Beyond just tan(θ), combine all 4 dimensions:

```python
def calculate_composite_danger(theta, R, D, N):
    """
    Composite danger score ∈ [0, ∞)
    Higher = more dangerous
    """
    # Tangent component (can be huge)
    tan_danger = abs(math.tan(theta)) if abs(math.tan(theta)) < 100 else 100
    
    # Weak resonance amplifies danger
    resonance_penalty = (1 - R)
    
    # High drift and noise add danger
    drift_noise_factor = (D + N) / 2
    
    # Composite: tangent drives it, R/D/N modulate
    composite = tan_danger * (1 + resonance_penalty) * (1 + drift_noise_factor)
    
    return composite

# Example: SP-02 (Succession trigger misses)
theta = math.pi  # Late phase
R = 0.2          # Weak mitigation
D = 0.8          # High drift
N = 0.5          # Moderate noise

danger = calculate_composite_danger(theta, R, D, N)
# tan(π) ≈ 0, but large R/D/N still give danger ≈ 1.3
```

---

## Risk Evolution Over Time

### Tracking Phase Progression

Risks don't stay static—θ evolves:

```python
# Time series of failure phase
timeline = {
    "2024-01-01": 0.2,      # Early discovery
    "2024-02-01": 0.5,      # Growing concern
    "2024-03-01": 1.2,      # Accelerating
    "2024-04-01": 1.5,      # Approaching π/2
    "2024-05-01": 1.57,     # CRITICAL (intervention)
    "2024-06-01": 1.3,      # Mitigation deployed
    "2024-07-01": 0.8,      # Stabilizing
    "2024-08-01": 0.4,      # Controlled
}

# Velocity of phase change
dθ_dt = (theta_current - theta_previous) / time_delta

# Predict future danger
theta_future = theta_current + dθ_dt * forecast_horizon
if check_danger_zone(theta_future):
    trigger_early_intervention()
```

### Resonance Decay

Mitigations degrade over time without maintenance:

```python
# Exponential decay model
R(t) = R₀ * exp(-λ * t)

# Example: Security patches
R₀ = 0.9            # Initial strong protection
λ = 0.1/month       # Decay rate (new vulnerabilities)
t = 6 months        # Time since last patch

R_current = 0.9 * math.exp(-0.1 * 6) = 0.49  # Now weak!
```

### Drift Accumulation

Small deviations compound:

```python
# Random walk model
D(t+1) = D(t) + random_shock - corrective_action

# Without correction, D trends upward
# With active management, D oscillates around setpoint
```

---

## Fitness Function Revisited

**The Core Equation:**

```
Fitness = R × (1 - D) × (1 - N) × eq

Where:
  R ∈ [0, 1]     - Resonance (higher is better)
  D ∈ [0, 1]     - Drift (lower is better)
  N ∈ [0, 1]     - Noise (lower is better)
  eq ∈ [0, 1]    - Equation quality (code/commit quality)
```

**Interpretation:**
- **Perfect system**: R=1, D=0, N=0, eq=1 → Fitness = 1.0
- **Typical system**: R=0.7, D=0.3, N=0.4, eq=0.95 → Fitness = 0.28
- **Broken system**: R=0.2, D=0.9, N=0.8, eq=0.5 → Fitness = 0.001

**Evolution Gate:**

```python
def should_deploy(candidate_fitness, champion_fitness, threshold=0.02):
    """
    Deploy only if fitness improves by at least threshold.
    Prevents noise from triggering unnecessary changes.
    """
    return candidate_fitness > champion_fitness + threshold
```

---

## Visualization Techniques

### 1. Polar Plot (θ vs R)

```
     π/2 (Danger!)
        │
        │   R=0.8 ●
        │
π ──────┼──────── 0
        │
        │       ● R=0.3 (Weak!)
        │
     3π/2
```

### 2. 3D Risk Landscape

```
Axes: θ (x), D (y), R (z)
Surface: Fitness = R × (1-D)
Peaks: High R, Low D (good states)
Valleys: Low R, High D (bad states)
```

### 3. Time Series Dashboard

```
     R │ 1.0 ┤         ╭───────
       │ 0.8 ┤      ╭──╯
       │ 0.6 ┤   ╭──╯
       │ 0.4 ┤╭──╯
       │ 0.2 ┤╯
       └─────┴────────────────→ time
             ↑ Mitigation deployed
```

---

## Key Takeaways

1. **TRIG6 provides geometric framework** for risk analysis
2. **Four dimensions** (θ, R, D, N) encode complete risk state
3. **Danger zones** detected via tan(θ) asymptotes
4. **Fitness function** enables mathematical optimization
5. **Time evolution** tracked via phase progression

---

## Navigation

- [← Previous: Chapter 4 - 100 Bottlenecks](chapter_04_100_bottlenecks.md)
- [→ Next: Chapter 6 - Evolutionary Mitigations](chapter_06_evolutionary_mitigations.md)
- [↑ Full Failure Vectors](../../FAILURE_VECTORS_36.md)

---

*"Risk is geometry. Map it in TRIG6 space, and the optimal path becomes visible."*
