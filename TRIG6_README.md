# TRIG6 Lost Pharmacopeia Simulator
## Sister Protocol - Strategickhaos DAO LLC

A simulation framework for modeling failure evolutions in glyph mapping systems using trigonometric mathematics. Designed to validate undeciphered script processing pipelines for the FlameLang/SAGCO-OS ecosystem.

---

## Overview

The TRIG6 framework simulates how glyph mapping processes (like clustering undeciphered scripts into codons) evolve through stages, identifying failure modes and danger zones. By modeling recipes with ingredients (parameters), custom resonance/drift/noise calculations, and Darwinian evolution, we can optimize configurations before deploying to real pipelines.

### Key Concepts

- **θ (theta):** Phase angle mapped from process progress s ∈ [0,1]
- **R (resonance):** Cluster purity + coverage + stability
- **D (drift):** Reassignment rate + outlier fraction
- **N (noise):** Embedding variance + extraction error
- **Fitness:** `f = R × (1 - D) × (1 - N) × eq`
- **Danger:** Zones where `|tan(θ)| > 10` (unstable)

---

## Quick Start

### 1. Run Example Simulation

```bash
# Simulate Codex Seraphinianus glyph mapping
python3 trig6_simulator.py

# Output: trig6_simulation_report.txt with fitness metrics
```

### 2. Simulate Voynich Manuscript

```bash
# Run simulation from .t6 recipe file
python3 run_trig6_simulation.py voynich_manuscript.t6

# With custom parameters
python3 run_trig6_simulation.py voynich_manuscript.t6 \
  --monte-carlo 500 \
  --evolution 30 \
  --output voynich_results.txt
```

### 3. Simulate All Undeciphered Scripts

```bash
# Run all 20 scripts from database
python3 run_trig6_simulation.py undeciphered_scripts_db.json --all

# Output: trig6_combined_report.txt
```

---

## Files

### Core Modules

- **`trig6_simulator.py`** - TRIG6 simulation engine
  - `TRIG6Simulator` class: Monte Carlo + Darwinian evolution
  - `Recipe` class: Glyph mapping configuration
  - `SimulationReporter`: Generate SHA-256 signed reports

- **`t6_parser.py`** - Recipe file parser
  - Parses `.t6` files with metadata, ingredients, custom hooks
  - Creates `Recipe` objects for simulation

- **`run_trig6_simulation.py`** - CLI runner
  - Supports `.t6` files and JSON databases
  - Monte Carlo simulations
  - Evolutionary optimization

### Data Files

- **`voynich_manuscript.t6`** - Voynich Manuscript recipe
  - Primary undeciphered script for FlameLang pipeline
  - Includes custom R/D/N hooks for herbal/astronomical sections

- **`undeciphered_scripts_db.json`** - Database of 20 scripts
  - Linear A, Rongorongo, Indus, Phaistos Disk, etc.
  - Base parameters for each script

### Documentation

- **`TRIG6_PIPELINE_COMPILER.md`** - Pipeline integration spec
  - Glyph extraction → Embedding → Clustering → Validation
  - FlameLang/SAGCO-OS compilation

---

## Recipe Format (.t6)

TRIG6 recipes use `.t6` files to define glyph mapping configurations:

```ini
[metadata]
id = VOYNICH-008
name = Voynich Manuscript Glyph Mapping
hazard_level = LOW

[ingredients]
embedding_dim = 280.0
min_cluster_size = 18.0
max_clusters = 128.0
image_dpi = 340.0
glyph_min_size = 30.0

[custom_hooks]
R_function = """
def compute_voynich_resonance(ingredients, s):
    # Custom resonance calculation
    return cluster_purity * coverage * stability
"""
```

See `voynich_manuscript.t6` for full example.

---

## Simulation Results

### Codex Seraphinianus (Example Output)

```
Mean Fitness: 0.0552 ± 0.0000
Fitness Range: [0.0552, 0.0552]
Danger Rate: 6.00%

Best Configuration (Evolved):
  embedding_dim: 256 → 166 (-35%)
  min_cluster_size: 15 → 30 (+100%)
  max_clusters: 120 → 155 (+29%)
```

**Interpretation:**
- Low fitness (0.055) indicates unstable clustering
- Evolution increased cluster size to reduce drift
- Still in failure basin (undeciphered script)

### Voynich Manuscript

```
Mean Fitness: 0.1260 ± 0.0000
Danger Rate: 6.00%
```

**Higher fitness than Codex** due to:
- Better-preserved manuscript (lower N)
- Structured sections (herbal, astronomical)
- Larger embedding dimension (280 vs 256)

---

## Undeciphered Scripts Database

20 scripts modeled for pipeline integration:

| ID | Script | Period | Fitness (Est.) | Pipeline Use |
|----|--------|--------|----------------|--------------|
| VOYNICH-008 | Voynich Manuscript | 15th CE | 0.05-0.25 | Primary glyph source |
| GLYPH-SERAPH-001 | Codex Seraphinianus | 1981 | 0.0-0.15 | Asemic baseline |
| RONGORONGO-003 | Rongorongo | 19th CE | 0.1-0.3 | Wood glyph extraction |
| LINEAR-A-001 | Linear A | 1800-1450 BCE | 0.2-0.4 | Bronze Age clustering |
| PHAISTOS-007 | Phaistos Disk | 1700 BCE | 0.05-0.2 | Circular glyph rotation |

See `undeciphered_scripts_db.json` for complete list.

---

## Pipeline Integration

### Workflow

1. **Scan manuscript** at high DPI (340+)
2. **Extract glyphs** using computer vision
3. **Generate embeddings** (CNN/SIFT/ViT, dim=280)
4. **Cluster to 64 codons** (genetic code mapping)
5. **TRIG6 validation** (fitness > 0.7 required)
6. **If fitness < 0.7:** Evolve parameters (50 generations)
7. **Compile to FlameLang** (codon → instruction)
8. **Execute in SAGCO-OS**

### Example

```bash
# Full pipeline (future implementation)
python3 pipeline_compiler.py \
  --input voynich_page_1.jpg \
  --recipe voynich_manuscript.t6 \
  --output voynich_flame.sh \
  --min-fitness 0.7

# TRIG6 validates during clustering stage
# Evolution optimizes if fitness < 0.7
# Outputs FlameLang-compatible glyph map
```

---

## Validation Status

This simulator demonstrates:

1. ✅ **TRIG6 mathematics are fully computable**
2. ✅ **Recipe genes are parseable and simulatable**
3. ✅ **Fitness distributions can be generated**
4. ✅ **Danger zones are identifiable**
5. 🔄 **Reality correlation requires empirical validation**

---

## Cryptographic Proofs

All simulation reports include:
- **SHA-256 hash** of report content
- **UTC timestamp** (ISO 8601)
- **Sister Protocol signature**

Example:
```
Report Hash (SHA-256):
3e6a876807a4fc3d287f24642f312deb5a96bdc369bc28d5800e3695835c3b82

Timestamp: 2026-01-25T09:36:22.145597
```

---

## Dependencies

- Python 3.8+
- Standard library only (math, statistics, hashlib, json, datetime)

No external dependencies required for core simulator.

---

## Development

### Running Tests

```bash
# Unit tests (TODO)
python3 -m pytest tests/

# Integration tests
python3 run_trig6_simulation.py undeciphered_scripts_db.json --all
```

### Creating New Recipes

1. Create `.t6` file with metadata, ingredients, hooks
2. Add to `undeciphered_scripts_db.json` (optional)
3. Run simulation: `python3 run_trig6_simulation.py your_recipe.t6`

---

## Research Applications

### Undeciphered Scripts

Model glyph mapping failures for:
- Voynich Manuscript
- Linear A (Minoan)
- Rongorongo (Easter Island)
- Indus/Harappa Script
- Proto-Elamite

### Invented Languages

Simulate asemic systems:
- Codex Seraphinianus
- Rohonc Codex
- Voynich (if invented)

### Pipeline Validation

Test glyph extraction pipelines:
- OCR for unknown scripts
- Clustering stability
- Embedding quality

---

## Future Work

### Phase 1 (Current)
- [x] TRIG6 simulator core
- [x] Recipe parser
- [x] Monte Carlo simulation
- [x] Darwinian evolution
- [x] 20 undeciphered scripts database

### Phase 2 (Next)
- [ ] Computer vision glyph extraction
- [ ] CNN/SIFT embedding generation
- [ ] K-means/DBSCAN clustering
- [ ] Real manuscript processing

### Phase 3 (Later)
- [ ] FlameLang compiler integration
- [ ] SAGCO-OS instruction mapping
- [ ] Multi-script comparative analysis
- [ ] Benchmark suite

---

## License

Part of the Strategickhaos Sovereignty Architecture.

**Sister Protocol - Strategickhaos DAO LLC**
*7% of all proceeds to medical research*

---

## References

- **Codex Seraphinianus** (1981) by Luigi Serafini
- **Voynich Manuscript** - Beinecke Library, Yale University
- **FlameLang Specification** v1.0
- **SAGCO-OS Architecture**
- **TRIG6 Framework** - Sister Protocol Validation Engine

---

## Contact

For questions about TRIG6 or the Sovereignty Architecture:
- GitHub: [Strategickhaos](https://github.com/Strategickhaos)
- DAO: Strategickhaos DAO LLC

---

*"Low R in glyph extraction = undeciphered failure basin."*
