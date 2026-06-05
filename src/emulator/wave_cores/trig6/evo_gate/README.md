# FlameLang Evolutionary Gate

Darwinian compiler evolution system for SAGCO/FlameLang.

## Quick Start

```bash
# Evaluate a candidate mutation
python flamelang_evo_gate.py --candidate main --champion ../../../../champion.json

# With custom weights
python flamelang_evo_gate.py \
  --candidate $COMMIT_SHA \
  --champion ../../../../champion.json \
  --rho 0.25 \
  --gamma 0.35
```

## What This Does

Evaluates compiler mutations using a multi-domain fitness function that combines:

1. **TRIG6 swarm metrics** (resonance, drift, noise, invention, phase coherence)
2. **FlameBench performance** (p_success across test atoms)  
3. **Behavioral equivalence** (correctness on zyBooks labs)

## Fitness Formula

```
f = r(1-d)(1-h)i × eq + ρp + γb
```

See `docs/EVOLUTIONARY_GATE.md` for full details.

## Exit Codes

- `0` = Candidate ACCEPTED (new champion)
- `1` = Candidate REJECTED (failed hard gate or no improvement)

## Required Files

- `logs/trig_layer.jsonl` - TRIG6 metrics (auto-created with defaults if missing)
- `stress_results.json` - FlameBench results (auto-created with defaults if missing)
- `champion.json` - Current best (auto-created on first success)

## Example Output

```
============================================================
🔥 FlameLang Evolutionary Gate - Evaluating Candidate
============================================================

Candidate: abc123

📊 Loading TRIG6 metrics...
   Resonance: 0.750
   ...

✅ ACCEPTED - New champion! (Δf=+0.0343)
```

## Documentation

Full documentation: `/docs/EVOLUTIONARY_GATE.md`
