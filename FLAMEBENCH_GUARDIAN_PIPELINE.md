# FlameLang Benchmark → Guardian Uncertainty Pipeline

This document describes the compiler-probability plumbing system that connects FlameLang benchmark results to the SAGCO Guardian uncertainty and risk classification system.

## Overview

The pipeline consists of three main components:

1. **FlameBench** (Python) - Discovers, runs, and scores FlameLang compiler tests
2. **SAGCO Guardian** (Rust) - Uncertainty quantification and risk classification
3. **SAGCO DOM0 Daemon** (Rust) - Integration example showing the complete flow

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLAMELANG TEST PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│  1. GitHub Gists (*.flm + manifest.flame-test.json)            │
│     ↓                                                           │
│  2. FlameBench (flamebench.py)                                 │
│     - Discovers and fetches test gists                         │
│     - Compiles and runs FlameLang tests                        │
│     - Calculates Bayesian p_success                            │
│     - Outputs: bench_cache/results.json                        │
│     ↓                                                           │
│  3. SAGCO Guardian (sagco-guardian crate)                      │
│     - Loads results.json via bench_ingest module               │
│     - Converts test results → Uncertainty                      │
│     - Maps uncertainty → Geometry                              │
│     - Classifies safety → RiskLevel                            │
│     ↓                                                           │
│  4. SAGCO DOM0 Daemon (sagco-dom0d binary)                     │
│     - Orchestrates the pipeline                                │
│     - Provides concept-level aggregation                       │
│     - Reports risk classification for deployment decisions     │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Run FlameBench

```bash
# Generate benchmark results
cd flamebench
python3 flamebench.py
```

This creates `bench_cache/results.json` with Bayesian probability summaries:

```json
[
  {
    "test_id": "zyb-it145-ch3-3_2_5-even-odd",
    "concept_tags": ["if-else", "modulo"],
    "runs": 4,
    "successes": 4,
    "p_success": 0.8333333333333334
  }
]
```

### 2. Run Guardian Analysis

```bash
# Analyze compiler reliability
./target/release/sagco-dom0d
```

Output shows:
- Per-test risk classification
- Uncertainty metrics (p_correct, entropy, KL-divergence)
- Concept-level aggregation

## Components

### FlameBench (flamebench/flamebench.py)

**Purpose:** Automated test harness for FlameLang compiler

**Key Features:**
- Discovers test gists from `flame_gists.json`
- Caches gists locally in `bench_cache/`
- Runs tests with manifest-specified inputs/outputs
- Calculates Bayesian posterior probability with Beta(1,1) prior
- Formula: `p_success = (successes + 1) / (runs + 2)`

**Configuration:**
Edit `flamebench/flame_gists.json` to add test gists:

```json
[
  {
    "slug": "test-slug",
    "gist_id": "github-gist-id",
    "files": {
      "manifest.flame-test.json": {
        "id": "unique-test-id",
        "concept_tags": ["if-else", "loops"],
        "inputs": [1, 2, 3],
        "expected_outputs": [10, 20, 30]
      }
    }
  }
]
```

### SAGCO Guardian (crates/sagco-guardian)

**Purpose:** Core uncertainty quantification and risk classification library

**Modules:**

#### `lib.rs` - Core Guardian System
- `Uncertainty`: Represents (p_correct, entropy, kl_div)
- `GeometryPoint`: Maps uncertainty to semantic elements
- `RiskLevel`: Safe | Caution | Warning | Critical
- `Guardian`: Main orchestrator for uncertainty→geometry→risk

**Risk Classification Rules:**
- **Safe**: p_correct > 0.95, entropy < 0.2
- **Caution**: p_correct > 0.85, entropy < 0.5
- **Warning**: p_correct > 0.70, entropy < 0.8
- **Critical**: Below Warning thresholds

#### `bench_ingest.rs` - Benchmark Ingestion
- `BenchSummary`: Deserializes results.json
- `load_bench_summaries()`: Loads benchmark data
- `bench_to_uncertainty()`: Converts test results to Uncertainty

**Uncertainty Calculation:**
```rust
// Posterior Beta(α, β) parameters
let alpha_post = alpha0 + successes;
let beta_post = beta0 + (runs - successes);

// Posterior mean
let p_correct = alpha_post / (alpha_post + beta_post);

// Bernoulli entropy (bits)
let entropy = -(p * p.log2() + (1-p) * (1-p).log2());

// KL divergence (approximate)
let kl_div = sqrt((α'-α)² + (β'-β)²) / (α + β + 1);
```

### SAGCO DOM0 Daemon (crates/sagco-dom0d)

**Purpose:** Example integration showing complete pipeline

**Features:**
- Loads results.json via environment variable or default path
- Analyzes each test individually
- Aggregates by concept tags
- Reports risk levels for deployment decisions

**Environment Variables:**
- `FLAMEBENCH_RESULTS`: Path to results.json (default: `bench_cache/results.json`)

## Usage Examples

### Example 1: Basic Pipeline

```bash
# Step 1: Run benchmarks
python3 flamebench/flamebench.py

# Step 2: Analyze results
./target/release/sagco-dom0d
```

### Example 2: Custom Results Path

```bash
# Run with custom path
export FLAMEBENCH_RESULTS=/var/lib/flamebench/results.json
./target/release/sagco-dom0d
```

### Example 3: Programmatic Use

```rust
use sagco_guardian::{Guardian, bench_ingest::{load_bench_summaries, bench_to_uncertainty}};

fn main() -> anyhow::Result<()> {
    let guardian = Guardian::new();
    let summaries = load_bench_summaries("bench_cache/results.json")?;
    
    for summary in summaries {
        // Beta(1,1) uniform prior
        let uncertainty = bench_to_uncertainty(&summary, 1.0, 1.0);
        
        // Element ID 4 = branching constructs
        let point = guardian.map_uncertainty_to_geometry(uncertainty, 4);
        let risk = guardian.classify_safety(&point);
        
        println!("{}: {:?}", summary.test_id, risk);
    }
    
    Ok(())
}
```

## Bayesian Model

The system uses a **Beta-Bernoulli** conjugate prior model:

### Prior
- **Beta(α₀, β₀)** distribution over probability p
- Default: Beta(1, 1) = Uniform(0, 1)

### Likelihood
- Each test is a Bernoulli trial: pass (1) or fail (0)
- Likelihood: p^successes × (1-p)^failures

### Posterior
- **Beta(α₀ + successes, β₀ + failures)**
- Mean (point estimate): α' / (α' + β')
- Variance: (α'β') / ((α'+β')²(α'+β'+1))

### Why Bayesian?
- **Handles small sample sizes** gracefully (no 3/3 = 100% certainty)
- **Quantifies uncertainty** through entropy and variance
- **Updates incrementally** as more data arrives
- **Principled regularization** via prior selection

## Integration Scenarios

### Scenario 1: CI/CD Gate

```bash
#!/bin/bash
# .github/workflows/flamelang-gate.yml

python3 flamebench/flamebench.py
./target/release/sagco-dom0d > guardian_report.txt

# Parse risk levels, fail if Critical
if grep -q "Critical" guardian_report.txt; then
  echo "❌ Critical compiler issues detected"
  exit 1
fi
```

### Scenario 2: Per-Concept Blocking

```rust
// Block deployment if specific concepts are risky
let summaries = load_bench_summaries("results.json")?;
let if_else_tests: Vec<_> = summaries
    .iter()
    .filter(|s| s.concept_tags.contains(&"if-else".to_string()))
    .collect();

let total_successes: u32 = if_else_tests.iter().map(|t| t.successes).sum();
let total_runs: u32 = if_else_tests.iter().map(|t| t.runs).sum();

if (total_successes as f64) / (total_runs as f64) < 0.90 {
    return Err(anyhow!("if-else construct reliability too low"));
}
```

### Scenario 3: Runtime Introspection

```rust
// FlameLang programs query compiler reliability at runtime
fn guardian_bench(concept: &str) -> (f64, RiskLevel) {
    let summaries = load_bench_summaries("results.json").unwrap();
    // ... filter by concept, compute uncertainty
    (p_correct, risk_level)
}

// In FlameLang:
// let (p, risk) = guardian_bench("if-else");
// if risk == Critical { fallback_to_safe_mode(); }
```

## Future Extensions

### 1. Concept-Level Aggregation (Option 1 from spec)

Aggregate all tests with same concept tags into single Beta posterior:

```rust
fn aggregate_by_concept(summaries: &[BenchSummary]) -> HashMap<String, Uncertainty> {
    // Group by concept, sum successes/runs, compute joint posterior
}
```

### 2. Per-Build History (Option 2 from spec)

Track `results-<git_sha>.json` across builds:

```rust
fn compute_build_kl(prev_results: &Path, curr_results: &Path) -> f64 {
    // KL divergence between builds = "compiler behavior shift"
}
```

### 3. Guardian → FlameLang (Option 3 from spec)

Expose built-in function in FlameLang compiler:

```flamelang
let risk = guardian_bench("if-else")
if risk.level == "Critical" {
    compile_error!("Unreliable if-else construct")
}
```

## Technical Details

### File Locations

```
Sovereignty-Architecture-Elevator-Pitch-/
├── flamebench/
│   ├── flamebench.py          # Python test harness
│   └── flame_gists.json       # Test gist configuration
├── bench_cache/
│   ├── results.json           # Benchmark output (generated)
│   └── <slug>/                # Cached gists
│       ├── manifest.flame-test.json
│       └── *.flm
├── crates/
│   ├── sagco-guardian/        # Guardian library
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs         # Core uncertainty system
│   │       └── bench_ingest.rs # Results ingestion
│   └── sagco-dom0d/           # DOM0 daemon
│       ├── Cargo.toml
│       └── src/
│           └── main.rs        # Example integration
└── Cargo.toml                 # Rust workspace
```

### Dependencies

**Python:**
- Standard library only (json, os, subprocess, pathlib)

**Rust:**
- `serde` 1.0 - Serialization/deserialization
- `serde_json` 1.0 - JSON parsing
- `anyhow` 1.0 - Error handling

### Performance

- **FlameBench**: O(n×m) where n=tests, m=cases per test
- **Guardian**: O(n) for n summaries
- **Memory**: Minimal, results.json typically <1MB

## Troubleshooting

### Error: "Manifest not found"
- Ensure `flame_gists.json` specifies correct gist structure
- Run `flamebench.py` once to generate sample configuration

### Error: "Error loading benchmark results"
- Run `flamebench.py` first to generate `results.json`
- Check `FLAMEBENCH_RESULTS` environment variable path

### Tests show "Warning" despite 100% success
- This is expected with small sample sizes due to Bayesian smoothing
- Beta(1,1) prior adds +1 pseudocount to both success and failure
- Example: 4/4 successes → p_success = 5/6 ≈ 0.833, not 1.0

## References

- **Beta-Bernoulli Conjugate Prior**: [Wikipedia](https://en.wikipedia.org/wiki/Conjugate_prior#Discrete_distributions)
- **Shannon Entropy**: Measures uncertainty in bits
- **KL Divergence**: Measures information gain from prior to posterior
- **Bayesian A/B Testing**: Similar framework, applied to compiler reliability

---

*Generated for Strategickhaos DAO LLC | SAGCO OS v0.1.0*
