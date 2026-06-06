#!/usr/bin/env python3
"""Tests for BOARD-31 Mobius parser."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from parser import parse_source as parse, parse_file, MobiusAST, MobiusEquation


SAMPLE = """\
# SAGCO Cellphone Mobius Equations
LIMIT:   lim(cpu_load, t, steady_state) = 0.45
DERIV:   d/dt(citizen_count, t)         = 3449
PIECE:   piece(severity == CRITICAL, open_case, log_only)
ASSERT:  if(token_in_url) when(browser_nav) then(fire_antibody BROWSER_TOKEN_IN_REFERRER)
"""


def test_parse_count():
    ast = parse(SAMPLE)
    assert isinstance(ast, MobiusAST)
    assert len(ast.equations) >= 4, f"Expected ≥4 equations, got {len(ast.equations)}"
    print(f"  ✓ test_parse_count — {len(ast.equations)} equations")


def test_parse_kinds():
    ast   = parse(SAMPLE)
    kinds = [eq.kind for eq in ast.equations]
    assert "LIMIT"  in kinds
    assert "DERIV"  in kinds
    assert "PIECE"  in kinds
    assert "ASSERT" in kinds
    print(f"  ✓ test_parse_kinds — {kinds}")


def test_parse_file():
    board = Path(__file__).parents[1]
    mobius = board / "cellphones" / "5127739959" / "equations.mobius"
    if not mobius.exists():
        print("  ⚠ test_parse_file — equations.mobius not found, skipping")
        return
    ast = parse_file(str(mobius))
    assert len(ast.equations) >= 1
    print(f"  ✓ test_parse_file — {len(ast.equations)} equations from file")


if __name__ == "__main__":
    test_parse_count()
    test_parse_kinds()
    test_parse_file()
    print("\n  All parser tests passed.")
