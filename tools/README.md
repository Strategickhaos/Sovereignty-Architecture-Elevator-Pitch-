# NEURO-36 Immune Dashboard

## Overview

The NEURO-36 Immune Dashboard is a monitoring and reporting tool for the Sister Protocol execution system. It loads immune policy configuration, classifies nodes, displays hardware synthesis candidates, and generates comprehensive status reports.

## Author

**Domenic Gabriel Garza (Inventor)**  
Strategickhaos DAO LLC

## Features

- **Node Classification**: Automatically classifies nodes into categories:
  - 🛤️ **RAIL** - Core infrastructure nodes
  - 🚪 **GATE** - Security and access control nodes
  - 🏖️ **SANDBOX** - Experimental nodes in isolation
  - 🏆 **CHAMPION** - Proven high-performance nodes
  - ⭐ **CHAMPION_CANDIDATE** - Nodes being evaluated for champion status
  - 🧟 **MUTANT** - Nodes with concerning behavior
  - 💀 **CULL** - Nodes marked for removal

- **Status Monitoring**: Displays comprehensive metrics including:
  - Harmonic measure (H)
  - Fitness score
  - Danger rate
  - Mapping to system domains and traits
  - Hardware synthesis candidacy

- **TRIG6 Danger Zones**: Identifies nodes at critical angles (90° and 270°) where tan(θ) = ∞

- **Sister Protocol Execution Rules**: Documents policies for each classification type

- **Hardware Synthesis Candidates**: Lists priority nodes for hardware acceleration (FPGA, ASIC, GPU, etc.)

- **Kernel Protein Ligand (MACQGILP)**: Displays amino acid composition and instruction biases

- **JSON Export**: Exports dashboard data for programmatic access

## Installation

Ensure PyYAML is installed:

```bash
pip install pyyaml
```

## Usage

Run the dashboard from the repository root:

```bash
python3 tools/immune_dashboard.py
```

Or make it executable and run directly:

```bash
chmod +x tools/immune_dashboard.py
./tools/immune_dashboard.py
```

## Configuration

The dashboard reads its configuration from `config/neuro36_policy.yaml`. This file contains:

- Component definitions with simulation results
- Classification assignments
- Sister Protocol execution policies
- Hardware synthesis candidates
- Kernel ligand specifications

## Output

The dashboard generates:

1. **Console Output**: Comprehensive status tables and reports
2. **JSON Export**: `artifacts/immune_dashboard.json` with structured data

### Sample Output Sections

1. **Status Table**: Complete overview of all nodes with metrics
2. **Classification Summary**: Nodes grouped by classification
3. **TRIG6 Danger Zones**: Critical angle analysis
4. **Hardware Candidates**: Priority-sorted synthesis candidates
5. **Sister Protocol Rules**: Execution policies by classification
6. **Kernel Ligand**: MACQGILP amino acid analysis

## Architecture

### Classes

- **Classification (Enum)**: Enumeration of node classification types
- **ComponentStatus (dataclass)**: Represents status of a single immune component
- **ImmuneDashboard**: Main dashboard class with methods for:
  - Loading policy configuration
  - Filtering nodes by classification
  - Identifying hardware candidates
  - Printing various reports
  - Exporting to JSON

### Configuration Structure

```yaml
metadata:
  version: "1.0"
  author: "Domenic Gabriel Garza"
  system: "NEURO-36 Immune System"

components:
  - id: 1
    name: "Component Name"
    bio_role: "T Cell"
    theta_deg: 0
    mapping:
      domain: "Kernel"
      trait: "Memory Management"
    simulation:
      final_H: 0.95
      final_fitness: 0.920
      danger_rate: 0.05
    classification: "RAIL"
    policy:
      execution: "always_run"
      mutation_allowed: false
      hardware_candidate: true

sister_protocol:
  rail_policy:
    description: "..."
    nodes: [1, 2, 3]
    rules: [...]

hardware_candidates:
  priority_1:
    - id: 1
      name: "..."
      reason: "..."

kernel_ligand:
  amino_acids:
    M: "Memory - Manage allocation and deallocation"
    # ... more amino acids
```

## Example Usage

```python
from pathlib import Path
from tools.immune_dashboard import ImmuneDashboard, Classification

# Initialize dashboard
dashboard = ImmuneDashboard()

# Get all CHAMPION nodes
champions = dashboard.get_by_classification(Classification.CHAMPION)
for node in champions:
    print(f"{node.name}: fitness={node.final_fitness}")

# Get hardware synthesis candidates
hw_candidates = dashboard.get_hardware_candidates()
print(f"Total HW candidates: {len(hw_candidates)}")

# Export to JSON
dashboard.export_json(Path("artifacts/immune_dashboard.json"))
```

## Integration

The immune dashboard integrates with the Sovereignty Architecture by:

- Monitoring NEURO-36 immune system components
- Enforcing Sister Protocol execution policies
- Identifying candidates for hardware synthesis
- Tracking TRIG6 danger zones for security
- Maintaining kernel ligand instruction profiles

## License

Part of the Sovereignty Architecture Elevator Pitch project.  
Strategickhaos DAO LLC © 2026
