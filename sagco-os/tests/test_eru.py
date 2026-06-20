"""Tests for core/eru.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from sagco.core.eru import (
    compute_variance, eru_label, eru_variance_label,
    run_eru_on_rows, eru_summary, ERU_PASS, ERU_PARTIAL, ERU_FAIL,
    VARIANCE_0, OPEN_VARIANCE
)


class TestERU(unittest.TestCase):
    def test_compute_variance_numeric(self):
        self.assertEqual(compute_variance(10, 10), 0.0)
        self.assertEqual(compute_variance(10, 15), 5.0)
        self.assertEqual(compute_variance(15, 10), 5.0)
        self.assertEqual(compute_variance("$10", "$10"), 0.0)
        self.assertEqual(compute_variance("$10", "$15"), 5.0)

    def test_compute_variance_string(self):
        self.assertEqual(compute_variance("PASS", "PASS"), 0.0)
        self.assertEqual(compute_variance("PASS", "FAIL"), 1.0)

    def test_eru_label_pass(self):
        self.assertEqual(eru_label(10, 10), ERU_PASS)
        self.assertEqual(eru_label("test", "test"), ERU_PASS)

    def test_eru_label_partial(self):
        self.assertEqual(eru_label(10, 13, pass_threshold=0, partial_threshold=5), ERU_PARTIAL)

    def test_eru_label_fail(self):
        self.assertEqual(eru_label(10, 20, pass_threshold=0, partial_threshold=5), ERU_FAIL)

    def test_eru_variance_label(self):
        self.assertEqual(eru_variance_label(10, 10), VARIANCE_0)
        self.assertEqual(eru_variance_label("x", "x"), VARIANCE_0)
        self.assertEqual(eru_variance_label(10, 11), OPEN_VARIANCE)
        self.assertEqual(eru_variance_label("a", "b"), OPEN_VARIANCE)

    def test_run_eru_on_rows(self):
        rows = [
            {"ID": "1", "Expected Price": "16", "Actual Price": "16"},
            {"ID": "2", "Expected Price": "20", "Actual Price": "30"},
        ]
        results = run_eru_on_rows(rows)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].label, ERU_PASS)
        self.assertEqual(results[1].label, ERU_FAIL)

    def test_eru_summary(self):
        rows = [
            {"ID": str(i), "Expected Price": "10", "Actual Price": "10"} for i in range(8)
        ] + [
            {"ID": "9", "Expected Price": "10", "Actual Price": "12"},
            {"ID": "10", "Expected Price": "10", "Actual Price": "50"},
        ]
        results = run_eru_on_rows(rows)
        summary = eru_summary(results)
        self.assertEqual(summary["total"], 10)
        self.assertEqual(summary["PASS"], 8)
        self.assertGreater(summary["pass_rate"], 0)

    def test_real_flashcard_eru(self):
        """Test ERU on all 154 real flashcard rows."""
        xlsx_path = "/root/.claude/uploads/7048f7e4-f37d-5909-8791-a8759bd4982b/200fcaca-Oyster_Drop_Memory_Engine_SAGCO_Flashcards.xlsx"
        if os.path.exists(xlsx_path):
            from sagco.io.xlsx_reader import read_xlsx
            rows = read_xlsx(xlsx_path)
            results = run_eru_on_rows(rows)
            summary = eru_summary(results)
            self.assertEqual(summary["total"], 154)
            # All items have expected==actual in this dataset
            self.assertEqual(summary["PASS"], 154)
            self.assertEqual(summary["pass_rate"], 100.0)


if __name__ == "__main__":
    unittest.main()
