"""
Flashcard generator: XLSX rows → flashcards.csv
Uses stdlib csv only.
"""
import csv
import os


FLASHCARD_FIELDS = ["ID", "Category", "Item", "Price", "Question", "Answer",
                    "Mnemonic / Lyric Cue", "ERU", "Rust Token"]


def rows_to_flashcards(rows: list) -> list:
    """
    Convert raw XLSX rows to flashcard dicts.
    Each flashcard has: front (Question), back (Answer), category, item, price, etc.
    """
    cards = []
    for row in rows:
        card = {
            "id": row.get("ID", ""),
            "category": row.get("Category", ""),
            "item": row.get("Item", ""),
            "price": row.get("Price", ""),
            "front": row.get("Question", ""),
            "back": row.get("Answer", ""),
            "mnemonic": row.get("Mnemonic / Lyric Cue", ""),
            "eru": row.get("ERU", ""),
            "rust_token": row.get("Rust Token", ""),
            "expected_price": row.get("Expected Price", ""),
            "actual_price": row.get("Actual Price", ""),
            "variance": row.get("Variance", ""),
            "compression_ratio": row.get("Compression Ratio", ""),
        }
        if card["front"] or card["item"]:  # skip empty rows
            if not card["front"]:
                card["front"] = f"What is the price of {card['item']}?"
            if not card["back"]:
                card["back"] = f"${card['price']} — {card['category']}"
            cards.append(card)
    return cards


def save_flashcards_csv(cards: list, path: str):
    """Save flashcard list to CSV."""
    if not cards:
        return
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    fieldnames = list(cards[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cards)


def load_flashcards_csv(path: str) -> list:
    """Load flashcards from CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
