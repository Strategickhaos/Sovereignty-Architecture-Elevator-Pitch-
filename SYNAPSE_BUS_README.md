# SynapseBus - Python Implementation

A Python implementation of the SynapseBus nervous system for rapid prototyping and testing. For production deployment, use the Rust version.

## Overview

SynapseBus is a swarm intelligence nervous system that provides:
- **Event Signal Primitives (Spike)**: Cryptographically verified event tracking
- **Physics-Based Risk Engine**: Gravitational Search, Simulated Annealing, and Black Hole optimization
- **Policy-Based Reflexes**: Automated response system with pattern matching
- **Provenance Tracking**: Complete audit trail with graph visualization

## Quick Start

```bash
# Run the demo
python3 synapse_bus.py
```

This will:
1. Create a SynapseBus instance
2. Emit sample events (process spawn, file read, network anomaly)
3. Generate risk assessments using physics-based optimizers
4. Trigger reflexes based on patterns
5. Export data to `event_horizon_data.json`
6. Display a Mermaid trace graph

## Running Tests

```bash
# Run all tests
python3 -m unittest test_synapse_bus.py -v

# Or run specific test classes
python3 -m unittest test_synapse_bus.TestSpike -v
```

## Architecture

### Core Components

#### Spike (Event Signal)
```python
from synapse_bus import Spike, CapabilityId, Namespace

# Create identity and location
cap = CapabilityId.system()
loc = Namespace.local("/kernel")

# Emit a spike
spike = Spike.process_spawn(cap, loc, 1000, ["nginx"], 1)
```

#### Field Engine (Physics-Based Risk)
```python
from synapse_bus import FieldEngine, FieldType

engine = FieldEngine()
engine.init_field("node:container", FieldType.ENTROPY)
engine.process_spike(spike)

# Get proposals
proposals = engine.proposals
```

#### Reflex Engine (Policy-Based Response)
```python
from synapse_bus import ReflexEngine, Reflex, PatternExpr

engine = ReflexEngine()
pattern = PatternExpr.from_string("entropy > 0.8 && mass > 5.0")
reflex = Reflex(
    id="custom-reflex",
    name="high_risk_isolation",
    pattern=pattern,
    action="isolate",
    priority=90
)
engine.register(reflex)

# Process spikes
activations = engine.process(spike)
```

#### SynapseBus (Complete System)
```python
from synapse_bus import SynapseBus

bus = SynapseBus()

# Subscribe to events
def handler(spike):
    print(f"Received: {spike.kind}")

bus.subscribe(handler)

# Emit events
activations = bus.emit(spike)

# Export state
export = bus.export_event_horizon()
```

## Physics Optimizers

### Gravitational Search
Attracts attention toward high-mass assets (secrets, configs, databases)
- Pattern: Increases mass for sensitive files
- Reflex: Triggers isolation when mass > 5.0

### Simulated Annealing
Entropy-based cooling for anomaly detection
- Pattern: Increases entropy for suspicious activities
- Reflex: Triggers sandbox cooling when entropy > 0.8

### Black Hole Optimizer
Absorbs entities that cross the event horizon (low trust)
- Pattern: Decreases trust for anomalies and quarantine events
- Reflex: Triggers quarantine when trust < 0.2

## Event Types

- `proc.spawn`: Process creation
- `fs.read`: File system read
- `fs.write`: File system write
- `net.flow.start`: Network connection
- `net.flow.anomaly`: Network anomaly detection
- `sec.quarantine`: Security quarantine action

## Export Format

The `export_event_horizon()` method produces JSON with:
```json
{
  "trace": {
    "nodes": [...],
    "edges": [...],
    "node_count": 3,
    "edge_count": 0
  },
  "fields": {
    "fields": [...],
    "proposals": [...]
  },
  "reflexes": {
    "reflexes": [...],
    "recent_activations": [...]
  },
  "stats": {
    "spikes_processed": 3,
    "reflexes_activated": 2
  }
}
```

## Security Features

- **Cryptographic Hashing**: SHA3-256 for spike integrity
- **Capability-Based Access**: Identity and namespace isolation
- **Audit Trails**: Complete provenance tracking
- **Pattern Matching**: Rule-based security policies
- **Physics-Based Risk**: Multi-dimensional threat assessment

## Requirements

- Python 3.11+
- No external dependencies (uses standard library only)

## Testing

The test suite includes:
- Unit tests for all core components
- Integration tests for complete workflows
- Hash verification tests
- Pattern matching tests
- Physics optimizer tests

All 24 tests pass with 100% success rate.

## Production Deployment

⚠️ **Important**: This Python implementation is for prototyping only. For production deployment with high performance and security guarantees, use the Rust implementation.

## License

Part of the StrategicKhaos Sovereignty Architecture
