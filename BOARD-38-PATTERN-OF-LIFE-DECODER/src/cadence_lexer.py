"""
BOARD-38 — Pattern-of-Life Decoder
cadence_lexer.py — Tokenizes any input stream into cadence tokens.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class CadenceToken:
    token_type: str   # SYMBOL, PHRASE, LOOP, TRANSITION, TIC, SPIKE
    value: str
    frequency: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __repr__(self) -> str:
        return f"CadenceToken({self.token_type}, {self.value!r}, freq={self.frequency})"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.utcnow().isoformat()


def _classify_by_freq(freq: int, total: int) -> str:
    """Classify a token type based on its frequency relative to total tokens."""
    ratio = freq / max(total, 1)
    if ratio > 0.15:
        return "SPIKE"
    if ratio > 0.05:
        return "LOOP"
    if ratio > 0.02:
        return "PHRASE"
    return "SYMBOL"


# ── Public API ────────────────────────────────────────────────────────────────

def lex_word_frequency(data: list[dict]) -> list[CadenceToken]:
    """
    Convert a word-frequency list [{word: str, count: int}, ...] into
    CadenceTokens.  High-frequency words become SPIKE/LOOP; rare ones SYMBOL.

    Args:
        data: list of dicts with at least 'word' and 'count' keys.
    Returns:
        Sorted list of CadenceTokens (highest frequency first).
    """
    if not data:
        return []

    total = sum(d.get("count", 0) for d in data)
    tokens: list[CadenceToken] = []

    for entry in data:
        word = str(entry.get("word", entry.get("token", "")))
        count = int(entry.get("count", entry.get("frequency", 1)))
        if not word:
            continue
        tok_type = _classify_by_freq(count, total)
        tokens.append(CadenceToken(
            token_type=tok_type,
            value=word,
            frequency=count,
            timestamp=_now(),
        ))

    tokens.sort(key=lambda t: t.frequency, reverse=True)
    return tokens


def lex_music_tokens(notes: list) -> list[CadenceToken]:
    """
    Convert a list of music notes/events into CadenceTokens.
    notes can be:
      - strings like "C4", "D#5", "rest"
      - dicts with 'note', 'pitch', or 'event' keys + optional 'duration'

    Args:
        notes: list of note strings or note-event dicts.
    Returns:
        list of CadenceTokens.
    """
    if not notes:
        return []

    normalized: list[str] = []
    for n in notes:
        if isinstance(n, str):
            normalized.append(n)
        elif isinstance(n, dict):
            normalized.append(str(n.get("note", n.get("pitch", n.get("event", "?")))))
        else:
            normalized.append(str(n))

    freq_map = Counter(normalized)
    total = len(normalized)
    tokens: list[CadenceToken] = []

    for i, raw in enumerate(normalized):
        freq = freq_map[raw]
        tok_type = _classify_by_freq(freq, total)
        # Detect transition: note changes after a repeated block
        if i > 0 and normalized[i - 1] != raw and freq_map[normalized[i - 1]] > 2:
            tok_type = "TRANSITION"
        tokens.append(CadenceToken(
            token_type=tok_type,
            value=raw,
            frequency=freq,
            timestamp=_now(),
        ))

    return tokens


def lex_text(text: str) -> list[CadenceToken]:
    """
    Tokenize free text into CadenceTokens using word-level analysis.
    Detects TICs (short filler/repeated words), SPIKEs (very common words),
    PHRASEs (multi-word runs), TRANSITIONs (sentence boundaries), SYMBOLs.

    Args:
        text: raw input string.
    Returns:
        list of CadenceTokens.
    """
    if not text or not text.strip():
        return []

    # Split into sentences for transition detection
    sentences = re.split(r'[.!?]+', text)
    all_words: list[str] = []
    sentence_boundaries: set[int] = set()

    for sent in sentences:
        words = re.findall(r"[a-zA-Z']+", sent.lower())
        if words:
            sentence_boundaries.add(len(all_words))
            all_words.extend(words)

    if not all_words:
        return []

    freq_map = Counter(all_words)
    total = len(all_words)

    # Detect phrases: bigrams that appear >1 time
    bigrams = [f"{all_words[i]} {all_words[i+1]}" for i in range(len(all_words) - 1)]
    bigram_freq = Counter(bigrams)
    phrase_set = {bg for bg, cnt in bigram_freq.items() if cnt > 1}

    tokens: list[CadenceToken] = []
    i = 0
    while i < len(all_words):
        word = all_words[i]
        freq = freq_map[word]

        # Transition at sentence boundary
        if i in sentence_boundaries and i > 0:
            tokens.append(CadenceToken(
                token_type="TRANSITION",
                value="[sentence_break]",
                frequency=1,
                timestamp=_now(),
            ))

        # Check if this word starts a phrase
        if i < len(all_words) - 1:
            bigram = f"{word} {all_words[i+1]}"
            if bigram in phrase_set:
                tokens.append(CadenceToken(
                    token_type="PHRASE",
                    value=bigram,
                    frequency=bigram_freq[bigram],
                    timestamp=_now(),
                ))
                i += 2
                continue

        # TIC: very short words repeated often (the, a, i, is...)
        if len(word) <= 3 and freq > total * 0.03:
            tok_type = "TIC"
        else:
            tok_type = _classify_by_freq(freq, total)

        tokens.append(CadenceToken(
            token_type=tok_type,
            value=word,
            frequency=freq,
            timestamp=_now(),
        ))
        i += 1

    return tokens
