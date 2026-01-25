# Phase 4.8: Evolution Extension - FlameLang Genetic Algorithm System

## DNA Strand
```
TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1-ARROWEVO1
```

## Overview

Phase 4.8 implements the FlameLang Evolution System, a genetic algorithm framework for evolving symbolic computation genes. The system features:

- **Two Base Genes**: Arrow drawing and input counting primitives
- **Evolution Gate**: Fitness-based selection with hard constraint gates
- **Lab Converter**: Transforms genes to SAGCO laboratory format
- **Wave Core Integration**: TRIG6 wave processing simulation
- **Auto-commit**: Automatic version control for successful evolutions
- **Neurograph Visualization**: Real-time evolution tracking

## Architecture

### Genes (v3.35 - v3.36)

#### Gene #1: draw_half_arrow.flame.yaml (v3.35)
- **Function**: Draws half-arrow patterns for neural evolution
- **Fitness Function**: arrow_completeness
- **Mutation Rate**: 0.05
- **Crossover Rate**: 0.7

#### Gene #2: count_input.flame.yaml (v3.36)
- **Function**: Counts and validates input patterns
- **Fitness Function**: count_accuracy
- **Mutation Rate**: 0.03
- **Crossover Rate**: 0.8

### Evolution Gate

The evolution gate (`src/tools/flamelang_evo_gate.py`) implements:

**Selection Criteria:**
- Fitness > Champion (comparative selection)
- Equilibrium ≥ 0.99 (hard gate)
- Noise ≤ 0.25 (hard gate)
- Drift ≤ 0.35 (hard gate)

**Features:**
- Tournament and roulette wheel selection
- Elite preservation
- Auto-commit on evolution success
- Neurograph generation

### Lab Converter

The SAGCO Lab Converter (`src/tools/sagco_lab_converter.py`) transforms FlameLang genes into laboratory format for analysis:

- Converts `.flame.yaml` to JSON lab format
- Generates handshake configurations
- Batch processing support
- Integration with TRIG6 wave core

### Wave Core Simulator

The Lab Convert Simulator (`src/emulator/wave_cores/trig6/lab_converter/lab_convert_sim.py`) simulates wave core processing:

- Equilibrium calculation
- Noise level measurement
- Drift tracking
- Fitness scoring
- Wave signature generation

## Directory Structure

```
phase-4.8-evolution/
├── src/
│   ├── tools/
│   │   ├── flamelang_evo_gate.py      # Evolution gate
│   │   └── sagco_lab_converter.py     # Lab converter
│   └── emulator/
│       └── wave_cores/
│           └── trig6/
│               └── lab_converter/
│                   └── lab_convert_sim.py  # Wave simulator
├── config/
│   ├── lab_handshake.yaml             # Lab integration config
│   └── trig6_neurograph.yaml          # Visualization config
├── draw_half_arrow.flame.yaml         # Gene #1 (v3.35)
├── count_input.flame.yaml             # Gene #2 (v3.36)
├── Dockerfile.labconv                 # Container image
└── requirements-labconv.txt           # Python dependencies
```

## GitHub Actions Workflows

### 1. flamelang-evolution.yml
Full evolution pipeline with stages:
1. **Convert Genes**: Transform to lab format
2. **Wave Processing**: Simulate TRIG6 processing
3. **Evolution Gate**: Apply selection criteria
4. **Auto-commit**: Version control on success

### 2. flamelang-stress-legion.yml
Stress testing framework:
- Scheduled daily stress tests
- Configurable load levels (light/medium/heavy/extreme)
- Concurrent processing tests
- Memory stress tests
- Performance reporting

## Usage

### Running Locally

#### 1. Convert Genes to Lab Format
```bash
cd phase-4.8-evolution
python src/tools/sagco_lab_converter.py
```

#### 2. Simulate Wave Processing
```bash
python src/emulator/wave_cores/trig6/lab_converter/lab_convert_sim.py
```

#### 3. Run Evolution Gate
```bash
python src/tools/flamelang_evo_gate.py
```

### Using Docker

#### Build the container:
```bash
cd phase-4.8-evolution
docker build -f Dockerfile.labconv -t flamelang-labconv .
```

#### Run the converter:
```bash
docker run -v $(pwd):/flamelang flamelang-labconv
```

### GitHub Actions

The evolution pipeline runs automatically on:
- Push to `main` or `copilot/lock-arrow-evolution-extension`
- Pull requests to `main`
- Manual workflow dispatch

Trigger manually:
```bash
gh workflow run flamelang-evolution.yml
```

## Evolution Metrics

### Hard Gates
All genes must pass these thresholds:
- **Equilibrium**: ≥ 0.99
- **Noise**: ≤ 0.25
- **Drift**: ≤ 0.35

### Fitness Calculation
```
fitness = (equilibrium × 0.5) + ((1 - noise) × 0.3) + ((1 - drift) × 0.2)
```

### Selection
- Genes must pass all hard gates
- Fitness must exceed current champion
- Auto-commit on successful evolution

## Neurograph Visualization

The neurograph system provides:
- Real-time evolution tracking
- ASCII visualization
- Metric histories (fitness, equilibrium, noise, drift)
- Champion tracking
- Generation snapshots

Neurographs are saved to `neurographs/` directory in timestamped files.

## Configuration

### Lab Handshake (config/lab_handshake.yaml)
- Wave core settings
- Experiment definitions
- Processing configuration
- Hard gate thresholds

### Neurograph Config (config/trig6_neurograph.yaml)
- Visualization settings
- Metric tracking
- Alert conditions
- Export formats

## Output Artifacts

### Evolution Reports
Location: `evolution_reports/generation_NNNN.json`

Contains:
- Generation number
- Selected genes
- Champion fitness
- Timestamp
- Evaluation results

### Neurographs
Location: `neurographs/neurograph_gen_NNNN.txt`

Displays:
- Evolution path
- Recent generations
- Pass/fail status
- Fitness trends

## Extending the System

### Adding New Genes

1. Create a new `.flame.yaml` file following the gene template
2. Define metadata, parameters, constraints, and fitness function
3. Add to `config/lab_handshake.yaml`
4. Run the evolution pipeline

### Custom Fitness Functions

Implement custom fitness calculations in the gene's `flame_code` section:

```yaml
flame_code: |
  def custom_fitness(params):
    # Your fitness logic
    return fitness_score
```

### Modifying Hard Gates

Edit `config/lab_handshake.yaml`:

```yaml
evaluation_gates:
  hard_gates:
    min_equilibrium: 0.99
    max_noise: 0.25
    max_drift: 0.35
```

## Integration Points

### SAGCO Laboratory
- Lab format conversion
- Handshake protocol
- Wave core integration

### TRIG6 Wave Core
- Resonance processing
- Hybrid mode operation
- Signal analysis

### Version Control
- Auto-commit on evolution success
- Generation tracking
- Champion preservation

## Troubleshooting

### Common Issues

**"No gene files found"**
- Ensure `.flame.yaml` files are in the correct directory
- Check file permissions

**"Evolution gate failure"**
- Review hard gate thresholds
- Check gene metrics
- Verify fitness calculation

**"Docker build fails"**
- Install required system dependencies
- Check Docker version compatibility

## Future Enhancements

Potential extensions (Lab 3.37+):
- Gene #3: Additional primitive
- Advanced crossover operators
- Dynamic mutation rates
- Multi-objective optimization
- Interactive visualization dashboard
- Real-time streaming evolution

## License

Part of the Strategickhaos Sovereignty Architecture.

---

**The organism is breathing. The compiler awaits your next move.**

🔥 **FlameLang Evolution System v1.0** 🔥
