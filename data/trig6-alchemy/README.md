# TRIG6 Alchemy Recipe Encoding System

## Overview

This directory contains a complete TRIG6 (Trigonometric 6-parameter) encoding system for 36 historical alchemy recipes spanning four major traditions:

- **House of Hermes** (1-9): Hermetic Corpus, Emerald Tablet (100-300 CE)
- **House of Zosimos** (10-18): Greek-Egyptian practical alchemy (c. 300 CE)
- **House of Jabir** (19-27): Islamic Golden Age chemistry (8-9th century)
- **House of Paracelsus** (28-36): Renaissance medical alchemy (16th century)

This system is designed for **Chapter 16: Lost Pharmacopeia** of the Sovereignty Architecture book.

## Purpose

Transform historical alchemy from mystical tradition into a **computable dataset** for:

1. **Historical analysis**: Understanding which recipes succeeded vs. failed
2. **Basin geometry modeling**: Identifying stable vs. unstable chemical regimes
3. **Hypothesis generation**: Cross-mapping to modern disease classifications (NEURO-36)
4. **Educational demonstration**: Teaching TRIG6 framework with safe, historical examples

## ⚠️ Critical Safety Notice

**ALL RECIPES ARE FOR MODELING ONLY - NOT OPERATIONAL CHEMISTRY**

- All parameters are **normalized and symbolic** (no actual concentrations or temperatures)
- This is **computational archaeology**, not a chemistry manual
- Do **NOT** attempt to recreate any recipe, even "LOW" hazard ones
- Many historical recipes are **deadly** (mercury poisoning, acid burns, explosions)

## File Structure

```
data/trig6-alchemy/
├── README.md                          # This file
├── ALCHEMY_GENE_TEMPLATE.yaml         # Generic schema for all recipes
├── TRIG6_ALCHEMICAL_INDEX.yaml        # Complete 36-recipe index
└── examples/
    └── ALCH-ZOSIMOS-INK-001.yaml      # Fully worked safe example (lampblack ink)

docs/book/
├── chapters/chapter-16/
│   └── CHAPTER_16_LOST_PHARMACOPEIA.md   # Main chapter narrative
└── appendices/appendix-g/
    └── APPENDIX_G_ALCHEMICAL_INDEX.md    # Complete tabular index
```

## TRIG6 Framework Components

Each recipe is encoded with six key parameters:

### 1. θ (Theta) - Process Phase
- Maps normalized process state s ∈ [0,1] to θ ∈ [0, 2π]
- Constructed from: time, temperature, concentration (all normalized)
- **θ = 0**: Preparation (grinding, dissolving)
- **θ = π**: Transformation (heating, reacting)
- **θ = 2π**: Completion (cooling, crystallizing)

### 2. R (Resonance) - Efficacy
- Did the process produce the intended effect?
- Range: [0, 1] where 1 = perfect outcome, 0 = complete failure
- Example: R = 0.7 for lampblack ink (good legibility)

### 3. D (Drift) - Side Effects
- How much unwanted toxicity or byproducts?
- Range: [0, 1] where 0 = clean process, 1 = catastrophic
- Example: D = 0.9 for aqua regia (extremely corrosive)

### 4. N (Noise) - Uncertainty
- How reproducible are the results?
- Range: [0, 1] where 0 = highly reliable, 1 = totally random
- Example: N = 0.4 for bronze alloy (well-understood process)

### 5. Danger Zones
- Unstable regimes where |tan(θ)| > 10
- Extreme toxicity where D > 0.7
- Hardware failure risks (corrosion, explosions)

### 6. Fitness Function
```
f = R × (1 - D) × (1 - N) × eq
```
Where eq accounts for equilibrium stability.

## Quick Start

### 1. View the Template
```bash
cat data/trig6-alchemy/ALCHEMY_GENE_TEMPLATE.yaml
```
This shows the canonical schema for encoding any alchemy recipe.

### 2. Study the Safe Example
```bash
cat data/trig6-alchemy/examples/ALCH-ZOSIMOS-INK-001.yaml
```
Lampblack ink (Zosimos) is a fully worked, low-hazard example perfect for learning.

### 3. Browse the Complete Index
```bash
cat data/trig6-alchemy/TRIG6_ALCHEMICAL_INDEX.yaml
```
All 36 recipes with symbolic descriptions and TRIG6 signatures.

### 4. Read the Chapter
```bash
cat docs/book/chapters/chapter-16/CHAPTER_16_LOST_PHARMACOPEIA.md
```
Complete narrative explanation with visualizations and analysis.

### 5. Consult the Appendix
```bash
cat docs/book/appendices/appendix-g/APPENDIX_G_ALCHEMICAL_INDEX.md
```
Tabular reference with statistics and cross-mappings.

## Example Recipes by Hazard Level

### Safe Examples (LOW Hazard)
- **ALCH-ZOSIMOS-016**: Lampblack ink (carbon + gum + water)
- **ALCH-ZOSIMOS-011**: Purple dye (organic extraction)
- **ALCH-ZOSIMOS-012**: Bronze alloy (copper + tin)
- **ALCH-PARACELSUS-032**: Coral calx (calcium carbonate)
- **ALCH-JABIR-023**: Alum purification (aluminum potassium sulfate)

### Dangerous Examples (DO NOT ATTEMPT)
- **ALCH-HERMES-005**: Alkahest (theoretical "universal solvent")
- **ALCH-JABIR-019**: Aqua fortis (strong mineral acid)
- **ALCH-JABIR-020**: Aqua regia (dissolves gold)
- **ALCH-PARACELSUS-028**: Laudanum (opiate addiction)
- **ALCH-PARACELSUS-029**: Antimony wine (severe toxicity)

## Key Insights from the Dataset

### Success Rates by House
- **Hermes**: 0% safe recipes (all theoretical/failed)
- **Zosimos**: 44% safe recipes (practical crafts)
- **Jabir**: 44% safe recipes (salts and minerals)
- **Paracelsus**: 44% safe recipes (herbal preparations)

### θ-Class Distribution
Most successful recipes cluster around:
- **θ = π/6**: Early-mid preparation (stable)
- **θ = π/4**: Mid-process (stable)

Most failures occur at:
- **θ = π/2**: Critical instability (|tan(θ)| → ∞)
- **θ = 3π/4**: Near-critical (extreme sensitivity)

### NEURO-36 Cross-Mapping
4 recipes validated by modern science:
1. **Coral Calx → GI-012** (antacid, still used as Tums)
2. **Spagyric Essence → INF-008** (herbal anti-inflammatory)
3. **Melissa Cordial → ANX-005** (herbal anxiolytic tea)
4. **Verdigris → INF-011** (copper antimicrobial)

## Schema Fields Explained

### Meta Section
```yaml
meta:
  id: "ALCH-[SOURCE]-[INDEX]"
  era: "Historical period"
  hazard_level: "LOW | MEDIUM | HIGH | EXTREME"
```

### Ingredients Section
```yaml
ingredients:
  - name: "symbolic_name"
    role: "solvent | pigment | catalyst | etc."
    hazard_class: "inert | toxic | corrosive | etc."
    amount_range: [min, max]  # normalized 0-1
```

### Process Section
```yaml
process:
  stages:
    - id: "stage_name"
      theta_range: [start, end]  # normalized 0-1
      control_axes: ["time_norm", "temp_norm"]
```

### TRIG6 Hooks Section
```yaml
trig6_hooks:
  theta_fn: "theta = 2 * PI * s"
  resonance_fn: "R = clamp(effectiveness_score, 0, 1)"
  drift_fn: "D = clamp(toxicity_score + impurity_score, 0, 1)"
  noise_fn: "N = clamp(experimental_uncertainty, 0, 1)"
```

### Danger Zones Section
```yaml
danger_zones:
  - id: "zone_name"
    condition: "mathematical_condition"
    action: "mark_unstable_regime"
```

### Fitness Section
```yaml
fitness:
  weights:
    intended_effect: 0.40
    low_toxicity: 0.30
    low_drift: 0.20
  function: "f = R * (1 - D) * (1 - N) * eq"
  threshold: 0.5
```

## Use Cases

### For Researchers
- Study basin dynamics in chemical parameter spaces
- Train ML models on historical chemical datasets
- Generate hypotheses for pharmaceutical research
- Analyze evolution of chemical knowledge

### For Educators
- Teach TRIG6 framework with concrete examples
- Demonstrate difference between stable and unstable regimes
- Show importance of parameter normalization
- Illustrate computational archaeology methods

### For Historians
- Quantify success/failure of alchemical traditions
- Compare knowledge across cultures and eras
- Understand technological evolution
- Identify precursors to modern chemistry

## Extending the Dataset

To add new recipes, follow this process:

1. **Copy the template**
   ```bash
   cp ALCHEMY_GENE_TEMPLATE.yaml new_recipe.yaml
   ```

2. **Fill in metadata**
   - Assign unique ID following pattern
   - Set appropriate hazard level
   - Document historical source

3. **Define ingredients symbolically**
   - Use generic role names (not specific chemicals)
   - Keep amounts normalized [0-1]
   - Classify hazards appropriately

4. **Map process to θ stages**
   - Divide into prep/transform/complete
   - Assign θ ranges [0-1]
   - List control axes (normalized)

5. **Estimate TRIG6 parameters**
   - R: Based on historical success reports
   - D: Based on known toxicity/side effects
   - N: Based on reproducibility in texts

6. **Add to index**
   - Update TRIG6_ALCHEMICAL_INDEX.yaml
   - Include in appropriate house
   - Update summary statistics

## Citations and Sources

Primary sources:
- Zosimos of Panopolis (c. 300 CE). *On the Letter Omega*
- Jabir ibn Hayyan (8-9th C.). *The Book of Seventy*
- Paracelsus (1493-1541). *Opus Paramirum*

Modern references:
- Newman, W. R. (2004). *Promethean Ambitions*
- Principe, L. M. (2013). *The Secrets of Alchemy*

## License and Attribution

This dataset is part of the Sovereignty Architecture project.

When citing this work, please reference:
- Chapter 16: Lost Pharmacopeia
- TRIG6 Alchemical Encoding System
- Strategickhaos Sovereignty Architecture

## Contact and Contributions

For questions, corrections, or additions to the dataset, please see the main repository README.

---

**Remember: This is for modeling and education only. Never attempt to recreate historical alchemy recipes.**
