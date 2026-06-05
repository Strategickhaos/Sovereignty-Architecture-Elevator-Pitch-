#!/usr/bin/env python3
"""
TRIG6 Doctor Module Tests
=========================
Unit tests for the TRIG6 self-validation system.

Owner: Strategickhaos DAO LLC
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys
import os

# Add parent directory to path so we can import doctor module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from doctor import Doctor, DoctorResult


class TestDoctorResult:
    """Test DoctorResult class functionality."""
    
    def test_doctor_result_pass(self):
        """Test creating a passing result."""
        result = DoctorResult("test_name", True)
        assert result.name == "test_name"
        assert result.passed is True
        assert result.message == ""
        assert "✓ PASS" in str(result)
    
    def test_doctor_result_fail(self):
        """Test creating a failing result."""
        result = DoctorResult("test_name", False, "Error message")
        assert result.name == "test_name"
        assert result.passed is False
        assert result.message == "Error message"
        assert "✗ FAIL" in str(result)
        assert "Error message" in str(result)
    
    def test_doctor_result_repr(self):
        """Test string representation of results."""
        pass_result = DoctorResult("pass_test", True)
        fail_result = DoctorResult("fail_test", False, "reason")
        
        assert "✓ PASS: pass_test" == str(pass_result)
        assert "✗ FAIL: fail_test - reason" == str(fail_result)


class TestDoctorCoreMath:
    """Test built-in math validation tests."""
    
    def test_core_tests_count(self):
        """Test that core math tests are automatically registered."""
        doc = Doctor()
        assert len(doc.tests) == 5  # 5 core math tests
    
    def test_sin_cos_identity(self):
        """Test sin²+cos²=1 validation."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        # Find sin²+cos²=1 test result
        identity_result = next((r for r in doc.results if "sin²+cos²=1" in r.name), None)
        assert identity_result is not None
        assert identity_result.passed is True
    
    def test_sec_at_60(self):
        """Test sec(60°)=2 validation."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        sec_result = next((r for r in doc.results if "sec(60°)=2" in r.name), None)
        assert sec_result is not None
        assert sec_result.passed is True
    
    def test_tan_at_45(self):
        """Test tan(45°)=1 validation."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        tan_result = next((r for r in doc.results if "tan(45°)=1" in r.name), None)
        assert tan_result is not None
        assert tan_result.passed is True
    
    def test_bridle_120_equals_load(self):
        """Test bridle(120°)=W validation."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        bridle_result = next((r for r in doc.results if "bridle(120°)=W" in r.name), None)
        assert bridle_result is not None
        assert bridle_result.passed is True
    
    def test_highline_30_equals_load(self):
        """Test highline(30°)=W validation."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        highline_result = next((r for r in doc.results if "highline(30°)=W" in r.name), None)
        assert highline_result is not None
        assert highline_result.passed is True
    
    def test_all_core_tests_pass(self):
        """Test that all core math tests pass."""
        doc = Doctor()
        passed, total = doc.run_all()
        
        assert passed == 5
        assert total == 5
        assert all(r.passed for r in doc.results)


class TestDoctorCustomTests:
    """Test custom test registration."""
    
    def test_add_custom_test(self):
        """Test adding a custom test."""
        doc = Doctor()
        
        def custom_test():
            return DoctorResult("custom", True)
        
        doc.add_test(custom_test)
        assert len(doc.tests) == 6  # 5 core + 1 custom
    
    def test_custom_test_execution(self):
        """Test that custom tests are executed."""
        doc = Doctor()
        
        def custom_pass_test():
            return DoctorResult("custom_pass", True)
        
        def custom_fail_test():
            return DoctorResult("custom_fail", False, "Test failure")
        
        doc.add_test(custom_pass_test)
        doc.add_test(custom_fail_test)
        
        passed, total = doc.run_all()
        
        assert total == 7  # 5 core + 2 custom
        assert passed == 6  # 5 core pass + 1 custom pass
        
        custom_pass_result = next((r for r in doc.results if r.name == "custom_pass"), None)
        custom_fail_result = next((r for r in doc.results if r.name == "custom_fail"), None)
        
        assert custom_pass_result.passed is True
        assert custom_fail_result.passed is False


class TestDoctorBoundsValidation:
    """Test constant bounds validation."""
    
    def test_value_within_bounds(self):
        """Test validating a value within bounds."""
        doc = Doctor()
        result = doc.validate_constant_bounds("test_key", 5.0, 0.0, 10.0)
        
        assert result.passed is True
        assert "bounds:test_key" in result.name
    
    def test_value_below_bounds(self):
        """Test validating a value below bounds."""
        doc = Doctor()
        result = doc.validate_constant_bounds("test_key", -1.0, 0.0, 10.0)
        
        assert result.passed is False
        assert "bounds:test_key" in result.name
        assert "not in" in result.message
    
    def test_value_above_bounds(self):
        """Test validating a value above bounds."""
        doc = Doctor()
        result = doc.validate_constant_bounds("test_key", 11.0, 0.0, 10.0)
        
        assert result.passed is False
        assert "bounds:test_key" in result.name
        assert "not in" in result.message
    
    def test_value_at_lower_bound(self):
        """Test validating a value at lower bound."""
        doc = Doctor()
        result = doc.validate_constant_bounds("test_key", 0.0, 0.0, 10.0)
        
        assert result.passed is True
    
    def test_value_at_upper_bound(self):
        """Test validating a value at upper bound."""
        doc = Doctor()
        result = doc.validate_constant_bounds("test_key", 10.0, 0.0, 10.0)
        
        assert result.passed is True


class TestDoctorConstantsFile:
    """Test constants file validation."""
    
    def test_valid_constants_file(self):
        """Test validating a properly formatted constants file."""
        doc = Doctor()
        
        # Create a temporary constants file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {
                "constants": [
                    {
                        "key": "pi",
                        "value": 3.14159,
                        "units": "dimensionless",
                        "provenance": ["mathematical constant"],
                        "entered_by": "test_user",
                        "range": [3.0, 3.2]
                    }
                ]
            }
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have: load success, bounds check
            assert len(results) >= 2
            assert results[0].passed is True  # File loaded
            
            # Find bounds check result
            bounds_result = next((r for r in results if "bounds:pi" in r.name), None)
            assert bounds_result is not None
            assert bounds_result.passed is True
        finally:
            os.unlink(temp_path)
    
    def test_missing_required_fields(self):
        """Test detecting missing required fields."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {
                "constants": [
                    {
                        "key": "incomplete",
                        "value": 1.0
                        # Missing: units, provenance, entered_by
                    }
                ]
            }
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have failures for missing fields
            failed_results = [r for r in results if not r.passed]
            assert len(failed_results) > 0
            
            # Check for specific missing field errors
            field_errors = [r for r in results if "required_field" in r.name]
            assert len(field_errors) >= 3  # Missing units, provenance, entered_by
        finally:
            os.unlink(temp_path)
    
    def test_empty_provenance(self):
        """Test detecting empty provenance."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {
                "constants": [
                    {
                        "key": "test_constant",
                        "value": 1.0,
                        "units": "meters",
                        "provenance": [],  # Empty provenance
                        "entered_by": "test_user"
                    }
                ]
            }
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have failure for empty provenance
            provenance_errors = [r for r in results if "provenance:test_constant" in r.name]
            assert len(provenance_errors) > 0
            assert provenance_errors[0].passed is False
        finally:
            os.unlink(temp_path)
    
    def test_value_out_of_range(self):
        """Test detecting values outside specified range."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {
                "constants": [
                    {
                        "key": "out_of_range",
                        "value": 100.0,
                        "units": "meters",
                        "provenance": ["test"],
                        "entered_by": "test_user",
                        "range": [0.0, 10.0]  # Value is outside this range
                    }
                ]
            }
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have failure for out of range value
            bounds_errors = [r for r in results if "bounds:out_of_range" in r.name]
            assert len(bounds_errors) > 0
            assert bounds_errors[0].passed is False
        finally:
            os.unlink(temp_path)
    
    def test_invalid_json_file(self):
        """Test handling of invalid JSON files."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have failure to load
            assert len(results) == 1
            assert results[0].passed is False
            assert "load:" in results[0].name
        finally:
            os.unlink(temp_path)
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent files."""
        doc = Doctor()
        results = doc.validate_constants_file("/nonexistent/file.json")
        
        # Should have failure to load
        assert len(results) == 1
        assert results[0].passed is False
        assert "load:" in results[0].name
    
    def test_malformed_range(self):
        """Test detecting malformed range fields."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {
                "constants": [
                    {
                        "key": "bad_range_single",
                        "value": 5.0,
                        "units": "meters",
                        "provenance": ["test"],
                        "entered_by": "test_user",
                        "range": [1.0]  # Only one value instead of two
                    },
                    {
                        "key": "bad_range_triple",
                        "value": 5.0,
                        "units": "meters",
                        "provenance": ["test"],
                        "entered_by": "test_user",
                        "range": [1.0, 5.0, 10.0]  # Three values instead of two
                    },
                    {
                        "key": "bad_range_string",
                        "value": 5.0,
                        "units": "meters",
                        "provenance": ["test"],
                        "entered_by": "test_user",
                        "range": "not a list"  # String instead of list
                    }
                ]
            }
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = doc.validate_constants_file(temp_path)
            
            # Should have failures for malformed ranges
            range_format_errors = [r for r in results if "range_format:" in r.name]
            assert len(range_format_errors) == 3
            for error in range_format_errors:
                assert error.passed is False
                assert "exactly 2 values" in error.message
        finally:
            os.unlink(temp_path)


class TestDoctorPackValidation:
    """Test pack validation."""
    
    def test_valid_pack(self):
        """Test validating a valid pack with domain files."""
        doc = Doctor()
        
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create domains directory
            domains_dir = tmppath / "domains"
            domains_dir.mkdir()
            
            # Create a domain
            physics_dir = domains_dir / "physics"
            physics_dir.mkdir()
            
            # Create constants file for domain
            constants_file = physics_dir / "constants.json"
            with open(constants_file, 'w') as f:
                data = {
                    "constants": [
                        {
                            "key": "g",
                            "value": 9.8,
                            "units": "m/s²",
                            "provenance": ["gravitational constant"],
                            "entered_by": "test_user",
                            "range": [9.0, 10.0]
                        }
                    ]
                }
                json.dump(data, f)
            
            # Create packs directory
            packs_dir = tmppath / "packs"
            packs_dir.mkdir()
            
            # Create pack file
            pack_file = packs_dir / "test_pack.json"
            with open(pack_file, 'w') as f:
                pack_data = {
                    "domains": {
                        "physics": {
                            "enabled": True
                        }
                    }
                }
                json.dump(pack_data, f)
            
            # Validate pack
            results = doc.validate_pack(str(pack_file))
            
            # Should have: pack load success, constants file load success, bounds check
            assert len(results) >= 3
            
            # Check pack loaded
            pack_load = next((r for r in results if "load_pack:" in r.name), None)
            assert pack_load is not None
            assert pack_load.passed is True
            
            # Check constants file loaded
            const_load = next((r for r in results if "load:" in r.name and str(constants_file) in r.name), None)
            assert const_load is not None
            assert const_load.passed is True
    
    def test_pack_with_missing_domain_file(self):
        """Test pack validation with missing domain file."""
        doc = Doctor()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create packs directory
            packs_dir = tmppath / "packs"
            packs_dir.mkdir()
            
            # Create pack file referencing non-existent domain
            pack_file = packs_dir / "test_pack.json"
            with open(pack_file, 'w') as f:
                pack_data = {
                    "domains": {
                        "missing_domain": {
                            "enabled": True
                        }
                    }
                }
                json.dump(pack_data, f)
            
            # Validate pack
            results = doc.validate_pack(str(pack_file))
            
            # Should have failure for missing domain file
            missing_errors = [r for r in results if "exists:missing_domain" in r.name]
            assert len(missing_errors) > 0
            assert missing_errors[0].passed is False
    
    def test_pack_with_disabled_domain(self):
        """Test pack validation skips disabled domains."""
        doc = Doctor()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create packs directory
            packs_dir = tmppath / "packs"
            packs_dir.mkdir()
            
            # Create pack file with disabled domain
            pack_file = packs_dir / "test_pack.json"
            with open(pack_file, 'w') as f:
                pack_data = {
                    "domains": {
                        "disabled_domain": {
                            "enabled": False
                        }
                    }
                }
                json.dump(pack_data, f)
            
            # Validate pack
            results = doc.validate_pack(str(pack_file))
            
            # Should only have pack load success, no domain validation
            assert len(results) == 1
            assert results[0].passed is True
            assert "load_pack:" in results[0].name
    
    def test_invalid_pack_file(self):
        """Test handling of invalid pack file."""
        doc = Doctor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name
        
        try:
            results = doc.validate_pack(temp_path)
            
            # Should have failure to load
            assert len(results) == 1
            assert results[0].passed is False
            assert "load_pack:" in results[0].name
        finally:
            os.unlink(temp_path)


class TestDoctorReporting:
    """Test report generation."""
    
    def test_report_all_pass(self):
        """Test report generation when all tests pass."""
        doc = Doctor()
        passed, total = doc.run_all()
        report = doc.report()
        
        assert "TRIG6 DOCTOR REPORT" in report
        assert f"PASSED: {passed}" in report
        assert "FAILED: 0" in report
        assert "ALL SYSTEMS NOMINAL ✓" in report
        
        # Check no failures in the test results section (before STATUS)
        report_sections = report.split("STATUS:")
        test_results_section = report_sections[0]
        assert "✗ FAIL" not in test_results_section
    
    def test_report_with_failures(self):
        """Test report generation with failures."""
        doc = Doctor()
        
        # Add a failing test
        def failing_test():
            return DoctorResult("failing_test", False, "Test failed")
        
        doc.add_test(failing_test)
        passed, total = doc.run_all()
        report = doc.report()
        
        assert "TRIG6 DOCTOR REPORT" in report
        assert f"PASSED: {passed}" in report
        assert "FAILED: 1" in report
        assert "VALIDATION FAILED ✗" in report
        assert "✗ FAIL: failing_test" in report
    
    def test_report_format(self):
        """Test report formatting."""
        doc = Doctor()
        doc.run_all()
        report = doc.report()
        
        # Check report structure
        assert "=" * 50 in report  # Header separator
        assert "-" * 50 in report  # Footer separator
        assert "PASSED:" in report
        assert "FAILED:" in report
        assert "TOTAL:" in report
        assert "STATUS:" in report


class TestDoctorIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_validation_workflow(self):
        """Test complete validation workflow."""
        doc = Doctor()
        
        # Run built-in tests
        passed, total = doc.run_all()
        assert passed == 5
        assert total == 5
        
        # Add custom validation
        def custom_validation():
            return DoctorResult("custom_check", True)
        
        doc.add_test(custom_validation)
        
        # Run again
        passed, total = doc.run_all()
        assert passed == 6
        assert total == 6
        
        # Generate report
        report = doc.report()
        assert "ALL SYSTEMS NOMINAL ✓" in report


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
