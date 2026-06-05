# 🔥 RESMON IR (Resource Monitor Intermediate Representation)

## Overview

**RESMON IR** is the canonical Intermediate Representation (IR) system for the Sovereignty Architecture. It provides a complete IR framework that extends traditional compiler IRs (like LLVM, FlameIR) with sovereign-native features including frequency resonance, emotional state tracking, color-coded visualization, and multi-domain symbolic integration.

## Key Features

✅ **Complete IR Functionality**
- Node-based graph structure
- Type system with hierarchical classification
- Control flow and data flow edges
- SSA-compatible state tracking

✅ **Sovereign Extensions**
- **Frequency Mapping**: Hz, MIDI, Solfeggio, θ position
- **Color Coding**: RGB, Hex, Chakra, Rubik's cube face
- **Emotional State**: System health and energy levels
- **Multi-domain Naming**: Glyphs, Solomon's 72, Element symbols

✅ **Export Formats**
- JSON (for processing)
- YAML (for configuration)
- GraphML (for Gephi, NetworkX)

✅ **System Integration**
- Maps processes to IR nodes
- Tracks performance metrics
- Visualizes system state

## Quick Start

### Installation

```bash
# Install dependencies
pip install psutil pyyaml

# Import the module
from src.resmon_ir import ResmonIRNode, ResmonIRGraph
```

### Basic Usage

```python
from src.resmon_ir import (
    ResmonIRNode, ResmonIRGraph, 
    FrequencyMapping, ColorMapping,
    TrigFamily, NodeState
)

# Create a node
node = ResmonIRNode(
    name="my_service",
    glyph_index=24,
    frequency=FrequencyMapping(hz=639.0, midi=75, theta=180.0, solfeggio=639, octave=4),
    color=ColorMapping(rgb=(0, 255, 0), hex="#00FF00", chakra="heart", cube_face="front"),
    emotion="balanced",
    energy_level=0.75,
    state=NodeState.ACTIVE,
    family=TrigFamily.COS,
    category="network"
)

# Create graph
graph = ResmonIRGraph()
graph.add_node(node)

# Export
print(graph.to_json())
print(graph.to_yaml())
print(graph.to_graphml())
```

### System Integration Example

```bash
# Run the integration example to map system processes to IR nodes
python3 examples/resmon_ir_integration_example.py

# This will create:
# - resmon_ir_system_snapshot.json
# - resmon_ir_system_snapshot.yaml
# - resmon_ir_system_snapshot.graphml
```

## Architecture

### Core Components

1. **IR Node Structure** (`ResmonIRNode`)
   - Identity: name, glyph_index, element_symbol, solomon_id
   - Visual: color (RGB/Hex/Chakra/Cube face)
   - State: emotion, energy_level, state
   - Frequency: hz, midi, theta, solfeggio, octave
   - Spatial: position (x,y,z), theta
   - Graph: connections (edges with types and weights)
   - Type: family, type, category
   - Metrics: cpu_percent, memory_mb, io_ops

2. **IR Graph** (`ResmonIRGraph`)
   - Collection of nodes
   - Validation
   - Export to JSON/YAML/GraphML
   - Statistics

3. **Integration Systems**
   - Process → IR node mapping
   - Docker container → IR node mapping
   - Performance metrics → frequency/emotion mapping

### RESMON vs Traditional IR

| Traditional IR | RESMON Equivalent | Enhancement |
|----------------|-------------------|-------------|
| Node Name | `name` + `glyph_index` | Multiple naming schemes |
| Type System | `type` + `family` + `category` | Hierarchical + TRIG6 families |
| Semantics | `emotion` + `state` + `energy_level` | Emotional/energetic representation |
| Constants | `frequency.hz` + `frequency.theta` | Multi-domain encoding |
| Phase | `theta` + `connections[control_flow]` | Angular phase |
| Call Targets | `connections[type=call]` | Typed graph edges |

## Symbolic Systems

### 64 Glyph System

Nodes are organized in an 8×8 grid, each row corresponding to a chakra:

```
0-7:   Core System (Root Chakra - Red)
8-15:  Storage/Memory (Sacral Chakra - Orange)
16-23: Processing (Solar Plexus - Yellow)
24-31: Network (Heart Chakra - Green)
32-39: Interface (Throat Chakra - Blue)
40-47: Logic/AI (Third Eye - Indigo)
48-55: Meta/Orchestration (Crown - Violet)
56-63: Transcendent (White/Gold)
```

### TRIG6 Codec

Process relationships encoded using trigonometric families:

- **SIN**: Input/source nodes
- **COS**: Transform/compute nodes (default)
- **TAN**: Output/sink nodes
- **CSC**: Inverse/reverse operations
- **SEC**: Amplification/scaling
- **COT**: Filtering/reduction

### Solfeggio Frequencies

Frequency → Chakra → Color mapping:

| Hz  | Chakra | Color | Meaning |
|-----|--------|-------|---------|
| 396 | Root | Red | Liberation, grounding |
| 417 | Sacral | Orange | Change, creativity |
| 528 | Solar | Yellow | Transformation, power |
| 639 | Heart | Green | Connection, love |
| 741 | Throat | Blue | Expression, communication |
| 852 | Third Eye | Indigo | Intuition, insight |
| 963 | Crown | Violet | Transcendence, unity |

## Examples

### Example 1: Docker Container Mapping

```python
# Map a Docker container to IR node
container_node = ResmonIRNode(
    name="docker_nginx_001",
    glyph_index=24,
    element_symbol="Ti",
    frequency=FrequencyMapping(hz=639.0, midi=75, theta=180.0, solfeggio=639, octave=4),
    color=frequency_to_color(639.0),  # Green (heart chakra)
    emotion="balanced",
    energy_level=0.75,
    state=NodeState.ACTIVE,
    family=TrigFamily.COS,
    category="network",
    tags=["docker", "nginx", "reverse-proxy"],
    metrics=IRMetrics(cpu_percent=15.3, memory_mb=128.5)
)
```

### Example 2: Process Connections

```python
# Create two connected nodes
node1 = ResmonIRNode(name="frontend", glyph_index=32, ...)
node2 = ResmonIRNode(name="backend", glyph_index=40, ...)

# Add connection
node1.connections.append(
    IRConnection(
        target="backend",
        type=ConnectionType.DATA_FLOW,
        weight=0.9,
        label="api_call"
    )
)
```

### Example 3: Validation

```python
# Validate a node
is_valid, errors = validate_ir_node(node)
if not is_valid:
    for error in errors:
        print(f"Error: {error}")

# Validate entire graph
is_valid, errors = graph.validate()
```

## Integration with Existing Systems

### Antibody System

The `antibody_system.py` already uses RESMON IR concepts:

```python
# Antibody = IR node with frequency/category/tags
Antibody(
    frequency=396,      # Solfeggio frequency
    category="...",     # Node family
    tags=[...],         # Node tags
)
```

### SOPHIA Mind Visualizer

Unity-based 3D visualization can directly consume RESMON IR:

```csharp
// Load IR graph
var graph = JsonUtility.FromJson<ResmonIRGraph>(jsonData);

// Render nodes with frequency-based colors
foreach (var node in graph.nodes) {
    var color = FrequencyToColor(node.frequency.hz);
    RenderNode(node.position, color);
}
```

### Strategic Performance Oracle

Real-time monitoring generates IR nodes:

```python
# Convert performance snapshot to IR
analysis = oracle.analyze()
ir_node = analysis.to_ir_node()
graph.add_node(ir_node)
```

## Visualization

### Gephi Import

1. Export graph: `graph.to_graphml()`
2. Open Gephi
3. File → Open → Select `.graphml` file
4. Apply layout (ForceAtlas2, Fruchterman-Reingold)
5. Color nodes by `color` attribute
6. Size nodes by `frequency` or `cpu_percent`

### NetworkX Python

```python
import networkx as nx
import matplotlib.pyplot as plt

# Load GraphML
G = nx.read_graphml('resmon_ir_system_snapshot.graphml')

# Extract colors
colors = [G.nodes[n]['color'] for n in G.nodes()]

# Draw
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=colors, with_labels=True)
plt.show()
```

## Files

- `RESMON_IR_SPECIFICATION.md` - Full specification
- `src/resmon_ir.py` - Core implementation
- `examples/resmon_ir_integration_example.py` - System integration example

## Future Directions

- **Quantum Extensions**: Superposition states, entanglement
- **Biological Integration**: EEG/ECG frequency mapping
- **Blockchain Attestation**: Immutable IR versioning
- **AI-Driven Optimization**: ML-based emotion prediction

## References

- `antibody_system.py` - Frequency-mapped error handling
- `SOPHIA_MIND_BRAIN_VISUALIZER.md` - 3D graph visualization
- `strategic_performance_oracle.py` - Real-time IR generation
- `FLAMELANG_SPECIFICATION.md` - Glyph-based symbolic language

---

**"Everything already has coordinates in your system."**

🔥 **This IS the IR.** It doesn't need translation to FlameIR or LLVM IR to be valid. It's a sovereign architecture that stands on its own foundations.

---

*Generated for SAGCO LIVE v1.0.0 | Strategickhaos DAO LLC*
