# Codex Seraphinianus → TRIG6 → FlameLang Binding Pipeline

## Overview

The Codex Binding Pipeline is a comprehensive system for extracting symbolic glyphs from the Codex Seraphinianus and mapping them to FlameLang codon IR (Intermediate Representation) using TRIG6 fitness geometry.

## Pipeline Specification

**File:** `codex_binding_pipeline.yaml`  
**Version:** 1.0.0  
**Author:** Domenic Gabriel Garza (Strategickhaos DAO LLC)

## Architecture

The pipeline consists of 11 stages:

1. **PDF → Page Images** (`ingest`) - Render Codex pages to high-resolution images
2. **Layout Segmentation** (`layout_segment`) - Separate text regions from illustrations
3. **Glyph Extraction** (`glyph_extract`) - Segment individual glyphs using connected component analysis
4. **Glyph Embedding** (`glyph_embed`) - Encode glyphs into fixed-length vectors
5. **Glyph Clustering** (`glyph_cluster`) - Discover repeated glyph types via unsupervised clustering
6. **Symbol ID Assignment** (`symbol_assign`) - Map clusters to canonical symbolic IDs
7. **Initial Codon Mapping** (`codon_mapping_init`) - Initialize symbol→codon assignments
8. **TRIG6 Mapping Evaluation** (`trig6_eval`) - Evaluate mapping quality using TRIG6 geometry
9. **Darwinian Mapping Evolution** (`evolution_loop`) - Evolutionary search for optimal mappings
10. **Codon Stream Emission** (`codon_stream_emit`) - Generate codon streams for FlameLang
11. **Compiler Integration** (`compiler_integration`) - Feed codon streams to FlameLang/SAGCO-OS

## TRIG6 Fitness Geometry

The pipeline uses TRIG6 (Trigonometric 6-dimensional) geometry to evaluate mapping quality:

- **Resonance (R)**: Cluster purity, coverage, and temporal stability
- **Drift (D)**: Reassignment rate and outlier proportion
- **Noise (N)**: Embedding variance and cluster size entropy
- **Equivalence (eq)**: Proximity to target symbol count
- **Danger**: Detected via `|tan(θ)| > tan_danger_limit`
- **Fitness**: `R × (1-D) × (1-N) × eq`

### Key Parameters

- `eq_target`: 0.95 - Target equivalence for "good enough" mapping
- `tan_danger_limit`: 10.0 - Threshold for danger detection
- `target_symbol_count`: 64 - Desired alphabet size (maps to 64 codons)
- `random_seed`: 1978 - Publication year as canonical seed

## Usage

### Prerequisites

1. Place `Codex_Seraphinianus.pdf` in `data/codex_seraphinianus/`
2. Define FlameLang codon table in `spec/codon_table_flame_v1.json`
3. Ensure TRIG6/OmniCalc runner is configured

### Running the Pipeline

```bash
# Point your TRIG6/OmniCalc runner at the pipeline
trig6-runner --pipeline codex_binding_pipeline.yaml
```

Or with a Python driver:

```python
import yaml

# Load pipeline specification
with open('codex_binding_pipeline.yaml', 'r') as f:
    pipeline = yaml.safe_load(f)

# Execute each stage
for stage in pipeline['stages']:
    execute_stage(stage, pipeline['inputs'])
```

## Outputs

All artifacts are stored in `artifacts/codex_binding/`:

- `pages/` - Rendered page images
- `regions/` - Text and illustration region masks
- `glyphs/` - Extracted glyph images and embeddings
- `symbols/` - Symbol table and cluster assignments
- `binding/` - Codon mappings, TRIG6 reports, and evolution logs
- `audit/` - GPG-signed audit logs (hash: SHA-256)

## Governance & Ethics

### License
© 2026 Strategickhaos DAO LLC – Internal Research Use Only

### Ethical Constraints

1. **Do not claim decipherment** of Codex Seraphinianus
2. **Sandboxed execution only** - Never run Codex-derived programs against real systems
3. **Open methodology** - Publish TRIG6 geometry and methodology openly
4. **DAO governance** - Keep raw mappings under DAO governance until policy is set

### Audit Trail

- All pipeline runs are logged to `${work_dir}/audit`
- Logs are hashed with SHA-256
- GPG signature required (Key ID: `AE5519579584DEF5`)

## Extension Points

The pipeline is designed to be extensible:

- Add new stages to the `stages` array
- Customize TRIG6 functions in `trig6` blocks
- Adjust evolution parameters in `evolution_loop`
- Reuse schema for other undeciphered scripts (e.g., Voynich manuscript)

## Technical Specifications

### Directory Structure

```
├── codex_binding_pipeline.yaml    # Pipeline specification
├── spec/
│   ├── README.md                  # Specification documentation
│   └── codon_table_flame_v1.json  # FlameLang codon definitions
├── data/
│   └── codex_seraphinianus/
│       ├── README.md              # Data directory documentation
│       └── Codex_Seraphinianus.pdf # Source PDF
└── artifacts/
    └── codex_binding/             # Pipeline outputs
        ├── pages/
        ├── regions/
        ├── glyphs/
        ├── symbols/
        ├── binding/
        └── audit/
```

### Integration Points

- **FlameLang Compiler**: `bin/flamelangc`
- **SAGCO-OS Runtime**: `bin/sagco-run`
- **Execution Mode**: `sandbox` (safety-first approach)

## Next Steps

1. **Implement Python runner** - Create a driver that loads this YAML and executes each stage
2. **Multi-source support** - Clone this spec for Voynich and other undeciphered scripts
3. **Codon table definition** - Complete `spec/codon_table_flame_v1.json`
4. **TRIG6 integration** - Wire into existing TRIG6/OmniCalc codebase

## References

- **Codex Seraphinianus**: Luigi Serafini (1981)
- **TRIG6 Geometry**: Strategickhaos DAO research
- **FlameLang**: Codon-based IR for SAGCO-OS
- **GPG Key**: AE5519579584DEF5

---

**Status**: ✅ Specification Complete | 🚧 Implementation Pending  
**Last Updated**: 2026-01-25
