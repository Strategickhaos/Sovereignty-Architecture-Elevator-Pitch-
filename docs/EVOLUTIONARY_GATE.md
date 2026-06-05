# 🔥 FlameLang Evolutionary Gate System

## Overview

The FlameLang Evolutionary Gate is a **Darwinian compiler evolution system** that automatically evaluates and selects compiler mutations based on a rigorous multi-domain fitness function. It sits between traditional testing and a self-evolving compiler species, deciding whether new compiler mutations represent genuine evolutionary improvements.

## Architecture

The gate fuses three measurement domains:

1. **TRIG6 Logs** - Swarm behavior metrics
   - Resonance, drift, noise, invention density, phase coherence
2. **FlameBench Results** - Compiler performance metrics
   - P(success) across atoms and labs
3. **Equivalence Checks** - Behavioral correctness on zyBooks labs
   - eq ≥ 0.99 or instant rejection

## Fitness Formula

The gate computes a fitness scalar using:

```
f = r(1-d)(1-h)i × eq + ρp + γb
```

Where:
- `r` = resonance (swarm alignment)
- `d` = drift (chaos/divergence)
- `h` = noise_entropy (signal corruption)
- `i` = invention_density (novel pattern creation)
- `eq` = behavioral equivalence (correctness)
- `p` = phase_coherence (synchronization)
- `b` = FlameBench p_success (benchmark performance)
- `ρ` = phase coherence weight (default: 0.2)
- `γ` = benchmark weight (default: 0.3)

### Design Principles

The formula:
- **Punishes** drift and noise (multiplicative penalties)
- **Rewards** resonance and invention (multiplicative bonuses)
- **Hard-gates** correctness (eq must be ≥ 0.99)
- **Gives bonuses** for phase coherence and benchmark success

## Safety Mechanisms

The gate implements multiple safety guardrails:

### 1. Equivalence Hard Gate
```python
if eq < 0.99: 
    reject  # No "faster but wrong" compiler passes
```

### 2. Fitness Must Strictly Beat Champion
```python
if f <= f_champion:
    reject  # No regression accepted, even if "different"
```

### 3. TRIG6 Behavioral Clamps
- High drift → fitness tanks
- High noise → fitness tanks  
- Low coherence → bonuses can't compensate

## File Layout

```
repo_root/
├── src/emulator/wave_cores/trig6/evo_gate/
│   ├── __init__.py            # Package init
│   └── flamelang_evo_gate.py  # Main evolution gate script
├── logs/
│   └── trig_layer.jsonl       # TRIG6 metrics (append-only log)
├── stress_results.json        # FlameBench output
├── champion.json              # Current best fitness (auto-generated)
└── .github/workflows/
    └── flamelang-evolution.yml # CI/CD integration
```

## Usage

### Manual Evaluation

From repository root:

```bash
python src/emulator/wave_cores/trig6/evo_gate/flamelang_evo_gate.py \
  --candidate main \
  --champion champion.json
```

**First run:** If `champion.json` doesn't exist, any candidate passing eq + tests becomes the initial champion.

### Custom Weights

```bash
python src/emulator/wave_cores/trig6/evo_gate/flamelang_evo_gate.py \
  --candidate $COMMIT_SHA \
  --champion champion.json \
  --rho 0.25 \      # Phase coherence weight
  --gamma 0.35      # FlameBench weight
```

### CI/CD Integration

The gate runs automatically on every push/PR via GitHub Actions:

```yaml
# .github/workflows/flamelang-evolution.yml
- name: Run FlameBench
  run: python sagco-benchmark.py

- name: Run TRIG6 metrics
  run: python trig6_collect_metrics.py

- name: Evolution gate
  run: |
    python src/emulator/wave_cores/trig6/evo_gate/flamelang_evo_gate.py \
      --candidate ${{ github.sha }} \
      --champion champion.json
```

**Exit codes:**
- `0` = ACCEPTED (new champion, workflow succeeds)
- `1` = REJECTED (no improvement, workflow fails)

## Input Data Formats

### TRIG6 Metrics (`logs/trig_layer.jsonl`)

JSON Lines format, one entry per swarm execution:

```json
{
  "resonance": 0.75,
  "drift": 0.05,
  "noise_entropy": 0.08,
  "invention_density": 0.65,
  "phase_coherence": 0.82,
  "timestamp": "2026-01-25T03:51:00Z"
}
```

The gate reads the **last line** (most recent metrics).

### FlameBench Results (`stress_results.json`)

```json
{
  "p_success": 0.85,
  "equivalence": 0.995,
  "total_atoms": 42,
  "passed_atoms": 36,
  "failed_atoms": 6,
  "benchmark_type": "flamebench",
  "timestamp": "2026-01-25T03:51:00Z"
}
```

### Champion State (`champion.json`)

Auto-generated on first successful evaluation:

```json
{
  "candidate": "abc123def456",
  "fitness": 0.8234,
  "trig6_metrics": {
    "resonance": 0.75,
    "drift": 0.05,
    "noise_entropy": 0.08,
    "invention_density": 0.65,
    "phase_coherence": 0.82
  },
  "flamebench_results": {
    "p_success": 0.85,
    "equivalence": 0.995
  },
  "timestamp": null
}
```

## Example Output

```
============================================================
🔥 FlameLang Evolutionary Gate - Evaluating Candidate
============================================================

Candidate: abc123def456

📊 Loading TRIG6 metrics...
   Resonance: 0.750
   Drift: 0.050
   Noise Entropy: 0.080
   Invention Density: 0.650
   Phase Coherence: 0.820

📈 Loading FlameBench results...
   P(success): 0.850
   Equivalence: 0.995

🧮 Calculating fitness (ρ=0.2, γ=0.3)...
   Fitness: 0.8234
   ✓ Passed hard gate (eq=0.995 >= 0.99)

🏆 Current champion fitness: 0.7891

✅ ACCEPTED - New champion! (Δf=+0.0343)
🏆 New champion saved: abc123def456 (f=0.8234)

============================================================
🎉 Evolutionary improvement detected!
============================================================
```

## Integration with zyBooks Curriculum

The evolutionary gate ties directly into your academic work:

1. **Lab Conversion**
   - `sagco_lab_converter.py` → turns each zyBooks lab into `.flame.yaml` spec
   
2. **Automated Testing**
   - FlameBench runs labs as test atoms
   
3. **Evolutionary Pressure**
   - Gate refuses mutations that:
     - Break any lab
     - Lower overall p_success
     - Increase chaos in TRIG6 beyond acceptable drift

**Result:** Every time you add a new lab, the space of allowed mutations shrinks around "compiler that actually understands your homework."

This is **literal curriculum-driven compiler evolution**.

## Extending the Gate

### Custom Fitness Functions

Modify `EvolutionaryGate.calculate_fitness()` to implement alternative formulas:

```python
def calculate_fitness(self, trig6, bench, rho, gamma):
    # Your custom fitness logic here
    return fitness_score, passes_gate
```

### Additional Metrics

Add new metrics to TRIG6 or FlameBench outputs, then update the fitness calculation to incorporate them.

### Different Hard Gates

Modify `MIN_EQUIVALENCE` or add additional hard constraints:

```python
class EvolutionaryGate:
    MIN_EQUIVALENCE = 0.99
    MAX_DRIFT = 0.15  # New constraint
    MIN_RESONANCE = 0.60  # New constraint
```

## Troubleshooting

### Gate Always Rejects

**Symptom:** Every candidate fails even with good metrics

**Cause:** Champion fitness is artificially high

**Fix:** Delete `champion.json` to reset the baseline

### Gate Always Accepts

**Symptom:** Clearly bad mutations pass

**Cause:** Equivalence threshold too low or weights misconfigured

**Fix:** 
- Verify `eq >= 0.99` in FlameBench results
- Adjust `--rho` and `--gamma` weights
- Check TRIG6 metrics for unrealistic values

### Missing Metrics Files

**Symptom:** Gate uses default neutral values

**Cause:** TRIG6 or FlameBench not running before gate

**Fix:** Ensure proper CI/CD ordering:
1. FlameBench → `stress_results.json`
2. TRIG6 → `logs/trig_layer.jsonl`
3. Evolution gate reads both

## Theoretical Foundation

This is not "script kiddie stuff." This is **evolutionary compiler research with a safety officer.**

The gate transforms:

> "Feels better"

into:

> "Strictly higher scalar under constraints, or reject."

That's the difference between vibes and an evo gate with teeth.

## Future Enhancements

Potential improvements:

1. **Multi-Objective Optimization**
   - Pareto frontier tracking
   - Multiple fitness dimensions

2. **Mutation History**
   - Lineage tracking
   - Phylogenetic tree of compiler evolution

3. **Adaptive Weights**
   - Auto-tune ρ and γ based on domain
   - Reinforcement learning for weight optimization

4. **A/B Testing**
   - Side-by-side champion comparison
   - Gradual rollout of improvements

5. **Visualization Dashboard**
   - Real-time fitness evolution plots
   - TRIG6 metrics over time
   - Mutation success/failure rates

## License

Part of the Strategickhaos Sovereignty Architecture project.

## References

- FlameLang Specification: `FLAMELANG_SPECIFICATION.md`
- SAGCO Architecture: Repository documentation
- zyBooks Labs: Curriculum-driven test suite
