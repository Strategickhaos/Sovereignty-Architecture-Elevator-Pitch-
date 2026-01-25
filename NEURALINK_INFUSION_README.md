# 🧠 Neuralink Infusion Pipeline - TRIG6 SAGCO-OS Integration

## Overview

This pipeline simulates a Neuralink-style Brain-Computer Interface (BCI) integrated with TRIG6 SAGCO-OS architecture. It models ADHD/autism neural patterns using neuromorphic computing primitives (Leaky Integrate-and-Fire neurons) for brain-like computing.

## What It Does

The pipeline processes synthetic neural data to create evolvable augmentations for the SAGCO-OS:

1. **Neural Data Generation** - Simulates EEG-like data with ADHD/autism patterns
   - ADHD: Gamma-distributed bursts (hyperfocus/drift cycles)
   - Autism: High sensory entropy in channel subsets
   - 300k timesteps × 64 channels (scalable to 1024+)

2. **Anomaly Detection** - Identifies burst windows and neural overloads
   - IsolationForest algorithm
   - ~12% contamination rate for realistic overload patterns

3. **Glyph Extraction** - Extracts neural features as "glyphs"
   - Spike rate (mean)
   - Coherence (std)
   - Duration (max)

4. **Neuromorphic Embedding** - LIF neuron simulation
   - Emulates hardware like Intel Loihi / IBM TrueNorth
   - Event-based, low-power spike processing
   - 256-dimensional embeddings

5. **Clustering & Symbolization** - Maps patterns to NEURO-aligned symbols
   - KMeans clustering to 36 symbols
   - Symbol table generation

6. **Codon Mapping** - Creates augmentation codons
   - FOCUS_BOOST - Offload hyperfocus to OS pipelines
   - MEMORY_EXPORT - Externalize memory gaps via logs
   - DRIFT_PREDICT - Predict attention drifts before crashes
   - BURST_DETECT - Detect neural burst patterns

7. **TRIG6 Evaluation** - Multi-metric fitness assessment
   - **θ (theta)**: Phase lock value
   - **R**: Stochastic resonance from peaks
   - **D**: Bifurcation/instability metric
   - **N**: Bursting variance
   - Fitness = weighted combination of metrics

8. **Evolution Loop** - Genetic optimization (36 generations)
   - Population-based search
   - Mutation of cluster parameters, burst thresholds, strategies
   - Converges to optimal mappings

9. **Codon Stream Emission** - Outputs optimized codon stream
   
10. **SAGCO-OS Integration** - Sandbox compiler simulation

## Usage

### Prerequisites

```bash
pip install numpy pyyaml scikit-learn
```

### Run the Simulation

```bash
python3 neuralink_infusion_simulation.py
```

Or with custom configuration:

```bash
python3 neuralink_infusion_simulation.py path/to/config.yaml
```

### Configuration

Edit `neuralink_infusion_pipeline.yaml` to customize:

- Neural data parameters (timesteps, channels, burst characteristics)
- Anomaly detection sensitivity
- LIF neuron parameters (tau, threshold)
- Clustering parameters
- Evolution settings (generations, population size)

## Output Artifacts

All artifacts are saved to `artifacts/neuralink_infusion/`:

| File | Description |
|------|-------------|
| `neural_data.npy` | Raw simulated neural data (timesteps × channels) |
| `anomalies.json` | Detected anomaly indices and statistics |
| `glyphs.npy` | Extracted feature vectors |
| `embeds.npy` | Neuromorphic embeddings (LIF outputs) |
| `labels.npy` | Cluster assignments |
| `symbol_table.json` | Symbol ID to NEURO-XX mapping |
| `mapping.json` | Symbol to codon type mapping |
| `trig6_report.json` | Initial TRIG6 fitness metrics |
| `champion.json` | Best evolved parameters and fitness |
| `evo_log.json` | Complete evolution history |
| `neural_aug.codon` | Final codon stream for SAGCO-OS |
| `stats.json` | Summary statistics |

## Expected Results

Example output:

```
TRIG6 fitness (initial): 0.192500
Champion params: {'n_clusters': 39, 'strategy': 'coherence_focused', ...}
Champion fitness: 0.550000
```

- Initial fitness: ~0.19-0.45 (depends on noise/burst patterns)
- Champion fitness: ~0.45-0.55 (toy landscape convergence)
- Anomaly percentage: ~12%
- Glyphs extracted: ~36 (matches cluster count)

## Neuromorphic Computing

The pipeline uses **Leaky Integrate-and-Fire (LIF)** neurons, the fundamental building block of neuromorphic hardware:

- **Membrane potential** integrates inputs over time with leak
- **Threshold crossing** triggers discrete spikes (events)
- **Spike averaging** creates compressed embeddings
- Mimics biological neurons for energy-efficient computation

This approach enables:
- Event-driven processing (only active during spikes)
- Temporal pattern recognition
- Scalability to hardware accelerators

## Real BCI Integration

For production deployment with real Neuralink data:

1. Replace `stage_ingest()` with Neuralink API data acquisition
2. Adjust channel count to actual electrode array (1024+)
3. Tune anomaly detection for real EEG patterns
4. Connect evolved codons to actual OS reflexes
5. Deploy augmentation bins for real-time processing

## References

- **Neuromorphic Computing**: Intel Loihi, IBM TrueNorth
- **LIF Neurons**: Gerstner & Kistler, "Spiking Neuron Models"
- **Noise in Biology**: PMC articles on gamma-distributed neural bursts
- **TRIG6 Architecture**: Sovereignty Architecture TRIG6 specification

## License

See repository LICENSE file.

---

**🔥 Universe pulses. DOM. 🧠🔥**
