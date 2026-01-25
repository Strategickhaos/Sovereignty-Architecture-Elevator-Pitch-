# FlameLang Evolutionary Gate - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLAMELANG EVOLUTIONARY GATE                      │
│                   Darwinian Compiler Evolution                      │
└─────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │  Code Push   │
                              │  to main/PR  │
                              └──────┬───────┘
                                     │
                     ┌───────────────┼───────────────┐
                     │               │               │
            ┌────────▼────────┐ ┌───▼────────┐ ┌───▼──────────┐
            │   FlameBench    │ │   TRIG6    │ │  zyBooks     │
            │   Stress Test   │ │  Metrics   │ │  Lab Tests   │
            │                 │ │  Collector │ │              │
            └────────┬────────┘ └─────┬──────┘ └──────┬───────┘
                     │                │               │
                     ▼                ▼               ▼
            ┌─────────────────────────────────────────────┐
            │        stress_results.json                  │
            │  ┌──────────────────────────────────────┐   │
            │  │ p_success: 0.85                      │   │
            │  │ equivalence: 0.995                   │   │
            │  └──────────────────────────────────────┘   │
            └──────────────────┬──────────────────────────┘
                               │
            ┌──────────────────┼──────────────────────────┐
            │  logs/trig_layer.jsonl                      │
            │  ┌──────────────────────────────────────┐   │
            │  │ resonance: 0.75                      │   │
            │  │ drift: 0.05                          │   │
            │  │ noise_entropy: 0.08                  │   │
            │  │ invention_density: 0.65              │   │
            │  │ phase_coherence: 0.82                │   │
            │  └──────────────────────────────────────┘   │
            └──────────────────┬──────────────────────────┘
                               │
                ┌──────────────▼──────────────┐
                │   EVOLUTIONARY GATE         │
                │   flamelang_evo_gate.py     │
                │                             │
                │  Fitness Formula:           │
                │  f = r(1-d)(1-h)i·eq        │
                │      + ρp + γb              │
                │                             │
                │  Safety Checks:             │
                │  ✓ eq ≥ 0.99 (hard gate)    │
                │  ✓ f > f_champion           │
                └──────────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Decision Point    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
         ┌──────▼─────┐  ┌────▼──────┐  ┌────▼──────┐
         │   REJECT   │  │  ACCEPT   │  │  REJECT   │
         │  (exit 1)  │  │  (exit 0) │  │  (exit 1) │
         │            │  │           │  │           │
         │ eq < 0.99  │  │ f > f_ch  │  │ f ≤ f_ch  │
         │ Hard gate  │  │ New       │  │ No        │
         │ failure    │  │ champion! │  │ improve   │
         └──────┬─────┘  └─────┬─────┘  └─────┬─────┘
                │              │              │
                ▼              ▼              ▼
         ┌────────────┐  ┌────────────┐  ┌────────────┐
         │ Champion   │  │ Update     │  │ Champion   │
         │ unchanged  │  │ champion.  │  │ unchanged  │
         │            │  │ json       │  │            │
         │ Workflow   │  │            │  │ Workflow   │
         │ FAILS ❌   │  │ Commit     │  │ FAILS ❌   │
         │            │  │ codon      │  │            │
         │            │  │            │  │            │
         │            │  │ Workflow   │  │            │
         │            │  │ SUCCESS ✅ │  │            │
         └────────────┘  └────────────┘  └────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                     FITNESS CALCULATION DETAIL                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Core Fitness (correctness-gated):                                 │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  core = r × (1-d) × (1-h) × i × eq                        │     │
│  │                                                            │     │
│  │  Where:                                                    │     │
│  │  r = resonance        (swarm alignment)                    │     │
│  │  d = drift            (chaos penalty)                      │     │
│  │  h = noise_entropy    (signal corruption penalty)          │     │
│  │  i = invention        (novelty bonus)                      │     │
│  │  eq = equivalence     (correctness hard gate)              │     │
│  └───────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Bonus Terms (weighted):                                            │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  bonus = ρ × p + γ × b                                     │     │
│  │                                                            │     │
│  │  Where:                                                    │     │
│  │  p = phase_coherence  (synchronization)                    │     │
│  │  b = FlameBench p_success (performance)                    │     │
│  │  ρ = 0.2 (default phase weight, configurable)             │     │
│  │  γ = 0.3 (default bench weight, configurable)             │     │
│  └───────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Final Fitness:                                                     │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  f = core + bonus                                          │     │
│  │                                                            │     │
│  │  Champion Update Rule:                                     │     │
│  │  IF eq ≥ 0.99 AND f > f_champion THEN                     │     │
│  │      ACCEPT (new champion)                                 │     │
│  │  ELSE                                                      │     │
│  │      REJECT                                                │     │
│  └───────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                   CURRICULUM-DRIVEN EVOLUTION                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  zyBooks Lab                                                        │
│  Assignment                                                         │
│       │                                                             │
│       ▼                                                             │
│  sagco_lab_                                                         │
│  converter.py                                                       │
│       │                                                             │
│       ▼                                                             │
│  .flame.yaml                                                        │
│  specification                                                      │
│       │                                                             │
│       ▼                                                             │
│  FlameBench                                                         │
│  test atom                                                          │
│       │                                                             │
│       ▼                                                             │
│  Evolutionary                                                       │
│  Pressure                                                           │
│       │                                                             │
│       └──► Mutations must:                                          │
│           ├─ Not break this lab                                    │
│           ├─ Not break any previous lab                            │
│           ├─ Maintain eq ≥ 0.99                                    │
│           └─ Improve overall fitness                               │
│                                                                     │
│  Result: Every new lab you complete shrinks the space of           │
│  allowed mutations around "compiler that understands your          │
│  homework."                                                         │
│                                                                     │
│  This is LITERAL curriculum-driven compiler evolution.             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### Multi-Domain Fitness
The gate doesn't just look at performance or correctness - it evaluates holistic fitness across three domains:
1. **Swarm behavior** (TRIG6) - Is the compiler thinking coherently?
2. **Performance** (FlameBench) - Does it actually work well?
3. **Correctness** (equivalence) - Does it produce the right results?

### Safety Layers
1. **Hard Gate**: equivalence ≥ 0.99 (instant rejection below this)
2. **Improvement Requirement**: fitness > champion (no regression)
3. **Behavioral Clamps**: drift/noise penalties in TRIG6

### Evolutionary Pressure
Not random mutation - **curriculum-driven evolution**:
- Your academic work (zyBooks labs) becomes ground truth
- Every lab added constrains the mutation space
- Only improvements that "understand your homework" survive

## Data Flow

```
Code Change → Tests → Metrics Collection → Gate Evaluation → Champion Update
     ↓            ↓              ↓                ↓                  ↓
   GitHub      FlameBench    TRIG6         fitness calc      champion.json
              stress_results  trig_layer      f > f_ch         (commit)
```

## Integration Points

### Required Inputs
1. `stress_results.json` - FlameBench output
2. `logs/trig_layer.jsonl` - TRIG6 metrics

### Outputs
1. `champion.json` - Current best (auto-created/updated)
2. Exit code 0 (accept) or 1 (reject)
3. Detailed console output

### CI/CD Hook
```yaml
- Run FlameBench
- Run TRIG6 metrics
- Run evolution gate
  ↓
  Accept → commit champion → workflow succeeds
  Reject → no changes → workflow fails (expected)
```
