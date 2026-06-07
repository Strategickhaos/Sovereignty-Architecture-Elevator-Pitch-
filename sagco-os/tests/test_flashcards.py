"""Tests for solver/flashcards.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import tempfile
import unittest


SAMPLE_ROWS = [
    {"ID": "1", "Category": "Sunday Brunch", "Item": "Eggs Benedict", "Price": "16",
     "Question": "What is the price of Eggs Benedict?", "Answer": "$16 — Sunday Brunch",
     "Mnemonic / Lyric Cue": "Eggs Benedict 16", "ERU": "PASS", "Rust Token": "eggs_benedict",
     "Expected Price": "16", "Actual Price": "16", "Variance": "0", "Compression Ratio": "1"},
    {"ID": "2", "Category": "Sushi", "Item": "Avocado Roll", "Price": "8",
     "Question": "What is the price of Avocado Roll?", "Answer": "$8 — Sushi",
     "Mnemonic / Lyric Cue": "Avocado Roll 8", "ERU": "PASS", "Rust Token": "avocado_roll",
     "Expected Price": "8", "Actual Price": "8", "Variance": "0", "Compression Ratio": "1"},
]


class TestFlashcards(unittest.TestCase):
    def test_rows_to_flashcards(self):
        from sagco.solver.flashcards import rows_to_flashcards
        cards = rows_to_flashcards(SAMPLE_ROWS)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["item"], "Eggs Benedict")
        self.assertEqual(cards[0]["front"], "What is the price of Eggs Benedict?")
        self.assertEqual(cards[0]["back"], "$16 — Sunday Brunch")

    def test_save_load_csv(self):
        from sagco.solver.flashcards import rows_to_flashcards, save_flashcards_csv, load_flashcards_csv
        cards = rows_to_flashcards(SAMPLE_ROWS)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name
        try:
            save_flashcards_csv(cards, path)
            loaded = load_flashcards_csv(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["item"], "Eggs Benedict")
        finally:
            os.unlink(path)

    def test_real_xlsx_flashcards(self):
        """Test flashcard generation from real XLSX."""
        xlsx_path = "/root/.claude/uploads/7048f7e4-f37d-5909-8791-a8759bd4982b/200fcaca-Oyster_Drop_Memory_Engine_SAGCO_Flashcards.xlsx"
        if os.path.exists(xlsx_path):
            from sagco.io.xlsx_reader import read_xlsx
            from sagco.solver.flashcards import rows_to_flashcards
            rows = read_xlsx(xlsx_path)
            cards = rows_to_flashcards(rows)
            self.assertEqual(len(cards), 154)
            # Check all cards have front and back
            for card in cards:
                self.assertTrue(card["front"], f"Card {card['id']} has no front")
                self.assertTrue(card["back"], f"Card {card['id']} has no back")


if __name__ == "__main__":
    unittest.main()
