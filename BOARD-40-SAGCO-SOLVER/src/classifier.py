"""
BOARD-40-SAGCO-SOLVER — classifier.py
Classify extracted content into one or more categories.
"""

CATEGORY_SIGNALS = {
    "menu":        ["price", "item", "category", "appetizer", "entree", "oyster",
                    "sushi", "brunch", "sandwiches", "mains", "roll", "shrimp",
                    "happy_hour", "specials"],
    "homework":    ["Q1", "Q2", "limit", "derivative", "find", "solve", "function",
                    "integral", "problem", "exercise", "homework", "assignment"],
    "music":       ["rank", "occurrence", "POS", "lemma", "pitch", "midi",
                    "note", "chord", "tempo", "beat", "frequency"],
    "code":        ["def ", "fn ", "impl", "struct", "class", "import", "cargo",
                    "function", "return", "if ", "for ", "while ", "let ", "const "],
    "engineering": ["board", "eru", "variance", "citizen", "sagco", "compiler",
                    "district", "physarum", "antibody", "node", "edge"],
    "finance":     ["price", "cost", "revenue", "profit", "budget", "invoice",
                    "tax", "balance", "ledger", "payment"],
    "data":        ["csv", "xlsx", "column", "row", "frequency", "count",
                    "dataset", "table", "schema", "record"],
}


def _score(text: str) -> dict:
    """Return {category: hit_count} for each category."""
    lower = text.lower()
    scores = {}
    for cat, signals in CATEGORY_SIGNALS.items():
        score = sum(1 for s in signals if s.lower() in lower)
        if score:
            scores[cat] = score
    return scores


def classify(extracted: dict) -> str:
    """Returns dominant category string."""
    text = extracted.get("text", "") + " " + str(extracted.get("rows", ""))
    scores = _score(text)
    if not scores:
        return "data"
    return max(scores, key=scores.get)


def multi_classify(extracted: dict) -> list:
    """Returns all matching categories sorted by score."""
    text = extracted.get("text", "") + " " + str(extracted.get("rows", ""))
    scores = _score(text)
    if not scores:
        return ["data"]
    return [cat for cat, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
