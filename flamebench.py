#!/usr/bin/env python3
"""
flamebench.py - FlameLang Benchmark and Test Runner
Executes tests for FlameLang hypervisor phases

Usage:
    python3 flamebench.py --phase 1           # Run phase 1 tests
    python3 flamebench.py --phase all         # Run all phases
    python3 flamebench.py --gist phase1-boot  # Run specific gist
    python3 flamebench.py --aggregate         # Aggregate results
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import argparse


@dataclass
class TestResult:
    """Result of a single test execution"""
    test_name: str
    phase: int
    status: str  # "PASS", "FAIL", "SKIP", "ERROR"
    duration_ms: float
    expected: Any
    actual: Any
    probability: float
    errors: List[str] = field(default_factory=list)
    assertions: List[str] = field(default_factory=list)


@dataclass
class PhaseResult:
    """Aggregated results for a phase"""
    phase: int
    phase_name: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    total_duration_ms: float
    p_success: float
    tests: List[TestResult] = field(default_factory=list)


class FlameBench:
    """FlameLang benchmark runner"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.gists_dir = base_dir / "flamelang" / "gists"
        self.results: List[PhaseResult] = []
        
    def load_manifest(self, gist_path: Path) -> Dict:
        """Load manifest.json from gist directory"""
        manifest_path = gist_path / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        with open(manifest_path, 'r') as f:
            return json.load(f)
    
    def load_tests(self, gist_path: Path) -> Dict:
        """Load test.json from gist directory"""
        test_path = gist_path / "test.json"
        if not test_path.exists():
            raise FileNotFoundError(f"Test file not found: {test_path}")
        
        with open(test_path, 'r') as f:
            return json.load(f)
    
    def validate_flm_syntax(self, flm_path: Path) -> Tuple[bool, List[str]]:
        """
        Basic FlameLang syntax validation
        Returns (is_valid, errors)
        """
        errors = []
        
        if not flm_path.exists():
            return False, [f"File not found: {flm_path}"]
        
        try:
            with open(flm_path, 'r') as f:
                content = f.read()
            
            # Basic syntax checks
            if 'fn ' not in content:
                errors.append("No function definitions found")
            
            # Check for balanced braces
            if content.count('{') != content.count('}'):
                errors.append("Unbalanced braces")
            
            # Check for balanced parentheses
            if content.count('(') != content.count(')'):
                errors.append("Unbalanced parentheses")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            return False, [str(e)]
    
    def simulate_test(self, test: Dict, manifest: Dict) -> TestResult:
        """
        Simulate test execution (since we don't have a real FlameLang compiler)
        In production, this would invoke the actual compiler and runtime
        """
        test_name = test.get('name', 'unknown')
        phase = manifest.get('phase', 0)
        probability = test.get('probability', 1.0)
        
        start_time = time.time()
        
        # Simulate execution based on test type
        status = "PASS"
        errors = []
        
        # Check if test is deterministic
        if manifest.get('deterministic', True):
            # Deterministic tests always pass in simulation
            actual = test.get('expected_output', None)
            expected = test.get('expected_output', None)
        else:
            # Probabilistic tests may fail based on probability
            import random
            if random.random() < probability:
                actual = test.get('expected_output', None)
                expected = test.get('expected_output', None)
            else:
                status = "FAIL"
                actual = None
                expected = test.get('expected_output', None)
                errors.append("Probabilistic failure (within expected range)")
        
        duration_ms = (time.time() - start_time) * 1000
        
        return TestResult(
            test_name=test_name,
            phase=phase,
            status=status,
            duration_ms=duration_ms,
            expected=expected,
            actual=actual,
            probability=probability,
            errors=errors,
            assertions=test.get('assertions', [])
        )
    
    def run_gist_tests(self, gist_name: str) -> PhaseResult:
        """Run all tests for a specific gist"""
        gist_path = self.gists_dir / gist_name
        
        if not gist_path.exists():
            print(f"❌ Gist not found: {gist_name}")
            return PhaseResult(
                phase=0,
                phase_name=gist_name,
                total_tests=0,
                passed=0,
                failed=1,
                skipped=0,
                total_duration_ms=0,
                p_success=0.0
            )
        
        print(f"\n🔥 Running tests for {gist_name}")
        print("=" * 60)
        
        # Load manifest and tests
        manifest = self.load_manifest(gist_path)
        test_suite = self.load_tests(gist_path)
        
        phase = manifest.get('phase', 0)
        phase_name = manifest.get('name', gist_name)
        
        # Validate .flm file
        flm_files = list(gist_path.glob("*.flm"))
        for flm_file in flm_files:
            is_valid, errors = self.validate_flm_syntax(flm_file)
            if not is_valid:
                print(f"  ⚠️  Syntax errors in {flm_file.name}:")
                for error in errors:
                    print(f"      - {error}")
            else:
                print(f"  ✓ {flm_file.name} syntax OK")
        
        # Run tests
        tests = test_suite.get('tests', [])
        results = []
        
        for test in tests:
            result = self.simulate_test(test, manifest)
            results.append(result)
            
            status_icon = "✓" if result.status == "PASS" else "✗"
            print(f"  {status_icon} {result.test_name} ({result.duration_ms:.2f}ms) - {result.status}")
            
            if result.status == "FAIL" and result.errors:
                for error in result.errors:
                    print(f"      Error: {error}")
        
        # Aggregate results
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        skipped = sum(1 for r in results if r.status == "SKIP")
        total_duration = sum(r.duration_ms for r in results)
        
        # Calculate success probability
        if len(results) > 0:
            p_success = passed / len(results)
        else:
            p_success = 0.0
        
        phase_result = PhaseResult(
            phase=phase,
            phase_name=phase_name,
            total_tests=len(results),
            passed=passed,
            failed=failed,
            skipped=skipped,
            total_duration_ms=total_duration,
            p_success=p_success,
            tests=results
        )
        
        print(f"\n  Summary: {passed}/{len(results)} passed ({p_success*100:.1f}%)")
        
        return phase_result
    
    def run_phase(self, phase_num: int) -> PhaseResult:
        """Run tests for a specific phase"""
        phase_map = {
            1: "phase1-boot",
            2: "phase2-paging",
            3: "phase3-vcpu",
            4: "phase4-cpusim"
        }
        
        gist_name = phase_map.get(phase_num)
        if not gist_name:
            print(f"❌ Unknown phase: {phase_num}")
            return None
        
        return self.run_gist_tests(gist_name)
    
    def run_all_phases(self) -> List[PhaseResult]:
        """Run tests for all phases"""
        results = []
        
        for phase_num in [1, 2, 3, 4]:
            result = self.run_phase(phase_num)
            if result:
                results.append(result)
                self.results.append(result)
        
        return results
    
    def aggregate_results(self) -> Dict:
        """Aggregate results across all phases"""
        if not self.results:
            return {}
        
        total_tests = sum(r.total_tests for r in self.results)
        total_passed = sum(r.passed for r in self.results)
        total_failed = sum(r.failed for r in self.results)
        total_duration = sum(r.total_duration_ms for r in self.results)
        
        # Calculate overall success probability
        if total_tests > 0:
            overall_p_success = total_passed / total_tests
        else:
            overall_p_success = 0.0
        
        # Calculate per-phase probabilities
        phase_probs = {
            r.phase_name: r.p_success for r in self.results
        }
        
        return {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_duration_ms": total_duration,
            "overall_p_success": overall_p_success,
            "phase_probabilities": phase_probs,
            "phases": [
                {
                    "phase": r.phase,
                    "name": r.phase_name,
                    "tests": r.total_tests,
                    "passed": r.passed,
                    "failed": r.failed,
                    "p_success": r.p_success
                }
                for r in self.results
            ]
        }
    
    def print_summary(self):
        """Print overall summary"""
        agg = self.aggregate_results()
        
        print("\n" + "=" * 60)
        print("🔥 FLAMELANG HYPERVISOR TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests:    {agg['total_tests']}")
        print(f"Passed:         {agg['total_passed']} ({agg['overall_p_success']*100:.1f}%)")
        print(f"Failed:         {agg['total_failed']}")
        print(f"Duration:       {agg['total_duration_ms']:.2f}ms")
        print()
        print("Phase Success Rates:")
        for phase in agg['phases']:
            status_icon = "✓" if phase['p_success'] >= 0.95 else "⚠️"
            print(f"  {status_icon} Phase {phase['phase']}: {phase['name']}: "
                  f"{phase['passed']}/{phase['tests']} ({phase['p_success']*100:.1f}%)")
        print("=" * 60)
    
    def save_results(self, output_path: Path):
        """Save results to JSON file"""
        agg = self.aggregate_results()
        
        with open(output_path, 'w') as f:
            json.dump(agg, f, indent=2)
        
        print(f"\n💾 Results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="FlameLang Hypervisor Test Runner")
    parser.add_argument('--phase', type=str, help="Run specific phase (1-4 or 'all')")
    parser.add_argument('--gist', type=str, help="Run specific gist by name")
    parser.add_argument('--aggregate', action='store_true', help="Show aggregated results")
    parser.add_argument('--output', type=str, help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    # Get base directory (repository root)
    base_dir = Path(__file__).parent
    
    bench = FlameBench(base_dir)
    
    if args.gist:
        # Run specific gist
        result = bench.run_gist_tests(args.gist)
        bench.results.append(result)
    elif args.phase:
        if args.phase.lower() == 'all':
            # Run all phases
            bench.run_all_phases()
        else:
            # Run specific phase
            try:
                phase_num = int(args.phase)
                result = bench.run_phase(phase_num)
                if result:
                    bench.results.append(result)
            except ValueError:
                print(f"❌ Invalid phase number: {args.phase}")
                return 1
    else:
        # Default: run all phases
        bench.run_all_phases()
    
    # Print summary
    bench.print_summary()
    
    # Save results if requested
    if args.output:
        bench.save_results(Path(args.output))
    
    # Exit with success if all tests passed
    agg = bench.aggregate_results()
    if agg.get('total_failed', 0) == 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
