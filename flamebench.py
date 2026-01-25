#!/usr/bin/env python3
"""
FlameBench - FlameLang Compiler Benchmark Harness
Dynamically discovers and runs test capsules from GitHub Gists
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Configuration
GITHUB_USER = os.getenv('GITHUB_USER', 'Strategickhaos')  # Can be overridden via env var
GIST_PREFIX = "FlameTest:"
BENCH_CACHE = Path("./bench_cache")
RESULTS_FILE = Path("./results.json")

# GISTS list (legacy, will be replaced by auto-discovery)
# Note: When API is unavailable, only tests with example files in bench_cache will work
GISTS = [
    # 'zyb-it145-ch3-3_2_5-even-odd',  # TODO: Add example files or create gist
    'zyb-it145-ch3-3_1-max-of-two',
    'zyb-it145-ch3-3_3-age-category',
]


def list_flame_gists() -> List[Tuple[str, str, Dict]]:
    """
    Fetch all FlameTest gists from GitHub user's account.
    
    Returns:
        List of tuples: (slug, gist_id, files_metadata)
    """
    url = f"https://api.github.com/users/{GITHUB_USER}/gists"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        gists = resp.json()
    except requests.RequestException as e:
        print(f"Error fetching gists: {e}")
        print("Falling back to hardcoded GISTS list")
        return [(slug, None, {}) for slug in GISTS]
    
    slugs = []
    for g in gists:
        desc = g.get("description") or ""
        if desc.startswith(GIST_PREFIX):
            # Extract slug from description, e.g. "FlameTest: zyb-it145-ch3-3_1-max-of-two"
            slug = desc.replace(GIST_PREFIX, "").strip()
            slugs.append((slug, g["id"], g["files"]))
    
    if not slugs:
        print(f"No gists found with prefix '{GIST_PREFIX}'. Using hardcoded GISTS list.")
        return [(slug, None, {}) for slug in GISTS]
    
    return slugs


def fetch_gist(slug: str, gist_id: str, files_meta: Dict) -> Path:
    """
    Download gist files to local cache.
    
    Args:
        slug: Gist identifier slug
        gist_id: GitHub gist ID
        files_meta: Gist files metadata from GitHub API
        
    Returns:
        Path to cached gist directory
    """
    path = BENCH_CACHE / slug
    path.mkdir(parents=True, exist_ok=True)
    
    if not gist_id or not files_meta:
        print(f"Skipping download for {slug} (no gist_id or files)")
        return path
    
    for fname, meta in files_meta.items():
        raw_url = meta.get("raw_url")
        if not raw_url:
            continue
            
        try:
            r = requests.get(raw_url, timeout=10)
            r.raise_for_status()
            with open(path / fname, "w", encoding="utf-8") as f:
                f.write(r.text)
        except requests.RequestException as e:
            print(f"Error downloading {fname}: {e}")
    
    print(f"✓ Fetched gist {slug} ({gist_id}) into {path}")
    return path


def load_manifest(gist_path: Path) -> Dict[str, Any]:
    """
    Load and parse manifest.flame-test.json from gist directory.
    
    Args:
        gist_path: Path to gist directory
        
    Returns:
        Parsed manifest dictionary
    """
    manifest_file = gist_path / "manifest.flame-test.json"
    
    if not manifest_file.exists():
        print(f"⚠ No manifest found at {manifest_file}")
        return {}
    
    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading manifest: {e}")
        return {}


def run_test(gist_path: Path, manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a FlameLang test based on manifest.
    
    Args:
        gist_path: Path to gist directory  
        manifest: Parsed manifest
        
    Returns:
        Test result dictionary
    """
    test_id = manifest.get("id", "unknown")
    inputs = manifest.get("inputs", [])
    expected = manifest.get("expected_outputs", [])
    
    # For now, this is a stub - actual FlameLang compiler execution would go here
    # In real implementation, this would:
    # 1. Compile the .flm file
    # 2. Run it with each input
    # 3. Compare outputs with expected_outputs
    # 4. Calculate p_success (Bernoulli probability)
    
    print(f"  Running test: {test_id}")
    print(f"    Inputs: {inputs}")
    print(f"    Expected: {expected}")
    
    # TODO: Replace stub with actual FlameLang compiler execution
    # When compiler is available, calculate actual p_success from test results
    # For stub demonstration, we use 1.0 to show the data flow works
    total_count = len(inputs)
    p_success = 1.0  # STUB: Will be calculated from actual test results when compiler integrated
    
    result = {
        "id": test_id,
        "source": manifest.get("source", ""),
        "concept_tags": manifest.get("concept_tags", []),
        "difficulty": manifest.get("difficulty", 1),
        "version": manifest.get("version", 1),
        "total_tests": total_count,
        "passed": total_count if p_success == 1.0 else 0,  # STUB
        "failed": 0 if p_success == 1.0 else total_count,   # STUB
        "p_success": p_success,
        "stub_execution": True,  # Flag indicating this is not real test execution
    }
    
    print(f"    Result: STUB (p={p_success:.2f}) - Awaiting compiler integration")
    
    return result


def run_all() -> List[Dict[str, Any]]:
    """
    Main benchmark runner - discovers and runs all FlameTest gists.
    
    Returns:
        List of test results
    """
    print("🔥 FlameBench - FlameLang Compiler Benchmark Harness")
    print("=" * 60)
    
    results = []
    
    # Discover gists
    print("\n📡 Discovering FlameTest gists...")
    gists = list_flame_gists()
    print(f"Found {len(gists)} test capsule(s)\n")
    
    # Run each test
    for slug, gist_id, files_meta in gists:
        print(f"\n🧪 Processing: {slug}")
        
        # Fetch gist files
        path = fetch_gist(slug, gist_id, files_meta)
        
        # Load manifest
        manifest = load_manifest(path)
        if not manifest:
            print(f"  ⚠ Skipping {slug} - no valid manifest")
            continue
        
        # Run test
        result = run_test(path, manifest)
        results.append(result)
    
    return results


def save_results(results: List[Dict[str, Any]]) -> None:
    """
    Save test results to JSON file.
    
    Args:
        results: List of test results
    """
    output = {
        "benchmark_suite": "FlameLang Compiler Tests",
        "version": "1.0",
        "total_tests": len(results),
        "results": results
    }
    
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results saved to {RESULTS_FILE}")


def print_summary(results: List[Dict[str, Any]]) -> None:
    """
    Print summary statistics of test results.
    
    Args:
        results: List of test results
    """
    print("\n" + "=" * 60)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 60)
    
    total_tests = sum(r["total_tests"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    
    # Calculate average p_success, handling potential None values
    valid_results = [r for r in results if r.get("p_success") is not None]
    avg_p_success = sum(r["p_success"] for r in valid_results) / len(valid_results) if valid_results else 0.0
    
    print(f"\nTest Capsules: {len(results)}")
    print(f"Total Test Cases: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Average p_success: {avg_p_success:.4f}")
    
    print("\n📋 Per-Capsule Results:")
    for r in results:
        tags = ", ".join(r["concept_tags"])
        print(f"  • {r['id']}: p={r['p_success']:.2f} [{tags}]")
    
    print("\n🔥 FlameBench complete.\n")


def main():
    """Main entry point."""
    # Create cache directory
    BENCH_CACHE.mkdir(exist_ok=True)
    
    # Run all benchmarks
    results = run_all()
    
    # Save results
    if results:
        save_results(results)
        print_summary(results)
    else:
        print("\n⚠ No test results generated")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
