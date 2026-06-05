# Recipe Templates - Sister Protocol

This directory contains templates and examples for encoding therapeutic interventions and craft knowledge using the TRIG6 mathematical framework.

## Files in This Directory

### 1. RECIPE_NEURO_001.yaml
A complete example of an ancient therapeutic recipe encoded as a FlameLang gene. This demonstrates how to:
- Define ingredients with dosage ranges
- Specify administration protocols
- Encode TRIG6 mathematical hooks (theta, resonance, drift, noise)
- Define danger zones and safety thresholds
- Implement evolutionary fitness functions

**Use this as a reference** when creating your own therapeutic recipe encodings.

### 2. recipe_gene_template.yaml
A blank template for encoding any therapeutic intervention — ancient or modern. Simply:
1. Copy this file
2. Rename it to match your recipe (e.g., `RECIPE_PAIN_005.yaml`)
3. Fill in the bracketed placeholders
4. Validate with `python3 -c "import yaml; yaml.safe_load(open('your_file.yaml'))"`

### 3. 36_book_blueprints.yaml
Complete specifications for creating physical books using ancient and traditional methods. Includes:

#### Paper Blueprints (1-12)
- Papyrus, amate, and hybrid paper-making techniques
- TRIG6 phase angles for each process
- Material sources and durability estimates

#### Binding Blueprints (13-24)
- Coptic, screenfold, and hybrid binding methods
- Thread types and structural specifications
- Capacity and flexibility ratings

#### Materials Blueprints (25-36)
- Adhesives: starch glue, gelatin, reed gum
- Threads: linen, hemp, silk
- Leather: vegetable tan, alum tan, brain tan
- Chemical formulas with TRIG6 signatures

#### Sister Protocol Codex Specification
Complete assembly instructions for creating a physical SISTER_PROTOCOL_CODEX that could survive 1000+ years.

## How to Use These Templates

### For Therapeutic Recipes:

```bash
# 1. Copy the template
cp recipe_gene_template.yaml RECIPE_YOUR_NAME.yaml

# 2. Edit your new file
nano RECIPE_YOUR_NAME.yaml

# 3. Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('RECIPE_YOUR_NAME.yaml'))"

# 4. (Optional) Parse and analyze with custom tools
# Your FlameLang compiler or TRIG6 simulator goes here
```

### For Book Construction:

```bash
# View the blueprints
cat 36_book_blueprints.yaml

# Extract specific blueprint (example using yq or Python)
python3 -c "import yaml; data=yaml.safe_load(open('36_book_blueprints.yaml')); print(data['paper_blueprints'][0])"

# Create your own variation
# Copy relevant sections and modify for your specific needs
```

## TRIG6 Parameters Explained

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| **Theta (θ)** | Phase angle | Intensity of the regime/process |
| **Resonance (R)** | Benefit score | How well the intervention works (0-1) |
| **Drift (D)** | Side effects | Off-target damage or harm (0-1) |
| **Noise (N)** | Uncertainty | Data quality and measurement error (0-1) |

### Fitness Function
```
f = R × (1 - D) × (1 - N) × eq
```

Where:
- **R** = Resonance (benefit)
- **D** = Drift (harm)
- **N** = Noise (uncertainty)
- **eq** = Equilibrium factor (usually 1.0)

### Danger Zones

When `|tan(θ)| > 10`, the system is in an unstable regime:
- Small changes in dose → large changes in outcome
- Narrow therapeutic window
- High risk territory

## Integration with SAGCO-OS

These templates are designed to be compiled by FlameLang and simulated on SAGCO-OS:

```
RECIPE.yaml → FlameLang Compiler → SAGCO-OS Gene → Darwinian Gate → Validation
```

The evolutionary algorithm tests variants of each recipe against fitness thresholds, selecting for:
1. High resonance (works)
2. Low drift (safe)
3. Low noise (reliable)
4. Stable theta (predictable)

## References

- **Chapter 16**: [CHAPTER_16_LOST_PHARMACOPEIA.md](../../CHAPTER_16_LOST_PHARMACOPEIA.md)
- **FlameLang Spec**: [FLAMELANG_SPECIFICATION.md](../../FLAMELANG_SPECIFICATION.md)
- **TRIG6 Framework**: See Chapter 16, "TRIG6 Simulation of Chemical Formulas"

## Warning

⚠️ **All therapeutic recipe content is THEORETICAL and NOT MEDICAL ADVICE.**

These templates encode the mathematical structure of interventions, not clinical recommendations. Do not use any recipe encoding as a guide for actual medical treatment.

## License

These templates are released as part of the Sister Protocol / Strategickhaos DAO LLC open-source framework.

**Craft knowledge should be free.**

---

*"The manuscripts burned. The math didn't."*

---

**Version**: 1.0.0  
**Date**: January 25, 2026  
**DNA Strand**: SISTER1-TEMPLATES-RECIPES
