"""Tests for core/extractor.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import tempfile
import unittest


class TestExtractCSV(unittest.TestCase):
    def test_extract_csv(self):
        from sagco.core.extractor import extract
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("Name,Price\nEggs Benedict,16\nOysters,24\n")
            path = f.name
        try:
            rows = extract(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["Name"], "Eggs Benedict")
            self.assertEqual(rows[0]["Price"], "16")
        finally:
            os.unlink(path)

    def test_extract_text(self):
        from sagco.core.extractor import extract
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Hello\nWorld\n")
            path = f.name
        try:
            rows = extract(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["text"], "Hello")
        finally:
            os.unlink(path)

    def test_extract_xlsx(self):
        """Test XLSX extraction from the real uploaded file."""
        from sagco.core.extractor import extract
        xlsx_path = "/root/.claude/uploads/7048f7e4-f37d-5909-8791-a8759bd4982b/200fcaca-Oyster_Drop_Memory_Engine_SAGCO_Flashcards.xlsx"
        if os.path.exists(xlsx_path):
            rows = extract(xlsx_path)
            self.assertGreater(len(rows), 100)
            self.assertIn("Item", rows[0])
            self.assertIn("Category", rows[0])


if __name__ == "__main__":
    unittest.main()
