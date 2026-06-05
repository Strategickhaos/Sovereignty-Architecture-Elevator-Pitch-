# DOM Biological-Computational Equivalence Map v1.0

## Overview

This simulation implements a **Potentiometer Simulation with Gene-Min Binding** based on the TRIG6 model for dynamic system threshold adjustment. It binds 36 immune genes/components to "min" values (minutes 1-36) using trigonometric functions to model biological-computational equivalence.

## Biological-Computational Model

### The TRIG6 Potentiometer

The simulation uses trigonometry as a "potentiometer" to adjust system thresholds and health parameters:

1. **Binding Mechanism**: Each of 36 immune genes is bound to a minute value (1-36)
2. **Degree Conversion**: Minutes are converted to decimal degrees using a standard trigonometry table
3. **Radians Conversion**: θ = deg × π / 180
4. **TRIG6 Modulation**: Trigonometric functions compute system parameters:
   - **R (Resonance/Coherence)**: |sin(θ)| - normalized [0,1] for system resonance
   - **eq (Equilibrium)**: |cos(θ)| - normalized for goal alignment
   - **D (Drift)**: (1 - cos(θ)) / 2 - drift as opposition to cosine stability
   - **N (Noise)**: (1 - sin(θ)) / 2 - noise as opposition to sine activation

5. **Fitness Computation**: f = R × (1 - D) × (1 - N) × eq
6. **Danger Check**: |tan(θ)| > 10 indicates danger zone (per TRIG6 specification)

### Outcome Classification

- **Unstable**: danger zone OR f < 0.3 (low fitness, system rejects binding)
- **Marginal**: 0.3 ≤ f ≤ 0.5 (evolving, partial bind)
- **Stable**: f > 0.5 (strong binding, potentiometer adjustment succeeds)

## The 36 Immune Genes/Components

1. Skin
2. Sebum
3. Anti-microbial elements
4. Probiotics
5. Holistic organ nose mouth throat
6. Inheleten exhibition
7. Harmonious Coexistens Symbosis
8. Pathogens
9. Mucus membrane
10. Cashingying
11. Innate Immune System
12. Adaptive Immune System
13. Cilia
14. Oral cavity
15. Lucoside
16. Neutrophil
17. Bone marrow
18. Immune cell
19. Blood sweat
20. Weak adhesion
21. Strong adhesion
22. Receptor
23. Asymmetric
24. Synthe cells
25. Division and maturation of neutrophils
26. Nucleosides
27. Progenitor cell
28. A stem cells
29. Connective Tissue
30. Bacteria
31. Toxins
32. Nutritional
33. Tumor Necrosis
34. Antigens
35. Thymus
36. Transition/Run/Gain/Advance/Set back

## Usage

### Run the Simulation

```bash
python3 dom_biological_computational_map.py
```

This will:
1. Run a **baseline simulation** (scale_factor = 1.0) 
2. Run a **scaled simulation** (scale_factor = 90.0) for comparison
3. Generate detailed results tables for both simulations
4. Save results to JSON files for integration with the ecosystem

### Output Files

- `dom_bio_comp_baseline_results.json` - Results from baseline simulation (unscaled)
- `dom_bio_comp_scaled_results.json` - Results from scaled simulation (90x scaling)

### JSON Output Format

```json
{
  "metadata": {
    "simulation": "DOM Biological-Computational Equivalence Map v1.0",
    "model": "TRIG6 Potentiometer",
    "total_bindings": 36
  },
  "bindings": [
    {
      "gene": "Skin",
      "min": 1,
      "deg": 0.0167,
      "theta_rad": 0.0003,
      "R": 0.0003,
      "D": 0.0000,
      "N": 0.4999,
      "eq": 1.0000,
      "fitness": 0.0001,
      "danger": false,
      "outcome": "Unstable (Danger or Low Fitness)"
    },
    ...
  ]
}
```

## Key Findings

### Baseline Simulation (scale_factor = 1.0)

**Result**: All 36 bindings are **Unstable**

- **Average Fitness**: ~0.0027 (extremely low)
- **Problem**: Small θ values (from small degree values) lead to:
  - Tiny R and eq values (~θ)
  - High N and D values (~0.5)
  - Resulting fitness f near 0

**Interpretation**: Binding genes to these minute values doesn't produce stable TRIG6 potentiometer adjustment. The system rejects all bindings as unstable.

### Scaled Simulation (scale_factor = 90.0)

**Result**: Mixed outcomes with improved stability

- **Unstable**: 19 bindings (52.8%)
- **Marginal**: 17 bindings (47.2%)
- **Stable**: 0 bindings (0.0%)
- **Average Fitness**: ~0.245 (90x improvement)

**Interpretation**: Scaling degrees by 90x pushes trigonometric functions into meaningful ranges, achieving marginal binding for genes 20-36. This demonstrates that effective TRIG6 potentiometer adjustment requires degree scaling.

## Ecosystem Integration

### Tie to Physarum Evolution

The low fitness values in baseline simulation indicate that minute bindings don't stabilize the TRIG6 compiler/OS. This mirrors concepts in:

- **Tube reinforcement** in Physarum slime mold networks
- **Compiler pass optimization** in OS development
- **Resonance gate adjustment** in biological systems

### Recommendations for Stable Binding

1. **Scale minute values** (e.g., × 90 or × 180) to push θ into ranges where sin/cos produce meaningful values
2. **Use tan(θ) amplification** for stronger effects (but risk danger zone at higher minutes)
3. **Adaptive scaling** based on gene criticality (e.g., scale immune system genes more than structural genes)
4. **Multi-modal potentiometer** combining sin, cos, and tan adjustments

## Scientific Basis

This simulation is based on:

1. **Trigonometry tables** for minute-to-degree conversion (standard mathematical reference)
2. **TRIG6 model** for biological-computational equivalence
3. **Fitness landscapes** in evolutionary biology
4. **Danger zone theory** from control systems (|tan(θ)| > 10 indicates instability)

## License

Part of the Sovereignty Architecture Elevator Pitch project.

## References

- Trigonometry booklet (minutes to decimals of degrees table)
- TRIG6 potentiometer invention documentation
- Physarum evolution simulation (physarum_evolution_36.json)
- DOM Biological-Computational Equivalence theory

---

**Generated by**: DOM Biological-Computational Equivalence Map v1.0  
**Date**: 2026-01-26  
**Model**: TRIG6 Potentiometer with Gene-Min Binding
