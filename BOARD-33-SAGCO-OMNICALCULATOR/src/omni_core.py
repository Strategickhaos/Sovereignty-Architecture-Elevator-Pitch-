#!/usr/bin/env python3
"""
BOARD-33 SAGCO OmniCalculator — Core Dispatcher

Beats Excel + Mobius combined.
All 33 missing links addressed.
Every operation runs through ERU + anti-hallucination sanity check.

Usage:
  sagco omni diff "x**3 + 2*x" x
  sagco omni diff "x**3 + 2*x" x 3          ← 3rd derivative (Mobius Q2!)
  sagco omni integrate "x**2" x 0 1
  sagco omni limit "sin(x)/x" x 0
  sagco omni solve "x**2 - 4"
  sagco omni solve-system "x+y=5" "x-y=1"
  sagco omni simplify "x**2 + 2*x + 1"
  sagco omni matrix "[[1,2],[3,4]]" det
  sagco omni stats normal 1.96
  sagco omni plot "sin(x)" -10 10
  sagco omni convert 100 mph km/h
  sagco omni ast "SUM(A1:A10) + IF(B1>0,B1,0)"
  sagco omni explain "SUM(A1:A10)/COUNT(A1:A10)"
  sagco omni ask "derivative of x squared plus 3x"
  sagco omni sheet --demo
  sagco omni sanity "any claim"
  sagco omni missing-links              ← show the 33 catalog
"""

from __future__ import annotations
import sys
from pathlib import Path

BOARD_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT  = BOARD_ROOT.parent
SRC        = BOARD_ROOT / "src"

BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║  SAGCO OmniCalculator — BOARD-33                                ║
║  CAS · Spreadsheet · Units · Compiler · ERU · NLP · Portfolio  ║
║  Beats Excel. Beats Mobius. Sovereign Truth Score enforced.     ║
╚══════════════════════════════════════════════════════════════════╝
"""

MATH_OPS   = {"diff", "integrate", "limit", "solve", "solve-system",
               "simplify", "factor", "expand", "matrix", "stats", "plot",
               "ode"}
CELL_OPS   = {"sheet", "import", "pivot"}
UNIT_OPS   = {"convert", "units"}
COMP_OPS   = {"ast", "compile", "explain", "mobius"}
NLP_OPS    = {"ask", "nl", "natural"}
SANITY_OPS = {"sanity", "check"}


def _run_math(op: str, args: list[str]):
    sys.path.insert(0, str(SRC))
    from math_engine import main as math_main
    math_main([op] + args)


def _run_cell(op: str, args: list[str]):
    sys.path.insert(0, str(SRC))
    from cell_engine import main as cell_main
    if op == "sheet":
        cell_main(["--demo"] + args)
    elif op == "import":
        cell_main(["--import"] + args)
    elif op == "pivot":
        cell_main(["--pivot"] + args)


def _run_unit(op: str, args: list[str]):
    sys.path.insert(0, str(SRC))
    from unit_converter import main as unit_main
    if op == "units":
        unit_main(["--list"])
    else:
        unit_main(args)


def _run_compiler(op: str, args: list[str]):
    sys.path.insert(0, str(SRC))
    from formula_compiler import main as comp_main
    comp_main([op] + args)


def _run_nlp(args: list[str]):
    sys.path.insert(0, str(SRC))
    from nlp_formula import main as nlp_main
    nlp_main(args)


def _run_sanity(args: list[str]):
    import subprocess
    agent = REPO_ROOT / "sagco-agents" / "agent_sanity.py"
    subprocess.run([sys.executable, str(agent)] + args)


def _show_missing_links():
    import yaml
    catalog = BOARD_ROOT / "manifests" / "missing_links_catalog.yaml"
    if not catalog.exists():
        print("  Catalog not found"); return
    data = yaml.safe_load(catalog.read_text())
    links = data.get("missing_links", [])
    impl  = sum(1 for l in links if l.get("status") == "IMPLEMENTED")
    partial = sum(1 for l in links if l.get("status") == "PARTIAL")
    print(f"\n  THE 33 MISSING LINKS — SAGCO vs Excel vs Mobius")
    print(f"  {'─'*65}")
    print(f"  {'ID':<14} {'NAME':<40} {'BEATS':<8} STATUS")
    print(f"  {'─'*65}")
    for link in links:
        sym = "✓" if link.get("status") == "IMPLEMENTED" else \
              "~" if link.get("status") == "PARTIAL"     else "✗"
        print(f"  {sym} {link['id']:<13} {link['name']:<40} {link.get('beats','?'):<8} {link.get('status','?')}")
    print(f"\n  Implemented: {impl}/33   Partial: {partial}/33")


def _inspect_func(name: str):
    from formula_compiler import FUNC_EXPLANATIONS, EXCEL_FUNCTIONS
    from unit_converter import UNITS
    from math_engine import main as _  # ensure sympy check

    name_upper = name.upper()
    if name_upper in FUNC_EXPLANATIONS:
        print(f"\n  {name_upper}: {FUNC_EXPLANATIONS[name_upper]}")
    elif name_upper in EXCEL_FUNCTIONS:
        print(f"\n  {name_upper}: Known Excel function — use 'explain' for ERU breakdown")
    elif name.lower() in {u.lower() for u in UNITS}:
        u = UNITS[name]
        print(f"\n  Unit: {name}  →  {u[2]} (SI factor: {u[0]}, base: {u[1]})")
    else:
        print(f"\n  '{name}' not found in functions or units")


def dispatch(op: str, args: list[str]):
    if op in MATH_OPS:
        _run_math(op, args)
    elif op in CELL_OPS:
        _run_cell(op, args)
    elif op in UNIT_OPS:
        _run_unit(op, args)
    elif op in COMP_OPS:
        _run_compiler(op, args)
    elif op in NLP_OPS:
        _run_nlp(args)
    elif op in SANITY_OPS:
        _run_sanity(args)
    elif op == "inspect":
        _inspect_func(args[0] if args else "")
    elif op in ("missing-links", "ml", "33"):
        _show_missing_links()
    else:
        print(f"  Unknown omni operation: {op}")
        print(f"  Math   : {', '.join(sorted(MATH_OPS))}")
        print(f"  Cell   : {', '.join(sorted(CELL_OPS))}")
        print(f"  Units  : {', '.join(sorted(UNIT_OPS))}")
        print(f"  Compile: {', '.join(sorted(COMP_OPS))}")
        print(f"  NLP    : {', '.join(sorted(NLP_OPS))}")
        print(f"  Other  : inspect, missing-links, sanity")


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]

    print(BANNER)

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    dispatch(args[0], args[1:])


if __name__ == "__main__":
    main()
