# Voynich Diagnostic Pipeline

## Overview

This pipeline implements a TRIG6-based diagnostic system for analyzing Voynich manuscript glyphs, clustering them into symbols, and evolving optimal mappings using Darwinian selection algorithms.

## Files

- **`voynich_diag_pipeline.yaml`** - Pipeline configuration with TRIG6 parameters and stage definitions
- **`voynich_runner.py`** - Python runner implementing TRIG6 evaluation and evolution loops
- **`spec/codon_table_voy_diag_v1.json`** - Codon mapping table for diagnostic operations

## Pipeline Stages

1. **Ingest** - Parse Voynich PDF into structured glyph data
2. **Anomaly Detection** - Identify glyph deviations using Isolation Forest
3. **Glyph Extraction** - Extract visual features (shape entropy, stroke count, etc.)
4. **Glyph Embedding** - Generate 192-dimensional embeddings using autoencoder
5. **Glyph Clustering** - Cluster glyphs into 48 symbol groups using K-means
6. **Symbol Assignment** - Map clusters to Voynich symbol identifiers
7. **Codon Mapping** - Initialize diagnostic codon mappings
8. **TRIG6 Evaluation** - Calculate fitness metrics:
   - **Theta (θ)** - Decipher progress phase
   - **Resonance (R)** - Pattern consistency and coverage
   - **Drift (D)** - Variance rate and outlier fraction
   - **Noise (N)** - Embedding variance and entropy
   - **Equilibrium (eq)** - Count vs target alignment
   - **Fitness** - Overall quality: R × (1 - D) × (1 - N) × eq
9. **Evolution Loop** - Darwinian optimization over 48 generations
10. **Codon Stream Emission** - Output optimized diagnostic codons
11. **Compiler Integration** - Compile for SAGCO-OS sandbox

## TRIG6 Formulas

```python
theta = 2 * PI * decipher_progress
R = clamp(0.55 * pattern_consistency + 0.45 * coverage, 0.0, 1.0)
D = clamp(0.65 * variance_rate + 0.35 * outlier_frac, 0.0, 1.0)
N = clamp(0.55 * embed_variance + 0.45 * entropy_norm, 0.0, 1.0)
eq = clamp(1.0 - abs(count - target) / target, 0.0, 1.0)
danger = abs(tan(theta)) > tan_danger_limit or variance_rate > 0.1
fitness = R * (1.0 - D) * (1.0 - N) * eq
```

## Evolution Parameters

- **Generations**: 48 (matching Voynich alphabet estimate)
- **Population Size**: 12
- **Top K Selection**: 3
- **Mutation Rate**: 0.28
- **Mutation Targets**: n_clusters, strategy, thresholds, glyph_variance_threshold

## Usage

```bash
# Run the pipeline
python3 voynich_runner.py

# View outputs
ls artifacts/voynich_diag/
```

## Dependencies

```bash
pip install pyyaml numpy scikit-learn
```

## Output Structure

```
artifacts/voynich_diag/
├── glyphs.json                          # Raw glyph data
├── anomalies.json                       # Detected anomalies
├── glyphs/
│   ├── raw/                            # Raw glyph features
│   ├── embeddings.npy                  # 192-dim embeddings
│   ├── cluster_labels.npy              # Cluster assignments
│   ├── cluster_stats.json              # Clustering statistics
│   └── metadata.json                   # Glyph metadata
├── symbols/
│   └── symbol_table.json               # Symbol assignments
├── binding/
│   ├── symbol_to_codon_v0.json         # Initial mapping
│   ├── symbol_to_codon_champion.json   # Evolved champion
│   ├── trig6_report.json               # TRIG6 metrics
│   ├── trig6_state_history.json        # Evolution state
│   ├── evolution_log.json              # Generation history
│   ├── codon_streams/                  # Emitted codons
│   ├── fix_bins/                       # Compiled binaries
│   └── runtime_logs/                   # Execution logs
└── audit/                              # GPG-signed audit logs
```

## Target Metrics

- **Equilibrium Target**: 0.92
- **Tan Danger Limit**: 7.5
- **Warning Threshold**: 0.65
- **Target Fitness**: 0.85+

## Governance

**License**: © 2026 Strategickhaos DAO LLC – Internal Use  
**Constraints**: No decipher claims, Sandbox only, Open methodology  
**Audit**: SHA256 hashing + GPG signing (key: AE5519579584DEF5)

## Author

Domenic Gabriel Garza  
Strategickhaos DAO LLC  
Version: 1.0.1
