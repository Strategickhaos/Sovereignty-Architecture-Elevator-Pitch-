# FlameBench - FlameLang Compiler Test Harness

Automated test discovery, execution, and Bayesian probability analysis for the FlameLang compiler.

## Overview

FlameBench discovers FlameLang test gists from GitHub, runs them against the compiler, and outputs Bayesian probability summaries for integration with the SAGCO Guardian uncertainty system.

## Quick Start

```bash
# Run the benchmark suite
python3 flamebench.py

# Output: ../bench_cache/results.json
```

## Configuration

Edit `flame_gists.json` to configure test gists:

```json
[
  {
    "slug": "zyb-it145-ch3-3_2_5-even-odd",
    "gist_id": "sample-gist-id-1",
    "files": {
      "manifest.flame-test.json": {
        "id": "zyb-it145-ch3-3_2_5-even-odd",
        "concept_tags": ["if-else", "modulo"],
        "inputs": [2, 3, 10, 15],
        "expected_outputs": ["even", "odd", "even", "odd"]
      }
    }
  }
]
```

## Gist Structure

Each test gist should contain:

- **manifest.flame-test.json** - Test specification
  - `id`: Unique test identifier
  - `concept_tags`: Language concepts being tested
  - `inputs`: Test inputs (any JSON-serializable data)
  - `expected_outputs`: Expected outputs for each input
- **\*.flm** - FlameLang implementation
- **README.md** (optional) - Test description
- Reference implementations in Java/C/Rust (optional)

## Output Format

`results.json` contains an array of test summaries:

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

### Bayesian p_success

Uses Beta-Bernoulli conjugate prior model:

```
Prior: Beta(1, 1)  [uniform prior]
Posterior: Beta(1 + successes, 1 + failures)
p_success = (1 + successes) / (2 + runs)
```

This provides **Bayesian smoothing** to avoid overconfidence with small sample sizes.

## Integration

FlameBench output feeds into the SAGCO Guardian system:

```
FlameBench → results.json → Guardian → Risk Classification
```

See `../FLAMEBENCH_GUARDIAN_PIPELINE.md` for full pipeline documentation.

## Extending FlameBench

### Adding Real Compiler Integration

Currently, `run_single_case()` is a stub. To integrate with actual FlameLang compiler:

```python
def run_single_case(flm_file: str, test_input: Any, expected_output: Any) -> bool:
    # 1. Compile the .flm file
    compile_result = subprocess.run(
        ['flamec', flm_file, '-o', 'output.bin'],
        capture_output=True,
        text=True
    )
    if compile_result.returncode != 0:
        print(f"    Compilation failed: {compile_result.stderr}")
        return False
    
    # 2. Run with input
    run_result = subprocess.run(
        ['flamerun', 'output.bin'],
        input=json.dumps(test_input),
        capture_output=True,
        text=True
    )
    
    # 3. Compare output
    actual = run_result.stdout.strip()
    expected = str(expected_output)
    return actual == expected
```

### Adding GitHub API Integration

To automatically fetch gists from GitHub:

```python
import requests

def fetch_gist_from_github(gist_id: str, dest_dir: str):
    response = requests.get(f"https://api.github.com/gists/{gist_id}")
    gist_data = response.json()
    
    for filename, file_info in gist_data['files'].items():
        file_path = os.path.join(dest_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_info['content'])
```

## Dependencies

- Python 3.6+
- Standard library only (no external packages required)

Optional for extended functionality:
- `requests` - For GitHub API integration
- FlameLang compiler (`flamec`, `flamerun`) - For actual test execution

---

*Part of the Strategickhaos SAGCO OS Project*
