# Book Structure: TRIG6 Alchemy System

This directory contains book chapters and appendices for the TRIG6 alchemy recipe encoding system.

## Contents

### Chapter 16: Lost Pharmacopeia
**Location:** `chapters/chapter-16/CHAPTER_16_LOST_PHARMACOPEIA.md`

Main narrative chapter covering:
- TRIG6 framework applied to alchemy
- Fully worked safe example (Lampblack Ink)
- 36-recipe overview organized by house
- NEURO-36 cross-mapping and hypothesis generation
- Safety considerations and ethical guidelines

**Key Sections:**
1. The TRIG6 Framework Applied to Alchemy
2. A Fully Worked Example: Lampblack Ink (Zosimos)
3. The 36-Recipe Index: Four Houses of Alchemy
4. Connecting to NEURO-36: Hypothesis Generation
5. Safety and Ethical Considerations
6. Conclusion: TRIG6 as Alchemical Compass

### Appendix G: Alchemical TRIG6 Index
**Location:** `appendices/appendix-g/APPENDIX_G_ALCHEMICAL_INDEX.md`

Comprehensive tabular reference containing:
- Complete index table of all 36 recipes
- Summary statistics by house, hazard, θ-class
- NEURO-36 cross-mapping candidates
- Red-flag recipes to avoid
- Using the index (for different audiences)

**Key Sections:**
1. Complete Index Table
2. Summary Statistics (by house, hazard, θ-class, fitness)
3. NEURO-36 Cross-Mapping
4. Red-Flag Recipes (DO NOT INVESTIGATE)
5. Using This Index (historians, chemists, AI researchers)
6. Accessing Full Recipe Data
7. Safety Disclaimer

## Relationship to Data Files

The book chapters reference detailed data files in `data/trig6-alchemy/`:

- **ALCHEMY_GENE_TEMPLATE.yaml** - Generic schema
- **TRIG6_ALCHEMICAL_INDEX.yaml** - Complete dataset
- **ALCH-ZOSIMOS-INK-001.yaml** - Safe worked example
- **README.md** - Technical documentation
- **VISUALIZATION_GUIDE.md** - How to create basin plots
- **QUICK_REFERENCE.md** - Summary stats

## Reading Order

### For General Readers
1. Start with **Chapter 16** for narrative introduction
2. Consult **Appendix G** for specific recipes
3. See **QUICK_REFERENCE.md** for summary stats

### For Researchers
1. Read **data/trig6-alchemy/README.md** for technical details
2. Study **ALCHEMY_GENE_TEMPLATE.yaml** for schema
3. Analyze **TRIG6_ALCHEMICAL_INDEX.yaml** for full dataset
4. Refer to **Chapter 16** and **Appendix G** for context

### For Developers
1. Check **ALCHEMY_GENE_TEMPLATE.yaml** for schema
2. Load **TRIG6_ALCHEMICAL_INDEX.yaml** for data
3. Use **VISUALIZATION_GUIDE.md** for plotting
4. See **QUICK_REFERENCE.md** for statistics

## The Four Houses

### House of Hermes (1-9)
- **Era:** Greco-Egyptian (100-300 CE)
- **Focus:** Transmutation, universal solvents
- **Success Rate:** 0% (all theoretical)
- **Key Recipes:** Philosopher's Stone, Elixir of Life, Alkahest

### House of Zosimos (10-18)
- **Era:** Late Antiquity (c. 300 CE)
- **Focus:** Practical crafts, dyes, metallurgy
- **Success Rate:** 44% safe
- **Key Recipes:** Lampblack ink, Bronze alloy, Purple dye

### House of Jabir (19-27)
- **Era:** Islamic Golden Age (8-9th century)
- **Focus:** Acids, salts, mineral processing
- **Success Rate:** 44% safe
- **Key Recipes:** Aqua regia, Alum, Borax, Oil of vitriol

### House of Paracelsus (28-36)
- **Era:** Renaissance (16th century)
- **Focus:** Medical alchemy, tinctures
- **Success Rate:** 44% safe
- **Key Recipes:** Laudanum, Antimony wine, Coral calx, Melissa cordial

## TRIG6 Quick Primer

Each recipe has 6 parameters:

1. **θ (theta)**: Process phase [0, 2π]
2. **R**: Resonance (efficacy) [0, 1]
3. **D**: Drift (toxicity) [0, 1]
4. **N**: Noise (uncertainty) [0, 1]
5. **Danger Zones**: Unstable regimes
6. **Fitness**: f = R × (1 - D) × (1 - N)

## Safety Warning

⚠️ **FOR MODELING ONLY - NOT OPERATIONAL CHEMISTRY**

All recipes use normalized, symbolic parameters. This is computational archaeology, not a chemistry manual. Do not attempt to recreate any recipe.

## Contributing

To add new recipes or improve documentation:
1. Follow the schema in `ALCHEMY_GENE_TEMPLATE.yaml`
2. Update `TRIG6_ALCHEMICAL_INDEX.yaml`
3. Update summary statistics in Appendix G
4. Maintain safety disclaimers

## References

See Chapter 16 for complete citations.

---

**Last Updated:** 2026-01-25  
**Status:** Complete - 36 recipes encoded across 4 houses
