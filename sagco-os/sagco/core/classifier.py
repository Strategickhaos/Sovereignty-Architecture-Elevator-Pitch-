"""
Signal-based category detection.
Classifies items into categories based on text signals.
"""
import re

# Category signals: (category_name, [signal_strings])
CATEGORY_SIGNALS = [
    ("price",        ["$", "price", "cost", "fee", "rate", "amount"]),
    ("menu_item",    ["brunch", "lunch", "dinner", "oyster", "sushi", "roll", "eggs", "salmon", "shrimp"]),
    ("contact",      ["email", "phone", "address", "street", "city", "zip"]),
    ("date",         ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                      "january", "february", "march", "april", "may", "june",
                      "july", "august", "september", "october", "november", "december"]),
    ("numeric",      ["total", "count", "number", "qty", "quantity", "sum"]),
    ("formula",      ["=", "eru", "guard", "morse", "sanity", "variance"]),
    ("flashcard",    ["question", "answer", "mnemonic", "cue", "category"]),
]


def classify(text: str) -> str:
    """
    Classify a text string into a category based on signal words.
    Returns the best-matching category name, or 'unknown'.
    """
    if not text:
        return "unknown"
    text_lower = text.lower()
    scores = {}
    for category, signals in CATEGORY_SIGNALS:
        score = 0
        for sig in signals:
            if sig in text_lower:
                score += 1
        if score > 0:
            scores[category] = score
    if not scores:
        return "unknown"
    return max(scores, key=scores.get)


def classify_row(row: dict) -> str:
    """Classify a dict row by combining all its values."""
    combined = " ".join(str(v) for v in row.values())
    return classify(combined)


def classify_rows(rows: list) -> list:
    """Return list of (row, category) tuples."""
    return [(row, classify_row(row)) for row in rows]


def detect_price(text: str) -> float | None:
    """Extract a price value from a string. Returns float or None."""
    m = re.search(r"\$\s*(\d+(?:\.\d{1,2})?)", text)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+(?:\.\d{1,2})?)\s*(?:dollars?|usd)", text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None
