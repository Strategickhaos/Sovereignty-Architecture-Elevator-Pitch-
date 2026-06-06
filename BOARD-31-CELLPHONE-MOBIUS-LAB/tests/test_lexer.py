#!/usr/bin/env python3
"""Tests for BOARD-31 Mobius lexer."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from lexer import tokenize, KEYWORD, IDENT, NUMBER, EQUALS, COMMENT


def test_limit_line():
    src = "LIMIT: lim(cpu_load, t, steady_state) = 0.45"
    toks = tokenize(src)
    kinds = [t.kind for t in toks]
    assert KEYWORD in kinds, "LIMIT should tokenize as KEYWORD"
    numbers = [t.value for t in toks if t.kind == NUMBER]
    assert "0.45" in numbers, "0.45 should be tokenized as NUMBER"
    print("  ✓ test_limit_line")


def test_assert_line():
    src = 'ASSERT: if(token_in_url) when(browser_nav) then(fire_antibody BROWSER_TOKEN_IN_REFERRER)'
    toks = tokenize(src)
    keywords = [t.value for t in toks if t.kind == KEYWORD]
    assert "ASSERT" in keywords
    idents = [t.value for t in toks if t.kind == IDENT]
    assert any("token_in_url" in i for i in idents)
    print("  ✓ test_assert_line")


def test_comment_skipped():
    src = "# This is a comment\nLIMIT: lim(x, t, 0) = 0.45"
    toks = tokenize(src, skip_comments=True)
    assert all(t.kind != COMMENT for t in toks), "Comments should be skipped"
    # With skip_comments=False comments appear
    toks_full = tokenize(src, skip_comments=False)
    assert any(t.kind == COMMENT for t in toks_full)
    print("  ✓ test_comment_skipped")


if __name__ == "__main__":
    test_limit_line()
    test_assert_line()
    test_comment_skipped()
    print("\n  All lexer tests passed.")
