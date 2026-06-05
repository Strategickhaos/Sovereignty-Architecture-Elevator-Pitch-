# TRIG6 Alchemy System - Quick Reference

## What Was Implemented

A complete TRIG6 (Trigonometric 6-parameter) encoding system for 36 historical alchemy recipes spanning four major traditions (100 CE - 16th century).

## File Structure

```
Sovereignty-Architecture-Elevator-Pitch-/
├── data/trig6-alchemy/
│   ├── README.md                          # Main documentation
│   ├── VISUALIZATION_GUIDE.md             # How to visualize basin plots
│   ├── ALCHEMY_GENE_TEMPLATE.yaml         # Generic schema (template)
│   ├── TRIG6_ALCHEMICAL_INDEX.yaml        # All 36 recipes with stats
│   └── examples/
│       └── ALCH-ZOSIMOS-INK-001.yaml      # Safe worked example
│
└── docs/book/
    ├── chapters/chapter-16/
    │   └── CHAPTER_16_LOST_PHARMACOPEIA.md   # Full narrative chapter
    └── appendices/appendix-g/
        └── APPENDIX_G_ALCHEMICAL_INDEX.md    # Tabular reference
```

## The 36 Recipes

### House of Hermes (1-9) - Greco-Egyptian, 100-300 CE
Transmutation, elixirs, universal solvents
- **Success Rate:** 0% (all theoretical/failed)
- **Avg Fitness:** 0.28
- **Notable:** Philosopher's Stone, Elixir of Life, Alkahest

### House of Zosimos (10-18) - Late Antiquity, c. 300 CE  
Practical alchemy, dyes, metallurgy, crafts
- **Success Rate:** 44% (safe recipes)
- **Avg Fitness:** 0.48
- **Notable:** Lampblack ink, Bronze alloy, Purple dye

### House of Jabir (19-27) - Islamic Golden Age, 8-9th Century
Acids, salts, mineral processing
- **Success Rate:** 44% (safe recipes)
- **Avg Fitness:** 0.41
- **Notable:** Aqua regia, Alum, Borax, Oil of vitriol

### House of Paracelsus (28-36) - Renaissance, 16th Century
Medical alchemy, tinctures, iatrochemistry
- **Success Rate:** 44% (safe recipes)
- **Avg Fitness:** 0.39
- **Notable:** Laudanum, Antimony wine, Coral calx, Melissa cordial

## TRIG6 Parameters

Each recipe encoded with:

1. **θ (Theta)** - Process phase [0, 2π]
   - Maps time, temperature, concentration (normalized)
   - 0 = prep, π = transformation, 2π = completion

2. **R (Resonance)** - Efficacy [0, 1]
   - Did it work? 1 = perfect, 0 = complete failure

3. **D (Drift)** - Side effects [0, 1]
   - Toxicity/impurities. 0 = clean, 1 = catastrophic

4. **N (Noise)** - Uncertainty [0, 1]
   - Reproducibility. 0 = reliable, 1 = random

5. **Danger Zones** - Unstable regimes
   - |tan(θ)| > 10, D > 0.7, etc.

6. **Fitness** - Overall quality
   - f = R × (1 - D) × (1 - N)

## Safety Classification

- **LOW (13):** Safe for study, low toxicity
- **MEDIUM (10):** Caution required, moderate hazards
- **HIGH (5):** Dangerous, severe toxicity
- **EXTREME (8):** Deadly, never attempt

## NEURO-36 Cross-Mapping

4 recipes validated by modern science:

| Recipe | Disease | Status |
|--------|---------|--------|
| Coral Calx | GI-012 (antacid) | ✓ Still used (Tums) |
| Spagyric Essence | INF-008 (inflammation) | ✓ Herbal medicine |
| Melissa Cordial | ANX-005 (anxiety) | ✓ Herbal tea |
| Verdigris | INF-011 (antimicrobial) | ○ Research continues |

## Key Insights

1. **θ Distribution:** Most successful recipes at π/6 to π/4 (stable regimes)
2. **Failure Pattern:** Dangerous recipes cluster near π/2, 3π/4 (unstable)
3. **Historical Success:** Zosimos had highest practical success (44%)
4. **Modern Validation:** 4 of 36 recipes still used or studied today

## How to Use

### For Quick Reference
```bash
cat data/trig6-alchemy/README.md
```

### For Full Chapter
```bash
cat docs/book/chapters/chapter-16/CHAPTER_16_LOST_PHARMACOPEIA.md
```

### For Data Analysis
```bash
cat data/trig6-alchemy/TRIG6_ALCHEMICAL_INDEX.yaml
```

### For Visualizations
```bash
cat data/trig6-alchemy/VISUALIZATION_GUIDE.md
```

### For Safe Example
```bash
cat data/trig6-alchemy/examples/ALCH-ZOSIMOS-INK-001.yaml
```

## Sample Recipes by Category

### Safe Examples (Learn From)
- ALCH-ZOSIMOS-016: Lampblack ink
- ALCH-ZOSIMOS-012: Bronze alloy  
- ALCH-PARACELSUS-032: Coral calx (antacid)
- ALCH-JABIR-023: Alum purification

### Dangerous (Study Only - Never Attempt)
- ALCH-HERMES-005: Alkahest (theoretical)
- ALCH-JABIR-020: Aqua regia (dissolves gold)
- ALCH-PARACELSUS-028: Laudanum (opiate)
- ALCH-PARACELSUS-029: Antimony wine (toxic)

## Statistics Summary

```
Total Recipes: 36
Houses: 4 (Hermes, Zosimos, Jabir, Paracelsus)
Time Span: ~1500 years (100 CE - 16th century)

Hazard Distribution:
  LOW:     13 (36%)
  MEDIUM:  10 (28%)
  HIGH:     5 (14%)
  EXTREME:  8 (22%)

θ-Class Distribution:
  Stable (π/8 to π/4):   19 (53%)
  Moderate (π/3):         6 (17%)
  Unstable (π/2+):       11 (30%)

Danger Flag:
  Safe:      13 (36%)
  Dangerous: 23 (64%)

Fitness Distribution:
  Excellent (>0.5):      8 (22%)
  Good (0.3-0.5):       12 (33%)
  Marginal (0.2-0.3):    9 (25%)
  Poor (≤0.2):           7 (19%)
```

## Primary Use Cases

1. **Historical Analysis** - Understanding evolution of chemistry
2. **Basin Modeling** - Teaching stable vs. unstable regimes
3. **Hypothesis Generation** - Cross-mapping to modern medicine
4. **Computational Archaeology** - Quantifying ancient knowledge
5. **Educational Demonstrations** - Safe examples of TRIG6 framework

## Safety Reminders

⚠️ **ALL RECIPES FOR MODELING ONLY**
- Parameters are normalized and symbolic
- No actual concentrations or temperatures provided
- This is computational archaeology, not a chemistry manual
- Never attempt any recipe, even "LOW" hazard ones
- Historical alchemy was often deadly

## What Makes This Different

Traditional alchemy books either:
- Mystify the subject (occult symbolism)
- Ignore it entirely (irrelevant to modern chemistry)

This approach:
- **Quantifies** historical recipes with TRIG6 parameters
- **Classifies** them by safety and efficacy
- **Connects** them to modern disease categories
- **Preserves** them as computational datasets
- **Prevents** misuse through parameter normalization

## Next Steps

The framework is extensible. Future additions could include:

1. **More traditions:** Chinese, Indian, Mesoamerican alchemy
2. **Finer granularity:** Sub-recipes, variations, regional differences
3. **Computational simulations:** Basin dynamics, mutation evolution
4. **Cross-cultural analysis:** Comparing θ-spaces across traditions
5. **Modern parallels:** Pharmaceutical R&D, materials science

## Credits

Based on historical sources:
- Hermes Trismegistus - Emerald Tablet
- Zosimos of Panopolis - Greek alchemical corpus  
- Jabir ibn Hayyan - Arabic chemical texts
- Paracelsus - Renaissance medical alchemy

Modern scholarship:
- Newman, W. R. *Promethean Ambitions* (2004)
- Principe, L. M. *The Secrets of Alchemy* (2013)

## License

Part of the Sovereignty Architecture project.  
For educational and research purposes.

---

**Remember: This is for modeling and education only. Never attempt to recreate historical alchemy recipes.**
