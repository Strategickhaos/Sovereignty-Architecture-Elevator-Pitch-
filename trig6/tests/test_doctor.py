#!/usr/bin/env python3
"""
Test suite for TRIG6 Doctor Module
===================================
Comprehensive tests for all doctor functionality.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from trig6.doctor import Doctor, DoctorResult


class TestDoctorResult(unittest.TestCase):
    """Test DoctorResult class."""
    
    def test_pass_result(self):
        """Test passing result representation."""
        result = DoctorResult("test_name", True)
        self.assertTrue(result.passed)
        self.assertIn("✓ PASS", str(result))
        self.assertIn("test_name", str(result))
    
    def test_fail_result(self):
        """Test failing result representation."""
        result = DoctorResult("test_name", False, "Error message")
        self.assertFalse(result.passed)
        self.assertIn("✗ FAIL", str(result))
        self.assertIn("test_name", str(result))
        self.assertIn("Error message", str(result))


class TestDoctorCoreMath(unittest.TestCase):
    """Test core mathematical validation tests."""
    
    def setUp(self):
        self.doctor = Doctor()
    
    def test_sin_cos_identity(self):
        """Test that sin²+cos²=1 identity is validated."""
        passed, total = self.doctor.run_all()
        results_names = [r.name for r in self.doctor.results]
        self.assertIn("sin²+cos²=1", results_names)
        # Should pass
        sin_cos_result = next(r for r in self.doctor.results if r.name == "sin²+cos²=1")
        self.assertTrue(sin_cos_result.passed)
    
    def test_sec_at_60(self):
        """Test that sec(60°)=2 is validated."""
        passed, total = self.doctor.run_all()
        results_names = [r.name for r in self.doctor.results]
        self.assertIn("sec(60°)=2", results_names)
        sec_result = next(r for r in self.doctor.results if r.name == "sec(60°)=2")
        self.assertTrue(sec_result.passed)
    
    def test_tan_at_45(self):
        """Test that tan(45°)=1 is validated."""
        passed, total = self.doctor.run_all()
        results_names = [r.name for r in self.doctor.results]
        self.assertIn("tan(45°)=1", results_names)
        tan_result = next(r for r in self.doctor.results if r.name == "tan(45°)=1")
        self.assertTrue(tan_result.passed)
    
    def test_bridle_120_equals_load(self):
        """Test bridle angle calculation at 120°."""
        passed, total = self.doctor.run_all()
        results_names = [r.name for r in self.doctor.results]
        self.assertIn("bridle(120°)=W", results_names)
        bridle_result = next(r for r in self.doctor.results if r.name == "bridle(120°)=W")
        self.assertTrue(bridle_result.passed)
    
    def test_highline_30_equals_load(self):
        """Test highline calculation at 30° sag."""
        passed, total = self.doctor.run_all()
        results_names = [r.name for r in self.doctor.results]
        self.assertIn("highline(30°)=W", results_names)
        highline_result = next(r for r in self.doctor.results if r.name == "highline(30°)=W")
        self.assertTrue(highline_result.passed)
    
    def test_all_core_tests_pass(self):
        """Test that all core tests pass."""
        passed, total = self.doctor.run_all()
        self.assertEqual(passed, total)
        self.assertEqual(total, 5)  # 5 core tests


class TestDoctorBoundsValidation(unittest.TestCase):
    """Test constant bounds validation."""
    
    def setUp(self):
        self.doctor = Doctor()
    
    def test_value_within_bounds(self):
        """Test that value within bounds passes."""
        result = self.doctor.validate_constant_bounds("test_key", 5.0, 0.0, 10.0)
        self.assertTrue(result.passed)
    
    def test_value_at_lower_bound(self):
        """Test that value at lower bound passes."""
        result = self.doctor.validate_constant_bounds("test_key", 0.0, 0.0, 10.0)
        self.assertTrue(result.passed)
    
    def test_value_at_upper_bound(self):
        """Test that value at upper bound passes."""
        result = self.doctor.validate_constant_bounds("test_key", 10.0, 0.0, 10.0)
        self.assertTrue(result.passed)
    
    def test_value_below_lower_bound(self):
        """Test that value below lower bound fails."""
        result = self.doctor.validate_constant_bounds("test_key", -1.0, 0.0, 10.0)
        self.assertFalse(result.passed)
        self.assertIn("not in", result.message)
    
    def test_value_above_upper_bound(self):
        """Test that value above upper bound fails."""
        result = self.doctor.validate_constant_bounds("test_key", 11.0, 0.0, 10.0)
        self.assertFalse(result.passed)
        self.assertIn("not in", result.message)


class TestDoctorConstantsFile(unittest.TestCase):
    """Test constants file validation."""
    
    def setUp(self):
        self.doctor = Doctor()
    
    def test_valid_constants_file(self):
        """Test validation of a valid constants file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "constants": [
                    {
                        "key": "test_const",
                        "value": 3.14,
                        "units": "radians",
                        "range": [3.0, 3.2]
                    }
                ]
            }, f)
            temp_path = f.name
        
        try:
            results = self.doctor.validate_constants_file(temp_path)
            # Should have: load, bounds check
            self.assertTrue(any(r.passed and "load:" in r.name for r in results))
            self.assertTrue(any(r.passed and "bounds:" in r.name for r in results))
        finally:
            os.unlink(temp_path)
    
    def test_missing_required_field(self):
        """Test that missing required fields are detected."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "constants": [
                    {
                        "key": "test_const",
                        "value": 3.14
                        # Missing "units"
                    }
                ]
            }, f)
            temp_path = f.name
        
        try:
            results = self.doctor.validate_constants_file(temp_path)
            # Should have a failure for missing units
            self.assertTrue(any(not r.passed and "required_field" in r.name for r in results))
        finally:
            os.unlink(temp_path)
    
    def test_strict_provenance_enforcement(self):
        """Test that strict_provenance setting is enforced."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "constants": [
                    {
                        "key": "test_const",
                        "value": 3.14,
                        "units": "radians"
                        # Missing provenance
                    }
                ]
            }, f)
            temp_path = f.name
        
        try:
            # Without strict mode - should pass
            results = self.doctor.validate_constants_file(temp_path, strict_provenance=False)
            provenance_failures = [r for r in results if "provenance:" in r.name and not r.passed]
            self.assertEqual(len(provenance_failures), 0)
            
            # With strict mode - should fail
            results = self.doctor.validate_constants_file(temp_path, strict_provenance=True)
            provenance_failures = [r for r in results if "provenance:" in r.name and not r.passed]
            self.assertGreater(len(provenance_failures), 0)
        finally:
            os.unlink(temp_path)
    
    def test_require_entered_by_enforcement(self):
        """Test that require_entered_by setting is enforced."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "constants": [
                    {
                        "key": "test_const",
                        "value": 3.14,
                        "units": "radians"
                        # Missing entered_by
                    }
                ]
            }, f)
            temp_path = f.name
        
        try:
            # Without require_entered_by - should pass
            results = self.doctor.validate_constants_file(temp_path, require_entered_by=False)
            entered_by_failures = [r for r in results if "entered_by:" in r.name and not r.passed]
            self.assertEqual(len(entered_by_failures), 0)
            
            # With require_entered_by - should fail
            results = self.doctor.validate_constants_file(temp_path, require_entered_by=True)
            entered_by_failures = [r for r in results if "entered_by:" in r.name and not r.passed]
            self.assertGreater(len(entered_by_failures), 0)
        finally:
            os.unlink(temp_path)
    
    def test_invalid_json_file(self):
        """Test handling of invalid JSON files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json {")
            temp_path = f.name
        
        try:
            results = self.doctor.validate_constants_file(temp_path)
            # Should fail to load
            self.assertTrue(any(not r.passed and "load:" in r.name for r in results))
        finally:
            os.unlink(temp_path)
    
    def test_provenance_missing_source_title(self):
        """Test that provenance without source_title is detected."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "constants": [
                    {
                        "key": "test_const",
                        "value": 3.14,
                        "units": "radians",
                        "provenance": [
                            {
                                "author": "Someone"
                                # Missing source_title
                            }
                        ]
                    }
                ]
            }, f)
            temp_path = f.name
        
        try:
            results = self.doctor.validate_constants_file(temp_path)
            # Should have a failure for missing source_title
            self.assertTrue(any(not r.passed and "provenance_source:" in r.name for r in results))
        finally:
            os.unlink(temp_path)


class TestDoctorPackValidation(unittest.TestCase):
    """Test pack validation with real sample files."""
    
    def setUp(self):
        self.doctor = Doctor()
        self.test_dir = Path(__file__).parent.parent
    
    def test_standard_pack_validation(self):
        """Test validation of standard pack."""
        pack_path = self.test_dir / "packs" / "standard.json"
        if pack_path.exists():
            results = self.doctor.validate_pack(str(pack_path))
            # Should load successfully
            load_results = [r for r in results if "load_pack:" in r.name]
            self.assertTrue(len(load_results) > 0)
            self.assertTrue(load_results[0].passed)
            
            # Should have no failures for standard pack with lenient settings
            failures = [r for r in results if not r.passed]
            if failures:
                print("\nStandard pack failures:")
                for f in failures:
                    print(f"  {f}")
            self.assertEqual(len(failures), 0, f"Standard pack should have no failures, but got {len(failures)}")
    
    def test_strict_pack_validation(self):
        """Test validation of strict pack."""
        pack_path = self.test_dir / "packs" / "strict.json"
        if pack_path.exists():
            results = self.doctor.validate_pack(str(pack_path))
            # Should load successfully
            load_results = [r for r in results if "load_pack:" in r.name]
            self.assertTrue(len(load_results) > 0)
            self.assertTrue(load_results[0].passed)
            
            # With strict settings, all constants should pass if they have provenance
            failures = [r for r in results if not r.passed]
            if failures:
                print("\nStrict pack failures:")
                for f in failures:
                    print(f"  {f}")
    
    def test_nonexistent_pack(self):
        """Test handling of nonexistent pack file."""
        results = self.doctor.validate_pack("/nonexistent/path/pack.json")
        # Should fail to load
        self.assertTrue(any(not r.passed and "load_pack:" in r.name for r in results))
    
    def test_pack_with_disabled_domain(self):
        """Test that disabled domains are not validated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create pack with disabled domain
            pack_data = {
                "pack_name": "test",
                "version": "1.0.0",
                "settings": {},
                "domains": {
                    "test_domain": {
                        "enabled": False,
                        "constants_file": "domains/test_domain/constants.json"
                    }
                }
            }
            pack_path = tmpdir / "packs" / "test.json"
            pack_path.parent.mkdir(parents=True)
            with open(pack_path, 'w') as f:
                json.dump(pack_data, f)
            
            results = self.doctor.validate_pack(str(pack_path))
            # Should not try to validate disabled domain
            domain_results = [r for r in results if "test_domain" in r.name]
            self.assertEqual(len(domain_results), 0)


class TestDoctorCustomTests(unittest.TestCase):
    """Test custom test registration."""
    
    def test_add_custom_test(self):
        """Test adding custom tests to the doctor."""
        doctor = Doctor()
        
        def custom_test():
            return DoctorResult("custom_test", True, "Custom test passed")
        
        initial_count = len(doctor.tests)
        doctor.add_test(custom_test)
        self.assertEqual(len(doctor.tests), initial_count + 1)
        
        passed, total = doctor.run_all()
        # Should include custom test
        self.assertTrue(any(r.name == "custom_test" for r in doctor.results))


class TestDoctorReport(unittest.TestCase):
    """Test report generation."""
    
    def test_report_generation(self):
        """Test that report is generated correctly."""
        doctor = Doctor()
        doctor.run_all()
        report = doctor.report()
        
        self.assertIn("TRIG6 DOCTOR REPORT", report)
        self.assertIn("PASSED:", report)
        self.assertIn("FAILED:", report)
        self.assertIn("TOTAL:", report)
    
    def test_report_with_all_pass(self):
        """Test report when all tests pass."""
        doctor = Doctor()
        doctor.run_all()
        report = doctor.report()
        
        self.assertIn("ALL SYSTEMS NOMINAL", report)
    
    def test_report_with_failure(self):
        """Test report when tests fail."""
        doctor = Doctor()
        
        def failing_test():
            return DoctorResult("failing_test", False, "Expected failure")
        
        doctor.add_test(failing_test)
        doctor.run_all()
        report = doctor.report()
        
        self.assertIn("VALIDATION FAILED", report)
        self.assertIn("✗ FAIL", report)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
