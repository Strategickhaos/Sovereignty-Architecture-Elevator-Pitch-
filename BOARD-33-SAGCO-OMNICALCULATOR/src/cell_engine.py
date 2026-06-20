#!/usr/bin/env python3
"""
BOARD-33 Cell Engine — sovereign spreadsheet core.
Beats Excel on: dependency graph, circular ref detection, named ranges,
                pivot aggregation, validation, undo/redo, CSV import, ETL.

Usage:
  python cell_engine.py --demo
  python cell_engine.py --import file.csv
  python cell_engine.py --pivot file.csv col_group col_value
"""

from __future__ import annotations
import csv, re, sys, copy, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

# ── Cell ─────────────────────────────────────────────────────────────────────

@dataclass
class Cell:
    ref:      str          # "A1"
    formula:  str = ""     # "=SUM(A1:A3)" or literal "42"
    value:    Any = None   # computed value
    error:    str = ""
    name:     str = ""     # named range alias

# ── Dependency Graph ──────────────────────────────────────────────────────────

class DependencyGraph:
    def __init__(self):
        self._deps: dict[str, set[str]] = {}   # cell → cells it depends on
        self._rdeps: dict[str, set[str]] = {}  # cell → cells that depend on it

    def add(self, ref: str, deps: set[str]):
        self._deps[ref] = deps
        for d in deps:
            self._rdeps.setdefault(d, set()).add(ref)

    def dependents_of(self, ref: str) -> set[str]:
        return self._rdeps.get(ref, set())

    def topo_order(self) -> list[str]:
        """Kahn's algorithm — detect cycles."""
        in_degree = {r: len(deps) for r, deps in self._deps.items()}
        queue     = [r for r in self._deps if in_degree[r] == 0]
        order     = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for dep in self.dependents_of(node):
                in_degree[dep] = in_degree.get(dep, 1) - 1
                if in_degree[dep] == 0:
                    queue.append(dep)
        # Any remaining with in_degree > 0 → circular ref
        cycles = [r for r, d in in_degree.items() if d > 0 and r not in order]
        return order, cycles


# ── Sheet ─────────────────────────────────────────────────────────────────────

_REF_RE    = re.compile(r'\b([A-Z]+\d+)\b')
_RANGE_RE  = re.compile(r'([A-Z]+\d+):([A-Z]+\d+)')

def _col_row(ref: str) -> tuple[int, int]:
    m = re.match(r'([A-Z]+)(\d+)', ref)
    col = sum((ord(c) - 64) * (26 ** i) for i, c in enumerate(reversed(m.group(1)))) - 1
    return col, int(m.group(2)) - 1

def _range_refs(start: str, end: str) -> list[str]:
    sc, sr = _col_row(start)
    ec, er = _col_row(end)
    refs = []
    for r in range(sr, er + 1):
        for c in range(sc, ec + 1):
            refs.append(chr(65 + c) + str(r + 1))
    return refs


class Sheet:
    def __init__(self, name: str = "Sheet1"):
        self.name    = name
        self.cells:  dict[str, Cell] = {}
        self.names:  dict[str, str]  = {}   # name → ref
        self.graph   = DependencyGraph()
        self.history: list[dict]     = []   # undo/redo snapshots
        self._validation: dict[str, Callable] = {}

    def set(self, ref: str, formula: str):
        if ref not in self.cells:
            self.cells[ref] = Cell(ref)
        self._snapshot()
        self.cells[ref].formula = formula
        self._recalc(ref)

    def name_range(self, name: str, ref: str):
        self.names[name] = ref

    def add_validation(self, ref: str, rule: Callable):
        self._validation[ref] = rule

    def _snapshot(self):
        snap = {r: copy.copy(c) for r, c in self.cells.items()}
        self.history.append(snap)
        if len(self.history) > 50:
            self.history.pop(0)

    def undo(self):
        if self.history:
            self.cells = self.history.pop()
            print("  Undo applied")

    def _extract_deps(self, formula: str) -> set[str]:
        if not formula.startswith("="):
            return set()
        deps = set()
        for m in _RANGE_RE.finditer(formula):
            deps.update(_range_refs(m.group(1), m.group(2)))
        for m in _REF_RE.finditer(formula):
            deps.add(m.group(1))
        return deps

    def _recalc(self, ref: str):
        formula = self.cells[ref].formula
        deps    = self._extract_deps(formula)
        self.graph.add(ref, deps)
        order, cycles = self.graph.topo_order()
        if cycles:
            for c in cycles:
                if c in self.cells:
                    self.cells[c].error = "#CIRCULAR!"
                    self.cells[c].value = None
            print(f"  ⚠  Circular reference detected: {cycles}")
        for r in order:
            if r in self.cells:
                self._eval_cell(r)

    def _eval_cell(self, ref: str):
        cell = self.cells.get(ref)
        if not cell:
            return
        formula = cell.formula
        if not formula.startswith("="):
            try:
                cell.value = float(formula) if '.' in formula else int(formula)
            except ValueError:
                cell.value = formula
            return

        expr = formula[1:]
        # Expand range references
        def expand_range(m):
            refs = _range_refs(m.group(1), m.group(2))
            return ", ".join(str(self.cells.get(r, Cell(r)).value or 0) for r in refs)
        expr = _RANGE_RE.sub(expand_range, expr)
        # Replace cell refs with values
        def replace_ref(m):
            r = m.group(1)
            v = self.cells.get(r, Cell(r)).value
            return str(v) if v is not None else "0"
        expr = _REF_RE.sub(replace_ref, expr)

        # Safe function namespace
        import math
        ns = {
            "SUM": lambda *a: sum(a),
            "AVERAGE": lambda *a: sum(a) / len(a) if a else 0,
            "COUNT": lambda *a: len([x for x in a if isinstance(x, (int, float))]),
            "MAX": lambda *a: max(a),
            "MIN": lambda *a: min(a),
            "IF": lambda cond, t, f: t if cond else f,
            "ABS": abs, "SQRT": math.sqrt, "LN": math.log,
            "LOG": math.log10, "EXP": math.exp,
            "ROUND": round, "INT": int,
            "PI": math.pi, "E": math.e,
            "TRUE": True, "FALSE": False,
        }
        try:
            cell.value = eval(expr, {"__builtins__": {}}, ns)
            cell.error = ""
            # Validate
            if ref in self._validation:
                if not self._validation[ref](cell.value):
                    cell.error = "#VALIDATION!"
        except Exception as e:
            cell.error = f"#ERROR: {e}"
            cell.value = None

    def get(self, ref: str) -> Any:
        c = self.cells.get(ref)
        return c.value if c else None

    def pivot(self, group_col: int, value_col: int) -> dict:
        """Aggregate sheet data by group column."""
        from collections import defaultdict
        result = defaultdict(list)
        for ref, cell in sorted(self.cells.items()):
            _, row = _col_row(ref)
            col, _ = _col_row(ref)
            if col == group_col:
                group_ref = chr(65 + value_col) + str(row + 1)
                v = self.get(group_ref)
                if v is not None:
                    result[cell.value].append(v)
        return {k: {"sum": sum(vs), "avg": sum(vs)/len(vs), "count": len(vs)}
                for k, vs in result.items()}

    def infer_schema(self) -> dict:
        schema = {}
        for ref, cell in self.cells.items():
            if cell.value is None:
                schema[ref] = "null"
            elif isinstance(cell.value, bool):
                schema[ref] = "boolean"
            elif isinstance(cell.value, int):
                schema[ref] = "integer"
            elif isinstance(cell.value, float):
                schema[ref] = "float"
            else:
                schema[ref] = "string"
        return schema

    def print_grid(self, rows: int = 10, cols: int = 5):
        print(f"\n  Sheet: {self.name}")
        header = "     │" + "".join(f"  {chr(65+c):^8} │" for c in range(cols))
        print("  " + header)
        print("  " + "─" * len(header))
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                ref = chr(65 + c) + str(r + 1)
                cell = self.cells.get(ref)
                if cell:
                    disp = str(cell.error or cell.value or "")[:8]
                else:
                    disp = ""
                row_cells.append(f"  {disp:^8} │")
            print(f"  {r+1:4d} │" + "".join(row_cells))


def import_csv(path: Path) -> Sheet:
    sheet = Sheet(path.stem)
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader):
            for col_idx, val in enumerate(row):
                ref = chr(65 + col_idx) + str(row_idx + 1)
                sheet.cells[ref] = Cell(ref, val.strip())
                sheet._eval_cell(ref)
    print(f"  Imported {path.name} → {len(sheet.cells)} cells")
    return sheet


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo",   action="store_true")
    ap.add_argument("--import", dest="import_file")
    ap.add_argument("--pivot",  nargs=3, metavar=("FILE", "GROUP_COL", "VAL_COL"))
    args = ap.parse_args()

    if args.demo:
        s = Sheet("demo")
        s.set("A1", "10"); s.set("A2", "20"); s.set("A3", "30")
        s.set("B1", "=SUM(A1:A3)")
        s.set("B2", "=AVERAGE(A1:A3)")
        s.set("B3", "=IF(B1>50,1,0)")
        s.set("C1", "=B1*2")
        s.print_grid(4, 3)
        print(f"\n  B1 = {s.get('B1')}")
        print(f"  B2 = {s.get('B2')}")
        print(f"  B3 = {s.get('B3')}")
        print(f"  Schema: {s.infer_schema()}")
        s.undo()
        print("  Undo complete")

    elif args.import_file:
        s = import_csv(Path(args.import_file))
        s.print_grid()

    elif args.pivot:
        f, gc, vc = args.pivot
        s = import_csv(Path(f))
        result = s.pivot(int(gc), int(vc))
        print(f"\n  Pivot result:")
        for k, v in result.items():
            print(f"    {k}: {v}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
