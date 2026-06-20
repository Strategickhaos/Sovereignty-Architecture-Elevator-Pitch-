"""
BOARD-40-SAGCO-SOLVER — eru_solver.py
Expected / Actual variance report for the solver pipeline.
"""

from typing import List


def build_eru(extracted: dict, classified: str, cards: list, seeds: list) -> dict:
    """
    Expected: all items classified, all flashcards generated, variance=0
    Actual:   N items, M cards, K seeds
    Returns eru dict with status PASS / PARTIAL / FAIL
    """
    row_count = len(extracted.get("rows", []))
    # for nested menu YAML, count via items if rows is 1 big dict
    rows = extracted.get("rows", [])
    if isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict):
        data = rows[0]
        if "categories" in data:
            # count menu items
            cat_dict = data["categories"]
            row_count = sum(
                len(v.get("items", [])) if isinstance(v, dict) else 0
                for v in cat_dict.values()
            )

    expected_cards = max(row_count, 1)
    actual_cards   = len(cards)
    actual_seeds   = len(seeds)

    variance = expected_cards - actual_cards

    if variance == 0:
        status = "PASS"
    elif variance <= expected_cards * 0.2:
        status = "PARTIAL"
    else:
        status = "FAIL"

    return {
        "eru": {
            "expected": {
                "items_classified": row_count,
                "flashcards_generated": expected_cards,
                "seeds_generated": max(actual_seeds, 1),
                "variance": 0,
            },
            "actual": {
                "items_classified": row_count,
                "flashcards_generated": actual_cards,
                "seeds_generated": actual_seeds,
                "variance": variance,
            },
            "status":   status,
            "category": classified,
            "notes":    (
                "All items accounted for." if status == "PASS"
                else f"Variance of {variance} flashcards from expected {expected_cards}."
            ),
        }
    }
