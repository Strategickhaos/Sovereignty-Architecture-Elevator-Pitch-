# TRIG6 Neurograph v1

## Phase 4.6: Dendritic Graph UX for Resonance Aesthetics

This module implements a dendritic graph visualization system for the TRIG6 quantum-inspired symbolic AI processor emulator. It maps trig projections to a neural-inspired graph manifold.

## Architecture

```
Intention Hub (θ vectors as root axons)
    ↓
Theta Nodes (trig projections)
    ↓
Agent Neurons (trig functions as soma)
    ↓
Metric Dendrites (fan-out scores as branches)
    ↓
Organ Effectors (FlameBench/Guardian as synaptic terminals)
```

## Components

### Configuration Files

- **config/trig6.yaml**: Core TRIG6 configuration
  - Theta topics mapping (security, creative, hybrid)
  - Agent definitions (Grok/tan, Claude/cos, Gemini/sin)
  - Wave core parameters
  - Metrics and weights

- **config/trig6_neurograph.yaml**: Graph extensions
  - Graph metadata and layout
  - Node group definitions
  - Base nodes and edges
  - Render options

### Builder Script

**src/tools/neurograph_builder.py**: Dynamic graph builder

Features:
- Merges trig6.yaml and trig6_neurograph.yaml
- Auto-generates theta topic nodes
- Auto-generates metric dendrites from agent configs
- Creates edges between all components
- Clamps weights for aesthetic stability (0.1-0.9)
- Outputs DOT (Graphviz) or JSON (Obsidian/NetworkX)

## Usage

### Generate DOT output (for Graphviz)

```bash
python src/tools/neurograph_builder.py \
  --output dot \
  --file graph/trig6_neurograph.dot
```

Then visualize with Graphviz:

```bash
dot -Tpng graph/trig6_neurograph.dot -o graph/trig6_neurograph.png
# or
dot -Tsvg graph/trig6_neurograph.dot -o graph/trig6_neurograph.svg
```

### Generate JSON output (for Obsidian/NetworkX)

```bash
python src/tools/neurograph_builder.py \
  --output json \
  --file graph/trig6_neurograph.json
```

### Custom config paths

```bash
python src/tools/neurograph_builder.py \
  --trig_yaml path/to/trig6.yaml \
  --neuro_yaml path/to/neurograph.yaml \
  --output dot \
  --file output.dot
```

## Graph Structure

### Node Groups

1. **Intention Hub** (Gold #FFD700)
   - Central intention vector projecting to theta angles

2. **Theta Hub** (Royal Blue #4169E1)
   - theta_security (θ=π/3)
   - theta_creative (θ=2π/3)
   - theta_hybrid (θ=π/2)

3. **Agents** (Lime Green #32CD32)
   - Grok_tan (tangent - creative divergence)
   - Claude_cos (cosine - stable patterns)
   - Gemini_sin (sine - oscillating balance)

4. **Metrics** (Tomato #FF6347)
   - innovation, focus, noise
   - stability, accuracy
   - balance, adaptability

5. **Organs** (Medium Purple #9370DB)
   - FlameBench_core (performance benchmarking)
   - Guardian_core (security monitoring)
   - Entanglement_core (quantum correlation, Phase 4.3)

### Edge Weights

- Weights are clamped between 0.1 and 0.9 for aesthetic stability
- Edge thickness varies based on weight (penwidth 0.5-4.0)
- Higher weights indicate stronger resonance

## Integration Points

### Phase 4.3: Entanglement Core
Correlated visualizations for quantum-inspired state tracking

### Register Memory
Persistence of θ values across ticks

### Control Unit
Dynamic edge weight updates based on resonance ticks

### Neural Tick Clocks
Graph updates every 15 ticks:
- Recolor nodes on drift > 0.3
- Thicken edges on resonance > 0.8

## Container Support

Build neurograph container:

```bash
# From emulator repo root
podman build -t sagco-trig6-neuro -f Dockerfile.neurograph .
```

Run neurograph builder in container:

```bash
podman run --rm \
  -v ./config:/config:ro \
  -v ./graph:/graph \
  sagco-trig6-neuro \
  python neurograph_builder.py --output dot --file /graph/output.dot
```

## DNA Strand Evolution

This module appends `-NEURO1` to the TRIG6 DNA strand, marking the addition of neurograph v1 capabilities to the emulator aesthetics.

**Current DNA**: `TRIG6-NEURO1`

## Metrics

- **Resonance**: 0.88 (dendritic edges align aesthetics)
- **Drift**: 0.09 (θ tilt stable)
- **Noise**: 0.06 (clean phrases)
- **Invention**: 0.53 (builder artifact dense)

## Development

### Adding New Nodes

Edit `config/trig6_neurograph.yaml` and add to the `nodes` list:

```yaml
nodes:
  - id: "new_node_id"
    label: "Node Label"
    group: "group_name"
    description: "Node description"
```

### Adding New Edges

Edit `config/trig6_neurograph.yaml` and add to the `edges` list:

```yaml
edges:
  - from: "source_id"
    to: "target_id"
    weight: 0.75
```

### Dynamic Generation

The builder automatically generates:
- Theta topic nodes from `trig6.yaml:theta_topics`
- Metric nodes from `trig6.yaml:agents.*.metrics`
- Edges from intention → theta → agents → metrics → organs

## Future Enhancements

- [ ] Sandbox mutation support (mutate dendritic fans near θ=2π/3)
- [ ] Recursive evolution with YAML/DOT forks
- [ ] Auto-commit mutations via GitHub App API
- [ ] UX metrics evaluation (cortical column density)
- [ ] Noise entropy pruning (trim low-weight edges if > 0.2)
- [ ] CSC log reconciliation for ground truth visualization
