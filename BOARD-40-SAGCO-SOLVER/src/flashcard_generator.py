"""
BOARD-40-SAGCO-SOLVER — flashcard_generator.py
Generate flashcards and quiz rows from extracted content.
"""

import csv
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Flashcard:
    front: str
    back: str
    category: str
    difficulty: str  # easy / medium / hard


def _difficulty(price: float) -> str:
    if price < 15:
        return "easy"
    elif price < 30:
        return "medium"
    return "hard"


def _flatten_menu(rows_or_dict) -> list:
    """Flatten a menu YAML structure into [{item, price, cat, description}] entries."""
    items = []
    if isinstance(rows_or_dict, list):
        for r in rows_or_dict:
            if isinstance(r, dict):
                item = r.get("item") or r.get("name")
                price = r.get("price")
                cat = r.get("category", "menu")
                if item and price is not None:
                    items.append({
                        "item": item,
                        "price": float(price),
                        "cat": cat,
                        "description": r.get("description", ""),
                    })
    elif isinstance(rows_or_dict, dict):
        # YAML with categories key
        cats = rows_or_dict.get("categories", rows_or_dict)
        for cat_name, cat_data in cats.items():
            if cat_name == "happy_hour":
                continue
            sub_items = cat_data.get("items", []) if isinstance(cat_data, dict) else []
            for entry in sub_items:
                if isinstance(entry, dict):
                    item = entry.get("item")
                    price = entry.get("price")
                    if item and price is not None:
                        items.append({
                            "item": item,
                            "price": float(price),
                            "cat": cat_name,
                            "description": entry.get("description", ""),
                        })
    return items


def _oyster_variety_cards(cats: dict) -> List[Flashcard]:
    """Generate 'Where is [oyster] from?' cards for oysters_varieties."""
    cards = []
    variety_data = cats.get("oysters_varieties", {})
    sub_items = variety_data.get("items", []) if isinstance(variety_data, dict) else []
    for entry in sub_items:
        if isinstance(entry, dict) and entry.get("item") and entry.get("origin"):
            cards.append(Flashcard(
                front=f"Where is {entry['item']} from?",
                back=f"{entry['origin']} (oyster)",
                category="menu",
                difficulty="easy",
            ))
    return cards


def _happy_hour_card(cats: dict) -> List[Flashcard]:
    """Generate a summary card for happy_hour."""
    hh = cats.get("happy_hour", {})
    if not hh:
        return []
    time_str = hh.get("time", "")
    specials = hh.get("specials", [])
    if not time_str and not specials:
        return []
    specials_short = ", ".join(
        s.replace("1/2 price ", "1/2 price ") for s in specials
    )
    # abbreviate for back
    abbrev = []
    for s in specials:
        abbrev.append(s)
    back = f"{time_str}: {' | '.join(abbrev)}"
    return [Flashcard(
        front="Happy hour time?",
        back=back,
        category="menu",
        difficulty="easy",
    )]


def generate_flashcards(extracted: dict, category: str) -> List[Flashcard]:
    cards = []

    if category == "menu":
        rows = extracted.get("rows", [])
        # rows could be a list (from CSV) or the parsed YAML dict
        raw = rows[0] if (isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict)) else rows
        # if parsed YAML dict has "categories" key use it
        if isinstance(raw, dict) and "categories" in raw:
            items = _flatten_menu(raw)
            # Also generate oyster variety + happy hour special cards
            cats = raw.get("categories", {})
            cards.extend(_oyster_variety_cards(cats))
            cards.extend(_happy_hour_card(cats))
        else:
            items = _flatten_menu(rows)

        for entry in items:
            back_parts = [f"${entry['price']:.0f} — {entry['cat']}"]
            if entry.get("description"):
                back_parts.append(entry["description"])
            cards.append(Flashcard(
                front=entry["item"],
                back=" | ".join(back_parts),
                category="menu",
                difficulty=_difficulty(entry["price"]),
            ))

    elif category == "homework":
        text = extracted.get("text", "")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for i, line in enumerate(lines):
            if any(line.startswith(q) for q in ("Q", "Problem", "Exercise", "Find", "Solve")):
                answer_hint = lines[i + 1] if i + 1 < len(lines) else "See solution manual"
                cards.append(Flashcard(
                    front=line,
                    back=answer_hint,
                    category="homework",
                    difficulty="medium",
                ))

    elif category == "music":
        # frequency-style: word → rank/occurrence
        from tokenizer import tokenize, word_frequency
        tokens = tokenize(extracted.get("text", ""))
        freq = word_frequency(tokens, top_n=50)
        for entry in freq:
            cards.append(Flashcard(
                front=entry["word"],
                back=f"rank {entry['rank']}, {entry['count']} occurrences, {entry['pct']}%",
                category="music",
                difficulty="easy" if entry["rank"] <= 10 else "medium",
            ))

    elif category == "code":
        import re
        text = extracted.get("text", "")
        # find function definitions
        defs = re.findall(r"(?:def |fn |function |class )(\w+)\s*\(([^)]*)\)(?:\s*->.*?)?:", text)
        for name, params in defs:
            cards.append(Flashcard(
                front=f"{name}({params})",
                back=f"Function/class defined in {extracted.get('metadata', {}).get('name', '?')}",
                category="code",
                difficulty="medium",
            ))

    else:
        # generic: top tokens as cards
        from tokenizer import tokenize, word_frequency
        tokens = tokenize(extracted.get("text", ""))
        freq = word_frequency(tokens, top_n=20)
        for entry in freq:
            cards.append(Flashcard(
                front=entry["word"],
                back=f"frequency rank {entry['rank']}: appears {entry['count']} times ({entry['pct']}%)",
                category=category,
                difficulty="easy",
            ))

    return cards


def save_flashcards_csv(cards: List[Flashcard], path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Front", "Back", "Category", "Difficulty"])
        for c in cards:
            writer.writerow([c.front, c.back, c.category, c.difficulty])


def save_quiz_csv(cards: List[Flashcard], path: str):
    """Quiz format: Front, OptionA, OptionB, OptionC, OptionD, CorrectAnswer"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    all_backs = [c.back for c in cards]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Front", "OptionA", "OptionB", "OptionC", "OptionD", "CorrectAnswer"])
        for card in cards:
            correct = card.back
            distractors = [b for b in all_backs if b != correct]
            random.shuffle(distractors)
            options = distractors[:3] + [correct]
            random.shuffle(options)
            # pad if not enough distractors
            while len(options) < 4:
                options.append("N/A")
            writer.writerow([card.front] + options[:4] + [correct])
