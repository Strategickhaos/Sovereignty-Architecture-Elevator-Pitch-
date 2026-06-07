"""
Frequency analysis using collections.Counter (stdlib).
"""
from collections import Counter
from typing import List, Dict


def word_frequency(texts: List[str]) -> Counter:
    """Count word frequencies across all texts."""
    counter = Counter()
    for text in texts:
        import re
        words = re.findall(r"[a-zA-Z]+", text.lower())
        counter.update(words)
    return counter


def category_frequency(rows: List[Dict]) -> Counter:
    """Count how many rows fall into each category."""
    from sagco.core.classifier import classify_row
    cats = [classify_row(row) for row in rows]
    return Counter(cats)


def price_distribution(rows: List[Dict], price_field: str = "Price") -> dict:
    """
    Compute price distribution stats.
    Returns: {min, max, mean, median, count, histogram}
    """
    prices = []
    for row in rows:
        val = row.get(price_field, "")
        try:
            prices.append(float(str(val).replace("$", "").strip()))
        except (ValueError, AttributeError):
            pass
    if not prices:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    prices.sort()
    n = len(prices)
    mean = sum(prices) / n
    mid = n // 2
    median = prices[mid] if n % 2 == 1 else (prices[mid - 1] + prices[mid]) / 2
    # Simple histogram: 5 buckets
    min_p, max_p = prices[0], prices[-1]
    bucket_size = (max_p - min_p) / 5 if max_p != min_p else 1
    histogram = Counter()
    for p in prices:
        bucket = int((p - min_p) / bucket_size)
        bucket = min(bucket, 4)
        label = f"${min_p + bucket * bucket_size:.0f}-${min_p + (bucket + 1) * bucket_size:.0f}"
        histogram[label] += 1
    return {
        "count": n,
        "min": min_p,
        "max": max_p,
        "mean": round(mean, 2),
        "median": median,
        "histogram": dict(histogram),
    }


def top_items(rows: List[Dict], text_field: str = "Item", n: int = 10) -> List[tuple]:
    """Return the n most common item names."""
    from sagco.core.tokenizer import tokenize_words
    counter = Counter()
    for row in rows:
        text = str(row.get(text_field, ""))
        words = tokenize_words(text)
        counter.update(words)
    return counter.most_common(n)
