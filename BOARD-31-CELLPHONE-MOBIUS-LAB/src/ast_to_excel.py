#!/usr/bin/env python3
"""
BOARD-31 AST → Excel (CSV) renderer.

Columns: Equation | Kind | Expected | Actual | Variance | ERU_Note
"""

from __future__ import annotations
import csv, sys
from pathlib import Path

BOARD_ROOT = Path(__file__).resolve().parents[1]


def ast_to_rows(equations: list) -> list[dict]:
    rows = []
    for eq in equations:
        kind = eq.kind if hasattr(eq, "kind") else eq.get("kind", "?")
        name = eq.name if hasattr(eq, "name") else eq.get("name", "?")
        args = eq.args if hasattr(eq, "args") else eq.get("args", [])
        body = eq.body if hasattr(eq, "body") else eq.get("body", "")

        if kind == "LIMIT":
            expected = f"lim({args[0] if args else '?'}, {args[2] if len(args)>2 else '?'})" if args else body
            actual   = "observed at boundary"
            variance = "delta from limit"
            note     = "boundary convergence check"
        elif kind == "DERIV":
            expected = f"d/dt rate = {body}"
            actual   = "measured rate"
            variance = "slope divergence"
            note     = "rate-of-change ERU"
        elif kind == "PIECE":
            expected = "branch fires on condition"
            actual   = "branch result"
            variance = "condition mismatch"
            note     = "piecewise branch check"
        elif kind == "ASSERT":
            expected = "assertion passes"
            actual   = "assertion result"
            variance = "failure mode"
            note     = "if/when/then gate"
        elif kind == "INTEGRAL":
            expected = f"integral over [{args[1] if len(args)>1 else 'a'},{args[2] if len(args)>2 else 'b'}]"
            actual   = "computed area"
            variance = "cumulative drift"
            note     = "area under variance curve"
        else:
            expected = body
            actual   = "?"
            variance = "?"
            note     = ""

        rows.append({
            "Equation": name,
            "Kind":     kind,
            "Expected": expected,
            "Actual":   actual,
            "Variance": variance,
            "ERU_Note": note,
        })
    return rows


def write_csv(equations: list, out_path: Path):
    rows = ast_to_rows(equations)
    fieldnames = ["Equation", "Kind", "Expected", "Actual", "Variance", "ERU_Note"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  Excel view → {out_path}")
    return rows


def print_table(rows: list[dict]):
    print(f"\n  {'Equation':<25} {'Kind':<10} {'Expected':<35} {'Variance'}")
    print("  " + "-" * 100)
    for r in rows:
        print(f"  {r['Equation']:<25} {r['Kind']:<10} {r['Expected']:<35} {r['Variance']}")


if __name__ == "__main__":
    from parser import parse_file
    mobius_file = sys.argv[1] if len(sys.argv) > 1 else \
                  str(BOARD_ROOT / "cellphones" / "5127739959" / "equations.mobius")
    ast = parse_file(mobius_file)
    number = Path(mobius_file).parent.name
    out = BOARD_ROOT / "reports" / f"{number}_excel_view.csv"
    rows = write_csv(ast.equations, out)
    print_table(rows)
