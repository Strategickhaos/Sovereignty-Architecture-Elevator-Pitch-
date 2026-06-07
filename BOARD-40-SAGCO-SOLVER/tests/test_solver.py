"""
BOARD-40-SAGCO-SOLVER — test_solver.py
Unit tests for the universal solver pipeline.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

MENU_FILE = Path(__file__).parent.parent / "demo" / "water_street_menu.yaml"


def test_fingerprint_returns_sha256():
    from fingerprint import fingerprint
    result = fingerprint(str(MENU_FILE))
    assert "sha256" in result
    assert len(result["sha256"]) == 64
    assert result["extension"] == "yaml"
    assert result["size_bytes"] > 0
    print(f"  [PASS] fingerprint: sha256={result['sha256'][:16]}...")


def test_classifier_detects_menu():
    from extractor import extract
    from classifier import classify
    extracted = extract(str(MENU_FILE))
    category = classify(extracted)
    assert category == "menu", f"Expected 'menu', got '{category}'"
    print(f"  [PASS] classifier: detected '{category}'")


def test_flashcard_generator_produces_cards():
    from extractor import extract
    from classifier import classify
    from flashcard_generator import generate_flashcards
    extracted = extract(str(MENU_FILE))
    category = classify(extracted)
    cards = generate_flashcards(extracted, category)
    assert len(cards) >= 60, f"Expected >= 60 cards, got {len(cards)}"
    print(f"  [PASS] flashcard_generator: {len(cards)} cards generated")


def test_tokenizer_finds_numbers():
    from tokenizer import tokenize
    text = "Eggs Benedict 16.00, Surf and Turf 61.00, Raw Oysters half dozen 18"
    tokens = tokenize(text)
    assert len(tokens["numbers"]) >= 3
    assert 16.0 in tokens["numbers"]
    print(f"  [PASS] tokenizer: found {len(tokens['numbers'])} numbers")


def test_eru_solver_returns_pass():
    from extractor import extract
    from classifier import classify
    from flashcard_generator import generate_flashcards
    from eru_solver import build_eru
    extracted = extract(str(MENU_FILE))
    category = classify(extracted)
    cards = generate_flashcards(extracted, category)
    seeds = [{"seed_id": "SEED-001", "idea": "test"}]
    eru = build_eru(extracted, category, cards, seeds)
    status = eru["eru"]["status"]
    assert status in ("PASS", "PARTIAL"), f"Expected PASS or PARTIAL, got {status}"
    print(f"  [PASS] eru_solver: status={status}")


if __name__ == "__main__":
    print("\n  BOARD-40-SAGCO-SOLVER tests\n")
    test_fingerprint_returns_sha256()
    test_classifier_detects_menu()
    test_flashcard_generator_produces_cards()
    test_tokenizer_finds_numbers()
    test_eru_solver_returns_pass()
    print("\n  All tests passed.\n")
