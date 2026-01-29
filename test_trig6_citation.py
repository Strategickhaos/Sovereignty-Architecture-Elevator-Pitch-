#!/usr/bin/env python3
"""
Test Suite for TRIG6 Citation System
=====================================
Validates provenance tracking, citation formatting, and data persistence.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

import unittest
import json
import os
import tempfile
from pathlib import Path

# Import the TRIG6 citation system
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trig6_citation import (
    Provenance, 
    Validation, 
    ConstantRecord,
    load_constants_file,
    save_constants_file
)


class TestProvenance(unittest.TestCase):
    """Test cases for Provenance dataclass."""
    
    def test_provenance_minimal(self):
        """Test creating provenance with minimal required fields."""
        p = Provenance(
            source_title="Test Source",
            publisher="Test Publisher"
        )
        self.assertEqual(p.source_title, "Test Source")
        self.assertEqual(p.publisher, "Test Publisher")
        self.assertIsNone(p.edition_or_rev)
        
    def test_provenance_full(self):
        """Test creating provenance with all fields."""
        p = Provenance(
            source_title="Full Source",
            publisher="Publisher Inc.",
            edition_or_rev="2nd Edition",
            date="2023-01-15",
            section_or_page="Chapter 5, p. 42",
            url="https://example.com/source",
            notes="Additional context"
        )
        self.assertEqual(p.source_title, "Full Source")
        self.assertEqual(p.date, "2023-01-15")
        self.assertEqual(p.url, "https://example.com/source")
        
    def test_provenance_to_dict(self):
        """Test converting provenance to dictionary."""
        p = Provenance(
            source_title="Dict Test",
            publisher="Test Pub",
            date="2023"
        )
        d = p.to_dict()
        self.assertIn("source_title", d)
        self.assertIn("publisher", d)
        self.assertIn("date", d)
        self.assertNotIn("edition_or_rev", d)  # Should not include None values
        
    def test_provenance_format_citation(self):
        """Test citation string formatting."""
        p = Provenance(
            source_title="Citation Test",
            publisher="Citation Pub",
            edition_or_rev="1st Ed",
            date="2022",
            section_or_page="p. 10"
        )
        citation = p.format_citation()
        self.assertIn("Citation Test", citation)
        self.assertIn("(1st Ed)", citation)
        self.assertIn("[2022]", citation)
        self.assertIn("@ p. 10", citation)


class TestValidation(unittest.TestCase):
    """Test cases for Validation dataclass."""
    
    def test_validation_basic(self):
        """Test creating validation with basic fields."""
        v = Validation(
            doctor_test="test.bounds_check"
        )
        self.assertEqual(v.doctor_test, "test.bounds_check")
        self.assertEqual(v.constraints, [])
        
    def test_validation_with_constraints(self):
        """Test creating validation with constraints."""
        v = Validation(
            doctor_test="test.range_check",
            constraints=["value >= 0", "value <= 100"]
        )
        self.assertEqual(len(v.constraints), 2)
        self.assertIn("value >= 0", v.constraints)
        
    def test_validation_to_dict(self):
        """Test converting validation to dictionary."""
        v = Validation(
            doctor_test="test.dict_check",
            constraints=["constraint1"]
        )
        d = v.to_dict()
        self.assertEqual(d["doctor_test"], "test.dict_check")
        self.assertIsInstance(d["constraints"], list)


class TestConstantRecord(unittest.TestCase):
    """Test cases for ConstantRecord dataclass."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_provenance = Provenance(
            source_title="Test Manual",
            publisher="Test Inc.",
            date="2023"
        )
        
    def test_constant_record_minimal(self):
        """Test creating constant record with minimal fields."""
        c = ConstantRecord(
            key="test.constant",
            value=42.0,
            units="meters",
            context="Test constant for unit testing",
            provenance=[self.sample_provenance],
            entered_by="Test User",
            entered_date="2026-01-29"
        )
        self.assertEqual(c.key, "test.constant")
        self.assertEqual(c.value, 42.0)
        self.assertEqual(c.jurisdiction, "global")
        self.assertEqual(c.confidence, "medium")
        
    def test_constant_record_full(self):
        """Test creating constant record with all fields."""
        validation = Validation(
            doctor_test="test.validation",
            constraints=["value > 0"]
        )
        c = ConstantRecord(
            key="test.full",
            value=100.0,
            units="kg",
            context="Full test",
            provenance=[self.sample_provenance],
            entered_by="Tester",
            entered_date="2026-01-29",
            range=(90.0, 110.0),
            jurisdiction="USA",
            confidence="high",
            validation=validation
        )
        self.assertEqual(c.range, (90.0, 110.0))
        self.assertEqual(c.jurisdiction, "USA")
        self.assertEqual(c.confidence, "high")
        self.assertIsNotNone(c.validation)
        
    def test_constant_record_to_dict(self):
        """Test converting constant record to dictionary."""
        c = ConstantRecord(
            key="test.dict",
            value=3.14,
            units="ratio",
            context="Test",
            provenance=[self.sample_provenance],
            entered_by="User",
            entered_date="2026-01-29",
            range=(3.0, 3.5)
        )
        d = c.to_dict()
        self.assertEqual(d["key"], "test.dict")
        self.assertEqual(d["value"], 3.14)
        self.assertIsInstance(d["range"], list)
        self.assertEqual(d["range"], [3.0, 3.5])
        self.assertIsInstance(d["provenance"], list)
        
    def test_constant_record_from_dict(self):
        """Test creating constant record from dictionary."""
        d = {
            "key": "test.from_dict",
            "value": 5.5,
            "units": "seconds",
            "context": "Test",
            "provenance": [
                {
                    "source_title": "Test",
                    "publisher": "Pub"
                }
            ],
            "entered_by": "User",
            "entered_date": "2026-01-29",
            "range": [5.0, 6.0],
            "jurisdiction": "EU",
            "confidence": "low"
        }
        c = ConstantRecord.from_dict(d)
        self.assertEqual(c.key, "test.from_dict")
        self.assertEqual(c.value, 5.5)
        self.assertEqual(c.range, (5.0, 6.0))
        self.assertEqual(c.jurisdiction, "EU")
        self.assertEqual(len(c.provenance), 1)
        
    def test_constant_record_format_full(self):
        """Test formatting constant record as human-readable text."""
        c = ConstantRecord(
            key="test.format",
            value=7.7,
            units="meters",
            context="Format test",
            provenance=[self.sample_provenance],
            entered_by="Formatter",
            entered_date="2026-01-29"
        )
        formatted = c.format_full()
        self.assertIn("KEY: test.format", formatted)
        self.assertIn("VALUE: 7.7 meters", formatted)
        self.assertIn("SOURCES:", formatted)
        self.assertIn("ENTERED BY: Formatter", formatted)
        
    def test_constant_record_requires_provenance(self):
        """Test that constant record requires at least one provenance entry."""
        with self.assertRaises(ValueError) as context:
            ConstantRecord(
                key="test.no_provenance",
                value=1.0,
                units="unit",
                context="Should fail",
                provenance=[],  # Empty provenance list should raise error
                entered_by="Tester",
                entered_date="2026-01-29"
            )
        self.assertIn("must have at least one provenance entry", str(context.exception))


class TestFileOperations(unittest.TestCase):
    """Test cases for file loading and saving."""
    
    def setUp(self):
        """Set up temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_save_and_load_constants(self):
        """Test saving and loading constants to/from JSON file."""
        # Create sample constants
        constants = [
            ConstantRecord(
                key="test.save_load.1",
                value=1.0,
                units="unit",
                context="Test 1",
                provenance=[Provenance(source_title="S1", publisher="P1")],
                entered_by="User",
                entered_date="2026-01-29"
            ),
            ConstantRecord(
                key="test.save_load.2",
                value=2.0,
                units="unit",
                context="Test 2",
                provenance=[Provenance(source_title="S2", publisher="P2")],
                entered_by="User",
                entered_date="2026-01-29"
            )
        ]
        
        # Save to file
        file_path = os.path.join(self.temp_dir, "test_constants.json")
        metadata = {"version": "1.0", "test": True}
        save_constants_file(file_path, constants, metadata)
        
        # Verify file exists
        self.assertTrue(os.path.exists(file_path))
        
        # Load from file
        loaded = load_constants_file(file_path)
        
        # Verify loaded constants
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].key, "test.save_load.1")
        self.assertEqual(loaded[1].value, 2.0)
        
    def test_load_example_constants(self):
        """Test loading the example constants file."""
        # Find the example constants file
        example_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data", "constants", "example_constants.json"
        )
        
        if os.path.exists(example_path):
            constants = load_constants_file(example_path)
            self.assertGreater(len(constants), 0)
            
            # Verify first constant has required fields
            c = constants[0]
            self.assertIsNotNone(c.key)
            self.assertIsNotNone(c.value)
            self.assertIsNotNone(c.units)
            self.assertGreater(len(c.provenance), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_complete_workflow(self):
        """Test complete workflow from creation to persistence."""
        # Create a constant
        constant = ConstantRecord(
            key="integration.test",
            value=99.9,
            units="percent",
            context="Integration test constant",
            provenance=[
                Provenance(
                    source_title="Integration Test Manual",
                    publisher="Test Suite Inc.",
                    edition_or_rev="v1.0",
                    date="2026-01-29",
                    section_or_page="Test Section"
                )
            ],
            entered_by="Integration Tester",
            entered_date="2026-01-29",
            range=(99.0, 100.0),
            validation=Validation(
                doctor_test="integration.bounds",
                constraints=["value >= 99", "value <= 100"]
            )
        )
        
        # Convert to dict and back
        d = constant.to_dict()
        restored = ConstantRecord.from_dict(d)
        
        # Verify restoration
        self.assertEqual(constant.key, restored.key)
        self.assertEqual(constant.value, restored.value)
        self.assertEqual(constant.range, restored.range)
        
        # Format as text
        text = constant.format_full()
        self.assertIn("integration.test", text)
        self.assertIn("99.9 percent", text)


if __name__ == "__main__":
    print("=== TRIG6 Citation System Test Suite ===\n")
    unittest.main(verbosity=2)
