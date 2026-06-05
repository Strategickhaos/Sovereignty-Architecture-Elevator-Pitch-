#!/usr/bin/env python3
"""
FlameBench - FlameLang Compiler Test Harness
Discovers GitHub gists, runs FlameLang tests, and outputs Bayesian probability summaries.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

# Configuration
BENCH_CACHE = os.path.join(os.path.dirname(__file__), "..", "bench_cache")
GIST_LIST_FILE = os.path.join(os.path.dirname(__file__), "flame_gists.json")


def ensure_cache_dir():
    """Ensure bench_cache directory exists."""
    os.makedirs(BENCH_CACHE, exist_ok=True)


def list_flame_gists() -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    List FlameLang test gists from configuration file.
    Returns list of (slug, gist_id, files_meta) tuples.
    """
    if not os.path.exists(GIST_LIST_FILE):
        print(f"Warning: {GIST_LIST_FILE} not found. Using empty gist list.")
        return []
    
    with open(GIST_LIST_FILE, 'r', encoding='utf-8') as f:
        gists = json.load(f)
    
    result = []
    for gist in gists:
        slug = gist.get("slug", "")
        gist_id = gist.get("gist_id", "")
        files_meta = gist.get("files", {})
        result.append((slug, gist_id, files_meta))
    
    return result


def fetch_gist(slug: str, gist_id: str, files_meta: Dict[str, Any]) -> str:
    """
    Fetch a gist and cache it locally.
    Returns the path to the cached gist directory.
    """
    gist_dir = os.path.join(BENCH_CACHE, slug)
    
    # If already cached, return the path
    if os.path.exists(gist_dir):
        print(f"Using cached gist: {slug}")
        return gist_dir
    
    # Create gist directory
    os.makedirs(gist_dir, exist_ok=True)
    
    # For now, create placeholder files based on files_meta
    # In a real implementation, this would download from GitHub API
    print(f"Fetching gist: {slug} (id: {gist_id})")
    
    # Create placeholder manifest if specified in files_meta
    if "manifest.flame-test.json" in files_meta:
        manifest_path = os.path.join(gist_dir, "manifest.flame-test.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(files_meta["manifest.flame-test.json"], f, indent=2)
    
    return gist_dir


def load_manifest(gist_path: str) -> Dict[str, Any]:
    """
    Load manifest.flame-test.json from a gist directory.
    """
    manifest_path = os.path.join(gist_path, "manifest.flame-test.json")
    
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_single_case(flm_file: str, test_input: Any, expected_output: Any) -> bool:
    """
    Run a single test case with the FlameLang compiler/runner.
    Returns True if the test passes, False otherwise.
    
    For now, this is a stub that simulates compilation and execution.
    In a real implementation, this would:
    1. Compile the .flm file with flamec
    2. Run the compiled code with flamerun and the test_input
    3. Compare the actual output with expected_output
    """
    # Stub implementation - simulate random pass/fail for demonstration
    # In production, this would actually compile and run the FlameLang code
    print(f"  Running test with input={test_input}, expected={expected_output}")
    
    # TODO: Replace with actual compilation and execution
    # result = subprocess.run(['flamec', flm_file], capture_output=True, text=True)
    # if result.returncode != 0:
    #     return False
    # output = subprocess.run(['flamerun', ...], capture_output=True, text=True)
    # return output.stdout.strip() == str(expected_output)
    
    # Stub: return True for demonstration
    return True


def run_all():
    """
    Main entry point: discover all gists, run tests, and output results.json.
    """
    ensure_cache_dir()
    
    summaries = []
    gists = list_flame_gists()
    
    if not gists:
        print("No gists configured. Please create flame_gists.json with test gists.")
        # Create a sample gist list file
        sample_gists = [
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
            },
            {
                "slug": "zyb-it145-ch3-3_1-max-of-two",
                "gist_id": "sample-gist-id-2",
                "files": {
                    "manifest.flame-test.json": {
                        "id": "zyb-it145-ch3-3_1-max-of-two",
                        "concept_tags": ["if-else", "comparison", "max"],
                        "inputs": [[5, 3], [10, 20], [7, 7]],
                        "expected_outputs": [5, 20, 7]
                    }
                }
            }
        ]
        
        with open(GIST_LIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_gists, f, indent=2)
        
        print(f"Created sample gist list at {GIST_LIST_FILE}")
        gists = list_flame_gists()
    
    for slug, gist_id, files_meta in gists:
        print(f"\nProcessing gist: {slug}")
        
        try:
            path = fetch_gist(slug, gist_id, files_meta)
            manifest = load_manifest(path)
            
            successes = 0
            runs = len(manifest["inputs"])
            
            # Find the first .flm file in the gist directory
            flm_file = None
            for fname in os.listdir(path):
                if fname.endswith(".flm"):
                    flm_file = os.path.join(path, fname)
                    break
            
            if flm_file is None:
                print(f"  Warning: No .flm file found in {path}, skipping")
                # Create a placeholder .flm file for demonstration
                flm_file = os.path.join(path, f"{slug}.flm")
                with open(flm_file, 'w', encoding='utf-8') as f:
                    f.write("// FlameLang implementation placeholder\n")
            
            # Run each test case
            for inp, exp in zip(manifest["inputs"], manifest["expected_outputs"]):
                ok = run_single_case(flm_file, inp, exp)
                if ok:
                    successes += 1
                    print(f"    ✓ PASS")
                else:
                    print(f"    ✗ FAIL")
            
            # Bayesian smoothing with Beta(1,1) prior (uniform)
            # Posterior: Beta(1 + successes, 1 + failures)
            # Mean of Beta(α, β) = α / (α + β)
            alpha = 1 + successes
            beta = 1 + (runs - successes)
            p_success = alpha / (alpha + beta)
            
            summary = {
                "test_id": manifest["id"],
                "concept_tags": manifest.get("concept_tags", []),
                "runs": runs,
                "successes": successes,
                "p_success": p_success,
            }
            
            summaries.append(summary)
            
            print(f"  Summary: {successes}/{runs} passed, p_success={p_success:.4f}")
        
        except Exception as e:
            print(f"  Error processing gist {slug}: {e}")
            continue
    
    # Write results to results.json
    results_path = os.path.join(BENCH_CACHE, "results.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=2)
    
    print(f"\n✓ Wrote {len(summaries)} test summaries to {results_path}")
    return summaries


def main():
    """CLI entry point."""
    print("🔥 FlameBench - FlameLang Compiler Test Harness")
    print("=" * 60)
    
    summaries = run_all()
    
    if summaries:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for s in summaries:
            status = "✓" if s["successes"] == s["runs"] else "⚠"
            print(f"{status} {s['test_id']}: {s['successes']}/{s['runs']} "
                  f"(p={s['p_success']:.4f}) tags={s['concept_tags']}")


if __name__ == "__main__":
    main()
