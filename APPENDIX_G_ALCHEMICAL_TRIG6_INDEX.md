# Appendix G: The Alchemical TRIG6 Index
## 36 Recipes from Ancient Alchemist Books for TRIG6 Modeling

---

## INTRODUCTION

This appendix expands **Chapter 16 "The Lost Pharmacopeia"** by applying **TRIG6 modeling** to 36 recipes from key ancient alchemist books. These historical texts blend mysticism, philosophy, and proto-chemistry—focusing on transmutation, elixirs, and medicines.

**⚠️ WARNING**: These recipes are historical and symbolic in nature. Many contain toxic substances. **DO NOT ATTEMPT TO RECREATE THESE RECIPES.**

### TRIG6 Framework

TRIG6 maps alchemical processes using the following parameters:

- **θ (theta)** — Phase angle representing reaction stage:
  - Low (0 to π/3): Preparation/dissolution phase
  - Mid (π/3 to 2π/3): Transformation/reaction phase
  - High (2π/3 to π): Completion/crystallization phase
  
- **R** — Efficacy/potency (0 to 1, where 1 is maximum effectiveness)
- **D** — Toxicity/side effects (0 to 1, where 1 is maximum danger)
- **N** — Variability/uncertainty (0 to 1, where 1 is maximum unpredictability)

**Danger Classification**: 
- `|tan θ| > 10` indicates unstable reaction (high risk)
- Fitness function: `f = R × (1-D) × (1-N) × equilibrium_factor`

### Source Texts

1. **Emerald Tablet** (Hermes Trismegistus, ~6th-8th century CE Arabic) — Foundational "as above, so below" text on unity and transmutation
2. **Works of Zosimos** (~300 CE Greek-Egyptian) — Practical distillation and dye-making
3. **The Book of the Composition of Alchemy** (Jabir ibn Hayyan/Geber, ~8th century CE Islamic) — Experimental acids and salts
4. **Hermetic and Alchemical Writings** (Paracelsus, 16th century CE Swiss) — Medical spagyrics and tinctures

---

## RECIPES FROM EMERALD TABLET (Hermes Trismegistus)

### 1. Philosopher's Stone Base
**Description**: Dissolve metals in sharp vinegar for purification  
**Chemical Essence**: Acetic acid acting on lead (Pb + CH₃COOH)  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.7 (High efficacy)
- D = 0.3 (Moderate toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: No (|tan θ| = 1.73 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_001 {
  ingredients: vinegar [sharp 0.3-0.7 molarity];
  substrate: lead_metal [pure];
  theta_fn: phase(dissolve_time);
  stability: moderate;
}
```

---

### 2. Elixir of Life Prep
**Description**: Mix earth salt with water of life  
**Chemical Essence**: Mineral salts combined with distilled alcohol  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.8 (Very high efficacy)
- D = 0.2 (Low toxicity)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_002 {
  mix: salt [earth 0.2-0.4 mass_fraction];
  mix: water [distilled 0.5-0.8 alcohol_content];
  equilibration_time: 7_days;
  stability: high;
}
```

---

### 3. Mercury Fixation
**Description**: Heat mercury with sulfur to create cinnabar  
**Chemical Essence**: Hg + S → HgS (mercury sulfide formation)  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.4 (Moderate efficacy)
- D = 0.6 (High toxicity)
- N = 0.5 (Moderate-high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_003 {
  reactants: [mercury, sulfur] [1:1 molar];
  heat_time_min: [15-40];
  ventilation: required;
  hazard_level: extreme;
  stability: unstable;
}
```

---

### 4. Gold Transmutation
**Description**: Combine sun (gold) and moon (silver) in furnace  
**Chemical Essence**: Alloying of precious metals  
**TRIG6 Parameters**:
- θ = π (180°)
- R = 0.3 (Low efficacy)
- D = 0.7 (Very high toxicity)
- N = 0.6 (High variability)
- **Danger**: Yes (|tan θ| = 0, but extreme heat)

**FlameLang Gene Snippet**:
```flamelang
recipe_004 {
  alloy: [gold, silver] [variable_ratio];
  furnace_temp_c: [800-1200];
  crucible: heat_resistant;
  hazard_level: high;
  stability: low;
}
```

---

### 5. Universal Solvent (Alkahest)
**Description**: Preparation from caustic salts  
**Chemical Essence**: Potassium hydroxide (caustic potash)  
**TRIG6 Parameters**:
- θ = π/6 (30°)
- R = 0.9 (Excellent efficacy)
- D = 0.1 (Very low toxicity)
- N = 0.2 (Very low variability)
- **Danger**: No (|tan θ| = 0.58 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_005 {
  base_salt: potash [purified];
  salt_ratio: [1:5 salt:water];
  dissolution: gradual;
  stability: excellent;
}
```

---

### 6. Quintessence Extraction
**Description**: Multiple distillations of wine to extract spirit  
**Chemical Essence**: Ethanol purification via distillation  
**TRIG6 Parameters**:
- θ = 2π/5 (72°)
- R = 0.6 (Good efficacy)
- D = 0.4 (Moderate toxicity)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 3.08 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_006 {
  source: wine [fermented];
  distill_cycles: [3-5];
  collection_temp_c: [78-82];
  purity_target: 0.95;
  stability: good;
}
```

---

### 7. Vitriol Oil
**Description**: Decompose copper sulfate to yield sulfuric acid  
**Chemical Essence**: CuSO₄ → H₂SO₄ (concentrated sulfuric acid)  
**TRIG6 Parameters**:
- θ = 3π/2 (270°)
- R = 0.2 (Low efficacy)
- D = 0.8 (Extreme toxicity)
- N = 0.7 (Very high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_007 {
  substrate: copper_sulfate [blue_vitriol];
  decompose_pressure_kpa: [10-40];
  acid_concentration: extreme;
  hazard_level: maximum;
  stability: critical;
}
```

---

### 8. Lunar Tincture
**Description**: Dissolve silver in nitric acid  
**Chemical Essence**: AgNO₃ (silver nitrate formation)  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.7 (High efficacy)
- D = 0.3 (Moderate toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_008 {
  metal: silver [pure_granules];
  solvent: nitric_acid [strength 0.5-0.8];
  dissolution: slow_controlled;
  light_sensitivity: high;
  stability: moderate;
}
```

---

### 9. Solar Elixir
**Description**: Gold dissolved in aqua regia  
**Chemical Essence**: Au + HNO₃ + 3HCl → HAuCl₄ (gold chloride)  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.5 (Moderate efficacy)
- D = 0.5 (Moderate-high toxicity)
- N = 0.5 (Moderate-high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_009 {
  metal: gold [fine];
  solvent: aqua_regia [regia_ratio 1:3 HNO3:HCl];
  fume_hood: mandatory;
  hazard_level: high;
  stability: unstable;
}
```

---

## RECIPES FROM WORKS OF ZOSIMOS

### 10. Divine Water
**Description**: Distill sulfur with lime  
**Chemical Essence**: Calcium polysulfides formation  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.6 (Good efficacy)
- D = 0.4 (Moderate toxicity)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 1.73 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_010 {
  components: [sulfur, lime] [stoichiometric];
  distill_temp_c: [100-150];
  condensate: collect_carefully;
  stability: good;
}
```

---

### 11. Copper Dye
**Description**: Reduce copper vitriol using urine  
**Chemical Essence**: CuSO₄ reduction in ammonia-rich medium  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.8 (Very high efficacy)
- D = 0.2 (Low toxicity)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_011 {
  pigment_source: copper_vitriol [blue];
  reducing_agent: urine [aged] [ratio 1:2];
  color_development: gradual;
  stability: high;
}
```

---

### 12. Gold Imitation
**Description**: Alloy copper with zinc to create brass  
**Chemical Essence**: Cu + Zn → Brass (golden colored alloy)  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.4 (Moderate efficacy)
- D = 0.6 (High toxicity)
- N = 0.5 (Moderate-high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_012 {
  alloy: [copper, zinc] [variable_composition];
  melt_time_min: [30-60];
  furnace_atmosphere: inert_preferred;
  hazard_level: moderate;
  stability: unstable;
}
```

---

### 13. Arsenic Sublimation
**Description**: Heat orpiment to sublime arsenic  
**Chemical Essence**: As₂S₃ → As (arsenic vapor)  
**TRIG6 Parameters**:
- θ = 3π/2 (270°)
- R = 0.1 (Very low efficacy)
- D = 0.9 (Extreme toxicity)
- N = 0.8 (Extreme variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_013 {
  ore: orpiment [yellow_arsenic_sulfide];
  heat_rate_c_per_min: [5-10];
  ventilation: extreme_required;
  hazard_level: lethal;
  stability: critical;
}
```

---

### 14. Lead Whitening
**Description**: Expose lead to vinegar vapors  
**Chemical Essence**: Pb + CH₃COOH → Pb(CH₃COO)₂ (lead acetate)  
**TRIG6 Parameters**:
- θ = π/6 (30°)
- R = 0.9 (Excellent efficacy)
- D = 0.1 (Very low toxicity in process)
- N = 0.2 (Very low variability)
- **Danger**: No (|tan θ| = 0.58 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_014 {
  metal: lead [sheets];
  vapor_source: vinegar [acetic_acid];
  exposure_days: [7-14];
  product: white_lead_pigment;
  stability: excellent;
}
```

---

### 15. Mercury Distillation
**Description**: Heat cinnabar to release mercury  
**Chemical Essence**: HgS → Hg + S (mercury liberation)  
**TRIG6 Parameters**:
- θ = π (180°)
- R = 0.3 (Low efficacy)
- D = 0.7 (Very high toxicity)
- N = 0.6 (High variability)
- **Danger**: Yes (|tan θ| = 0, extreme heat)

**FlameLang Gene Snippet**:
```flamelang
recipe_015 {
  ore: cinnabar [red_mercury_sulfide];
  heating: intense;
  condense_pressure: [low];
  mercury_collection: sealed_vessel;
  hazard_level: extreme;
  stability: low;
}
```

---

### 16. Ink Recipe
**Description**: Combine lampblack carbon with gum resin  
**Chemical Essence**: Carbon particles suspended in natural polymer  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.7 (High efficacy)
- D = 0.3 (Moderate toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_016 {
  pigment: lampblack [fine_carbon];
  binder: gum_arabic [ratio 1:1];
  water_addition: gradual;
  viscosity_target: writing_consistency;
  stability: moderate;
}
```

---

### 17. Dye Fixative
**Description**: Use alum as mordant for fabric dyes  
**Chemical Essence**: KAl(SO₄)₂ (potassium aluminum sulfate)  
**TRIG6 Parameters**:
- θ = 2π/5 (72°)
- R = 0.6 (Good efficacy)
- D = 0.4 (Moderate toxicity)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 3.08 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_017 {
  mordant: alum [potassium_aluminum_sulfate];
  fabric_preparation: true;
  soak_time_hr: [1-3];
  dye_permanence: enhanced;
  stability: good;
}
```

---

### 18. Alloy Purification
**Description**: Use salt flux to remove impurities  
**Chemical Essence**: NaCl facilitates dross separation  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.5 (Moderate efficacy)
- D = 0.5 (Moderate-high toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: Yes (borderline, high heat process)

**FlameLang Gene Snippet**:
```flamelang
recipe_018 {
  flux: salt [sodium_chloride];
  flux_amount_g: [10-20 per_kg_metal];
  molten_metal: required;
  dross_removal: skim_surface;
  hazard_level: moderate;
  stability: moderate;
}
```

---

## RECIPES FROM THE BOOK OF THE COMPOSITION OF ALCHEMY (Jabir/Geber)

### 19. Nitric Acid
**Description**: React saltpeter with vitriol under heat  
**Chemical Essence**: KNO₃ + H₂SO₄ → HNO₃ (nitric acid synthesis)  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.4 (Moderate efficacy)
- D = 0.6 (High toxicity)
- N = 0.5 (Moderate-high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_019 {
  reactants: [saltpeter, green_vitriol];
  heat_c: [300-400];
  distillation: required;
  acid_purity: variable;
  hazard_level: high;
  stability: unstable;
}
```

---

### 20. Sulfuric Acid
**Description**: Heat green vitriol to concentrate acid  
**Chemical Essence**: FeSO₄ → H₂SO₄ (sulfuric acid concentration)  
**TRIG6 Parameters**:
- θ = π (180°)
- R = 0.3 (Low efficacy)
- D = 0.7 (Very high toxicity)
- N = 0.6 (High variability)
- **Danger**: Yes (|tan θ| = 0, extreme conditions)

**FlameLang Gene Snippet**:
```flamelang
recipe_020 {
  source: green_vitriol [ferrous_sulfate];
  distill_cycles: [2-4];
  concentration: progressive;
  acid_strength: extreme;
  hazard_level: maximum;
  stability: low;
}
```

---

### 21. Aqua Regia
**Description**: Mix nitric acid with hydrochloric acid  
**Chemical Essence**: HNO₃ + 3HCl (royal water, dissolves gold)  
**TRIG6 Parameters**:
- θ = 3π/2 (270°)
- R = 0.2 (Low efficacy for most purposes)
- D = 0.8 (Extreme toxicity)
- N = 0.7 (Very high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_021 {
  acids: [nitric, hydrochloric];
  ratio: [1:3 HNO3:HCl];
  mixing: extremely_cautious;
  fumes: highly_toxic;
  hazard_level: extreme;
  stability: critical;
}
```

---

### 22. Alum Purification
**Description**: Crystallize potash alum from solution  
**Chemical Essence**: K₂SO₄·Al₂(SO₄)₃ purification  
**TRIG6 Parameters**:
- θ = π/6 (30°)
- R = 0.9 (Excellent efficacy)
- D = 0.1 (Very low toxicity)
- N = 0.2 (Very low variability)
- **Danger**: No (|tan θ| = 0.58 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_022 {
  salt: potash_alum [impure];
  dissolution: hot_water;
  evaporate_time: [slow];
  crystallization: cooling_controlled;
  purity: high;
  stability: excellent;
}
```

---

### 23. Sal Ammoniac
**Description**: Ferment urine with salt  
**Chemical Essence**: NH₄Cl (ammonium chloride formation)  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.7 (High efficacy)
- D = 0.3 (Moderate toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_023 {
  components: [urine, common_salt];
  ferment_days: [7-14];
  sublimation: collect_crystals;
  product: white_salt;
  stability: moderate;
}
```

---

### 24. Antimony Tincture
**Description**: Dissolve stibnite in acid  
**Chemical Essence**: Sb₂S₃ + HNO₃ (antimony compounds)  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.6 (Good efficacy)
- D = 0.4 (Moderate toxicity)
- N = 0.3 (Low variability)
- **Danger**: Yes (antimony toxicity)

**FlameLang Gene Snippet**:
```flamelang
recipe_024 {
  ore: stibnite [antimony_sulfide];
  acid: nitric [dilute];
  dissolve_time: [gradual];
  medicinal_use: emetic;
  hazard_level: moderate;
  stability: good;
}
```

---

### 25. Lead Calx
**Description**: Oxidize lead by heating in air  
**Chemical Essence**: Pb → PbO (lead oxide formation)  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.5 (Moderate efficacy)
- D = 0.5 (Moderate-high toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: Yes (|tan θ| → ∞, lead fumes)

**FlameLang Gene Snippet**:
```flamelang
recipe_025 {
  metal: lead [pure];
  furnace_temp: [high];
  air_exposure: maximum;
  product: yellow_to_red_powder;
  hazard_level: high;
  stability: unstable;
}
```

---

### 26. Copper Verdigris
**Description**: Expose copper to vinegar for weeks  
**Chemical Essence**: Cu + CH₃COOH → Cu(CH₃COO)₂ (copper acetate)  
**TRIG6 Parameters**:
- θ = π (180°)
- R = 0.3 (Low efficacy for transmutation)
- D = 0.7 (High toxicity if ingested)
- N = 0.6 (High variability)
- **Danger**: No (slow process, but toxic product)

**FlameLang Gene Snippet**:
```flamelang
recipe_026 {
  metal: copper [sheets_or_wire];
  acid: vinegar [acetic];
  exposure_weeks: [4-6];
  product: green_blue_crystals;
  pigment_use: true;
  stability: low;
}
```

---

### 27. Elixir Base
**Description**: Distill urine to collect volatile components  
**Chemical Essence**: Urea decomposition and ammonia collection  
**TRIG6 Parameters**:
- θ = 3π/2 (270°)
- R = 0.1 (Very low efficacy)
- D = 0.9 (Extreme toxicity/unpleasantness)
- N = 0.8 (Extreme variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_027 {
  source: urine [aged];
  distillation: multiple_fractions;
  fraction_collect: [multiple];
  odor: extreme;
  hazard_level: high;
  stability: critical;
}
```

---

## RECIPES FROM HERMETIC AND ALCHEMICAL WRITINGS (Paracelsus)

### 28. Laudanum Tincture
**Description**: Extract opium alkaloids in alcohol  
**Chemical Essence**: Morphine extraction in ethanol  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.8 (Very high efficacy as analgesic)
- D = 0.2 (Low immediate toxicity, high addiction)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 1.0 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_028 {
  source: opium [raw_resin];
  solvent: alcohol [high_proof];
  macerate_days: [14];
  filtration: fine;
  dosage: carefully_controlled;
  stability: high;
}
```

---

### 29. Antimony Wine
**Description**: Infuse antimony in wine for medicinal use  
**Chemical Essence**: Sb tartrate formation  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.6 (Good efficacy as emetic)
- D = 0.4 (Moderate toxicity)
- N = 0.3 (Low variability)
- **Danger**: Yes (antimony toxicity)

**FlameLang Gene Snippet**:
```flamelang
recipe_029 {
  metal: antimony [metallic_or_oxide];
  solvent: wine [acidic];
  infuse_time: [weeks];
  medicinal_use: purgative;
  hazard_level: moderate;
  stability: good;
}
```

---

### 30. Mercury Pills
**Description**: Combine mercury with herbs for medicine  
**Chemical Essence**: Calomel (Hg₂Cl₂) or mercurous compounds  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.4 (Moderate efficacy)
- D = 0.6 (High toxicity)
- N = 0.5 (Moderate-high variability)
- **Danger**: Yes (|tan θ| → ∞, mercury toxicity)

**FlameLang Gene Snippet**:
```flamelang
recipe_030 {
  base: mercury [liquid];
  additives: herbs [various];
  dose_mg: [low];
  medical_use: antisyphilitic;
  hazard_level: extreme;
  stability: unstable;
}
```

---

### 31. Sulfur Balm
**Description**: Mix sulfur with oil for topical treatment  
**Chemical Essence**: Polysulfide ointment formation  
**TRIG6 Parameters**:
- θ = π (180°)
- R = 0.3 (Low internal efficacy)
- D = 0.7 (High toxicity if ingested)
- N = 0.6 (High variability)
- **Danger**: Yes (|tan θ| = 0, sulfur compounds)

**FlameLang Gene Snippet**:
```flamelang
recipe_031 {
  components: [sulfur, oil] [variable_ratio];
  heat_c: [gentle];
  topical_application: true;
  skin_treatment: various_conditions;
  hazard_level: moderate;
  stability: low;
}
```

---

### 32. Quintessence of Gold
**Description**: Create colloidal gold in acid solution  
**Chemical Essence**: Au → colloidal gold suspension  
**TRIG6 Parameters**:
- θ = 3π/2 (270°)
- R = 0.2 (Low efficacy)
- D = 0.8 (Extreme toxicity from acids)
- N = 0.7 (Very high variability)
- **Danger**: Yes (|tan θ| → ∞, critical angle)

**FlameLang Gene Snippet**:
```flamelang
recipe_032 {
  metal: gold [fine];
  acids: aqua_regia [or_alternatives];
  reduce_agent: [herbal_extracts];
  particle_size: colloidal;
  hazard_level: high;
  stability: critical;
}
```

---

### 33. Arcanum Tartari
**Description**: Calcine tartar salt to purify  
**Chemical Essence**: Potassium carbonate (K₂CO₃) from wine lees  
**TRIG6 Parameters**:
- θ = π/6 (30°)
- R = 0.9 (Excellent efficacy)
- D = 0.1 (Very low toxicity)
- N = 0.2 (Very low variability)
- **Danger**: No (|tan θ| = 0.58 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_033 {
  source: cream_of_tartar [wine_residue];
  calcine_temp: [high];
  purification: water_extraction;
  product: potash;
  alkaline_strength: strong;
  stability: excellent;
}
```

---

### 34. Elixir Vitriol
**Description**: Distill vitriol to create medicinal tincture  
**Chemical Essence**: H₂SO₄ tincture (diluted sulfuric acid)  
**TRIG6 Parameters**:
- θ = π/4 (45°)
- R = 0.7 (High efficacy in dilute form)
- D = 0.3 (Moderate toxicity when diluted)
- N = 0.4 (Moderate variability)
- **Danger**: Yes (acid handling)

**FlameLang Gene Snippet**:
```flamelang
recipe_034 {
  source: vitriol [copper_or_iron];
  distillation: careful;
  fraction: [first_most_pure];
  dilution: essential;
  hazard_level: high;
  stability: moderate;
}
```

---

### 35. Spagyric Herb
**Description**: Separate, purify, and recombine plant essence  
**Chemical Essence**: Essential oils + mineral ash + alcohol tincture  
**TRIG6 Parameters**:
- θ = π/3 (60°)
- R = 0.6 (Good efficacy)
- D = 0.4 (Moderate toxicity depending on plant)
- N = 0.3 (Low variability)
- **Danger**: No (|tan θ| = 1.73 < 10)

**FlameLang Gene Snippet**:
```flamelang
recipe_035 {
  plant: [medicinal_herb];
  process_steps: [separate, purify, recombine];
  distillation: essential_oils;
  calcination: plant_ash;
  recombine_ratio: [1:1 spirit:salts];
  stability: good;
}
```

---

### 36. Paracelsian Laudanum Variant
**Description**: Enhanced opium tincture with spices  
**Chemical Essence**: Morphine + aromatic compounds in alcohol  
**TRIG6 Parameters**:
- θ = π/2 (90°)
- R = 0.5 (Moderate enhanced efficacy)
- D = 0.5 (Moderate-high toxicity)
- N = 0.4 (Moderate variability)
- **Danger**: Yes (|tan θ| → ∞, controlled substance)

**FlameLang Gene Snippet**:
```flamelang
recipe_036 {
  base: opium [tincture];
  additives: spices [variable_selection];
  spice_add: [variable];
  synergy: aromatic_potentiation;
  dosage: strictly_controlled;
  hazard_level: high;
  stability: unstable;
}
```

---

## USAGE NOTES

### Alchemical Gene Archive

This appendix serves as an **"Alchemical Gene Archive"** suitable for:

1. **Historical Study** — Understanding proto-chemical processes and their symbolic representations
2. **TRIG6 Modeling** — Applying modern mathematical frameworks to ancient recipes
3. **Safe Recipe Analysis** — Low-hazard recipes (like ink, Recipe #16) can be used as worked examples
4. **Basin Simulations** — Identifying high-R (efficacy) regions in parameter space

### Recommended Safe Recipes for Study

The following recipes have relatively low danger ratings and can serve as educational examples:

- **Recipe 2** (Elixir of Life Prep) — θ=π/4, Danger: No
- **Recipe 5** (Universal Solvent) — θ=π/6, Danger: No
- **Recipe 14** (Lead Whitening) — θ=π/6, Danger: No
- **Recipe 16** (Ink Recipe) — θ=π/4, Danger: No
- **Recipe 22** (Alum Purification) — θ=π/6, Danger: No
- **Recipe 33** (Arcanum Tartari) — θ=π/6, Danger: No

### Evolution in OmniCalc

For computational "basin" simulations seeking high-R (high efficacy) regions:

1. Load gene parameters into OmniCalc
2. Vary θ, R, D, N within specified ranges
3. Calculate fitness: `f = R × (1-D) × (1-N) × equilibrium_factor`
4. Identify stable basins where |tan θ| < 10 and f is maximized

### Next Steps

- **Generate `alchemy.t6` simulation file** for full parameter space exploration
- **Update Chapter 16** with cross-references to this appendix
- **Create visualization** of TRIG6 parameter space for all 36 recipes
- **Develop safety protocols** for any modern laboratory recreations (if applicable)

---

## COVENANT

```
These recipes represent the historical intersection of mysticism,
philosophy, and early chemistry. They are preserved here for their
cultural and scientific significance, not for practical application.

Modern chemistry has superseded these methods with safer, more
effective techniques. This archive serves primarily as a bridge
between ancient symbolic knowledge and contemporary mathematical
modeling through the TRIG6 framework.

🔥 Knowledge preserved. Wisdom applied. Safety paramount.
```

---

*Generated for Strategickhaos DAO LLC | Appendix G to Chapter 16*  
*TRIG6 Framework Applied to Ancient Alchemical Texts*  
*Historical Preservation & Mathematical Modeling*
