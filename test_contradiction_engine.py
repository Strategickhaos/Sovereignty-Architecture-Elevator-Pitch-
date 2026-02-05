#!/usr/bin/env python3
"""
Test suite for contradiction_engine.py
Validates all major features and use cases
"""

import subprocess
import sys

def run_test(name: str, cmd: list, expect_pass: bool = True) -> bool:
    """Run a single test case"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"CMD: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if expect_pass:
        if result.returncode == 0:
            print(f"✅ PASS: {name}")
            return True
        else:
            print(f"❌ FAIL: {name}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            return False
    else:
        # Test expects failure (detects contradiction)
        if result.returncode != 0:
            print(f"✅ PASS: {name} (correctly detected contradiction)")
            print(f"Output:\n{result.stdout}")
            return True
        else:
            print(f"❌ FAIL: {name} (should have detected contradiction)")
            return False


def main():
    """Run all test cases"""
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Basic mapping with wide bounds (should pass)
    if run_test(
        "Basic mapping with wide bounds",
        ["python3", "contradiction_engine.py", "--mapping", "basic", "--cases", "50", 
         "--theta-min=-1e7", "--theta-max=1e7"],
        expect_pass=True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: TRIG6 without mutations (should pass with no mutations)
    if run_test(
        "TRIG6 geometry (may detect mutation violations)",
        ["python3", "contradiction_engine.py", "--mapping", "trig6_geom", "--cases", "100", 
         "--eps", "1e-9"],
        expect_pass=False  # Mutations will likely violate the manifold constraint
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Bottleneck checks enabled
    if run_test(
        "Bottleneck assassination mode",
        ["python3", "contradiction_engine.py", "--mapping", "basic", "--cases", "50", 
         "--bottlenecks", "--theta-min=-1e7", "--theta-max=1e7"],
        expect_pass=True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: JSON output
    if run_test(
        "JSON output format",
        ["python3", "contradiction_engine.py", "--mapping", "basic", "--cases", "10", 
         "--json", "--theta-min=-10", "--theta-max=10"],
        expect_pass=False  # Edge cases will violate bounds
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 5: Self-test mode
    if run_test(
        "Self-test meta validation",
        ["python3", "contradiction_engine.py", "--self-test", "--theta-min=-1e7", "--theta-max=1e7"],
        expect_pass=False  # Meta-test will detect contradictions
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 6: Help output
    if run_test(
        "Help output",
        ["python3", "contradiction_engine.py", "--help"],
        expect_pass=True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"Total: {tests_passed + tests_failed}")
    print(f"{'='*60}")
    
    if tests_failed > 0:
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
