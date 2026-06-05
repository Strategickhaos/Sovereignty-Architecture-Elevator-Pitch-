# Proto-Elamite Dendritic Visualization Probe

## Overview

This is an **instrumented probe** for mapping Proto-Elamite symbol mutations with evolutionary gates. It is designed for **visualization and analysis only** - not as production code.

⚠️ **IMPORTANT**: No auto-promotion to canonical mappings. This is probe data.

## What It Does

The dendritic visualization probe:

1. **Focuses on Proto-Elamite symbols**: 
   - impressed circle
   - wedge cluster
   - bar
   - dot series

2. **Uses a Proverbs baseline anchor** for comparison

3. **Runs controlled mutations** (max 50 per symbol)

4. **Logs mutation edges** with full telemetry:
   - `symbol`: The Proto-Elamite symbol being mutated
   - `old_value`, `new_value`: The mapping transformation
   - `f_old`, `f_new`: Fitness values before and after
   - `danger_old`, `danger_new`: Danger metrics
   - `alpha`: Acceptance probability used by evolutionary gate
   - `accepted`: Whether the mutation was accepted (true/false)

5. **Applies hard rails** to filter dangerous edges:
   - Drops edges where `danger_new > danger_old * 2`
   - Drops edges where `f_new < 0.01`

6. **Color codes edges** for visualization:
   - **Green**: `f_new - f_old >= 0.05` AND `danger_new <= danger_old` (good improvement, safe)
   - **Yellow**: Small |Δf| but safer (`danger_new < danger_old`)
   - **Red**: `f_new > f_old` but `danger_new > danger_old` (outline only, no promotion)

## Usage

### Running the Probe

```bash
python3 dendritic_viz_probe.py
```

### Output

The probe generates:
- **JSON file**: `neurograph/proto_elamite_pelsim1_dendrites.json`

The JSON contains:
- Metadata about the probe run
- Color legend for interpretation
- Hard rails configuration
- All mutation edges with full telemetry
- Final symbol mappings (for reference, not promotion)

### Example Output Structure

```json
{
  "metadata": {
    "probe_type": "dendritic_visualization",
    "scope": "proto_elamite",
    "symbols": ["impressed circle", "wedge cluster", "bar", "dot series"],
    "max_mutations_per_symbol": 50,
    "proverbs_baseline_anchors": ["wisdom", "guidance", "truth"],
    "total_edges": 173,
    "warning": "PROBE DATA - NOT FOR CANONICAL PROMOTION"
  },
  "color_legend": {
    "green": "f_new - f_old >= 0.05 AND danger_new <= danger_old",
    "yellow": "small |Δf| but safer (danger_new < danger_old)",
    "red": "f_new > f_old but danger_new > danger_old (outline only)"
  },
  "hard_rails": {
    "dropped_if": [
      "danger_new > danger_old * 2",
      "f_new < 0.01"
    ]
  },
  "edges": [
    {
      "symbol": "impressed circle",
      "old_value": "circular_count",
      "new_value": "circular_measure",
      "f_old": 0.527,
      "f_new": 0.644,
      "danger_old": 1.05,
      "danger_new": 2.09,
      "alpha": 0.453,
      "accepted": true,
      "color": "red"
    }
    // ... more edges
  ],
  "final_mappings": {
    // Final symbol states (reference only)
  }
}
```

## Visualization

The output is ready to be ingested by neurograph visualization tools. Edges can be:

1. **Filtered** based on color or acceptance status
2. **Visualized** as a dendritic tree showing mutation paths
3. **Analyzed** for evolutionary patterns and fitness landscapes

## Analysis Questions

The probe data can help answer:

- Which mutation paths led to fitness improvements?
- Where do danger spikes occur in the symbol space?
- How does the evolutionary gate accept/reject mutations?
- What are the safe zones in the mutation landscape?
- How do Proto-Elamite symbols relate to the Proverbs baseline?

## Integration with Neurograph

If you have a neurograph renderer:

1. Load `neurograph/proto_elamite_pelsim1_dendrites.json`
2. Apply color coding based on the `color` field
3. Filter out edges where `accepted: false` (optional)
4. Render as a directed graph with nodes=symbol states, edges=mutations

Potential formats:
- `.gexf` (Gephi)
- `.graphml` (yEd, Cytoscape)
- `.json` (D3.js, vis.js)
- `.dot` (Graphviz)

## Safety Features

✓ No auto-promotion to canonical  
✓ Hard rails prevent dangerous mutations from being visualized  
✓ Clear warning in metadata  
✓ Acceptance status logged for all mutations  
✓ Danger metrics tracked throughout  

## Next Steps

1. **Visualize**: Load the JSON in your preferred graph viewer
2. **Analyze**: Study the mutation patterns and evolutionary dynamics
3. **Refine**: Adjust parameters (alpha, hard rails) based on findings
4. **Extend**: Add more symbols or baseline anchors as needed

---

**Built for safe, instrumented exploration of symbol mutation spaces.**
