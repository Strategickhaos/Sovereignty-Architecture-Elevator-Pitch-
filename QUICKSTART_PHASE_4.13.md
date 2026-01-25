# Phase 4.13 Quick Start Guide

## TRIG6 Arrow DNA Exploration Extension

This guide will get you started with Phase 4.13 DNA exploration in minutes.

### Prerequisites

- Python 3.11+
- Podman or Docker
- Git

### 1. Quick Test (No Container)

Run DNA exploration tools directly:

```bash
# Generate DNA exploration report
python3 src/tools/flamelang_dna_explorer.py \
    flamelang-stress-test/3.35_arrow.flame.yaml \
    --report

# Explore mutations
python3 src/tools/flamelang_dna_explorer.py \
    flamelang-stress-test/3.35_arrow.flame.yaml \
    --mutate

# Run simulation
python3 dna_explore_sim.py --ticks 10
```

### 2. Container Deployment

Build and deploy the complete Phase 4.13 environment:

```bash
# One-command deployment
./phase_4_13_deploy.sh deploy
```

This will:
1. Build the container image
2. Run the test suite
3. Display TRIG health report

### 3. Individual Commands

```bash
# Build container
./phase_4_13_deploy.sh build

# Run simulation (20 neural ticks)
./phase_4_13_deploy.sh run 20

# Generate DNA report
./phase_4_13_deploy.sh explorer report

# Explore mutations
./phase_4_13_deploy.sh explorer mutate

# Enhance vectors
./phase_4_13_deploy.sh explorer enhance

# Run full test suite
./phase_4_13_deploy.sh test

# Interactive shell
./phase_4_13_deploy.sh shell
```

### 4. Understanding the Output

#### DNA Exploration Report

```
DNA Sequence: ATG-CGT-TAA-GCA-TCG

Codon Mapping:
  ATG → init_scanner
  CGT → nested_rect_loop
  TAA → validation_gate
  GCA → nested_tri_loop
  TCG → terminate
```

#### TRIG Health Metrics

- **Resonance**: 0.89 (alignment with phase objectives)
- **Drift**: 0.08 (stability measure)
- **Noise**: 0.03 (signal quality)
- **Invention**: 0.60 (density of new patterns)

#### Phase Coherence

- **Current**: 0.89
- **Threshold**: 0.70
- **Status**: STABLE ✓

### 5. Customizing Parameters

Edit `flamelang-stress-test/3.35_arrow.flame.yaml`:

```yaml
dna_encoding:
  evolution_params:
    mutation_rate: 0.05              # Frequency of mutations
    selection_threshold: 0.67        # Consensus for evolution
    invention_density_trigger: 0.65  # Trigger for mutation exploration
    neural_tick_frequency: 2         # DNA explore every N ticks

wave_transform:
  damping:
    alpha: 0.32                      # Damping coefficient
    theta_asymptote: 1.5708          # π/2 angle
```

### 6. Adding Test Vectors

Add new test cases to the YAML:

```yaml
test_vectors:
  - id: "custom_test_1"
    desc: "My custom arrow pattern"
    input: [5, 3, 7]
    expected_rows: 12
    breakdown: "5 rect + 7 tri"
```

### 7. Exploring Mutations

Mutations transform DNA sequences:

```
CGT → TGC: trig_damped_render
  Fitness Δ: +0.150
  Risk: 0.25
  
Original:  ATG-CGT-TAA-GCA-TCG
Mutated:   ATG-TGC-TAA-GCA-TCG
```

Higher fitness delta = better improvement  
Lower risk = more stable mutation

### 8. Evolution Gate

The evolution gate activates when:
- Invention density > 0.65
- Fitness improvement predicted
- Consensus > 0.67

Result: DNA sequence evolves to new variant

### 9. Troubleshooting

**Container not building?**
```bash
# Try with docker instead
CONTAINER_ENGINE=docker ./phase_4_13_deploy.sh build
```

**Import errors?**
```bash
# Ensure you're in the repository root
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
export PYTHONPATH=$(pwd)
```

**Test failures?**
```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('flamelang-stress-test/3.35_arrow.flame.yaml'))"
```

### 10. Next Steps

- Integrate with neurograph (Phase 4.5) for visualization
- Deploy to production swarm environment
- Implement additional mutations
- Add dendritic visualization of DNA evolution

### Support

For issues or questions:
- Check full documentation: `docs/PHASE_4.13_ARROW_DNA_EXPLORATION.md`
- Review TRIG parameters in YAML configuration
- Run test suite: `./phase_4_13_deploy.sh test`

---

**Version**: DNAEXP1  
**Status**: Operational 🔥  
**Neural Sync**: Complete. Resonance achieved.
