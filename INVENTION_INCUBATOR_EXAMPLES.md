# INVENTION INCUBATOR - Quick Start Examples

## Example 1: Basic Usage (Interactive)

```bash
./invention_incubator.py
```

The script will prompt you:
```
🎭 PIVOT SYNTHESIZER - Context Intake

Enter file paths to analyze (absolute paths recommended)
Type 'done' when finished, or press Ctrl+C to cancel

Path 1: /path/to/your/file1.py
✓ Added: /path/to/your/file1.py
Path 2: /path/to/your/file2.md
✓ Added: /path/to/your/file2.md
Path 3: done
```

## Example 2: Programmatic Usage

```python
#!/usr/bin/env python3
from invention_incubator import PivotThrow

# Initialize synthesizer
synthesizer = PivotThrow()

# Specify files to analyze
files = [
    "./README.md",
    "./main.py",
    "./config.json"
]

# Run synthesis
synthesis_id = synthesizer.synthesize_pivot(files)
print(f"Synthesis ID: {synthesis_id}")

# Detect context
pivot_data = synthesizer.detect_pivot_context(files)
print(f"Calibration Score: {pivot_data['calibration_score']}/100")

# Generate variants
synthesizer.generate_variant_table()

# Display results
synthesizer.display_results()

# Save to JSON
synthesizer.save_to_json("my_analysis.json")
```

## Example 3: Analyze Your Project

```bash
# Create a test with your project files
./invention_incubator.py

# Example paths you might enter:
Path 1: ./src/main.py
Path 2: ./README.md
Path 3: ./package.json
Path 4: ./Dockerfile
Path 5: done
```

## Example 4: Batch Analysis Script

```python
#!/usr/bin/env python3
"""Batch analyze multiple file groups"""
from invention_incubator import PivotThrow
import glob

def analyze_directory(directory_path, pattern="**/*"):
    """Analyze all files matching pattern in directory"""
    
    # Find all matching files
    files = glob.glob(f"{directory_path}/{pattern}", recursive=True)
    
    # Filter to only files (not directories)
    files = [f for f in files if os.path.isfile(f)]
    
    print(f"Found {len(files)} files to analyze")
    
    # Create synthesizer
    synthesizer = PivotThrow()
    
    # Run analysis
    synthesizer.synthesize_pivot(files)
    synthesizer.detect_pivot_context(files)
    synthesizer.generate_variant_table()
    synthesizer.display_results()
    
    # Save with directory name
    output_name = f"analysis_{os.path.basename(directory_path)}.json"
    synthesizer.save_to_json(output_name)
    
    return synthesizer

# Usage
if __name__ == "__main__":
    analyze_directory("./src", pattern="**/*.py")
```

## Example 5: Compare Two Versions

```python
#!/usr/bin/env python3
"""Compare synthesis IDs between two versions"""
from invention_incubator import PivotThrow

def compare_versions(files_v1, files_v2):
    """Compare two sets of files"""
    
    # Analyze version 1
    synth1 = PivotThrow()
    id1 = synth1.synthesize_pivot(files_v1)
    
    # Analyze version 2
    synth2 = PivotThrow()
    id2 = synth2.synthesize_pivot(files_v2)
    
    # Compare
    if id1 == id2:
        print("✅ Identical - No changes detected")
    else:
        print("⚠️  Different synthesis IDs")
        print(f"V1: {id1[:32]}...")
        print(f"V2: {id2[:32]}...")
    
    return id1, id2

# Usage
v1_files = ["./v1/main.py", "./v1/config.json"]
v2_files = ["./v2/main.py", "./v2/config.json"]
compare_versions(v1_files, v2_files)
```

## Example 6: Integration Test

```python
#!/usr/bin/env python3
"""Integration test - verify all features work"""
from invention_incubator import PivotThrow
import tempfile
import os

def integration_test():
    """Complete integration test"""
    
    # Create temporary test files
    test_dir = tempfile.mkdtemp()
    test_files = []
    
    for i, content in enumerate([
        "# Python code\nprint('test')",
        "# Markdown\n## Header",
        '{"json": true}'
    ]):
        file_path = os.path.join(test_dir, f"test_{i}.txt")
        with open(file_path, 'w') as f:
            f.write(content)
        test_files.append(file_path)
    
    # Run full pipeline
    synthesizer = PivotThrow()
    
    # Phase 1: Synthesis
    synthesis_id = synthesizer.synthesize_pivot(test_files)
    assert synthesis_id, "Synthesis ID generated"
    
    # Phase 2: Context detection
    pivot_data = synthesizer.detect_pivot_context(test_files)
    assert pivot_data['context_detected'], "Context detected"
    
    # Phase 3: Variant table
    variants = synthesizer.generate_variant_table()
    assert len(variants) == 4, "4 variants generated"
    
    # Phase 4: Reward formula
    formula = synthesizer.compute_reward_formula()
    assert formula['bounded_reward'] > 0, "Reward computed"
    
    # Phase 5: JSON output
    json_path = os.path.join(test_dir, "test_output.json")
    saved = synthesizer.save_to_json(json_path)
    assert os.path.exists(json_path), "JSON saved"
    
    # Cleanup
    for f in test_files:
        os.remove(f)
    
    print("✅ Integration test PASSED")
    return True

if __name__ == "__main__":
    integration_test()
```

## Example 7: Watch for Changes

```python
#!/usr/bin/env python3
"""Watch files and re-synthesize on changes"""
from invention_incubator import PivotThrow
import time
import hashlib

def watch_and_synthesize(files, interval=5):
    """Watch files and re-run synthesis when changed"""
    
    synthesizer = PivotThrow()
    last_id = None
    
    print(f"Watching {len(files)} files (checking every {interval}s)...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Run synthesis
            current_id = synthesizer.synthesize_pivot(files)
            
            # Check if changed
            if last_id and current_id != last_id:
                print(f"\n⚠️  CHANGE DETECTED!")
                print(f"Previous: {last_id[:32]}...")
                print(f"Current:  {current_id[:32]}...")
                synthesizer.display_results()
            elif not last_id:
                print(f"Initial synthesis: {current_id[:32]}...")
            
            last_id = current_id
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Stopped watching")

# Usage
if __name__ == "__main__":
    watch_files = ["./main.py", "./config.json"]
    watch_and_synthesize(watch_files)
```

## Tips

1. **Use Absolute Paths**: Always prefer absolute paths for reliability
2. **Install Rich**: `pip install rich` for beautiful output formatting
3. **Check JSON Output**: Review the JSON files for detailed analysis
4. **Batch Processing**: Use glob patterns to analyze multiple files
5. **Version Control**: Use synthesis IDs to track file changes over time

## Output Files

All synthesis results are saved to JSON files:
- Interactive mode: `pivot_synthesis_YYYYMMDD_HHMMSS.json`
- Programmatic: Specify your own filename

## Need Help?

See the full documentation in `INVENTION_INCUBATOR_README.md`
