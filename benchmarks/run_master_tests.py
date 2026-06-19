#!/usr/bin/env python3
"""
SAGCO-HYDRA Master Test Runner
Executes all benchmark test suites:
- Oracle Tests (ORC-001 to ORC-010)
- FlameLang Tests (FLC-001 to FLC-008)
- Hypervisor Tests (HYP-001 to HYP-006)
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_test_suite(name, script_path):
    """Run a test suite and return success status"""
    print(f"\n{'='*75}")
    print(f" Running {name}")
    print(f"{'='*75}\n")
    
    try:
        result = subprocess.run(
            ['python3', str(script_path)],
            cwd=script_path.parent,
            timeout=60
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ {name} timed out!")
        return False
    except Exception as e:
        print(f"❌ {name} failed: {e}")
        return False

def main():
    """Main entry point"""
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║        SAGCO-HYDRA MASTER BENCHMARK TEST RUNNER v1.0.6               ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"🧬 DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1")
    print(f"🕐 Timestamp: {datetime.now().isoformat()}")
    print()
    
    base_path = Path(__file__).parent
    
    # Test suites to run
    suites = [
        ("Oracle Tests (ORC-001 to ORC-010)", base_path / "oracle-tests" / "run_oracle_tests.py"),
        ("FlameLang Tests (FLC-001 to FLC-008)", base_path / "flamelang-specs" / "run_flamelang_tests.py"),
        ("Hypervisor Tests (HYP-001 to HYP-006)", base_path / "hypervisor-tests" / "run_hypervisor_tests.py"),
    ]
    
    results = {}
    
    for name, script_path in suites:
        if script_path.exists():
            success = run_test_suite(name, script_path)
            results[name] = success
        else:
            print(f"⚠️  {name} not found at {script_path}")
            results[name] = False
    
    # Summary
    print("\n" + "="*75)
    print(" BENCHMARK SUMMARY")
    print("="*75 + "\n")
    
    for name, success in results.items():
        icon = "✅" if success else "❌"
        print(f"{icon} {name}")
    
    total = len(results)
    passed = sum(1 for s in results.values() if s)
    
    print()
    print(f"📊 Overall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("✅ All benchmark suites passed!")
        return 0
    elif passed > 0:
        print("⚠️  Some benchmark suites need attention")
        return 1
    else:
        print("❌ All benchmark suites failed or pending")
        return 2

if __name__ == '__main__':
    sys.exit(main())
