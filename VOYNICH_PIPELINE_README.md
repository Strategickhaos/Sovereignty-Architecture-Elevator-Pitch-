# Voynich Diagnostic Pipeline - TRIG6 Cognitive Architecture

## Overview

This diagnostic pipeline implements the TRIG6 cognitive architecture for analyzing the Voynich Manuscript glyphs as a test substrate. It demonstrates the same cognitive framework used for Starlink and Codex analysis, proving the reusability of the architecture across different problem domains.

## Architecture

The pipeline uses **TRIG6** - a 6-component cognitive evaluation framework:

- **θ (Theta)**: Angular progress indicator [0, 2π]
- **R (Resonance)**: Pattern alignment quality [0, 1]
- **D (Drift)**: Variance and instability [0, 1]  
- **N (Noise)**: Embedding quality metrics [0, 1]
- **eq (Equilibrium)**: Distance from target state [0, 1]
- **Danger**: Safety threshold monitoring (boolean)

**Fitness Function**: `F = R × (1 - D) × (1 - N) × eq`

## Files

- `voynich_diag_pipeline.yaml` - Complete pipeline configuration
- `voynich_runner.py` - Executable Python implementation

## Usage

### Quick Start

```bash
# Install dependencies
pip install numpy pyyaml scikit-learn

# Run the pipeline
python3 voynich_runner.py
```

### What It Does

1. **Ingest**: Generate/extract glyph features (stub using synthetic data)
2. **Anomaly Detection**: IsolationForest identifies irregular patterns
3. **Glyph Extraction**: Feature engineering (shape, stroke, context)
4. **Embedding**: Dimensionality reduction via autoencoder
5. **Clustering**: KMeans groups similar glyphs into ~48 symbols
6. **Symbol Assignment**: Map clusters to VSYM_XXX identifiers
7. **Initial Codon Mapping**: Bootstrap symbol→codon bindings
8. **TRIG6 Evaluation**: Compute fitness metrics
9. **Evolution Loop**: Genetic algorithm optimizes parameters (50 generations)
10. **Codon Stream Emit**: Generate .codon files
11. **Compiler Integration**: Sandbox compile (stub for FlameLang)

### Output Structure

```
data/voynich_work/
├── glyphs.json                              # Raw glyph data
├── anomalies.json                           # Detected anomalies
├── glyphs/
│   ├── embeddings.npy                       # Dimensional embeddings
│   ├── cluster_labels.npy                   # Cluster assignments
│   └── cluster_stats.json                   # Cluster statistics
├── symbols/
│   └── symbol_table.json                    # VSYM mapping
└── binding/
    ├── symbol_to_codon_v0.json              # Initial mapping
    ├── trig6_report.json                    # TRIG6 metrics
    ├── symbol_to_codon_champion.json        # Best evolved params
    ├── evolution_log.json                   # Generation history
    └── codon_streams/
        └── voynich_diag.codon               # Output stream
```

## Configuration

Edit `voynich_diag_pipeline.yaml` to adjust:

- **Target alphabet size**: `anomaly_target_count` (default: 48)
- **Evolution parameters**: `pop_size`, `generations`, `mutation_rate`
- **TRIG6 weights**: Resonance, Drift, Noise component weights
- **Danger thresholds**: `tan_danger_limit`, `drift_danger_threshold`

## Evolution Parameters

The genetic algorithm evolves three key parameters:

1. **n_clusters** (int): Number of glyph clusters [8-100]
   - Mutation: ±4 with bounds
   
2. **strategy** (categorical): Clustering strategy
   - Options: entropy_weighted, frequency_weighted, uniform
   - Mutation: Random choice excluding current
   
3. **glyph_variance_threshold** (float): Variance tolerance [0.01-0.5]
   - Mutation: ±0.02 uniform

## Extending the Pipeline

### Real Glyph Extraction

Replace the `ingest` stage stub with:
- PDF → image extraction (via OmniCalc)
- OpenCV connected components
- Custom autoencoder training

### FlameLang Integration

Wire the `compiler_integration` stage to:
- SAGCO-OS kernel
- FlameLang compiler
- Execution sandbox

### Additional Mutation Targets

Add new parameters in `mutate_params()`:
```python
elif target == "embedding_dim":
    val = params.get("embedding_dim", 32)
    params["embedding_dim"] = clamp(val + np.random.randint(-8, 9), 8, 128)
```

## TRIG6 Conceptual Mapping

For Voynich analysis:
- **Anomalies** = Weird glyph variants / layout irregularities
- **Theta** = Decipher progress indicator
- **Resonance** = Pattern consistency + coverage quality
- **Drift** = Variance in cluster sizes + outlier fraction
- **Noise** = Embedding variance + symbol entropy
- **Equilibrium** = Distance from target 48-symbol alphabet
- **Danger** = Over-confident mappings in high-drift (keeps sandboxed)

## Performance

- Initial fitness: ~0.58
- Champion fitness: ~0.57 (toy landscape)
- Generations: 50
- Population: 20 individuals
- Runtime: ~30 seconds (synthetic data)

## Safety Features

1. **Sandboxed Mode**: Compiler runs isolated
2. **Danger Detection**: Monitors tan(θ) and drift thresholds
3. **Mutation Bounds**: All parameters have safe ranges
4. **Deep Copy**: Prevents shared-reference bugs in evolution

## Integration Points

This pipeline is ready to integrate with:

- **OmniCalc**: Real PDF glyph extraction
- **FlameLang**: Codon → executable compilation
- **SAGCO-OS**: Operating system kernel hooks
- **NEURO-36**: Core Genome YAML tagging system

## Next Steps

1. **Real Data**: Replace synthetic glyphs with actual Voynich scans
2. **Neural Network**: Train proper autoencoder for embeddings
3. **Genome Tagging**: Add NEURO-36 cognitive gene annotations
4. **Multi-Pipeline**: Extend to Codex, Starlink, other substrates

## License

Part of Strategickhaos DAO LLC Sovereignty Architecture
Operator: Dominic Garza (Me10101)
