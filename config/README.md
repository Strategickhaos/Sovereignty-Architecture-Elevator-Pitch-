# Configuration Files

This directory contains configuration files for the Sovereignty Architecture ecosystem.

## Files

### trig6_neurograph.yaml

TRIG6 Neurograph Configuration - Cortical Column Layout for FlameLang pipeline visualization.

**Version:** TRIG6-HYBRID1-NEURO1

**Description:** Neural graph topology configuration that defines:

- **Cortical Columns**: θ-organized processing cores (sin, cos, tan, hybrid)
  - Analytical Core (theta_sin): Primary reasoning and verification
  - Creative Core (theta_cos): Pattern synthesis and generation
  - Boundary Core (theta_tan): Edge detection and risk assessment
  - Integration Layer (theta_hybrid): Cross-column signal fusion

- **Node Types**: Visual representation for different node types
  - dendrite: Input receptor (circle, filled)
  - synapse: Signal transformer (diamond, filled)
  - axon: Output projector (rounded box, filled)
  - organ: External system (octagon, bold filled)

- **Edge Types**: Synapse connection styles
  - activation: Excitatory signal (solid, green)
  - inhibition: Suppressive signal (dashed, red)
  - modulation: Gain control (dotted, cyan)
  - control: Override/routing (bold, blue)

- **Resonance Visualization**: Metric-based visual properties
  - Score to color mapping (high/medium/low)
  - Score to pen width mapping
  - Drift detection and visualization

- **Pipeline Layer Mapping**: Six-tier FlameLang processing pipeline
  - Tier 0: English (dendrite, theta_sin)
  - Tier 1: Hebrew (synapse, theta_cos)
  - Tier 2: Unicode (synapse, theta_hybrid)
  - Tier 3: Wave (synapse, theta_tan)
  - Tier 4: DNA (synapse, theta_hybrid)
  - Tier 5: LLVM (axon, theta_sin)

- **Layout Configuration**: Graph visualization settings
  - Graphviz dot engine
  - Top-to-bottom ranking
  - Radial layout for cortical columns

- **Export Formats**: Multiple output formats
  - DOT, JSON, SVG, PNG
  - Obsidian canvas integration

## Usage

This configuration file is designed to be consumed by neurograph visualization tools that support the TRIG6 architecture. It provides a complete specification for rendering neural topology graphs of the FlameLang compilation pipeline.

## Related Files

- Export directory: `../graph/` - Contains generated graph outputs
- Obsidian vault: `Strategickhaos` - Obsidian integration target
