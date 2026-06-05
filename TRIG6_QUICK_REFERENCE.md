# Quick Reference: TRIG6 Failure Framework

This is a condensed reference guide for the TRIG6 failure vectorization framework detailed in [book.md](book.md).

## Core Concepts

### TRIG6 Vector Components

| Component | Name | Range | Meaning |
|-----------|------|-------|---------|
| **θ** (theta) | Phase Angle | 0 to 2π | Position in failure cycle |
| **R** | Resonance | 0 to 1 | System stability/consistency |
| **D** | Drift | 0 to 1 | Distance from mission |
| **N** | Noise | 0 to 1 | Uncertainty/chaos level |

### Phase Angle (θ) Interpretation

- **θ = 0**: Aligned, healthy state
- **θ = π/4 (45°)**: Early warning signs
- **θ = π/2 (90°)**: CATASTROPHIC - orthogonal to mission
- **θ = π (180°)**: Complete reversal
- **θ = 3π/2 (270°)**: Terminal failure

### Danger Criterion

**tan θ > 10** → System in unstable territory

When θ approaches π/2, tan θ → ∞, indicating imminent catastrophic failure.

### Fitness Function

**f = r(1-d)(1-n)·eq**

Where:
- **r** = resonance (higher is better)
- **d** = drift (lower is better)  
- **n** = noise (lower is better)
- **eq** = mission equivalence (higher is better)

**Target**: f ≥ 0.7 for production deployment

**Perfect Score**: f = 1.0 (r=1, d=0, n=0, eq=1)

## The 36 Failure Modes

### Sister Protocol (Mission/Legal) - SP-01 to SP-09

| ID | Failure | θ | R | D | N | Danger | Key Mitigation |
|----|---------|---|---|---|---|--------|----------------|
| SP-01 | 7% bypass | π/2 | 0.4 | 0.6 | 0.3 | ✓ | eq ≥0.99 codon lock |
| SP-02 | Succession fail | π | 0.2 | 0.8 | 0.5 | ✓ | Dead man R <0.5 trigger |
| SP-03 | Profit drift | 3π/2 | 0.1 | 0.9 | 0.7 | ✓ | Inverse D <0.2 gate |
| SP-04 | GPG forgery | π/4 | 0.8 | 0.2 | 0.1 | ✗ | Behavioral N=0 fingerprints |
| SP-05 | Charity misroute | π/2 | 0.5 | 0.5 | 0.4 | ✓ | 4/5 vote R mean |
| SP-06 | Entity dissolution | π | 0.3 | 0.7 | 0.6 | ✓ | PBC eq=1.0 |
| SP-07 | Promise dilution | 3π/2 | 0.1 | 0.9 | 0.8 | ✓ | TRIG6 low R mute |
| SP-08 | KPI misalignment | π/4 | 0.7 | 0.3 | 0.2 | ✗ | "Help?" i ↑ override |
| SP-09 | Witness corruption | π/2 | 0.4 | 0.6 | 0.3 | ✓ | KPD N from logs |

### NEURO-36 Genome (Modeling/Research) - N36-01 to N36-09

| ID | Failure | θ | R | D | N | Danger | Key Mitigation |
|----|---------|---|---|---|---|--------|----------------|
| N36-01 | EEG poison | π/4 | 0.6 | 0.4 | 0.5 | ✗ | Provenance R >0.5 |
| N36-02 | Wave mismatch | π/2 | 0.4 | 0.6 | 0.4 | ✓ | Tan mute bad sim |
| N36-03 | Codon overflow | π | 0.2 | 0.8 | 0.6 | ✓ | eq ≥0.99 evo |
| N36-04 | Resonance underestimate | 3π/2 | 0.1 | 0.9 | 0.8 | ✓ | α damping R ↑ |
| N36-05 | Category misfit | π/4 | 0.7 | 0.3 | 0.2 | ✗ | Prefix D <0.2 |
| N36-06 | Hypothesis divergence | π/2 | 0.5 | 0.5 | 0.3 | ✓ | Theorem 2 bound |
| N36-07 | Fitness false+ | π | 0.3 | 0.7 | 0.5 | ✓ | i > threshold |
| N36-08 | Study gap | 3π/2 | 0.1 | 0.9 | 0.7 | ✓ | Cross-graph low N |
| N36-09 | KPI mismeasure | π/2 | 0.4 | 0.6 | 0.4 | ✓ | Manual "help?" gate |

### Wait Chain Logic (Tech/Stack) - WC-01 to WC-09

| ID | Failure | θ | R | D | N | Danger | Key Mitigation |
|----|---------|---|---|---|---|--------|----------------|
| WC-01 | Trig API diverge | π/4 | 0.8 | 0.2 | 0.1 | ✗ | Mod 2π reset |
| WC-02 | FlameLang break | π/2 | 0.4 | 0.6 | 0.3 | ✓ | Physics eq=1.0 |
| WC-03 | DNA corruption | π | 0.2 | 0.8 | 0.5 | ✓ | Checksum R >0.5 |
| WC-04 | SAGCO halt | 3π/2 | 0.1 | 0.9 | 0.7 | ✓ | Initramfs low D |
| WC-05 | HYDRA config error | π/4 | 0.7 | 0.3 | 0.2 | ✗ | FFI N <0.2 retry |
| WC-06 | Darwinian stall | π/2 | 0.5 | 0.5 | 0.4 | ✓ | +0.02 adjust |
| WC-07 | Mesh lag | π | 0.3 | 0.7 | 0.6 | ✓ | CRDT Theorem 3 |
| WC-08 | Multi-AI bias | 3π/2 | 0.1 | 0.9 | 0.8 | ✓ | Mute low R |
| WC-09 | Outer leak | π/2 | 0.4 | 0.6 | 0.3 | ✓ | 7% eq gate |

### 100 Bottlenecks (Pillar/Algo) - BN-01 to BN-09

| ID | Failure | θ | R | D | N | Danger | Key Mitigation |
|----|---------|---|---|---|---|--------|----------------|
| BN-01 | Compute starvation | π/4 | 0.6 | 0.4 | 0.5 | ✗ | Gray R >0.5 |
| BN-02 | Power denial | π/2 | 0.4 | 0.6 | 0.4 | ✓ | Distributed D bound |
| BN-03 | Memory shortage | π | 0.2 | 0.8 | 0.6 | ✓ | Quant eq ≥0.99 |
| BN-04 | Scaling break | 3π/2 | 0.1 | 0.9 | 0.7 | ✓ | MoE low N mute |
| BN-05 | Alignment explosion | π/4 | 0.7 | 0.3 | 0.2 | ✗ | DPO i ↑ |
| BN-06 | Data poison | π/2 | 0.5 | 0.5 | 0.3 | ✓ | Provenance danger tan |
| BN-07 | Latency spike | π | 0.3 | 0.7 | 0.5 | ✓ | Spec Theorem 1 |
| BN-08 | Context overflow | 3π/2 | 0.1 | 0.9 | 0.8 | ✓ | RAG coherence |
| BN-09 | Tool failure | π/2 | 0.4 | 0.6 | 0.4 | ✓ | Chain > champion |

## Evolution Gates

### R > 0.5 Gate (Resonance Threshold)
- **Purpose**: Ensure stability before proceeding
- **Use case**: Critical path operations
- **Effect**: Blocks unstable states from propagating

### eq ≥ 0.99 Gate (Mission Equivalence Lock)
- **Purpose**: Prevent mission drift
- **Use case**: Resource allocation, strategic decisions
- **Effect**: Rejects actions < 99% aligned with core mission

### D < 0.2 Gate (Drift Boundary)
- **Purpose**: Maintain mission proximity
- **Use case**: Ongoing operations, incremental changes
- **Effect**: Triggers reset when drift exceeds 20%

### N = 0 Gate (Zero Noise Requirement)
- **Purpose**: Enforce determinism
- **Use case**: Security-critical paths, reproducible builds
- **Effect**: Rejects any uncertainty on critical paths

## Diagnostic Workflow

1. **Measure** current state → Determine θ, R, D, N
2. **Calculate** danger → Check if tan θ > 10
3. **Project** trajectory → Use theorems to predict future state
4. **Identify** intervention → Where can we ↑R, ↓D, ↓N?
5. **Apply** mitigation → Execute evolved solution
6. **Re-measure** → Validate improvement

## Key Theorems

### Theorem 1: Resonance Decay
```
R(t) = R₀ · e^(-αt)
```
All systems lose resonance over time without active maintenance.

### Theorem 2: Drift Accumulation  
```
D(t) = D₀ + β∫(1-R)dt
```
Drift accumulates proportional to inverse resonance over time.

### Theorem 3: Noise Amplification
```
N_out = N_in · (1 + tan²θ)
```
Noise amplifies with phase angle, exploding near π/2.

## Quick Commands

```bash
# Run a TRIG6 simulation
omnicalc run failure.t6

# Visualize evolution trajectory
omnicalc run failure.t6 --visualize

# Verify mission alignment
omnicalc verify --mission-eq 0.99 solution.t6

# Batch process all failures
omnicalc batch run simulations/*.t6 --parallel 8
```

## Resources

- **Full Book**: [book.md](book.md)
- **Simulations**: [simulations/](simulations/)
- **Example .t6**: [simulations/SP-01-bypass.t6](simulations/SP-01-bypass.t6)

## The Core Question

**Did it help?**

That's the only KPI that matters. If this framework helps you vectorize, analyze, and evolve beyond your failures—it succeeded.

---

*Target: θ → 0, R → 1, D → 0, N → 0*

🧬🔥
