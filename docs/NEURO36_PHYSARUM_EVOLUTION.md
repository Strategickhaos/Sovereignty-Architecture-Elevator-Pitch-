# NEURO-36 Physarum DNA Evolution Layer

## Overview

The NEURO-36 Physarum DNA Evolution Layer extends the immune system simulation with molecular biology concepts and evolutionary algorithms. It implements the central dogma of molecular biology (DNA → RNA → Protein) integrated with TRIG6 fitness metrics and Physarum polycephalum-inspired flow-based adaptation.

## Features

### 1. Molecular Biology Simulation
- **DNA → RNA Transcription**: Converts DNA sequences to RNA (T → U substitution)
- **RNA → Protein Translation**: Uses standard genetic code codon table for amino acid translation
- **GC Content Analysis**: Measures genomic coherence as a proxy for resonance

### 2. Evolutionary Algorithm
- **50-Generation Evolution**: Each of 36 immune components evolves over 50 generations
- **Mutation System**: Point mutations with adaptive mutation rate based on fitness
- **Selection Pressure**: TRIG6 fitness gating determines survival and adaptation

### 3. TRIG6 Integration
- **Resonance (R)**: Derived from GC content (genomic coherence)
- **Drift (D)**: Tracks deviation from target state
- **Noise (N)**: Measures random fluctuations
- **Fitness Function**: f = R × (1-D) × (1-N) × equilibrium
- **Danger Zone Detection**: Identifies components requiring reset

### 4. Physarum Flow Adaptation
- **Conductivity (H)**: Heritability metric for information propagation
- **Flow Accumulation**: Tracks fitness contributions over time
- **Dynamic Reinforcement**: High fitness reinforces conductivity, low fitness causes decay
- **Network Optimization**: Inspired by Physarum polycephalum adaptive networks

## Architecture

```
src/
├── neuro36_immune.py              # Base immune system with TRIG6 state
└── neuro36_physarum_evolution.py  # DNA evolution layer

artifacts/
├── physarum_evolution_36.json     # Evolution results (83KB)
└── neuro36_sweep.json             # Isolation sweep results (11KB)

benchmarks/
└── test_neuro36_physarum.py       # Test suite
```

## Usage

### Running the Full Simulation

```bash
python3 src/neuro36_physarum_evolution.py
```

This will:
1. Run a 36-node isolation sweep to measure TRIG6 signatures
2. Evolve all 36 components for 50 generations each (1,800 total steps)
3. Export results to JSON files in the `artifacts/` directory

### Example Output

```
================================================================================
NEURO-36 Physarum DNA Evolution
50 generations per component, TRIG6 fitness gating
================================================================================
 1. Skin                                → TRIG6 Trait: Resonance Gate    | f=0.458 H=0.50 🧬 EVOLVING
 2. Sebum                               → Compiler Pass: Parsing         | f=0.317 H=0.29 🧬 EVOLVING
...
36. Transition/Run/Gain/Advance/Set back → OS Module: Physarum Evolver    | f=0.337 H=0.23 🧬 EVOLVING

================================================================================
SUMMARY
================================================================================
Average Fitness: 0.398
Average H (Conductivity): 0.42
Status Distribution: {'EVOLVING': 36}
```

### Running Tests

```bash
python3 benchmarks/test_neuro36_physarum.py
```

## Component Status Classifications

- **🏆 CHAMPION**: Fitness ≥ 0.8 (highly adapted)
- **🧬 EVOLVING**: 0.3 ≤ Fitness < 0.8 and H > 0 (stable evolution)
- **⚠️ MUTANT**: Fitness < 0.3 (poor adaptation, needs intervention)
- **💀 CULL**: H ≤ 0 (degraded conductivity, recommend removal)

## 36 Immune Components

The system models 36 biological immune components mapped to computational equivalents:

1. **Biological Components**: Skin, Sebum, Neutrophils, T-cells, etc.
2. **TRIG6 Traits**: Resonance Gate, Drift Detector, Noise Filter, etc.
3. **Compiler Passes**: Parsing, Codegen, Optimization, etc.
4. **OS Modules**: Scheduler, Memory Manager, Quantum Gate Array, etc.

## Data Output

### Evolution Results (`physarum_evolution_36.json`)

```json
{
  "metadata": {
    "generations": 50,
    "base_mutation_rate": 0.01,
    "initial_dna": "ATGGCATGCCAAGGTATCTTACCG"
  },
  "components": [
    {
      "component_id": 1,
      "component_name": "Skin",
      "ecosystem_mapping": "TRIG6 Trait: Resonance Gate",
      "final_status": "EVOLVING",
      "final_dna": "ATGGCATGCCAAGGTATCTTACCG",
      "final_fitness": 0.458,
      "final_H": 0.5,
      "summaries": [...]
    }
  ],
  "summary": {
    "avg_fitness": 0.398,
    "avg_H": 0.42
  }
}
```

### Sweep Results (`neuro36_sweep.json`)

Contains TRIG6 signatures for each component in isolation:

```json
{
  "sweep_results": [
    {
      "node_id": 1,
      "node_name": "Skin",
      "state": {"R": 0.8, "D": 0.05, "N": 0.01},
      "delta_fitness": -0.048
    }
  ]
}
```

## Integration with Existing Systems

The Physarum Evolution Layer can be integrated with:

- **Immune System Simulations**: Real-time tracking of immune responses
- **Compiler Optimization**: Using TRIG6 metrics for code quality
- **OS Resource Management**: Adaptive scheduling based on conductivity
- **Network Flow Analysis**: Physarum-inspired routing optimization

## Scientific Basis

Based on Dom's Biological-Computational Equivalence Map v1.0, which establishes correspondences between:

1. **Central Dogma**: DNA → RNA → Protein ≈ Data → Process → Function
2. **TRIG6 Metrics**: Trigonometric fitness functions for stability
3. **Physarum Networks**: Bio-inspired adaptive network optimization
4. **Immune Memory**: Heritability as computational state persistence

## Author

**Domenic Gabriel Garza (Inventor)**  
Strategickhaos DAO LLC

## License

See repository LICENSE file.
