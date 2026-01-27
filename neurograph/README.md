# Proto-Elamite Neurograph Dendrites (PELSIM1)

Instrumented probe run for tracking Proto-Elamite symbol mutations through a dendrite graph structure.

## 📋 Overview

This system simulates the evolution of Proto-Elamite symbols through mutation events, applying safety rails and classification logic to generate a neurograph of mutation dendrites.

**Status**: Lab probe - not canonical. All mappings are instrumented for research purposes.

## 🏗️ Schema Structure

The neurograph JSON follows this structure:

```json
{
  "meta": { ... },      // Simulation metadata
  "nodes": [ ... ],     // Symbol states (initial + mutated)
  "edges": [ ... ]      // Mutation events (dendrites)
}
```

### Meta Section

Configuration and run metadata:

- **id**: Unique identifier for this dendrite set
- **script**: Script family (Proto-Elamite)
- **symbols_scoped**: List of symbols tracked in this run
- **max_mutations_per_symbol**: Maximum mutations allowed per symbol (50)
- **trig_layer**: TRIG layer association (TRIG6-proto-elamite-sim)
- **alpha_default**: Default alpha value for evolution gate (0.32)
- **created_at**: ISO 8601 timestamp
- **run_id**: Run identifier (PELSIM1-RUN-001)
- **notes**: Run description

### Nodes

Each node represents a specific state of a symbol:

- **id**: Stable unique ID in format `<symbol_slug>:v<value>`
- **symbol**: Human-readable symbol name
- **value**: Numeric value for this symbol state
- **role**: Either "initial" or "mutated"
- **runs**: Array of run IDs that observed this node

**Example**:
```json
{
  "id": "impressed_circle:v12",
  "symbol": "impressed circle",
  "value": 12,
  "role": "mutated",
  "runs": ["PELSIM1-RUN-001"]
}
```

### Edges (Mutation Dendrites)

Each edge represents one mutation event from (symbol, old_value) → (symbol, new_value).

**Rail Filters** (edges failing these are excluded):
- `danger_new <= danger_old * 2`
- `f_new >= 0.01`

**Fields**:
- **id**: Unique edge ID (e0001, e0002, etc.)
- **from/to**: Node IDs for source and target
- **symbol**: Symbol being mutated
- **old_value/new_value**: Value transition
- **f_old/f_new**: Frequency metrics before/after
- **danger_old/danger_new**: Danger metrics before/after
- **alpha**: Evolution gate parameter (0.32)
- **accepted**: Whether evo gate accepted this mapping (true for all passing rails)
- **classification**: Color code (green/yellow/red)
- **delta_f**: Change in frequency (f_new - f_old)
- **delta_danger**: Change in danger (danger_new - danger_old)
- **timestamp**: ISO 8601 timestamp
- **run_id**: Run identifier

## 🎨 Classification Logic

Edges are classified by color based on their fitness and danger characteristics:

### Green 🟢
**Better & Safer**
- `delta_f >= 0.05` AND `danger_new <= danger_old`
- Significant improvement in frequency with same or better safety
- Visualization: Bright, thick lines

### Yellow 🟡
**Neutral/Ambiguous**
- `abs(delta_f) < 0.05` AND `danger_new < danger_old` (small change but safer)
- OR any other combination not matching green/red
- Visualization: Normal lines, possibly dashed

### Red 🔴
**Better but Riskier**
- `delta_f > 0` AND `danger_new > danger_old`
- Improved frequency but increased danger
- Visualization: Outline/halo only (warning, not promotion)

## 🚀 Usage

### Generate New Simulation

```bash
cd neurograph
python3 proto_elamite_simulator.py
```

This will:
1. Initialize 4 Proto-Elamite symbols (impressed circle, wedge cluster, bar, dot series)
2. Generate up to 50 mutations per symbol
3. Apply safety rails to filter dangerous mutations
4. Classify each edge by color
5. Output `proto_elamite_pelsim1_dendrites.json`

### Customize Parameters

Edit `proto_elamite_simulator.py` to modify:

```python
symbols = [
    "impressed circle",
    "wedge cluster",
    "bar",
    "dot series"
]

max_mutations_per_symbol = 50  # Adjust mutation count
alpha = 0.32                    # Evolution gate parameter
run_id = "PELSIM1-RUN-001"     # Unique run identifier
```

## 📊 Output Statistics

The simulator outputs:
- Total nodes generated
- Total edges generated
- Classification breakdown (green/yellow/red counts)
- Rail validation results

Example output:
```
✓ Simulation complete!
  Generated 131 nodes
  Generated 200 edges
  Saved to: proto_elamite_pelsim1_dendrites.json

  Edge classifications:
    green: 32
    yellow: 92
    red: 76
```

## 🔬 Research Notes

This is an **instrumented probe run** - results are for analysis only and not promoted to canonical mappings.

Key research questions:
1. How do Proto-Elamite symbols evolve under mutation pressure?
2. What percentage of mutations pass safety rails?
3. What is the distribution of green/yellow/red classifications?
4. Which symbols show the most stable evolution patterns?

## 📁 Files

- `proto_elamite_pelsim1_dendrites.json` - Generated dendrite graph (117KB, 200 edges)
- `proto_elamite_simulator.py` - Simulation engine
- `analyze_neurograph.py` - Analysis and demonstration script
- `validate_schema.py` - JSON schema validation tool
- `README.md` - This file

### Helper Scripts

**Analyze Neurograph** (`analyze_neurograph.py`)
```bash
python3 analyze_neurograph.py
```
Demonstrates how to:
- Load and query the neurograph
- Analyze symbol evolution patterns
- Find mutation chains
- Filter by classification
- Calculate statistics

**Validate Schema** (`validate_schema.py`)
```bash
python3 validate_schema.py [filepath]
```
Validates:
- JSON syntax and structure
- Required fields in meta/nodes/edges
- Data types
- Rails compliance
- Classification values
- ISO 8601 timestamps

## 🔗 Integration

This neurograph can be loaded by visualization tools that support the dendrite schema. The JSON structure is designed for:

- Graph visualization (nodes + edges)
- Time-series analysis (timestamp on edges)
- Classification filtering (by color)
- Multi-run comparison (runs arrays on nodes)

## ⚡️ Safety Rails

All edges in the output have passed these rails:

1. **Danger Rail**: `danger_new <= danger_old * 2`
   - Prevents dangerous runaway mutations
   - Ensures new states aren't wildly more dangerous than parent states

2. **Frequency Rail**: `f_new >= 0.01`
   - Ensures minimum viable frequency
   - Filters out extremely rare/unstable states

Edges that fail these rails are **not included** in the output.

---

**Lab Probe Status**: 🧪⚡️ Active  
**TRIG Layer**: TRIG6-proto-elamite-sim  
**Run ID**: PELSIM1-RUN-001
