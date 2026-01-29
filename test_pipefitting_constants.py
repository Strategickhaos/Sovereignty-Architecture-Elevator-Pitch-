#!/usr/bin/env python3
"""
Tests for Pipefitting Constants Module
Strategickhaos DAO LLC
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pipefitting_constants import (
    PipefittingConstants,
    thermal_expansion_in_range,
    wall_thickness_positive,
    takeout_positive,
    weld_gap_in_range,
    pi_is_pi
)


class TestPipefittingConstants:
    """Test suite for pipefitting constants."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.constants = None
    
    def setup(self):
        """Initialize the constants loader."""
        try:
            self.constants = PipefittingConstants()
            return True
        except Exception as e:
            print(f"✗ Setup failed: {e}")
            return False
    
    def assert_true(self, condition, message):
        """Assert a condition is true."""
        if condition:
            self.passed += 1
            print(f"✓ {message}")
        else:
            self.failed += 1
            print(f"✗ {message}")
    
    def assert_equal(self, actual, expected, message):
        """Assert two values are equal."""
        if actual == expected:
            self.passed += 1
            print(f"✓ {message}")
        else:
            self.failed += 1
            print(f"✗ {message}: expected {expected}, got {actual}")
    
    def assert_not_none(self, value, message):
        """Assert a value is not None."""
        if value is not None:
            self.passed += 1
            print(f"✓ {message}")
        else:
            self.failed += 1
            print(f"✗ {message}: value is None")
    
    def test_metadata_loading(self):
        """Test that metadata loads correctly."""
        print("\n=== Test: Metadata Loading ===")
        metadata = self.constants.get_metadata()
        
        self.assert_equal(metadata.get('domain'), 'pipe', 
                         "Domain is 'pipe'")
        self.assert_equal(metadata.get('maintainer'), 'Domenic G. Garza',
                         "Maintainer is correct")
        self.assert_equal(metadata.get('version'), '1.0.0',
                         "Version is correct")
        self.assert_true('ASME B31.1' in metadata.get('regulatory_frameworks', []),
                        "ASME B31.1 in regulatory frameworks")
    
    def test_constant_loading(self):
        """Test that constants load correctly."""
        print("\n=== Test: Constant Loading ===")
        
        # Check that constants are loaded
        constants_list = self.constants.list_constants()
        self.assert_true(len(constants_list) > 0,
                        "Constants list is not empty")
        self.assert_equal(len(constants_list), 8,
                         "Expected 8 constants loaded")
    
    def test_get_constant(self):
        """Test retrieving a constant by key."""
        print("\n=== Test: Get Constant ===")
        
        # Test valid constant
        constant = self.constants.get_constant('pipe.thermal_expansion.carbon_steel')
        self.assert_not_none(constant, 
                            "Carbon steel thermal expansion constant exists")
        
        # Test invalid constant
        invalid = self.constants.get_constant('pipe.nonexistent.constant')
        self.assert_true(invalid is None,
                        "Nonexistent constant returns None")
    
    def test_get_value(self):
        """Test retrieving constant values."""
        print("\n=== Test: Get Value ===")
        
        # Test carbon steel thermal expansion
        value = self.constants.get_value('pipe.thermal_expansion.carbon_steel')
        self.assert_equal(value, 6.5e-6,
                         "Carbon steel thermal expansion value is correct")
        
        # Test Schedule 40 wall thickness
        value = self.constants.get_value('pipe.schedule.40.wall_thickness.2inch')
        self.assert_equal(value, 0.154,
                         "Schedule 40 2-inch wall thickness is correct")
        
        # Test pi constant
        value = self.constants.get_value('pipe.circumference_factor')
        self.assert_equal(value, 3.14159,
                         "Pi constant is correct")
    
    def test_search_constants(self):
        """Test searching for constants."""
        print("\n=== Test: Search Constants ===")
        
        # Search for thermal expansion
        results = self.constants.search_constants('thermal_expansion')
        self.assert_equal(len(results), 2,
                         "Found 2 thermal expansion constants")
        
        # Search for schedule
        results = self.constants.search_constants('schedule')
        self.assert_equal(len(results), 2,
                         "Found 2 schedule constants")
        
        # Search for elbow
        results = self.constants.search_constants('elbow')
        self.assert_equal(len(results), 2,
                         "Found 2 elbow constants")
    
    def test_validation_constraints(self):
        """Test validation constraint functions."""
        print("\n=== Test: Validation Constraints ===")
        
        # Test thermal expansion range
        self.assert_true(thermal_expansion_in_range(6.5e-6),
                        "Valid thermal expansion passes")
        self.assert_true(not thermal_expansion_in_range(0.5),
                        "Out of range thermal expansion fails")
        
        # Test wall thickness positive
        self.assert_true(wall_thickness_positive(0.154),
                        "Positive wall thickness passes")
        self.assert_true(not wall_thickness_positive(-0.1),
                        "Negative wall thickness fails")
        
        # Test weld gap range
        self.assert_true(weld_gap_in_range(0.09375),
                        "Valid weld gap passes")
        self.assert_true(not weld_gap_in_range(0.5),
                        "Out of range weld gap fails")
        
        # Test pi validation
        self.assert_true(pi_is_pi(3.14159),
                        "Pi constant passes")
        self.assert_true(not pi_is_pi(3.0),
                        "Invalid pi fails")
    
    def test_validate_constant(self):
        """Test validating individual constants."""
        print("\n=== Test: Validate Constant ===")
        
        # Validate carbon steel thermal expansion
        is_valid, messages = self.constants.validate_constant(
            'pipe.thermal_expansion.carbon_steel'
        )
        self.assert_true(is_valid,
                        "Carbon steel thermal expansion is valid")
        
        # Validate pi constant
        is_valid, messages = self.constants.validate_constant(
            'pipe.circumference_factor'
        )
        self.assert_true(is_valid,
                        "Pi constant is valid")
    
    def test_validate_all(self):
        """Test validating all constants."""
        print("\n=== Test: Validate All Constants ===")
        
        validation_results = self.constants.validate_all()
        
        # Check that all constants validate
        all_valid = all(result[0] for result in validation_results.values())
        self.assert_true(all_valid,
                        "All constants pass validation")
        
        # Check specific constants
        for key in self.constants.list_constants():
            is_valid, messages = validation_results[key]
            self.assert_true(is_valid,
                            f"Constant {key} is valid")
    
    def test_provenance(self):
        """Test retrieving provenance information."""
        print("\n=== Test: Provenance ===")
        
        # Get provenance for carbon steel thermal expansion
        provenance = self.constants.get_provenance(
            'pipe.thermal_expansion.carbon_steel'
        )
        self.assert_true(len(provenance) > 0,
                        "Carbon steel has provenance records")
        
        # Check provenance structure
        if len(provenance) > 0:
            source = provenance[0]
            self.assert_true('source_title' in source,
                            "Provenance has source_title")
            self.assert_true('publisher' in source,
                            "Provenance has publisher")
            self.assert_equal(source.get('publisher'),
                            'American Society of Mechanical Engineers',
                            "Publisher is ASME")
    
    def test_format_constant(self):
        """Test formatting a constant for display."""
        print("\n=== Test: Format Constant ===")
        
        formatted = self.constants.format_constant(
            'pipe.thermal_expansion.carbon_steel'
        )
        
        self.assert_true('Key:' in formatted,
                        "Formatted output includes key")
        self.assert_true('Value:' in formatted,
                        "Formatted output includes value")
        self.assert_true('Provenance:' in formatted,
                        "Formatted output includes provenance")
        self.assert_true('ASME B31.1' in formatted,
                        "Formatted output includes ASME standard")
    
    def test_specific_values(self):
        """Test specific constant values match ASME/API standards."""
        print("\n=== Test: Specific Values ===")
        
        # Test thermal expansion values
        carbon_steel = self.constants.get_value('pipe.thermal_expansion.carbon_steel')
        self.assert_equal(carbon_steel, 6.5e-6,
                         "Carbon steel thermal expansion (ASME B31.1)")
        
        stainless_304 = self.constants.get_value('pipe.thermal_expansion.stainless_304')
        self.assert_equal(stainless_304, 9.6e-6,
                         "Stainless 304 thermal expansion (ASME B31.3)")
        
        # Test wall thickness values
        sch40 = self.constants.get_value('pipe.schedule.40.wall_thickness.2inch')
        self.assert_equal(sch40, 0.154,
                         "2\" Schedule 40 wall thickness (ASME B36.10M)")
        
        sch80 = self.constants.get_value('pipe.schedule.80.wall_thickness.2inch')
        self.assert_equal(sch80, 0.218,
                         "2\" Schedule 80 wall thickness (ASME B36.10M)")
        
        # Test fitting takeouts
        elbow_90 = self.constants.get_value('pipe.fitting.takeout.90_elbow_lr.2inch')
        self.assert_equal(elbow_90, 3.0,
                         "2\" 90° LR elbow takeout (ASME B16.9)")
        
        elbow_45 = self.constants.get_value('pipe.fitting.takeout.45_elbow_lr.2inch')
        self.assert_equal(elbow_45, 1.5,
                         "2\" 45° LR elbow takeout (ASME B16.9)")
        
        # Test weld gap
        weld_gap = self.constants.get_value('pipe.weld_gap.standard')
        self.assert_equal(weld_gap, 0.09375,
                         "Standard weld gap (AWS D1.1)")
    
    def run_all_tests(self):
        """Run all tests."""
        if not self.setup():
            return False
        
        self.test_metadata_loading()
        self.test_constant_loading()
        self.test_get_constant()
        self.test_get_value()
        self.test_search_constants()
        self.test_validation_constraints()
        self.test_validate_constant()
        self.test_validate_all()
        self.test_provenance()
        self.test_format_constant()
        self.test_specific_values()
        
        return True
    
    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Summary")
        print(f"{'='*60}")
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        
        if self.failed == 0:
            print("\n✓ All tests passed!")
            return 0
        else:
            print(f"\n✗ {self.failed} test(s) failed")
            return 1


if __name__ == "__main__":
    tester = TestPipefittingConstants()
    tester.run_all_tests()
    exit_code = tester.print_summary()
    sys.exit(exit_code)
