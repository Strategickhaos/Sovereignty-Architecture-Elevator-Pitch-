"""
Text tokenizer: words via re, prices via regex, formulas.
"""
import re
from typing import List, Tuple


def tokenize_words(text: str) -> List[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r"[a-zA-Z]+", text.lower())


def tokenize_prices(text: str) -> List[float]:
    """Extract all price-like numbers from text."""
    matches = re.findall(r"\$\s*(\d+(?:\.\d{1,2})?)", text)
    return [float(m) for m in matches]


def tokenize_numbers(text: str) -> List[float]:
    """Extract all numbers from text."""
    matches = re.findall(r"-?\d+(?:\.\d+)?", text)
    return [float(m) for m in matches]


def tokenize_formulas(text: str) -> List[str]:
    """
    Extract formula-like tokens: ERU(...), GUARD(...), etc.
    Returns list of formula strings found.
    """
    pattern = re.compile(r"\b(ERU|GUARD|MORSE|SANITY|SOLVE|LEN|UPPER|LOWER)\s*\([^)]*\)", re.IGNORECASE)
    return [m.group(0) for m in pattern.finditer(text)]


def tokenize_cell_refs(text: str) -> List[str]:
    """Extract cell references like A1, B2, ZZ999."""
    pattern = re.compile(r"\b([A-Z]{1,2}\d{1,3})\b")
    return [m.group(1) for m in pattern.finditer(text.upper())]


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


def normalize_price_str(price_str: str) -> str:
    """Normalize a price string to '$XX.XX' format."""
    prices = tokenize_prices(str(price_str))
    if prices:
        return f"${prices[0]:.2f}"
    nums = tokenize_numbers(str(price_str))
    if nums:
        return f"${nums[0]:.2f}"
    return str(price_str)


def extract_tokens_summary(text: str) -> dict:
    """Return a summary dict of all token types found."""
    return {
        "words": tokenize_words(text),
        "prices": tokenize_prices(text),
        "numbers": tokenize_numbers(text),
        "formulas": tokenize_formulas(text),
        "cell_refs": tokenize_cell_refs(text),
    }
