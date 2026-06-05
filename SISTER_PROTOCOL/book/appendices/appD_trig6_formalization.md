# Appendix D: TRIG6 Mathematical Formalization

## Complete Mathematical Framework

---

## Core Variables

| Symbol | Name | Domain | Meaning |
|--------|------|--------|---------|
| θ | Theta (Phase Angle) | [0, 2π] radians | System state/position in phase space |
| R | Resonance | [0, 1] | Alignment with ideal/target state |
| D | Drift | [0, 1] | Deviation from target trajectory |
| N | Noise | [0, 1] | Uncertainty/variability in measurements |
| eq | Equivalence Coefficient | [0, 1] | Constitutional/legal compliance |
| f | Fitness | [0, 1] | Overall system health/viability |

---

## Canonical Fitness Function

```
f = R × (1 - D) × (1 - N) × eq
```

Where:
- **f = 1.0**: Perfect system (impossible in practice)
- **f ≥ 0.75**: Excellent performance
- **f ≥ 0.65**: Acceptable performance
- **f < 0.65**: System requires intervention
- **f < 0.30**: Critical failure imminent

---

## Danger Zone Mathematics

### Primary Danger Condition

```
|tan(θ)| > threshold
```

Default threshold = 10.0

### Why Tangent?

The tangent function approaches infinity as θ → π/2 (90°), creating a mathematical singularity that maps to real-world catastrophic failure:

- **θ ≈ 0**: System in safe baseline state
- **θ ≈ π/4** (45°): System under stress but stable
- **θ → π/2** (90°): Approaching catastrophe
- **|tan(θ)| > 10**: Mathematical instability = real-world collapse

### Critical Angles

| Angle (θ) | tan(θ) | Status | Real-World Interpretation |
|-----------|--------|--------|---------------------------|
| 0° | 0 | Safe | Baseline/rest state |
| 30° | 0.577 | Nominal | Normal operation |
| 45° | 1.0 | Stressed | Elevated but sustainable |
| 60° | 1.732 | Warning | Approaching limits |
| 75° | 3.732 | Caution | Close to danger zone |
| 84° | 9.514 | DANGER | On edge of catastrophe |
| 85° | 11.43 | CRITICAL | Catastrophic failure likely |
| 89° | 57.29 | TERMINAL | Mathematical singularity |
| 90° | ∞ | COLLAPSE | Undefined/catastrophic |

---

## Six Trigonometric Functions

While we primarily use tan(θ) for danger detection, all six trig functions provide information:

```python
sin(θ)  # Vertical component, oscillation amplitude
cos(θ)  # Horizontal component, phase coherence
tan(θ)  # Ratio, instability measure
csc(θ)  # 1/sin(θ), inverse amplitude
sec(θ)  # 1/cos(θ), inverse coherence  
cot(θ)  # 1/tan(θ), inverse instability
```

---

## Parameter Computation Functions

### Theta Computation

Generic form (override in specific genes):
```python
def compute_theta(params: Dict) -> float:
    """Map parameters to phase angle [0, 2π]."""
    values = list(params.values())
    normalized = sum(values) / len(values)
    return normalized * 2 * math.pi
```

Domain-specific examples:

**Failure Mode:**
```python
theta = π/2 * (attack_rate + (1 - clarity) + (1 - validation_quality)) / 3
```

**Craft Process:**
```python
theta = π/3 + π/6 * (deviation_from_ideal + environmental_factor)
```

**Medicine Dose:**
```python
theta = π/2 * dose_intensity * frequency_factor
```

### Resonance Computation

```python
def compute_resonance(metrics: Dict) -> float:
    """Compute alignment with ideal state [0, 1]."""
    if 'stability' in metrics:
        return clamp(metrics['stability'], 0, 1)
    if 'success_rate' in metrics:
        return clamp(metrics['success_rate'], 0, 1)
    return 0.5  # Default
```

### Drift Computation

```python
def compute_drift(metrics: Dict) -> float:
    """Compute deviation from target [0, 1]."""
    if 'deviation' in metrics:
        return clamp(metrics['deviation'], 0, 1)
    if 'error_rate' in metrics:
        return clamp(metrics['error_rate'], 0, 1)
    return 0.0  # Default: no drift
```

### Noise Computation

```python
def compute_noise(metrics: Dict) -> float:
    """Compute uncertainty/variability [0, 1]."""
    if 'uncertainty' in metrics:
        return clamp(metrics['uncertainty'], 0, 1)
    if 'variance' in metrics:
        return clamp(metrics['variance'], 0, 1)
    return 0.1  # Default: low noise
```

---

## Evolutionary Algorithm

### Darwinian Selection

```python
for generation in range(max_generations):
    # 1. MUTATION
    challenger = mutate(champion, mutation_rate)
    
    # 2. SIMULATION  
    metrics = simulate(gene, challenger)
    
    # 3. EVALUATION
    state = evaluate_gene(gene, challenger, metrics)
    
    # 4. SELECTION
    if (state.fitness > champion_fitness and 
        state.fitness > threshold and 
        not state.danger):
        champion = challenger
        champion_fitness = state.fitness
```

### Mutation Operator

```python
def mutate(params: Dict, rate: float) -> Dict:
    """Apply Gaussian mutation to random parameter."""
    challenger = params.copy()
    key = random.choice(list(params.keys()))
    param_range = gene['parameters'][key]
    
    if isinstance(param_range, list):
        mutation = random.gauss(0, (param_range[1] - param_range[0]) * rate)
        challenger[key] = clamp(
            challenger[key] + mutation,
            param_range[0],
            param_range[1]
        )
    
    return challenger
```

---

## Theoretical Foundations

### Why This Works

1. **Phase Space Geometry**: Systems naturally evolve through state space with angular dynamics
2. **Singularity Mapping**: Mathematical singularities (tan → ∞) correspond to real-world critical transitions
3. **Multi-Objective Optimization**: f = R × (1-D) × (1-N) × eq simultaneously optimizes four competing objectives
4. **Evolutionary Robustness**: Darwinian selection naturally finds parameter sets that survive edge cases

### Prior Art

- **Control Theory**: Phase angle control, stability analysis
- **Dynamical Systems**: Bifurcation theory, chaos theory
- **Signal Processing**: Fourier analysis, resonance detection
- **Evolutionary Algorithms**: Genetic algorithms, differential evolution

### Novel Contributions

1. **Unified failure framework** across domains (legal, technical, medical, craft)
2. **Tangent-based danger detection** with consistent threshold
3. **Ancient knowledge encoding** as evolvable genes
4. **Multi-layer compilation** from intuitive → mathematical → executable

---

## Validation

### Test Cases

All test cases in `/trig6/failures/` and `/craft_genes/` should:
- ✅ Load successfully with `load_gene()`
- ✅ Evaluate to valid TRIG6State
- ✅ Evolve to f > threshold within 100 generations
- ✅ Detect danger zones correctly

### Consistency Checks

```bash
# Run full validation suite
for gene in trig6/failures/*.yaml craft_genes/*.yaml; do
    python trig6_kernel.py "$gene" || echo "FAIL: $gene"
done
```

---

*"Mathematics is the language in which failure speaks. If you listen carefully, it tells you how to survive."*
