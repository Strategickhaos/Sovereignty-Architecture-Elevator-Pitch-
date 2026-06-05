# TRIG6 for Material Craft — Gene Repository

## Overview

This directory contains FlameLang gene definitions that encode ancient craft processes as TRIG6-monitored dynamical systems. These genes demonstrate that the same architecture used for modeling neural networks and AI swarms can be applied to material crafts.

> **"If I can use TRIG6 + FlameLang + SAGCO-OS to model brains and AI swarms, I should be able to model papyrus sheets and Mayan codices as dynamical systems too."**

---

## Philosophy

The Strategickhaos stack (TRIG6 + FlameLang + SAGCO-OS + HYDRA) treats computation, neural activity, and now material crafts as **wave-driven processes** monitored through universal trigonometric stability functions.

**Same architecture, different substrate:**
- **Neurons:** voltage spikes, synaptic weights, activation thresholds
- **Material craft:** time, heat, pressure, chemical reactions
- **Both:** modeled as θ (state deviation), R (resonance/stability), D (drift), N (noise)

This is not physically accurate FEM simulation — it's **formal craft knowledge encoding** that can be:
- **Simulated** (Monte Carlo runs across parameter distributions)
- **Evolved** (Darwinian compiler loop optimizes parameters)
- **Monitored** (TRIG6 flags danger zones in real-time)

---

## What's in a Gene File?

Each `.yaml` gene encodes a complete craft process with:

### 1. **Metadata**
- Unique ID, version, substrate, origin
- Intent and narrative description
- Target compiler (SAGCO-OS / HYDRA)

### 2. **Operations**
Sequential craft steps with:
- Parameter ranges (e.g., `soak_days: [5, 9]`)
- Optimal values
- Output functions (quality, strength, adhesion, etc.)

### 3. **TRIG6 Hooks**
Map each operation into trigonometric stability space:

```yaml
theta_fn: |
  # Normalize parameters to [0, 2π] space
  soak_norm = (soak_days - 7) / 2
  temp_norm = (water_temp_c - 24) / 4
  theta = π/2 * (soak_norm + temp_norm/2)

resonance_fn: |
  drift = sqrt(soak_norm² + temp_norm²) / sqrt(2)
  R = cos(drift * π/2) * (1 - noise)

danger_condition: "|tan(theta)| > 10"
```

**What this means:**
- `θ` (theta) = how far from optimal conditions
- `R` (resonance) = stability score (0 = unstable, 1 = perfect)
- `|tan(θ)| > 10` = danger threshold (approaching singularity)

### 4. **Probability Models**
Distributions for Monte Carlo simulation:
```yaml
probability_model:
  distributions:
    soak_days:
      type: "normal"
      mu: 7
      sigma: 1
  simulation:
    runs: 10000  # 10K simulated sheets
```

### 5. **Fitness Functions**
Multi-objective quality metrics:
```yaml
fitness:
  - id: "sheet_quality"
    weights:
      sheet_strength: 0.35
      smoothness_index: 0.25
      brittleness_index: -0.20  # negative = penalize
```

### 6. **Danger Zones**
Conditions that lead to failure:
```yaml
danger_zones:
  - id: "fiber_rot"
    condition: "soak_days > 9 OR water_temp_c > 28"
    severity: "CRITICAL"
    mitigation: "Reduce soak_days or lower water_temp_c"
```

### 7. **Evolutionary Parameters**
For Darwinian optimization:
```yaml
evolution:
  population_size: 100
  generations: 50
  optimization_target: "combined_fitness"
```

---

## Available Genes

### PAPYRUS-001-CLASSIC.yaml
**Ancient Egyptian papyrus sheet making**

- **Substrate:** Cyperus papyrus (Nile Delta sedge)
- **Process:** Harvest → Peel → Soak → Layer → Press → Polish
- **TRIG6 Monitoring:**
  - Soak stability (sugar extraction, adhesion potential)
  - Press/dry stability (moisture removal vs. brittleness)
  - Polish damage monitor (smoothness vs. surface abrasion)
- **Key Outputs:**
  - Sheet strength, smoothness, longevity estimate
  - Predicted lifespan: 300-500+ years
- **Fitness Target:** Combined fitness > 0.75

**Example Output:**
```
"This parameter set produces sheets with 87% predicted strength,
92% smoothness, and estimated 420-year lifespan under proper storage."
```

---

### MAYAN-CODEX-001.yaml
**Mesoamerican screenfold codex creation**

- **Substrate:** Ficus amate bark
- **Process:** Harvest bark → Pulp/beat → Form sheets → Gesso coating → Accordion folding → Bind covers
- **TRIG6 Monitoring:**
  - Pulping chemistry stability (lime concentration vs. fiber integrity)
  - Fold mechanical stress (crease fatigue over lifetime)
  - Aging degradation monitor (environmental + handling stress)
- **Key Outputs:**
  - Fold survival probability, surface quality
  - Usability index: predicted opening/closing cycles
  - Longevity estimate: 400-800 years
- **Fitness Target:** Combined fitness > 0.70

**Example Output:**
```
"This codex configuration survives 650 years and supports 460 opening/closing
cycles with 92% fold integrity. Optimal for archival preservation."
```

---

## How TRIG6 Works for Material Craft

### The Core Concept

TRIG6 uses **trigonometric functions** to model stability because:
1. **Periodicity** — Many processes are cyclic (day/night, wet/dry, fold/unfold)
2. **Resonance** — Systems have natural "sweet spots" (optimal temperature, pressure)
3. **Singularities** — Near-vertical `tan(θ)` slopes = instability zones
4. **Phase space** — Multi-parameter systems map naturally to angles

### Example: Papyrus Soaking

```
Optimal state:
  soak_days = 7
  water_temp_c = 24

Deviation mapping:
  θ = f(soak_days, water_temp_c)
  
When θ → π/2:
  |tan(θ)| → ∞
  System unstable (over-soaked → rot)

When θ → 0:
  R = cos(drift * π/2) → 1
  System stable (perfect adhesion)
```

This is **identical** to how TRIG6 monitors neural network activation functions — same math, different physics.

---

## Integration with the Stack

### FlameLang (Layer 0 → 1)
Compiles gene YAML into:
- Executable simulation code (LLVM IR)
- Parameter distributions
- Fitness evaluation functions
- TRIG6 monitoring hooks

### TRIG6 (Layer 2)
Provides real-time stability monitoring:
- Evaluates `θ`, `R`, `D`, `N` at each simulation step
- Flags danger zones when `|tan(θ)| > threshold`
- Logs resonance scores for evolutionary feedback

### SAGCO-OS / HYDRA (Layer 3)
Orchestrates distributed simulation:
- Runs 10,000+ Monte Carlo trials in parallel
- Logs statistical distributions of outcomes
- Feeds results to Darwinian compiler

### Darwinian Compiler (Layer 4)
Evolves optimal parameter ranges:
- Starts with wide initial ranges
- Selects high-fitness configurations
- Mutates/crosses parameters
- Converges on optimal recipe

---

## Usage Examples

### Scenario 1: Optimize Papyrus for Maximum Longevity

```bash
# Hypothetical FlameLang CLI usage
$ flamelang compile genes/craft-processes/PAPYRUS-001-CLASSIC.yaml
$ sagco-os simulate --gene PAPYRUS-001 --runs 10000 --optimize longevity_estimate
$ hydra execute --parallel --workers 128

Output:
  Optimal configuration found after 37 generations:
    soak_days: 7.2 ± 0.3
    press_pressure_kpa: 27 ± 3
    ambient_humidity_pct: 33 ± 5
  
  Predicted longevity: 487 years (95% CI: 420-540)
  Combined fitness: 0.89
  Danger zones avoided: 100%
```

### Scenario 2: Trade-off Analysis for Codex

```bash
$ flamelang simulate MAYAN-CODEX-001 --objective usability_index --constraint "longevity_estimate > 300"

Output:
  Pareto frontier found:
  
  Config A: High durability
    folds_count: 20
    longevity: 720 years
    usability: 380 cycles
  
  Config B: High usability
    folds_count: 16, thicker sheets
    longevity: 310 years
    usability: 490 cycles
  
  Recommendation: Config A for archival, Config B for teaching use
```

---

## Adding New Craft Genes

To add a new material craft process:

1. **Copy a template** (PAPYRUS-001 or MAYAN-CODEX-001)
2. **Define your operations** with parameter ranges
3. **Map to TRIG6 space:**
   - Identify critical stability points
   - Define `theta_fn` for state deviation
   - Define `resonance_fn` for quality metric
   - Set danger thresholds
4. **Define fitness functions** for your quality goals
5. **Test with small Monte Carlo runs** (100-1000)
6. **Evolve parameters** with larger runs (10,000+)

### Template Structure

```yaml
meta:
  id: "CRAFT-NAME-VERSION"
  substrate: "Material type"
  
operations:
  - id: "OP1"
    name: "step_name"
    params:
      param_name:
        range: [min, max]
        optimal: value
    outputs:
      quality_metric: "f(params)"

trig6_hooks:
  - step_id: "OP1"
    theta_fn: |
      # Normalize parameters to theta space
    resonance_fn: |
      # Calculate stability metric
    danger_condition: "|tan(theta)| > 10"

fitness:
  - id: "overall_quality"
    weights: { ... }
```

---

## Philosophical Context

This work demonstrates that **TRIG6 is substrate-agnostic**:

| Domain | θ (State) | R (Resonance) | Danger Zone |
|--------|-----------|---------------|-------------|
| **Neural Nets** | Activation level | Gradient stability | Exploding gradients |
| **Papyrus** | Soak time deviation | Adhesion quality | Fiber rot |
| **Codex** | Fold count × thickness | Crease integrity | Crack formation |

The **same wave-driven monitoring** applies across:
- Neurons firing
- Water molecules diffusing
- Fibers bonding
- Folds stressing

This is the **"probability of everything"** in action:
> "Treat time, heat, pressure, and chemistry as waves. Monitor their stability with trigonometry. Evolve toward optimal configurations."

---

## Future Directions

Potential craft processes to encode:

- **Bronze casting** (heat curves, mold stress, cooling rates)
- **Ceramic glazing** (kiln temperature profiles, chemical phase transitions)
- **Textile weaving** (thread tension, warp/weft ratios, loom mechanics)
- **Damascus steel forging** (folding cycles, carbon migration, quench rates)
- **Stained glass** (thermal expansion mismatch, lead came flexibility)
- **Violin varnish** (layer count, resin chemistry, acoustic damping)

Each of these is a **dynamical system** with:
- Time-dependent processes
- Temperature/pressure variables
- Quality trade-offs
- Danger zones to avoid

All can be encoded as TRIG6-monitored genes.

---

## References

- **FLAMELANG_SPECIFICATION.md** — Core symbolic language spec
- **EMPIRE_GENOME_v1.7.yaml** — Example of gene-based system definition
- **SWARM_DNA_v9.0-black-hole-resonance.yaml** — Neural swarm gene pattern

---

## Technical Appendix: TRIG6 Math

For the curious engineer, here's the full TRIG6 framework:

### State Variables
- **θ (theta):** Angular position in parameter space [0, 2π]
- **R (resonance):** Stability metric [0, 1], where 1 = perfectly stable
- **D (drift):** Euclidean distance from optimal parameters [0, ∞]
- **N (noise):** Stochastic variability [0, 1]

### Core Functions

```
Drift Calculation:
  D = ||params - params_optimal|| / ||params_range||

Theta Mapping:
  θ = f(params) where f normalizes to [0, 2π]

Resonance:
  R = cos(D * π/2) * (1 - N)
  
  When D = 0: R = 1 (perfect)
  When D = 1: R ≈ 0 (unstable)

Danger Detection:
  |tan(θ)| > threshold → flag instability
  
  As θ → π/2: tan(θ) → ∞ (singularity)
```

### Multi-Dimensional Extension

For N parameters:

```
θ_i = normalize(param_i - optimal_i)
θ_total = sqrt(Σ θ_i²) / sqrt(N)

D = sqrt(Σ (param_i - optimal_i)²) / sqrt(N)

R = cos(D * π/2) * Π(1 - N_i)
```

---

## License

All craft genes in this repository are released under the Strategickhaos DAO LLC licensing terms. Use these to encode traditional knowledge, but respect the cultural origins of these crafts.

---

**🔥 Reignite. As above, so below. As neurons, so fibers.**

*Generated by Strategickhaos DAO LLC | 2025-01-25*
