# Contradiction Engine v1.1

## Purpose
Adversarial invariant enforcement + bottleneck assassination for AI/ML systems.

**Philosophy:** Trust nothing until it survives crossfire—and actively try to kill it.

## Features

### 1. **Adversarial Invariant Checking**
- **Bounds**: Validates input values stay within specified ranges
- **Symmetry**: Checks mathematical identities (e.g., sin²θ + cos²θ = 1)
- **Stability**: Ensures outputs are finite and well-behaved
- **Termination**: Enforces timeout and step limits

### 2. **Bottleneck Assassination Suite**
Pluggable "attack vectors" that simulate common ML/AI bottlenecks:
- **#1 Unversioned Data**: Detects mutations without lineage tracking
- **#2 State Leakage**: Checks for non-deterministic behavior from global state
- **#3-12**: Extensible framework for additional bottlenecks (schema drift, gradient explosion, catastrophic forgetting, etc.)

### 3. **Mutation Pipeline (Crossfire Testing)**
Applies random transformations to test robustness:
- **Scale**: Multiply outputs by random factors
- **Noise**: Add Gaussian noise to outputs
- **Quantize**: Round to limited precision

### 4. **Self-Referential Testing**
Meta-validation mode where the engine tests itself for contradictions in its own logic.

### 5. **Pluggable Mappings**
- **basic/trig**: Standard trigonometric functions (sin, cos, tan)
- **trig6_geom**: 3D TRIG6 geometry with manifold constraints (x² + y² + z² ≈ 1)
- Extensible: Add your own mappings via `load_mapping()`

## Installation

No dependencies beyond Python 3.7+ standard library.

```bash
chmod +x contradiction_engine.py
```

## Usage

### Basic Run
```bash
python3 contradiction_engine.py --mapping basic --cases 250
```

### TRIG6 Geometry with High Precision
```bash
python3 contradiction_engine.py --mapping trig6_geom --cases 2000 --eps 1e-9
```

### Enable Bottleneck Attacks
```bash
python3 contradiction_engine.py --mapping trig6_geom --bottlenecks --cases 500
```

### Self-Test Mode (Meta-Validation)
```bash
python3 contradiction_engine.py --self-test
```

### JSON Output
```bash
python3 contradiction_engine.py --mapping basic --json --cases 100 > report.json
```

### Custom Bounds and Tolerance
```bash
python3 contradiction_engine.py \
  --mapping basic \
  --cases 1000 \
  --theta-min=-100 \
  --theta-max=100 \
  --eps 1e-12 \
  --seed 42
```

## Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--mapping` | string | `basic` | Mapping to test: `basic`, `trig`, `trig6_geom` |
| `--cases` | int | `250` | Number of test cases to generate |
| `--theta-min` | float | `-2π` | Minimum theta bound |
| `--theta-max` | float | `2π` | Maximum theta bound |
| `--eps` | float | `1e-9` | Tolerance for invariant checks |
| `--seed` | int | `137` | Random seed for reproducibility |
| `--timeout` | float | `2.0` | Timeout in seconds |
| `--step-limit` | int | `5000` | Maximum number of steps |
| `--json` | flag | - | Emit JSON report only |
| `--bottlenecks` | flag | - | Enable bottleneck attack checks |
| `--self-test` | flag | - | Run meta-validation self-test |

## Output

### Success (PASS)
```
[PASS] Contradiction Engine: 250 cases, 3 checks, seed=137, t=0.015s
```

### Failure (FAIL)
```
[FAIL] Check 'stability' found a contradiction.
  theta = -4.8059   meta = {'kind': 'fuzz', 'mutation': {...}}
  details = {
    "reason": "trig6 geometry violated",
    "theta": -4.805870541247071,
    "manifold_val": 1.00863745338146,
    "eps": 1e-09,
    "mutation_trace": {...}
  }
  seed=137 runtime=0.000813s
```

## Extending the Engine

### Adding a New Mapping

```python
def load_mapping(name: str) -> Dict[str, Callable[[float], float]]:
    # ... existing mappings ...
    
    if name == "freq_to_midi":
        return {
            "midi": lambda freq: 69 + 12 * math.log2(freq / 440.0),
        }
```

### Adding a New Bottleneck Check

```python
def assert_gradient_explosion(case: TestCase, mapping: Dict[str, Callable[[float], float]]) -> Optional[Dict[str, Any]]:
    # Inject large gradient via scaled theta
    scaled_theta = case.theta * 1e6
    for k, fn in mapping.items():
        try:
            v = fn(scaled_theta)
            if not math.isfinite(v):
                return {"reason": "gradient explosion detected", "mapping": k, "theta": scaled_theta}
        except:
            return {"reason": "gradient explosion caused exception", "mapping": k}
    return None

# Add to bottleneck_checks list
bottleneck_checks = [
    # ... existing checks ...
    ("gradient_explosion", assert_gradient_explosion),
]
```

### Adding a Custom Invariant

```python
def assert_my_invariant(case: TestCase, eps: float) -> Optional[Dict[str, Any]]:
    # Your invariant logic here
    if some_condition_violated:
        return {"reason": "my invariant violated", "theta": case.theta}
    return None

# In run_engine(), add to checks list
checks = [
    # ... existing checks ...
    ("my_invariant", lambda c: assert_my_invariant(c, eps)),
]
```

## Testing

Run the test suite:
```bash
python3 test_contradiction_engine.py
```

## Philosophy

The Contradiction Engine embodies three key principles:

1. **Adversarial Testing**: Don't just test happy paths—actively try to break the system
2. **Invariant-First**: Define what should *always* be true, then hunt for violations
3. **Chaos Monkey for Truth**: Inject mutations, noise, and perturbations to stress-test robustness

This approach is inspired by:
- Property-based testing (QuickCheck, Hypothesis)
- Chaos engineering (Netflix's Chaos Monkey)
- Formal verification and proof assistants
- Adversarial machine learning

## Next Steps

- Wire in the remaining 21 bottlenecks (#13-33)
- Add freq→MIDI mapping for audio applications
- Integrate with CI/CD for continuous invariant validation
- Add distributed testing for large-scale systems
- Create visualization dashboards for failure analysis

## License

See repository LICENSE file.
