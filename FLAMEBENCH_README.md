# 🔥 FlameBench - FlameLang Compiler Benchmark Harness

**FlameBench** is a self-evolving benchmark suite for the FlameLang compiler. It automatically discovers and runs test capsules from GitHub Gists, providing Bayesian probability metrics for compiler correctness.

## Overview

FlameBench implements a **gist-based test capsule** architecture where each test case is:
1. Stored as a GitHub Gist with description prefix `FlameTest:`
2. Contains FlameLang source code (`.flm` files)
3. Includes a `manifest.flame-test.json` with test metadata
4. Optionally includes reference implementations (e.g., Java)

The harness:
- Auto-discovers gists via GitHub API
- Caches test files locally
- Executes tests against the FlameLang compiler
- Generates probabilistic success metrics (Bernoulli probability)
- Outputs results in JSON format for integration with Guardian/SAGCO systems

## Quick Start

### Prerequisites

```bash
pip install requests
```

### Running FlameBench

```bash
python flamebench.py
```

This will:
1. Discover all `FlameTest:` gists from the configured GitHub user
2. Download gist files to `./bench_cache/`
3. Run each test capsule
4. Save results to `./results.json`
5. Print a summary report

## Configuration

Edit `flamebench.py` to configure:

```python
GITHUB_USER = "YOUR_GITHUB_USERNAME"  # Your GitHub username
GIST_PREFIX = "FlameTest:"            # Gist description prefix
BENCH_CACHE = Path("./bench_cache")   # Local cache directory
RESULTS_FILE = Path("./results.json") # Results output file
```

## Creating Test Capsules

### Step 1: Create a Gist

Create a new GitHub Gist with:
- **Description**: `FlameTest: zyb-it145-ch3-{section}-{name}`
- **Files**:
  - `{name}.flm` - FlameLang source code
  - `manifest.flame-test.json` - Test metadata
  - `{Name}.java` (optional) - Reference implementation

### Step 2: Write the FlameLang Code

Example (`max_of_two.flm`):

```flamelang
// FlameLang: max of two numbers
fn max_of_two(a: i32, b: i32) -> i32 {
    if a > b {
        return a;
    } else {
        return b;
    }
}
```

### Step 3: Create the Manifest

Example (`manifest.flame-test.json`):

```json
{
  "id": "zyb-it145-ch3-3_1-max-of-two",
  "source": "zyBooks-inspired, branching max-of-two",
  "concept_tags": ["if-else", "comparison", "max"],
  "language_under_test": "flamelang",
  "reference_language": "java",
  "inputs": [[5, 7], [10, -3], [4, 4]],
  "expected_outputs": [7, 10, 4],
  "difficulty": 1,
  "version": 1
}
```

### Step 4: Run FlameBench

```bash
python flamebench.py
```

The harness will automatically discover and test your new gist!

## Current Test Capsules

### 3.1 - Basic if/else (max of two)
- **Gist**: `FlameTest: zyb-it145-ch3-3_1-max-of-two`
- **Concepts**: if-else, comparison, max
- **Difficulty**: 1

### 3.3 - Range detection (age category)
- **Gist**: `FlameTest: zyb-it145-ch3-3_3-age-category`  
- **Concepts**: if-else-if, range-detection, comparison
- **Difficulty**: 2

### 3.2.5 - Even/Odd detection
- **Gist**: `FlameTest: zyb-it145-ch3-3_2_5-even-odd`
- **Concepts**: modulo, branching, parity
- **Difficulty**: 1

## Results Format

Results are saved to `results.json`:

```json
{
  "benchmark_suite": "FlameLang Compiler Tests",
  "version": "1.0",
  "total_tests": 3,
  "results": [
    {
      "id": "zyb-it145-ch3-3_1-max-of-two",
      "source": "zyBooks-inspired, branching max-of-two",
      "concept_tags": ["if-else", "comparison", "max"],
      "difficulty": 1,
      "version": 1,
      "total_tests": 3,
      "passed": 3,
      "failed": 0,
      "p_success": 1.0
    }
  ]
}
```

## Integration with Guardian/SAGCO

The `results.json` file can be ingested by the SAGCO Guardian system to:

1. **Aggregate by concept_tag** - Group results by branching patterns
2. **Compute Beta posterior** - Calculate (alpha, beta) for each tag & compiler version
3. **Feed uncertainty metrics** - Map `p_correct`, entropy, KL divergence to `Uncertainty::new`
4. **Geometry mapping** - Convert to safety classification zones
5. **Linguistic/Container quadrant** - Track branching logic evolution

### Example Rust Integration

```rust
// Load FlameBench results
let results = load_results("results.json")?;

// Aggregate by concept
let branching_stats = results.aggregate_by_tag("if-else");

// Compute Beta posterior
let (alpha, beta) = compute_beta_posterior(&branching_stats);

// Create Uncertainty object
let uncertainty = Uncertainty::new(
    p_correct: branching_stats.p_success,
    entropy: branching_stats.entropy(),
    kl_divergence: branching_stats.kl_from_prior(),
);

// Map to Guardian geometry
let safety_zone = guardian.classify(uncertainty);
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FLAMEBENCH                           │
├─────────────────────────────────────────────────────────┤
│  1. GIST DISCOVERY (GitHub API)                         │
│     └─▶ list_flame_gists() → [(slug, id, files)]       │
├─────────────────────────────────────────────────────────┤
│  2. GIST FETCHING (HTTP)                                │
│     └─▶ fetch_gist() → ./bench_cache/{slug}/           │
├─────────────────────────────────────────────────────────┤
│  3. MANIFEST LOADING (JSON)                             │
│     └─▶ load_manifest() → test metadata                │
├─────────────────────────────────────────────────────────┤
│  4. TEST EXECUTION (FlameLang compiler)                 │
│     └─▶ run_test() → {passed, failed, p_success}       │
├─────────────────────────────────────────────────────────┤
│  5. RESULTS AGGREGATION (JSON)                          │
│     └─▶ save_results() → results.json                  │
└─────────────────────────────────────────────────────────┘
```

## Naming Convention

Test gists follow the pattern:

```
FlameTest: zyb-it145-ch{chapter}-{section}-{name}
```

Examples:
- `FlameTest: zyb-it145-ch3-3_1-max-of-two`
- `FlameTest: zyb-it145-ch3-3_3-age-category`
- `FlameTest: zyb-it145-ch3-3_2_5-even-odd`

## Future Enhancements

- [ ] Actual FlameLang compiler integration
- [ ] Reference implementation auto-comparison
- [ ] Beta distribution parameter estimation
- [ ] Entropy and KL divergence calculation
- [ ] Parallel test execution
- [ ] CI/CD integration
- [ ] Performance benchmarking
- [ ] Coverage analysis
- [ ] Mutation testing

## License

Part of the Strategickhaos Sovereignty Architecture.

🔥 Reignite.
