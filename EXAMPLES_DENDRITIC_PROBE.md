# Proto-Elamite Dendritic Visualization - Usage Examples

## Quick Start

### 1. Run the Probe

```bash
# Simple run with defaults (50 mutations per symbol)
python3 dendritic_viz_probe.py

# Or use the quick start script
./run_dendritic_probe.sh
```

### 2. Analyze Output

```bash
# Generate analysis report
python3 analyze_dendritic_output.py neurograph/proto_elamite_pelsim1_dendrites.json
```

## Example Output

### Probe Execution

```
🧬 PROTO-ELAMITE DENDRITIC VISUALIZATION PROBE
============================================================
Scope: 4 Proto-Elamite symbols
Max mutations per symbol: 50
Proverbs baseline anchors: 3

Processing: impressed circle
  ✓ 15 accepted, 18 rejected
Processing: wedge cluster
  ✓ 14 accepted, 26 rejected
Processing: bar
  ✓ 21 accepted, 29 rejected
Processing: dot series
  ✓ 27 accepted, 23 rejected

Total edges logged: 173
✓ Output written to: neurograph/proto_elamite_pelsim1_dendrites.json
```

### Analysis Results

```
📊 COLOR DISTRIBUTION
============================================================
  GREEN   | ████████  29 ( 16.8%)
  YELLOW  | ███████████████████████████████████ 124 ( 71.7%)
  RED     | █████  20 ( 11.6%)

🎯 ACCEPTANCE RATES
============================================================
  Accepted:   77 ( 44.5%)
  Rejected:   96 ( 55.5%)

🔬 PER-SYMBOL ANALYSIS
============================================================

  impressed circle
    Mutations: 33
    Accepted:  15 (45.5%)
    Colors:    G=3 Y=24 R=6
    Avg Δf:    -0.1064
    Avg Δdanger: +0.8981
```

## Working with the Output

### JSON Structure

```json
{
  "metadata": {
    "probe_type": "dendritic_visualization",
    "scope": "proto_elamite",
    "symbols": ["impressed circle", "wedge cluster", "bar", "dot series"],
    "warning": "PROBE DATA - NOT FOR CANONICAL PROMOTION"
  },
  "edges": [
    {
      "symbol": "impressed circle",
      "old_value": "circular_count",
      "new_value": "circular_measure",
      "f_old": 0.5279,
      "f_new": 0.6441,
      "danger_old": 1.0500,
      "danger_new": 2.0992,
      "alpha": 0.4532,
      "accepted": true,
      "color": "red"
    }
  ]
}
```

### Filtering Examples

```python
import json

# Load data
with open('neurograph/proto_elamite_pelsim1_dendrites.json', 'r') as f:
    data = json.load(f)

# Get only green (safe improvement) edges
green_edges = [e for e in data['edges'] if e['color'] == 'green']
print(f"Safe improvements: {len(green_edges)}")

# Get accepted mutations
accepted = [e for e in data['edges'] if e['accepted']]
print(f"Accepted mutations: {len(accepted)}")

# Get mutations for specific symbol
impressed_circle = [e for e in data['edges'] if e['symbol'] == 'impressed circle']
print(f"Impressed circle mutations: {len(impressed_circle)}")

# Get high fitness improvements
high_improvements = [e for e in data['edges'] if e['f_new'] - e['f_old'] >= 0.1]
print(f"High fitness gains: {len(high_improvements)}")
```

## Visualization Workflows

### For Gephi

1. Load `neurograph/proto_elamite_pelsim1_dendrites.json`
2. Convert to GEXF format:

```python
import json
import networkx as nx

# Load data
with open('neurograph/proto_elamite_pelsim1_dendrites.json', 'r') as f:
    data = json.load(f)

# Create directed graph
G = nx.DiGraph()

# Add nodes (symbol states)
node_id = 0
node_map = {}

for edge in data['edges']:
    # Add old state node
    old_key = f"{edge['symbol']}:{edge['old_value']}"
    if old_key not in node_map:
        node_map[old_key] = node_id
        G.add_node(node_id, label=edge['old_value'], symbol=edge['symbol'], fitness=edge['f_old'], danger=edge['danger_old'])
        node_id += 1
    
    # Add new state node
    new_key = f"{edge['symbol']}:{edge['new_value']}"
    if new_key not in node_map:
        node_map[new_key] = node_id
        G.add_node(node_id, label=edge['new_value'], symbol=edge['symbol'], fitness=edge['f_new'], danger=edge['danger_new'])
        node_id += 1
    
    # Add edge
    G.add_edge(
        node_map[old_key],
        node_map[new_key],
        color=edge['color'],
        accepted=edge['accepted'],
        alpha=edge['alpha'],
        weight=edge['f_new'] - edge['f_old']  # Use fitness delta as weight
    )

# Export to GEXF
nx.write_gexf(G, 'neurograph/proto_elamite_dendrites.gexf')
print("✓ Exported to GEXF format")
```

### For D3.js

```javascript
// Load JSON directly
fetch('neurograph/proto_elamite_pelsim1_dendrites.json')
  .then(response => response.json())
  .then(data => {
    // Create nodes and links for D3 force graph
    const nodes = [];
    const links = [];
    const nodeMap = new Map();
    let nodeId = 0;
    
    data.edges.forEach(edge => {
      // Get or create old node
      const oldKey = `${edge.symbol}:${edge.old_value}`;
      if (!nodeMap.has(oldKey)) {
        nodeMap.set(oldKey, nodeId);
        nodes.push({
          id: nodeId,
          label: edge.old_value,
          symbol: edge.symbol,
          fitness: edge.f_old,
          danger: edge.danger_old
        });
        nodeId++;
      }
      
      // Get or create new node
      const newKey = `${edge.symbol}:${edge.new_value}`;
      if (!nodeMap.has(newKey)) {
        nodeMap.set(newKey, nodeId);
        nodes.push({
          id: nodeId,
          label: edge.new_value,
          symbol: edge.symbol,
          fitness: edge.f_new,
          danger: edge.danger_new
        });
        nodeId++;
      }
      
      // Create link
      links.push({
        source: nodeMap.get(oldKey),
        target: nodeMap.get(newKey),
        color: edge.color,
        accepted: edge.accepted,
        alpha: edge.alpha
      });
    });
    
    // Now use nodes and links with D3 force layout
    // ...
  });
```

## Advanced Analysis

### Finding Optimal Paths

```python
import json

# Load data
with open('neurograph/proto_elamite_pelsim1_dendrites.json', 'r') as f:
    data = json.load(f)

# Find paths with maximum fitness improvement and minimum danger increase
optimal_paths = []

for edge in data['edges']:
    fitness_gain = edge['f_new'] - edge['f_old']
    danger_change = edge['danger_new'] - edge['danger_old']
    
    # Optimal: positive fitness, negative or zero danger
    if fitness_gain > 0.05 and danger_change <= 0:
        optimal_paths.append({
            'symbol': edge['symbol'],
            'transformation': f"{edge['old_value']} → {edge['new_value']}",
            'fitness_gain': fitness_gain,
            'danger_reduction': -danger_change,
            'color': edge['color']
        })

# Sort by fitness gain
optimal_paths.sort(key=lambda x: x['fitness_gain'], reverse=True)

print(f"Found {len(optimal_paths)} optimal mutation paths:")
for i, path in enumerate(optimal_paths[:5], 1):
    print(f"{i}. {path['symbol']}: {path['transformation']}")
    print(f"   Fitness: +{path['fitness_gain']:.4f}, Safety: +{path['danger_reduction']:.4f}")
```

## Interpretation Guide

### Edge Colors

- **Green** 🟢: Safe improvements
  - Fitness increased by ≥5%
  - Danger stayed same or decreased
  - **Action**: These are ideal mutation paths

- **Yellow** 🟡: Neutral or safer mutations
  - Small fitness changes (|Δf| < 5%)
  - But danger decreased
  - **Action**: Consider for stability improvements

- **Red** 🔴: Risky improvements
  - Fitness increased
  - But danger also increased
  - **Action**: Review carefully, may not be worth the risk

### Hard Rails (Auto-Filtered)

Edges are automatically dropped if:
- `danger_new > danger_old * 2` (danger more than doubled)
- `f_new < 0.01` (fitness fell below threshold)

These never appear in the output, protecting against dangerous mutations.

### Acceptance Status

- `accepted: true` - Evolutionary gate accepted the mutation
- `accepted: false` - Gate rejected it (still logged for analysis)

The gate uses `alpha` (acceptance probability) to make this decision.

## Common Questions

**Q: Can I use these mappings in production?**
A: No. This is probe data only, marked with `"warning": "PROBE DATA - NOT FOR CANONICAL PROMOTION"`. Use it for visualization and analysis only.

**Q: How do I adjust the mutation rate?**
A: Modify `max_mutations_per_symbol` parameter when creating `ProtoDendriticProbe`:
```python
probe = ProtoDendriticProbe(max_mutations_per_symbol=100)  # More mutations
```

**Q: Can I add more symbols?**
A: Yes, modify the `proto_elamite_symbols` list in the probe initialization.

**Q: What format should I use for graph visualization?**
A: The JSON output works directly with D3.js and vis.js. For Gephi/Cytoscape, convert to GEXF/GraphML using the examples above.

## Next Steps

1. Run the probe with different parameters
2. Visualize the dendritic tree in your preferred tool
3. Analyze fitness landscapes and danger zones
4. Study the evolutionary dynamics of symbol mutations
5. Compare Proto-Elamite patterns with Proverbs baseline

See **README_DENDRITIC_PROBE.md** for more details.
