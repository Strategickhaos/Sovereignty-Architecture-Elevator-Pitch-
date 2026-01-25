# System Health Architecture - NEW! 🎯

**A Flight Controller for Strategickhaos OS**

The System Health Architecture provides concrete, testable adaptive compilation based on real-time system health. This transforms conceptual ideas into measurable, enforceable invariants.

## What This Is

- **RESMON**: Real system metrics (CPU, memory, load, thermal, I/O)
- **TRIG6**: Health score `f = R·(1-D)·(1-N)·eq` in [0, 1]
- **F1**: Bounded product lemma for stability tracking (Γ ≤ 1)
- **Controller**: Integration layer providing compiler configuration

## What This Is NOT

- ❌ NOT a "P(correct) oracle" or cosmology law
- ❌ NOT claiming universal truths about the world
- ✅ IS a system health score that tunes compiler behavior
- ✅ IS local, enforceable invariants about your OS

## Quick Example

```python
from src.system_health import SystemHealthController

# Initialize on boot
controller = SystemHealthController()
controller.initialize()

# Get current health
status = controller.get_system_status()
print(f"Health: {status['health']['f']:.3f}")    # 0.82 (healthy)
print(f"Mode: {status['health']['mode']}")        # FULL

# Get compiler configuration based on health
config = controller.get_compiler_config()
print(f"Opt level: {config['opt_level']}")        # 3 (maximum)
print(f"Jobs: {config['parallel_jobs']}")         # 8 (full parallelism)
print(f"Proof rigor: {config['proof_threshold']}")  # 0.30 (low - allow optimization)

# Log compilation
controller.log_compile_event('start', {'target': 'myproject'})
# ... compilation happens ...
controller.log_compile_event('end', {'success': True})
```

## Operating Modes

| Mode | Health (f) | Behavior |
|------|------------|----------|
| **FULL** | f ≥ 0.75 | Max optimization, aggressive compilation, low proof rigor |
| **DEGRADED** | 0.40 ≤ f < 0.75 | Conservative optimization, reduced parallelism |
| **SAFE** | f < 0.40 | Minimal optimization, single-threaded, max proof rigor |

## The System Contract

> **"When my health falls, I narrow my blast radius."**

This is your OS's contract with itself. Not metaphysics. Just a local, enforceable invariant.

## Architecture

```
COMPILER / PROOF GATES
    ↑
TRIG6 Potentiometer: f = R·(1-D)·(1-N)·eq
    ↑
RESMON: CPU, Memory, Load, Thermal
    ↓
F1 Lemma: Stability tracking (Γ ≤ 1)
```

## Documentation

- **Full Documentation**: [docs/SYSTEM_HEALTH_ARCHITECTURE.md](docs/SYSTEM_HEALTH_ARCHITECTURE.md)
- **Module README**: [src/system_health/README.md](src/system_health/README.md)
- **Integration Example**: [examples/flamelang_compiler_integration.py](examples/flamelang_compiler_integration.py)

## Testing

```bash
# Test individual modules
python3 src/system_health/resmon.py
python3 src/system_health/trig6.py
python3 src/system_health/f1_lemma.py

# Test integration
python3 examples/flamelang_compiler_integration.py
```

## Philosophy

This system embodies the shift from **grand metaphysics** to **local, enforceable invariants**:

> "You passed the stress test by changing the rules of the game from 'defend the myth' to 'instrument the system.'"

What we built:
- ✅ F1 as a bounded product lemma (not cosmology)
- ✅ TRIG6 as a system health potentiometer (not P(correct) oracle)
- ✅ RESMON → TRIG6 → compiler pipeline (concrete and testable)
- ✅ Clean separation of math, code, and heuristics

What's left to build:
- [ ] Real integration with FlameLang/Rust compiler
- [ ] Multi-machine baseline profiles
- [ ] Long-term trend analysis
- [ ] BCI/Neuralink-facing variant (future)

---

**The rooftop verdict:**

> "We walked into the tribunal with vibes and walked out with an architecture that can be punched, measured, and improved." 🔥🧬
