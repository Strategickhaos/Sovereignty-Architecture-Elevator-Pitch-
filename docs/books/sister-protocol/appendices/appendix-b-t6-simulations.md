# Appendix B: OmniCalc .t6 Failure Simulations

## Simulation Framework Documentation

This appendix provides comprehensive documentation for the OmniCalc .t6 simulation format used throughout "The Sister Protocol: Failures as Fuel."

---

## Overview

### What is .t6?

.t6 (TRIG6 Simulation Format) is a domain-specific language for:
- **Vectorizing failures:** Define (θ, R, D, N) states
- **Modeling progression:** How failures evolve over time
- **Testing mitigations:** Apply interventions, measure outcomes
- **Evolution cycles:** Run tournaments, select champions
- **Validation:** Compare theory vs. simulation vs. reality

### Why Simulation?

Testing mitigations in production is:
- **Expensive:** Real systems, real costs
- **Risky:** Failures can cause damage
- **Slow:** Must wait for results
- **Limited:** Can only test a few variants

Simulation allows:
- **Cheap:** CPU cycles, not dollars
- **Safe:** Failures are virtual
- **Fast:** Thousands of runs per hour
- **Comprehensive:** Test every variant

---

## .t6 File Structure

### Basic Template

```t6
# TRIG6 Simulation: [Vector ID] [Failure Name]
# Author: [Name]
# Date: [YYYY-MM-DD]

## Vector Initial State
vector [ID] {
    id: "[ID]"
    name: "[Failure Name]"
    component: "[Sister Protocol | NEURO-36 | Wait Chain | Bottlenecks]"
    category: "[Mission/Legal | Modeling/Research | Stack/Tech | Pillar/Algo]"
    
    # TRIG6 Parameters
    theta: [π/4 | π/2 | π | 3π/2]
    R: [0.0 to 1.0]
    D: [0.0 to 1.0]
    N: [0.0 to 1.0]
    
    # Derived
    tan_theta: tan([theta])
    danger: [true | false]
}

## Failure Scenario Definition
scenario [name] {
    description: "[What goes wrong]"
    
    env {
        # Environmental parameters
        [param1]: [value]
        [param2]: [value]
    }
    
    triggers {
        # Conditions that activate failure
        [trigger1]: [condition]
        [trigger2]: [condition]
    }
    
    phases {
        t0: { R: [value], D: [value], N: [value] }
        t1: { R: [value], D: [value], N: [value] }
        ...
    }
}

## Mitigation Strategy
mitigation [name] {
    description: "[How it fixes the problem]"
    
    algorithm {
        # Pseudocode or actual implementation
        [steps]
    }
    
    fitness(state) = {
        f = [formula]
        champion: f > [threshold] AND R > 0.5
    }
}

## Simulation Execution
simulation run {
    name: "[Descriptive name]"
    iterations: [count]
    time_steps: [count]
    
    scenario_a: [scenario] + [mitigation] {
        [results over time]
        outcome: [CHAMPION | STABLE | FAILURE]
    }
    
    scenario_b: [scenario] + no_mitigation {
        [results over time]
        outcome: [usually FAILURE]
    }
}

## Results Analysis
results {
    findings { ... }
    R_trajectory_with_mitigation: [pattern]
    R_trajectory_no_mitigation: [pattern]
    evolution { ... }
}

## Metadata
metadata {
    format: "OmniCalc .t6 v2.1"
    checksum: "sha256:[hash]"
    gpg_signature: "[signature]"
}
```

---

## Complete Example: BN-01 (Compute Starvation)

See `simulations/BN-01-compute-starvation.t6` for a full working example demonstrating:

- Vector definition with all TRIG6 parameters
- Failure scenario with environmental parameters and phase progression
- Mitigation strategy (gray scaling) with algorithm and fitness function
- Simulation runs comparing mitigation vs. no mitigation
- Results analysis with trajectory visualization
- Theorem validation (Theorems 1-3 confirmed)
- Deployment recommendations

**Key Insights from BN-01:**
- R_initial = 0.6 (borderline stable)
- Without mitigation: Decline to R=0.1, system failure at t4
- With gray scaling: Increase to R=0.75, champion status
- Fitness improvement: 32,000% over no mitigation
- Cost: 20% additional compute buffer, saves 100% downtime

---

## Running Simulations

### Command-Line Interface

**Basic run:**
```bash
t6sim run [filename].t6
```

**With options:**
```bash
t6sim run [filename].t6 \
  --iterations=10000 \
  --seed=42 \
  --output=results.json \
  --verbose
```

**Batch processing:**
```bash
t6sim batch simulations/*.t6 --parallel=8
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--iterations` | Monte Carlo runs | 1000 |
| `--seed` | Random seed for reproducibility | Random |
| `--output` | Results file (JSON/CSV) | stdout |
| `--verbose` | Detailed logging | false |
| `--parallel` | CPU cores for parallel sims | 1 |
| `--validate` | Run theorem validation | true |
| `--plot` | Generate trajectory plots | false |

### Output Format

**JSON:**
```json
{
  "vector_id": "BN-01",
  "simulations": [
    {
      "name": "with_mitigation",
      "outcome": "CHAMPION",
      "R_final": 0.75,
      "fitness": 0.64,
      "time_to_stable": 6
    },
    {
      "name": "no_mitigation",
      "outcome": "FAILURE",
      "R_final": 0.1,
      "time_to_failure": 4
    }
  ],
  "effectiveness": 6.5,
  "theorems_validated": 3
}
```

---

## Creating New Simulations

### Step 1: Define the Vector

Start with TRIG6 parameters from Appendix A:

```t6
vector SP-05 {
    id: "SP-05"
    name: "Charity misroute"
    component: "Sister Protocol"
    
    theta: π/2
    R: 0.5
    D: 0.5
    N: 0.4
    danger: true
}
```

### Step 2: Model the Failure Scenario

How does this failure progress without intervention?

```t6
scenario charity_misroute {
    description: "Charitable funds routed to wrong recipients"
    
    env {
        total_funds: 1000000
        recipient_count: 50
        verification_rate: 0.85
    }
    
    triggers {
        misroute_event: rand() > verification_rate
        cascade: misrouted_count > 5
    }
    
    phases {
        t0: { R: 0.5, D: 0.5, N: 0.4 }  # Baseline
        t1: { R: 0.45, D: 0.55, N: 0.5 }  # First misroutes
        t2: { R: 0.38, D: 0.62, N: 0.6 }  # Pattern emerges
        t3: { R: 0.25, D: 0.75, N: 0.7 }  # Crisis
    }
}
```

### Step 3: Design Mitigation

From Appendix A, SP-05 mitigation is "4/5 vote R mean":

```t6
mitigation voting_verification {
    description: "Multi-stakeholder approval for fund routing"
    
    algorithm {
        for each routing_decision:
            collect 5 stakeholder votes
            compute R_mean = average(R_vote_1...R_vote_5)
            
            if R_mean > 0.5:
                approve_routing()
            else:
                reject_and_review()
    }
    
    fitness(state) = {
        f = R * approval_rate * (1 - delay_penalty)
        champion: f > 0.7 AND R > 0.5
    }
}
```

### Step 4: Run Simulation

```t6
simulation run {
    iterations: 5000
    
    scenario_a: charity_misroute + voting_verification {
        t0: { R: 0.5 }
        t1: { R: 0.58 }  # Improvement!
        t2: { R: 0.65 }
        t3: { R: 0.72 }  # Champion
        
        outcome: CHAMPION
    }
    
    scenario_b: charity_misroute + no_mitigation {
        [same as phases above]
        outcome: FAILURE
    }
}
```

### Step 5: Analyze Results

```t6
results {
    findings {
        1: "Voting increases R by 44% (0.5 → 0.72)"
        2: "95% of misroutes prevented"
        3: "Delay increased by 12 hours (acceptable)"
    }
    
    champion: voting_verification
    fitness: 0.68
}
```

---

## Library of Simulation Patterns

### Pattern 1: Resource Starvation

**Used in:** BN-01, BN-02, BN-03  
**Structure:**
- Environment: baseline, growth_rate, elasticity
- Triggers: demand > supply
- Mitigation: Scaling, prioritization, graceful degradation

**Template:** `templates/resource-starvation.t6`

### Pattern 2: Data Quality Degradation

**Used in:** N36-01, BN-06  
**Structure:**
- Environment: contamination_rate, sources, validation
- Triggers: quality < threshold
- Mitigation: Provenance tracking, filtering, verification

**Template:** `templates/data-quality.t6`

### Pattern 3: Drift Amplification

**Used in:** SP-03, N36-06  
**Structure:**
- Environment: baseline_state, drift_rate, feedback
- Triggers: deviation > threshold
- Mitigation: Bounds enforcement, realignment, inverse gates

**Template:** `templates/drift-amplification.t6`

### Pattern 4: Phase Transition Crisis

**Used in:** SP-01, WC-02, multiple vectors at θ=π/2  
**Structure:**
- Environment: lifecycle_age, |tan θ|
- Triggers: |tan θ| > 10
- Mitigation: Tan mutes, caution protocols, phase acceleration

**Template:** `templates/phase-transition.t6`

### Pattern 5: Cascade Failures

**Used in:** SP-02, WC-07, multiple low-R vectors  
**Structure:**
- Environment: interconnections, R_individual
- Triggers: R_any < 0.3
- Mitigation: Isolation, redundancy, dead man triggers

**Template:** `templates/cascade-failure.t6`

---

## Advanced Features

### Multi-Agent Simulations

Model interactions between multiple vectors:

```t6
multi_agent {
    agents: [SP-01, SP-02, SP-03]
    
    coupling {
        SP-01.R affects SP-02.R: coupling_strength = 0.4
        SP-02.failure triggers SP-03.cascade
    }
    
    run {
        measure system_R = mean(agent.R for agent in agents)
        outcome = STABLE if system_R > 0.5 else FAILURE
    }
}
```

### Evolutionary Tournaments

Compete multiple mitigations:

```t6
tournament {
    candidates: [mitigation_A, mitigation_B, mitigation_C]
    generations: 20
    
    evolution {
        gen_0: all candidates compete
        gen_N: top 50% survive, generate variants
        gen_N+1: variants compete
    }
    
    champion: argmax(fitness) after convergence
}
```

### Sensitivity Analysis

Test robustness to parameter changes:

```t6
sensitivity {
    vary: [R, D, N] 
    range: [-20%, +20%]
    samples: 100
    
    measure: fitness_variance
    robust: variance < 0.1
}
```

---

## Validation and Verification

### Theorem Validation

Every simulation should validate relevant theorems:

```t6
theorems {
    theorem_1 {
        statement: "System stable iff R > 0.5"
        test: all(R > 0.5 implies stable)
        result: PASS | FAIL
    }
    
    theorem_2 {
        statement: "D + R ≈ 1.0"
        test: abs(D + R - 1.0) < 0.1
        result: PASS | FAIL
    }
}
```

### Real-World Calibration

Compare simulation to production:

```t6
calibration {
    simulation_R: 0.72
    production_R: 0.68
    error: 5.6%
    
    acceptable: error < 10%
    status: CALIBRATED
}
```

---

## Sample Simulations Included

This book includes .t6 files for key vectors:

### Sister Protocol
- SP-01: 7% bypass → codon locks
- SP-02: Succession failure → dead man triggers
- SP-03: Profit drift → inverse D gates

### NEURO-36 Genome
- N36-01: EEG poison → provenance R >0.5
- N36-02: Wave mismatch → tan mute
- N36-03: Codon overflow → eq ≥0.99

### Wait Chain Logic
- WC-02: FlameLang break → physics eq=1.0
- WC-06: Darwinian stall → +0.02 gradient
- WC-09: Outer leak → 7% eq gate

### 100 Bottlenecks
- BN-01: Compute starvation → gray scaling (detailed example)
- BN-06: Data poison → provenance tan danger
- BN-09: Tool failure → chain > champion

**Full set:** 36 simulations, one per vector, available at:
`docs/books/sister-protocol/simulations/[ID]-[name].t6`

---

## Future Enhancements

### Planned Features

1. **GPU Acceleration:** 100x faster Monte Carlo
2. **Real-Time Simulation:** Live dashboard of production vectors
3. **ML Integration:** Train mitigations via reinforcement learning
4. **Collaborative Evolution:** Share mitigations across organizations
5. **Formal Verification:** Prove mitigation correctness mathematically

### Community Contributions

We welcome:
- New simulation patterns
- Improved algorithms
- Cross-domain validations
- Bug reports and fixes
- Documentation improvements

**Contribute at:** `github.com/strategickhaos/t6-simulations`

---

## References

- OmniCalc specification: `docs/omnicalc/spec.md`
- TRIG6 theory: Chapter 5
- Darwinian evolution: Chapter 6
- Vector catalog: Appendix A
- Example simulations: `simulations/` directory

---

## License

.t6 simulation format and associated tools:
- **Format:** CC0 (public domain)
- **Simulations:** MIT + attribution
- **Commercial use:** Allowed with mission alignment clause

---

*"Simulate failures before they manifest. Evolve solutions before you need them. This is antifragility by design."*

**[End of Appendix B]**
