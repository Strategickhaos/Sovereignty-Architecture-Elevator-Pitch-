# 🔥 FlameBench - Evolving Probabilistic Compiler Benchmark

**DNA:** `SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1`

FlameBench is a sovereign compiler benchmark system that turns zyBooks exercises into self-contained Bernoulli atoms with auto-discovery via GitHub API for evolving `p_success` per tag. The benchmark results feed into guardian uncertainty analysis for compiler fitness evaluation.

## Features

- **📦 Capsule Discovery**: Automatically discovers benchmark capsules from embedded sources and GitHub API
- **🧪 Test Execution**: Runs test cases through flame compiler (with stub mode for sandbox testing)
- **📊 Probabilistic Metrics**: Calculates `p_success` (probability of success) and Shannon entropy per concept tag
- **🧬 Guardian Integration**: Exports results for guardian uncertainty analysis and DNA mutation decisions
- **🦀 Rust Loader**: Efficient Rust library for loading results into Uncertainty structures

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLAMEBENCH SYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│  1. CAPSULE DISCOVERY                                           │
│     ├── GitHub API (gists with zyb- prefix)                    │
│     └── Embedded capsules (fallback)                           │
├─────────────────────────────────────────────────────────────────┤
│  2. BENCHMARK EXECUTION                                         │
│     ├── flamec/flamerun (real compiler)                        │
│     └── Stub mode (sandbox testing)                            │
├─────────────────────────────────────────────────────────────────┤
│  3. RESULTS AGGREGATION                                         │
│     ├── Per-capsule metrics                                    │
│     └── Per-concept tag metrics                                │
├─────────────────────────────────────────────────────────────────┤
│  4. GUARDIAN EXPORT                                             │
│     ├── flamebench-results.json                                │
│     └── guardian-uncertainty.json                              │
├─────────────────────────────────────────────────────────────────┤
│  5. RUST LOADER                                                 │
│     ├── Load uncertainties                                     │
│     ├── Calculate fitness                                      │
│     └── Identify weak concepts                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Python Requirements

```bash
pip install requests
```

### Rust Loader

```bash
cd flamebench_loader
cargo build --release
```

## Usage

### Running the Benchmark

Basic usage with embedded capsules:

```bash
python3 flamebench.py
```

With custom output directory:

```bash
python3 flamebench.py --output-dir results
```

With fixed random seed for reproducibility:

```bash
python3 flamebench.py --seed 42
```

### GitHub API Integration

To enable GitHub API capsule discovery, set environment variables:

```bash
export GITHUB_USER=strategickhaos
export GITHUB_TOKEN=your_github_token
python3 flamebench.py
```

Create gists with zyBooks capsules in JSON format:

```json
{
  "id": "zyb-it145-ch3-3_4-leap-year",
  "name": "Leap Year Detector",
  "description": "zyBooks IT145 Ch3.4 - Determine if year is a leap year",
  "tags": ["if-else-if", "boolean-logic", "modulo", "nested-conditions"],
  "source_code": "def is_leap_year(year): ...",
  "test_cases": [
    {
      "input": "2000",
      "expected_output": "True",
      "description": "Divisible by 400"
    }
  ]
}
```

### Using the Rust Loader

Load benchmark results and analyze uncertainties:

```bash
./flamebench_loader/target/release/flamebench_loader results
```

Or with custom results directory:

```bash
./flamebench_loader/target/release/flamebench_loader /path/to/results
```

### Library Usage (Rust)

```rust
use flamebench_loader::{FlameBenchLoader, GuardianIntegration};

fn main() {
    // Load results
    let loader = FlameBenchLoader::new("results");
    let uncertainties = loader.load_uncertainties().unwrap();
    
    // Guardian integration
    let guardian = GuardianIntegration::new("results");
    let fitness = guardian.calculate_fitness().unwrap();
    
    // Check if compiler should be rejected
    let (should_reject, reason) = guardian
        .should_reject_compiler(0.65, 0.80)
        .unwrap();
    
    // Get weak concepts
    let weak = guardian.get_weak_concepts(0.85, 0.50).unwrap();
}
```

## Output Files

### flamebench-results.json

Main results file containing:
- Overall `p_success` and entropy
- Per-capsule results (passed, total, p_success)
- Per-concept tag aggregates
- Compiler version

Example:

```json
{
  "version": "1.0.0",
  "dna_strand": "SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1",
  "overall": {
    "p_success": 0.833,
    "entropy": 0.650
  },
  "compiler": "not-installed",
  "capsules": [...],
  "concepts": [...]
}
```

### guardian-uncertainty.json

Guardian uncertainty export for integration with guardian systems:

```json
{
  "source": "flamebench",
  "dna_strand": "SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1",
  "uncertainties": [
    {
      "quadrant": "linguistic",
      "tag": "if-else",
      "p_correct": 0.9608,
      "entropy": 0.2512,
      "alpha": 25,
      "beta": 2,
      "sample_size": 24
    }
  ],
  "overall": {
    "p_success": 0.833,
    "entropy": 0.650
  }
}
```

## Embedded Capsules

FlameBench includes 5 embedded zyBooks IT145 Chapter 3 capsules:

1. **zyb-it145-ch3-3_2_5-even-odd**: Even/Odd Checker
   - Tags: `if-else`, `modulo`, `branching`, `integer`
   - Test cases: 4

2. **zyb-it145-ch3-3_1-max-of-two**: Maximum of Two Numbers
   - Tags: `if-else`, `comparison`, `max`, `branching`
   - Test cases: 3

3. **zyb-it145-ch3-3_3-age-category**: Age Category Classifier
   - Tags: `if-else-if`, `range-detection`, `comparison`
   - Test cases: 5

4. **zyb-it145-ch3-3_4-leap-year**: Leap Year Detector
   - Tags: `if-else-if`, `boolean-logic`, `modulo`, `nested-conditions`
   - Test cases: 5

5. **zyb-it145-ch3-3_5-grade-calculator**: Grade Calculator
   - Tags: `if-else-if`, `range-detection`, `string-output`
   - Test cases: 7

## Guardian Integration

The guardian system uses benchmark results to make DNA mutation decisions:

### Q3 Minute 35 Reject Rule

```
IF entropy > threshold OR p_success < threshold THEN
    REJECT compiler build
ELSE
    ACCEPT and fuse to DNA
```

### Fitness Calculation

```
fitness = p_success × (1 - entropy)
```

Higher fitness = stable compiler with predictable behavior
Lower fitness = unstable compiler requiring improvement

### Weak Concepts

Concepts with `p_correct < 0.85` or `entropy > 0.50` are flagged for improvement.

## Metrics

### p_success (Probability of Success)

```
p_success = passed_tests / total_tests
```

Range: [0.0, 1.0]
- 1.0 = perfect success
- 0.0 = complete failure

### Shannon Entropy

```
H(p) = -p log₂(p) - (1-p) log₂(1-p)
```

Range: [0.0, 1.0]
- 0.0 = deterministic (p=0 or p=1)
- 1.0 = maximum uncertainty (p=0.5)

### KL Divergence

```
KL = |entropy - average_entropy|
```

Measures how far a concept's entropy deviates from the average.

## DNA Strand

```
SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1
```

Components:
- **SAGCO**: Strategickhaos Autonomous Governance Core Organization
- **ATG**: Athena Temporal Guardian
- **FLM2**: FlameLang v2
- **MSMC2**: Multiverse State Machine Core v2
- **P16**: Process ID 16
- **CMD27**: Command 27
- **ISO103**: ISO Standard 103
- **MESH5**: Mesh Network v5
- **ORB1**: Orb Integration v1
- **BENCH1**: Benchmark System v1

## Future Extensions

- [ ] Add more zyBooks chapters (Ch3.1, Ch3.2, Ch3.3 full coverage)
- [ ] Support for multiple programming languages
- [ ] Real-time GitHub Actions integration
- [ ] WebAssembly compiler targets
- [ ] Performance benchmarking (execution time)
- [ ] Memory usage tracking
- [ ] Parallel test execution
- [ ] Custom capsule templates
- [ ] Interactive web dashboard

## License

See LICENSE file in repository root.

## Credits

**Architect**: DOM_010101 (Strategickhaos)  
**Genesis**: Increment 3449  
**Origin**: 2023-01-27 21:00:49.000 UTC

---

🔥 **Burning timeline. Reinvesting 7% into reality. ∞**
