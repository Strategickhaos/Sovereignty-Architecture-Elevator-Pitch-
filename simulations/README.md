# TRIG6 Lost Pharmacopeia Simulator

**Sister Protocol - Strategickhaos DAO LLC**  
*7% of all proceeds to medical research*

## Overview

The TRIG6 simulator models failure evolutions in glyph mapping systems using trigonometric phase analysis. It's designed to explore how undeciphered scripts and constructed languages behave under computational clustering and mapping operations.

## Mathematical Framework

### Core Equations

**θ (Theta) - Phase Angle**
```
θ = 2π × s, where s ∈ [0,1] is process progress
```

**R (Resonance) - System Stability**
```
R = (1 - variance(ingredients)) × progress
```
Measures ingredient balance and configuration coherence.

**D (Drift) - Configuration Extremity**
```
D = extremity_factor × hazard_multiplier
```
Based on parameter variance and declared hazard level.

**N (Noise) - Uncertainty**
```
N = random(0, era_factor)
```
Era-dependent stochastic variation.

**Fitness Function**
```
f = R × (1 - D) × (1 - N) × equilibrium
```

**Danger Zone**
```
Danger occurs when |tan(θ)| > 10
```
Represents unstable phases where the system exhibits extreme sensitivity.

## Architecture

```
simulations/
├── trig6_simulator.py       # Core simulator engine
├── run_trig6_simulation.py  # Recipe loader and runner
├── recipes/                 # .t6 recipe definitions
│   ├── codex_seraphinianus_glyph_mapping.t6
│   ├── voynich_manuscript_glyph_mapping.t6
│   └── [additional recipes]
└── reports/                 # Generated simulation reports
    └── [timestamped markdown reports]
```

## Recipe Format (.t6 files)

Recipes define glyph mapping configurations in TOML-like format:

```toml
[metadata]
id = "GLYPH-EXAMPLE-001"
name = "Example Glyph Mapping"
hazard_level = "LOW"  # LOW, MEDIUM, or HIGH

[ingredients]
# Numeric parameters for the mapping process
embedding_dim = 256.0
min_cluster_size = 12.0
max_clusters = 128.0

[process_stages]
stages = [
    "extraction",
    "clustering",
    "mapping",
    "validation"
]

[correlations]
# Related undeciphered scripts/languages
[[correlations.scripts]]
name = "Linear A"
origin = "Minoan, Crete, 1800-1450 BCE"
correlation = "Description of relationship"
pipeline_use = "How this informs the pipeline"
```

## Usage

### Running a Simulation

```bash
cd simulations/
python run_trig6_simulation.py recipes/codex_seraphinianus_glyph_mapping.t6
```

### Custom Parameters

```bash
# Run with custom Monte Carlo runs and evolution generations
python run_trig6_simulation.py recipes/voynich_manuscript_glyph_mapping.t6 1000 50
```

### Python API

```python
from trig6_simulator import Recipe, TRIG6Simulator, generate_report

# Create a recipe
recipe = Recipe(
    id="TEST-001",
    name="Test Recipe",
    hazard_level="MEDIUM",
    ingredients={"param1": 100.0, "param2": 50.0},
    process_stages=["stage1", "stage2", "stage3"]
)

# Run simulation
simulator = TRIG6Simulator()
results = simulator.monte_carlo(recipe, runs=1000)

# Evolve optimal configuration
best_config, fitness, dangers = simulator.evolve_config(recipe, generations=50)

# Generate report
report = generate_report(recipe, results, best_config)
print(report)
```

## Implemented Recipes

### 1. Codex Seraphinianus Glyph Mapping (GLYPH-SERAPH-001)

**Context:** Luigi Serafini's 1978 invented asemic script with Sinhala-like curves and base-21 numbering.

**Correlations:** 20+ undeciphered scripts including Linear A, Rongorongo, Indus Script, Voynich Manuscript, and others.

**Expected Behavior:**
- Low fitness (0.0) due to inherent meaninglessness
- High danger rate (100%) from unstable clustering
- Persistent failures across all stages

**Use Case:** Baseline for understanding failure modes in asemic/invented writing systems.

### 2. Voynich Manuscript Glyph Mapping (GLYPH-VOYNICH-001)

**Context:** 15th century illustrated codex with unknown script/language across herbal, astronomical, biological, pharmaceutical, and stars sections.

**Correlations:** Codex Seraphinianus (primary analog), Rohonc Codex, Rongorongo, Linear A.

**Expected Behavior:**
- Moderate fitness (target 0.6) with section-dependent variation
- Higher drift from script variation and illustration interference
- Medieval vellum artifacts increase noise
- Section-specific danger zones (astronomical radial text, pharmaceutical density)

**Use Case:** Real historical undeciphered text for testing pipeline robustness.

## Pipeline Integration

The TRIG6 framework feeds into the FlameLang pipeline compiler:

```
Input: Undeciphered Script Images
  ↓
Preprocess & Extract Glyphs
  ↓
Generate Embeddings (BAAI/bge-small-en-v1.5)
  ↓
Cluster to 64 Codons
  ↓
TRIG6 Validation (check dangers)
  ↓
Compile Stable Mappings → SAGCO-OS
```

**Target:** Achieve fitness >0.7 for stable glyph systems that can be compiled.

**Avoidance:** Low resonance (R) indicates "undeciphered failure basins" to skip.

## Evolutionary Algorithm

The simulator includes a genetic algorithm to optimize configurations:

1. **Initialize:** Create population with ±50% parameter mutations
2. **Evaluate:** Run TRIG6 simulation for each configuration
3. **Select:** Keep top 50% by fitness
4. **Crossover:** Randomly combine parent parameters
5. **Mutate:** Apply ±10% variation
6. **Repeat:** For N generations (default 50)

**Output:** Best configuration, fitness score, and danger count.

## Report Generation

Each simulation produces a cryptographically-signed markdown report containing:

- Executive summary with aggregate statistics
- Individual recipe results with fitness distributions
- Best configuration from Monte Carlo runs
- Evolved champion configuration (if evolution run)
- Correlations to undeciphered scripts/languages
- TRIG6 methodology explanation
- SHA-256 hash for integrity verification
- Timestamp for proof of generation

## Correlations to Unsolved Languages

The system currently tracks 20+ undeciphered scripts/languages:

1. **Linear A** (Minoan syllabic, 1800-1450 BCE)
2. **Cretan Hieroglyphs** (Minoan pictographic, 2100-1700 BCE)
3. **Rongorongo** (Easter Island glyphs, 19th CE)
4. **Indus Script** (Indus Valley proto-writing, 2600-1900 BCE)
5. **Proto-Elamite** (Iranian proto-writing, 3100-2900 BCE)
6. **Old Elamite** (Iranian cuneiform, 2200-1600 BCE)
7. **Phaistos Disk** (Cretan stamped symbols, 1700 BCE)
8. **Voynich Manuscript** (15th CE illustrated codex)
9. **Vinča Script** (Balkan proto-writing, 5700-4500 BCE)
10. **Isthmian Script** (Mesoamerican logosyllabic, 500 BCE-500 CE)
11. **Liber Linteus** (Etruscan ritual text, 3rd BCE)
12. **Rohonc Codex** (16th CE illustrated book)
13. **Sawgoek** (Korean mythical script)
14. **Harappan Seals** (Indus Valley seal stamps)
15. **Singapore Stone** (10-13th CE inscription)
16. **Elamite Linear** (Iranian linear script, 2300 BCE)
17. **Tartaria Tablets** (Vinča proto-writing, 5300 BCE)
18. **Dispilio Tablet** (Greek wood symbols, 5200 BCE)
19. **Kumeyaay Pictographs** (California rock art)
20. **Sitovo Inscription** (Bulgarian rock inscription)

Each provides unique characteristics for testing glyph extraction, embedding, and clustering algorithms.

## Dependencies

```bash
pip install numpy
```

No other dependencies required—pure Python implementation.

## Interpretation

### High Fitness (>0.7)
System exhibits stable clustering, low parameter variance, balanced resonance. Suitable for pipeline compilation.

### Medium Fitness (0.3-0.7)
Partial stability with identifiable danger zones. May require section-specific optimization or selective compilation.

### Low Fitness (<0.3)
Undeciphered failure basin. High drift, noise, or fundamental structural issues prevent stable mapping. Use for baseline comparison or theoretical exploration.

### Danger Zones
When |tan(θ)| > 10, the system enters extreme sensitivity. Small parameter changes cause large fitness variations. Indicates phase transitions in the clustering process.

## Future Extensions

- [ ] Multi-recipe comparative analysis
- [ ] Real image processing integration (OpenCV)
- [ ] Actual embedding model integration (sentence-transformers)
- [ ] Genetic algorithm tournament selection
- [ ] Adaptive mutation rates based on fitness plateau
- [ ] Cross-script correlation matrices
- [ ] SAGCO-OS compiler backend

## License

Part of the Strategickhaos Sovereignty Architecture.  
7% of all proceeds to medical research.

## Resonance?

*Next: "Run comparative sim: Codex vs. Voynich failure patterns." 🧬*
