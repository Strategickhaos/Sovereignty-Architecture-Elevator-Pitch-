#!/usr/bin/env python3
"""
TRIG6 Truth Score Calculator Tests
Strategickhaos DAO LLC - Sovereignty Architecture
"""

import sys
import math
from pathlib import Path

# Add parent directory to path to import trig6_truth_score
sys.path.insert(0, str(Path(__file__).parent.parent))

from trig6_truth_score import (
    TRIG6Truth,
    clamp01,
    logit,
    sigmoid,
    trig6_truth_probability,
    format_score_report,
    score_all_claims,
    TAXONOMY_DEFAULTS,
)


class TRIG6Tests:
    """Test suite for TRIG6 Truth Score Calculator."""
    
    def test_basic_functions(self):
        """Test basic mathematical functions."""
        results = {"test_id": "trig6_1", "name": "Basic Functions", "status": "PASS"}
        
        try:
            # Test clamp01
            assert clamp01(0.5) == 0.5
            assert clamp01(-0.5) == 0.0
            assert clamp01(1.5) == 1.0
            
            # Test sigmoid/logit inverse
            for p in [0.1, 0.5, 0.9]:
                z = logit(p)
                p_recovered = sigmoid(z)
                assert abs(p - p_recovered) < 1e-6
            
            results["details"] = "All basic math functions working correctly"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def test_trig6truth_dataclass(self):
        """Test TRIG6Truth dataclass."""
        results = {"test_id": "trig6_2", "name": "TRIG6Truth Dataclass", "status": "PASS"}
        
        try:
            truth = TRIG6Truth(A=0.9, R=0.8, I=0.7, C=0.6, E=0.5, F=0.4)
            
            # Test attributes
            assert truth.A == 0.9
            assert truth.R == 0.8
            
            # Test as_tuple
            assert truth.as_tuple() == (0.9, 0.8, 0.7, 0.6, 0.5, 0.4)
            
            # Test mean
            assert abs(truth.mean() - 0.65) < 1e-6
            
            results["details"] = "TRIG6Truth dataclass working correctly"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def test_truth_probability_calculation(self):
        """Test trig6_truth_probability function."""
        results = {"test_id": "trig6_3", "name": "Truth Probability Calculation", "status": "PASS"}
        
        try:
            # Perfect evidence should yield high probability
            perfect = TRIG6Truth(A=1.0, R=1.0, I=1.0, C=1.0, E=1.0, F=1.0)
            prob_perfect = trig6_truth_probability(perfect, prior=0.7)
            assert prob_perfect > 0.95
            
            # Zero evidence should yield low probability
            zero = TRIG6Truth(A=0.0, R=0.0, I=0.0, C=0.0, E=0.0, F=0.0)
            prob_zero = trig6_truth_probability(zero, prior=0.5)
            assert prob_zero < 0.10
            
            # Neutral evidence should preserve prior roughly
            neutral = TRIG6Truth(A=0.5, R=0.5, I=0.5, C=0.5, E=0.5, F=0.5)
            prob_neutral = trig6_truth_probability(neutral, prior=0.5)
            assert 0.4 < prob_neutral < 0.6
            
            results["details"] = f"Perfect: {prob_perfect:.3f}, Zero: {prob_zero:.3f}, Neutral: {prob_neutral:.3f}"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def test_report_generation(self):
        """Test format_score_report function."""
        results = {"test_id": "trig6_4", "name": "Report Generation", "status": "PASS"}
        
        try:
            claim = TRIG6Truth(A=0.9, R=0.6, I=0.4, C=0.95, E=0.98, F=0.95)
            upgrades = {"R → 0.90": "Make repo public"}
            
            report = format_score_report("Test claim", claim, prior=0.7, upgrades=upgrades)
            
            # Check key elements
            assert "Test claim" in report
            assert "TRIG6 EVIDENCE VECTOR" in report
            assert "COMPUTED PROBABILITY" in report
            assert "Make repo public" in report
            
            results["details"] = f"Report generated successfully ({len(report)} chars)"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def test_score_all_claims(self):
        """Test score_all_claims function."""
        results = {"test_id": "trig6_5", "name": "Score All Claims", "status": "PASS"}
        
        try:
            output = score_all_claims()
            
            # Check all claims present
            assert "PR count >= 1194" in output
            assert "TRIG6" in output
            assert "SAGCO OS" in output
            assert "3,138 hours" in output
            
            # Check summary table
            assert "TRIG6 TRUTH SCORE SUMMARY" in output
            assert "LEGEND:" in output
            assert "CONFIDENCE TIERS:" in output
            
            results["details"] = f"All 4 claims scored successfully ({len(output)} chars)"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def test_taxonomy_defaults(self):
        """Test TAXONOMY_DEFAULTS mapping."""
        results = {"test_id": "trig6_6", "name": "Taxonomy Defaults", "status": "PASS"}
        
        try:
            # Check structure
            assert "VERIFIED" in TAXONOMY_DEFAULTS
            assert "UNCITED" in TAXONOMY_DEFAULTS
            assert "METAPHOR" in TAXONOMY_DEFAULTS
            
            # Check VERIFIED has high scores
            verified = TAXONOMY_DEFAULTS["VERIFIED"]
            assert verified.A >= 0.80
            assert verified.F >= 0.80
            
            # Check UNCITED has low scores
            uncited = TAXONOMY_DEFAULTS["UNCITED"]
            assert uncited.A <= 0.20
            
            # Check METAPHOR is None
            assert TAXONOMY_DEFAULTS["METAPHOR"] is None
            
            # Check probability ordering
            verified_prob = trig6_truth_probability(TAXONOMY_DEFAULTS["VERIFIED"], prior=0.5)
            uncited_prob = trig6_truth_probability(TAXONOMY_DEFAULTS["UNCITED"], prior=0.5)
            assert verified_prob > uncited_prob
            
            results["details"] = f"Verified prob: {verified_prob:.3f}, Uncited prob: {uncited_prob:.3f}"
        except Exception as e:
            results["status"] = "FAIL"
            results["error"] = str(e)
        
        return results
    
    def run_all_tests(self):
        """Run all tests and return results."""
        test_results = []
        test_results.append(self.test_basic_functions())
        test_results.append(self.test_trig6truth_dataclass())
        test_results.append(self.test_truth_probability_calculation())
        test_results.append(self.test_report_generation())
        test_results.append(self.test_score_all_claims())
        test_results.append(self.test_taxonomy_defaults())
        return test_results


if __name__ == "__main__":
    tests = TRIG6Tests()
    results = tests.run_all_tests()
    
    print("=" * 70)
    print("TRIG6 TRUTH SCORE CALCULATOR - TEST RESULTS")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for result in results:
        status_symbol = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_symbol} Test {result['test_id']}: {result['name']} - {result['status']}")
        
        if result["status"] == "PASS":
            passed += 1
            if "details" in result:
                print(f"  {result['details']}")
        else:
            failed += 1
            if "error" in result:
                print(f"  Error: {result['error']}")
    
    print("=" * 70)
    print(f"TOTAL: {passed} passed, {failed} failed out of {len(results)} tests")
    print("=" * 70)
    
    # Exit with error code if any tests failed
    sys.exit(0 if failed == 0 else 1)
