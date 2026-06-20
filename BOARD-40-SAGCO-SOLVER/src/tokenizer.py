"""
BOARD-40-SAGCO-SOLVER — tokenizer.py
Tokenize text into words, numbers, and formula patterns.
"""

import re
from collections import Counter


FORMULA_PATTERNS = [
    r"=\s*IF\s*\(",            # =IF(...) spreadsheet
    r"[a-zA-Z]\s*\([^)]+\)\s*=",  # f(x) = ...
    r"\blim\b.*->",            # lim ... ->
    r"∫[^d]*d[a-z]",          # ∫ ... dx
    r"∑[^=]*=",               # ∑ ...
    r"[a-zA-Z]\^[0-9]+",      # x^2 power notation
    r"d[a-zA-Z]/d[a-zA-Z]",   # dy/dx
]


def tokenize(text: str) -> dict:
    """
    Returns:
      words:    Counter of lowercase alphabetic words
      numbers:  list of floats found in text
      formulas: list of detected formula strings
    """
    # words: alphabetic tokens only
    word_tokens = re.findall(r"\b[a-zA-Z]{2,}\b", text)
    words = Counter(w.lower() for w in word_tokens)

    # numbers: integers and decimals
    number_strs = re.findall(r"-?\d+(?:\.\d+)?", text)
    numbers = [float(n) for n in number_strs]

    # formulas
    formulas = []
    for pattern in FORMULA_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        formulas.extend(matches)

    return {
        "words":    words,
        "numbers":  numbers,
        "formulas": formulas,
    }


def word_frequency(tokens: dict, top_n: int = 100) -> list:
    """
    Returns [{rank, word, count, pct}] sorted by count descending.
    """
    words: Counter = tokens.get("words", Counter())
    total = sum(words.values()) or 1
    ranked = []
    for rank, (word, count) in enumerate(words.most_common(top_n), start=1):
        ranked.append({
            "rank":  rank,
            "word":  word,
            "count": count,
            "pct":   round(count / total * 100, 4),
        })
    return ranked
