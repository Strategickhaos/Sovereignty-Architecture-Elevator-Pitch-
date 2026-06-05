# TRIG6 Failure Simulations

This directory contains `.t6` simulation files for modeling and evolving mitigations for the 36 documented failure modes.

## What is a .t6 File?

`.t6` files use the TRIG6 simulation language to:
- Define failure vectors (θ, R, D, N)
- Specify mitigation strategies
- Run Darwinian evolution simulations
- Calculate fitness: f = r(1-d)(1-n)·eq
- Output evolved solutions

## Running Simulations

```bash
# Install OmniCalc TRIG6 engine (hypothetical)
pip install omnicalc-trig6

# Run individual simulation
omnicalc run SP-01-bypass.t6

# Visualize evolution trajectory
omnicalc run SP-01-bypass.t6 --visualize --output trajectory.png

# Batch run all simulations
omnicalc batch run *.t6 --parallel 8

# Export results to JSON
omnicalc run SP-01-bypass.t6 --format json > results.json
```

## Simulation Files

### Sister Protocol (SP-01 to SP-09)
- `SP-01-bypass.t6` - 7% legal bypass failure
- `SP-02-succession.t6` - Succession planning failure
- `SP-03-profit-drift.t6` - Profit incentive corruption
- `SP-04-gpg-forgery.t6` - Cryptographic signature spoofing
- `SP-05-charity-misroute.t6` - Charitable fund misallocation
- `SP-06-entity-dissolution.t6` - Legal entity termination risk
- `SP-07-promise-dilution.t6` - Mission dilution over time
- `SP-08-kpi-misalignment.t6` - Wrong metrics driving wrong outcomes
- `SP-09-witness-corruption.t6` - Human witness unreliability

### NEURO-36 Genome (N36-01 to N36-09)
- `N36-01-eeg-poison.t6` - EEG data corruption
- `N36-02-wave-mismatch.t6` - Theoretical vs empirical divergence
- `N36-03-codon-overflow.t6` - Genetic encoding overflow
- `N36-04-resonance-underestimate.t6` - Stability underestimation
- `N36-05-category-misfit.t6` - Disease categorization failure
- `N36-06-hypothesis-divergence.t6` - Research hypothesis drift
- `N36-07-fitness-false-positive.t6` - Darwinian optimization errors
- `N36-08-study-gap.t6` - Research coverage gaps
- `N36-09-kpi-mismeasure.t6` - Medical KPI inadequacy

### Wait Chain Logic (WC-01 to WC-09)
- `WC-01-trig-api-diverge.t6` - Math library inconsistencies
- `WC-02-flamelang-break.t6` - Language semantics divergence
- `WC-03-dna-corruption.t6` - Configuration corruption
- `WC-04-sagco-halt.t6` - Kernel initialization failure
- `WC-05-hydra-config-error.t6` - Multi-head configuration conflict
- `WC-06-darwinian-stall.t6` - Evolutionary algorithm stall
- `WC-07-mesh-lag.t6` - Distributed synchronization lag
- `WC-08-multi-ai-bias.t6` - AI bias amplification
- `WC-09-outer-leak.t6` - Control loop information leak

### 100 Bottlenecks (BN-01 to BN-09)
- `BN-01-compute-starvation.t6` - Insufficient compute resources
- `BN-02-power-denial.t6` - Power access denial
- `BN-03-memory-shortage.t6` - RAM exhaustion
- `BN-04-scaling-break.t6` - Scale-dependent failure
- `BN-05-alignment-explosion.t6` - AI alignment cost explosion
- `BN-06-data-poison.t6` - Training data poisoning
- `BN-07-latency-spike.t6` - Tail latency failures
- `BN-08-context-overflow.t6` - LLM context collapse
- `BN-09-tool-failure.t6` - External tool dependency failure

## TRIG6 Framework Reference

### Vector Components
- **θ (theta)**: Phase angle - where in failure cycle (0 to 2π)
- **R**: Resonance - system stability (0 to 1)
- **D**: Drift - mission deviation (0 to 1)
- **N**: Noise - uncertainty/chaos (0 to 1)

### Danger Criterion
**tan θ > 10** indicates catastrophic instability

### Fitness Function
**f = r(1-d)(1-n)·eq**

Where:
- r = resonance (higher is better)
- d = drift (lower is better)
- n = noise (lower is better)
- eq = mission equivalence (higher is better)

Target: f ≥ 0.7 for production-ready mitigation

### Evolution Gates
- **R > 0.5 Gate**: Resonance threshold
- **eq ≥ 0.99 Gate**: Mission alignment lock
- **D < 0.2 Gate**: Drift boundary
- **N = 0 Gate**: Zero noise requirement for critical paths

## Example Output

```
╔══════════════════════════════════════════════════════════╗
║  SP-01: 7% Bypass Failure Simulation                    ║
║  Sister Protocol - Legal Gap Exploitation              ║
╚══════════════════════════════════════════════════════════╝

INITIAL STATE:
  Phase (θ):      1.5708 (90°)
  Resonance (R):  0.4
  Drift (D):      0.6
  Noise (N):      0.3
  Danger:         TRUE
  tan(θ):         ∞

RUNNING DARWINIAN EVOLUTION...

Gen 1: New champion 'eq_codon_lock_v1.1' fitness=0.52
Gen 5: New champion 'hybrid_5_8' fitness=0.68
Gen 12: New champion 'eq_codon_lock_v1.8' fitness=0.79
Target fitness reached at generation 12

EVOLVED MITIGATION:
  Name:           Equivalence Codon Lock v1.8
  Fitness:        0.79

FINAL STATE:
  Phase (θ):      0.4712 (27°)
  Resonance (R):  0.75
  Drift (D):      0.15
  Noise (N):      0.15
  Danger:         FALSE
  tan(θ):         0.51

IMPROVEMENTS:
  θ reduced:      70%
  R increased:    87.5%
  D reduced:      75%
  N reduced:      50%

✓ MISSION SAVED: Danger eliminated

=== Simulation Complete ===
```

## Contributing Simulations

To add a new failure simulation:

1. Create a new `.t6` file following naming convention
2. Define the failure vector with accurate θ, R, D, N values
3. Specify at least one mitigation strategy
4. Include evolution parameters (generations, mutation rate, etc.)
5. Add to appropriate category above
6. Test with `omnicalc verify <filename>.t6`

## License

These simulations are part of "The Sister Protocol—Failures as Fuel" book.  
Licensed under CC BY-SA 4.0 with mission alignment requirements (eq ≥ 0.99).

See [../book.md](../book.md) for full context and theoretical framework.
