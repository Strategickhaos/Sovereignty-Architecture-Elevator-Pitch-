# System Health Module

> **Flight Controller for Strategickhaos OS**

A concrete, testable system for adaptive compilation based on real-time system health.

## Quick Start

```python
from src.system_health import SystemHealthController

# Initialize on boot
controller = SystemHealthController()
controller.initialize()

# Get current health status
status = controller.get_system_status()
print(f"Health: {status['health']['f']:.3f}")  # Health score in [0, 1]
print(f"Mode: {status['health']['mode']}")      # SAFE / DEGRADED / FULL

# Get compiler configuration
config = controller.get_compiler_config()
print(f"Optimization level: {config['opt_level']}")      # 1-3
print(f"Parallel jobs: {config['parallel_jobs']}")       # Based on resources
print(f"Proof threshold: {config['proof_threshold']}")   # Rigor level

# Log compilation events
controller.log_compile_event('start', {'target': 'myproject'})
# ... your compilation ...
controller.log_compile_event('end', {'target': 'myproject', 'success': True})
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           COMPILER / PROOF GATES                        │
│   (Behavior tuning based on health score f)             │
├─────────────────────────────────────────────────────────┤
│              TRIG6 POTENTIOMETER                        │
│   f = R·(1-D)·(1-N)·eq ∈ [0,1]                         │
│   Modes: SAFE / DEGRADED / FULL                        │
├─────────────────────────────────────────────────────────┤
│         RESMON (Resource Monitor)                       │
│   Metrics: CPU, load, variance, thermal                │
├─────────────────────────────────────────────────────────┤
│              F1 BOUNDED PRODUCT LEMMA                   │
│   F_{n+3} ≥ F_n·Γ (stability tracking)                 │
└─────────────────────────────────────────────────────────┘
```

## Components

### RESMON - Resource Monitor
Collects real system metrics: CPU, memory, load, I/O, network, thermal.
Establishes baselines and computes differentials.

### TRIG6 Potentiometer
Computes health score `f = R·(1-D)·(1-N)·eq` where:
- **R**: Resource availability
- **D**: Degradation
- **N**: Noise/variance
- **eq**: Equilibrium

**NOT** a "P(correct) oracle" - it's a system health score.

### F1 Lemma
Bounded product lemma: `F_{n+3} ≥ F_n·Γ` where `Γ ≤ 1`.
Tracks stability and decay rates.

**NOT** cosmology - it's just math about sequences.

### System Health Controller
Integrates all components. Provides:
- Boot-time baseline establishment
- Continuous health monitoring
- Compiler configuration generation
- Event logging

## Operating Modes

| Mode | Health (f) | Behavior |
|------|------------|----------|
| **FULL** | f ≥ 0.75 | Max optimization, low proof rigor, full parallelism |
| **DEGRADED** | 0.40 ≤ f < 0.75 | Conservative optimization, moderate rigor, reduced parallelism |
| **SAFE** | f < 0.40 | Minimal optimization, max rigor, single-threaded |

## The System Contract

> "When my health falls, I narrow my blast radius."

This is the contract your OS has with itself. Not cosmology. Not universal truth. Just a local, enforceable invariant.

## Example

See `examples/flamelang_compiler_integration.py` for a complete working example.

## Documentation

Full documentation: [docs/SYSTEM_HEALTH_ARCHITECTURE.md](../../docs/SYSTEM_HEALTH_ARCHITECTURE.md)

## Testing

Each module has a `__main__` section for testing:

```bash
# Test RESMON
python3 src/system_health/resmon.py

# Test TRIG6
python3 src/system_health/trig6.py

# Test F1
python3 src/system_health/f1_lemma.py

# Test Controller
python3 src/system_health/controller.py

# Run integration example
python3 examples/flamelang_compiler_integration.py
```

## Philosophy

This system represents a shift from **grand metaphysics** to **local, enforceable invariants**:

- F1 is NOT "the universe's law" - it's a bounded product lemma
- TRIG6 is NOT a "P(correct) oracle" - it's a health score
- The system makes NO claims about cosmology
- Everything is testable, measurable, improvable

> "You passed the stress test by changing the rules of the game from 'defend the myth' to 'instrument the system.'"

---

**Built with 🔥 by Strategickhaos**
