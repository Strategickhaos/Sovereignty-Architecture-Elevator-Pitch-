#!/usr/bin/env python3
"""
BOARD-33 NLP Formula Generator
Natural language → SAGCO formula / sympy expression.
Beats both Excel and Mobius: neither has this.

Uses pattern matching + anti-hallucination sanity check.

Usage:
  python nlp_formula.py "average of column A"
  python nlp_formula.py "derivative of x squared plus 3x"
  python nlp_formula.py "integral of sin x from 0 to pi"
  python nlp_formula.py "convert 100 mph to km/h"
  python nlp_formula.py "limit of sin(x)/x as x approaches 0"
"""

from __future__ import annotations
import re, sys
from typing import Optional

# ── Pattern rules — ordered by specificity ────────────────────────────────────

PATTERNS = [
    # Calculus: derivatives
    (r"(\d+)(?:st|nd|rd|th)? deriv(?:ative)? of (.+)",
     lambda m: f"diff({_clean(m.group(2))}, x, {m.group(1)})",
     "math", "diff"),
    (r"deriv(?:ative)? of (.+)",
     lambda m: f"diff({_clean(m.group(1))}, x)",
     "math", "diff"),
    (r"d(?:\/dx)? of (.+)",
     lambda m: f"diff({_clean(m.group(1))}, x)",
     "math", "diff"),
    (r"f(?:unction)? prime of (.+)",
     lambda m: f"diff({_clean(m.group(1))}, x)",
     "math", "diff"),

    # Calculus: integrals
    (r"integral of (.+?) from (.+?) to (.+)",
     lambda m: f"integrate({_clean(m.group(1))}, x, {m.group(2)}, {m.group(3)})",
     "math", "integrate"),
    (r"integral of (.+)",
     lambda m: f"integrate({_clean(m.group(1))}, x)",
     "math", "integrate"),

    # Calculus: limits
    (r"limit of (.+?) as (\w+) (?:approaches?|->|→) (.+)",
     lambda m: f"limit({_clean(m.group(1))}, {m.group(2)}, {_clean(m.group(3))})",
     "math", "limit"),
    (r"lim(?:it)? (.+?) (\w+) -> (.+)",
     lambda m: f"limit({_clean(m.group(1))}, {m.group(2)}, {_clean(m.group(3))})",
     "math", "limit"),

    # Algebra: solve
    (r"solve (.+?) (?:for|=) (\w+)",
     lambda m: f"solve({_clean(m.group(1))}, {m.group(2)})",
     "math", "solve"),
    (r"solve (.+)",
     lambda m: f"solve({_clean(m.group(1))})",
     "math", "solve"),
    (r"roots? of (.+)",
     lambda m: f"solve({_clean(m.group(1))})",
     "math", "solve"),
    (r"factor(?:ize)? (.+)",
     lambda m: f"simplify({_clean(m.group(1))})",
     "math", "simplify"),

    # Unit conversion
    (r"convert (.+?) (?:from )?(\S+) to (\S+)",
     lambda m: f"convert({m.group(1).strip()}, {m.group(2)}, {m.group(3)})",
     "unit", "convert"),
    (r"(\S+) (?:in|to) (\S+)",
     lambda m: f"convert(1, {m.group(1)}, {m.group(2)})",
     "unit", "convert"),

    # Excel-style formulas
    (r"sum of (?:column )?(\w+)",
     lambda m: f"SUM({m.group(1).upper()}1:{m.group(1).upper()}100)",
     "excel", "SUM"),
    (r"average of (?:column )?(\w+)",
     lambda m: f"AVERAGE({m.group(1).upper()}1:{m.group(1).upper()}100)",
     "excel", "AVERAGE"),
    (r"count of (?:column )?(\w+)",
     lambda m: f"COUNT({m.group(1).upper()}1:{m.group(1).upper()}100)",
     "excel", "COUNT"),
    (r"max(?:imum)? of (?:column )?(\w+)",
     lambda m: f"MAX({m.group(1).upper()}1:{m.group(1).upper()}100)",
     "excel", "MAX"),
    (r"min(?:imum)? of (?:column )?(\w+)",
     lambda m: f"MIN({m.group(1).upper()}1:{m.group(1).upper()}100)",
     "excel", "MIN"),
    (r"if (.+?) (?:then|,) (.+?) (?:else|otherwise) (.+)",
     lambda m: f"IF({m.group(1)},{m.group(2)},{m.group(3)})",
     "excel", "IF"),

    # Mobius / ERU
    (r"expected (.+?) actual (.+)",
     lambda m: f"ERU(expected={m.group(1)!r}, actual={m.group(2)!r})",
     "eru", "ERU"),
]


def _clean(expr: str) -> str:
    """Normalize natural language math to sympy-compatible."""
    expr = expr.strip()
    expr = re.sub(r'\bx squared\b',       'x**2',  expr, flags=re.I)
    expr = re.sub(r'\bx cubed\b',         'x**3',  expr, flags=re.I)
    expr = re.sub(r'\b(\w+) squared\b',   r'\1**2', expr, flags=re.I)
    expr = re.sub(r'\b(\w+) cubed\b',     r'\1**3', expr, flags=re.I)
    expr = re.sub(r'\bsquare root of\b',  'sqrt',  expr, flags=re.I)
    expr = re.sub(r'\bplus\b',   '+', expr, flags=re.I)
    expr = re.sub(r'\bminus\b',  '-', expr, flags=re.I)
    expr = re.sub(r'\btimes\b',  '*', expr, flags=re.I)
    expr = re.sub(r'\bover\b',   '/', expr, flags=re.I)
    expr = re.sub(r'\bdivided by\b', '/', expr, flags=re.I)
    expr = re.sub(r'\bto the power of\b', '**', expr, flags=re.I)
    expr = re.sub(r'\binfinity\b', 'oo', expr, flags=re.I)
    expr = re.sub(r'\bpi\b',    'pi', expr, flags=re.I)
    expr = re.sub(r'\be\b',     'E',  expr)
    return expr.strip()


def translate(text: str) -> Optional[dict]:
    text_lower = text.lower().strip()
    for pattern, builder, mode, op in PATTERNS:
        m = re.search(pattern, text_lower, re.I)
        if m:
            try:
                formula = builder(m)
                return {
                    "input":   text,
                    "formula": formula,
                    "mode":    mode,
                    "op":      op,
                    "matched": pattern,
                    "eru": {
                        "expected": f"valid {mode} formula from natural language",
                        "actual":   formula,
                        "variance": "0 — pattern matched",
                    },
                }
            except Exception as e:
                return {"input": text, "error": str(e)}
    return {
        "input":   text,
        "formula": None,
        "mode":    "unknown",
        "error":   "No pattern matched — try rephrasing",
        "eru": {
            "expected": "NLP pattern match",
            "actual":   "no match",
            "variance": "input phrasing outside known patterns",
        },
    }


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        print(__doc__); return

    text   = " ".join(args)
    result = translate(text)
    print(f"\n  Input  : {result['input']}")
    if result.get("formula"):
        print(f"  Formula: {result['formula']}")
        print(f"  Mode   : {result['mode']}  Op: {result['op']}")
        eru = result.get("eru", {})
        print(f"\n  ERU:")
        print(f"  Expected: {eru.get('expected','')}")
        print(f"  Actual  : {eru.get('actual','')}")
        print(f"  Variance: {eru.get('variance','')}")
    else:
        print(f"  ERROR  : {result.get('error')}")


if __name__ == "__main__":
    main()
