# System Health Architecture

**A Flight Controller for Strategickhaos OS**

> "You passed the stress test by changing the rules of the game from 'defend the myth' to 'instrument the system.'"

## Overview

This architecture provides a concrete, testable system for adaptive compilation based on real-time system health. It transforms conceptual ideas into measurable, enforceable invariants.

### The Architecture Stack

```
┌─────────────────────────────────────────────────────────┐
│           COMPILER / PROOF GATES                        │
│   (Behavior tuning based on health score f)             │
├─────────────────────────────────────────────────────────┤
│              TRIG6 POTENTIOMETER                        │
│   f = R·(1-D)·(1-N)·eq ∈ [0,1]                         │
│   Modes: SAFE / DEGRADED / FULL                        │
│   Outputs: proof_threshold, opt_aggression             │
├─────────────────────────────────────────────────────────┤
│         RESMON (Resource Monitor)                       │
│   Metrics: CPU, load, variance, process, thermal       │
│   Baseline tracking + differential computation          │
├─────────────────────────────────────────────────────────┤
│              F1 BOUNDED PRODUCT LEMMA                   │
│   F_{n+3} ≥ F_n·Γ where Γ ≤ 1                          │
│   Stability/decay sequence tracking                     │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. RESMON - Resource Monitor

**Purpose**: Collect real system metrics and compute differentials vs baseline.

**Metrics Collected**:
- CPU utilization percentage
- Load average (1, 5, 15 min)
- Memory usage percentage
- Disk I/O rates (MB/s)
- Network I/O rates (MB/s)
- Process count
- Thermal readings (if available)

**Baseline Establishment**: Takes multiple samples at boot to establish normal operating parameters.

**Differential Computation**: Compares current metrics to baseline, producing normalized differentials in [0, 1].

**Usage**:
```python
from src.system_health import RESMON

resmon = RESMON(baseline_samples=10, sample_interval=0.5)
baseline = resmon.establish_baseline()

metrics = resmon.collect_metrics()
diff = resmon.compute_differential(metrics)

print(f"CPU: {metrics.cpu_percent}% (diff: {diff.cpu_diff})")
print(f"Variance: {diff.variance}")
```

### 2. TRIG6 Potentiometer

**Purpose**: Compute system health score and determine operating mode.

**NOT**: A "P(correct) oracle" or cosmology law.  
**IS**: A system potentiometer - tells your OS how hard it can push.

**Formula**:
```
f = R·(1-D)·(1-N)·eq

where:
  R = Resource availability [0, 1]
  D = Degradation factor [0, 1]
  N = Noise/variance factor [0, 1]
  eq = Equilibrium/stability factor [0, 1]
```

**Operating Modes**:
- **FULL** (f ≥ 0.75): All systems operational, aggressive optimization
- **DEGRADED** (0.40 ≤ f < 0.75): Reduced capacity, conservative operation
- **SAFE** (f < 0.40): Minimal blast radius, maximum safety

**Outputs**:
- `f`: Health score [0, 1]
- `mode`: Operating mode
- `proof_threshold`: Rigor required for proof validation (inverse to health)
- `opt_aggression`: Optimization aggression level (proportional to health)

**System Contract**:
> "When my health falls, I narrow my blast radius."

**Usage**:
```python
from src.system_health import TRIG6Potentiometer, TRIG6Params

trig6 = TRIG6Potentiometer()

params = TRIG6Params(R=0.85, D=0.10, N=0.05, eq=0.95)
health = trig6.assess(params, timestamp=time.time())

print(f"Health: f={health.f:.3f}")
print(f"Mode: {health.mode}")
print(f"Contract: {trig6.get_system_contract(health)}")
```

### 3. F1 - Bounded Product Lemma

**Purpose**: Track stability and provide decay bounds for sequences.

**NOT**: Cosmology or deep universal law.  
**IS**: A legit little lemma about stability/decay of sequences.

**Mathematical Foundation**:
```
Given three stepwise multiplicative bounds:
F_{n+3} ≥ F_n · Γ₁ · Γ₂ · Γ₃

Where each Γᵢ ≤ 1 (the core constraint)

Special case: Γ = Γ₁ · Γ₂ · Γ₃ ≤ 1
```

**Use Cases**:
- Proving stability bounds in iterative systems
- Tracking decay rates in resource allocation  
- Establishing convergence properties
- Predicting future system states (conservative lower bounds)

**Usage**:
```python
from src.system_health import F1Lemma, gamma_from_health_score

f1 = F1Lemma()

# Add sequence bounds
f1.add_bound(index=0, value=100.0, gamma=0.95)
f1.add_bound(index=1, value=95.0, gamma=0.95)
f1.add_bound(index=2, value=90.25, gamma=0.95)
f1.add_bound(index=3, value=85.74, gamma=0.95)

# Verify 3-step bound
verification = f1.verify_bound(n=0, k=3)
print(f"Bound satisfied: {verification['satisfied']}")

# Track health score stability
gamma = gamma_from_health_score(f_current=0.82, f_previous=0.85)
```

### 4. System Health Controller

**Purpose**: Integrate all components and provide actionable outputs.

**Pipeline**:
```
RESMON → TRIG6 → Compiler Configuration
   ↓
  F1 (stability tracking)
```

**Features**:
- Boot-time baseline establishment
- Continuous health monitoring
- Compiler configuration generation
- Event logging (boot, ticks, compilations)
- Stability tracking via F1

**Usage**:
```python
from src.system_health import SystemHealthController

controller = SystemHealthController(log_dir="./logs/system_health")

# Initialize on boot
controller.initialize()

# Get current health
status = controller.get_system_status()
print(f"Health: {status['health']['f']:.3f}")
print(f"Mode: {status['health']['mode']}")

# Get compiler configuration
config = controller.get_compiler_config()
print(f"Optimization level: {config['opt_level']}")
print(f"Parallel jobs: {config['parallel_jobs']}")

# Log compilation events
controller.log_compile_event('start', {'target': 'myproject'})
# ... compilation happens ...
controller.log_compile_event('end', {'target': 'myproject', 'success': True})
```

## Compiler Integration

The system provides concrete guidance for compiler behavior:

### FULL Mode (f ≥ 0.75)
```python
{
  'mode': 'FULL',
  'proof_threshold': 0.3,      # Low rigor, allow optimization
  'opt_level': 3,               # Maximum optimization
  'parallel_jobs': 8,           # Full parallelism
  'enable_aggressive_opts': True,
  'aggressive_inlining': True,
  'enable_lto': True
}
```

### DEGRADED Mode (0.40 ≤ f < 0.75)
```python
{
  'mode': 'DEGRADED',
  'proof_threshold': 0.6,       # Moderate rigor
  'opt_level': 2,                # Conservative optimization
  'parallel_jobs': 4,            # Reduced parallelism
  'enable_aggressive_opts': False,
  'aggressive_inlining': False,
  'enable_lto': False
}
```

### SAFE Mode (f < 0.40)
```python
{
  'mode': 'SAFE',
  'proof_threshold': 0.9,        # Maximum rigor
  'opt_level': 1,                 # Minimal optimization
  'parallel_jobs': 1,             # Single-threaded
  'enable_aggressive_opts': False,
  'enable_safety_checks': True
}
```

## Proof Gates

Proof gates read `proof_threshold` and adjust validation rigor:

```python
def validate_proof(proof, controller):
    config = controller.get_compiler_config()
    threshold = config['proof_threshold']
    
    if threshold > 0.8:
        # SAFE mode: maximum rigor
        return strict_validation(proof)
    elif threshold > 0.5:
        # DEGRADED mode: moderate rigor
        return standard_validation(proof)
    else:
        # FULL mode: accept with basic checks
        return fast_validation(proof)
```

## Logging

The system maintains comprehensive logs:

### Boot Logs
`logs/system_health/boot_YYYYMMDD_HHMMSS.json`:
```json
{
  "event": "boot",
  "timestamp": 1706198400.0,
  "baseline": {
    "cpu": 15.2,
    "load": [1.5, 1.3, 1.2],
    "memory": 45.3
  },
  "initial_health": {
    "f": 0.82,
    "mode": "FULL"
  }
}
```

### Tick Logs
`logs/system_health/ticks_YYYYMMDD.jsonl`:
```json
{"event": "tick", "tick": 10, "health": {"f": 0.78}, "compiler_config": {...}}
{"event": "tick", "tick": 20, "health": {"f": 0.75}, "compiler_config": {...}}
```

### Compile Logs
`logs/system_health/compile_YYYYMMDD.jsonl`:
```json
{"event": "start", "health": {"f": 0.82}, "details": {"target": "myproject"}}
{"event": "end", "health": {"f": 0.79}, "details": {"success": true}}
```

## What This Architecture Provides

### ✅ Solid Foundation
- F1 as a bounded product lemma
- TRIG6 as a system-health potentiometer
- RESMON → TRIG6 → compiler threshold pipeline
- Clean layering of math / code / heuristics

### ✅ Honest Claims
- NOT: "P(correct) oracle" or "cosmology law"
- IS: "System health score that tunes compiler behavior"
- NOT: "Universal truth about the world"
- IS: "Local, enforceable invariants about your OS"

### ✅ Testable & Measurable
- Real metrics from psutil
- Concrete thresholds and modes
- Logging for analysis over time
- Verifiable bounds via F1

### 📋 To Be Built
- Real integration with FlameLang/Rust pipeline
- Multiple machine baseline profiles
- Long-term trend analysis
- BCI/Neuralink-facing variant (future)

## Philosophy

This architecture embodies the shift from **grand metaphysics** to **local, enforceable invariants**:

> "F1 isn't 'the universe's law'; it's your OS's contract with itself: 'When my health falls, I narrow my blast radius.'"

The system is:
- **Honest**: Claims only what it can prove
- **Testable**: Every assertion is measurable
- **Practical**: Provides actionable compiler guidance
- **Modest**: F1 is just math about sequences, not cosmology

## Example: Complete Workflow

```python
from src.system_health import SystemHealthController
import time

# Boot sequence
controller = SystemHealthController()
controller.initialize()

# Main loop
while True:
    # Get current health
    status = controller.get_system_status()
    
    print(f"Health: {status['health']['f']:.3f}")
    print(f"Mode: {status['health']['mode']}")
    print(f"Contract: {status['contract']}")
    
    # Configure compiler
    config = controller.get_compiler_config()
    
    # Your compiler uses these settings
    if should_compile():
        controller.log_compile_event('start')
        compile_with_config(config)
        controller.log_compile_event('end', {'success': True})
    
    time.sleep(60)  # Check every minute
```

## References

- **RESMON**: Resource monitoring via psutil
- **TRIG6**: Health scoring potentiometer (f = R·(1-D)·(1-N)·eq)
- **F1**: Bounded product lemma (Γ ≤ 1)
- **Integration**: System health controller

---

**Built with 🔥 by Strategickhaos**

*"We walked into the tribunal with vibes and walked out with an architecture that can be punched, measured, and improved."*
