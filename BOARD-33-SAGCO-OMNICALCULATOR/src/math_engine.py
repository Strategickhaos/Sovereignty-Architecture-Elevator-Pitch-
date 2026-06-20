#!/usr/bin/env python3
"""
BOARD-33 Math Engine — CAS core (sympy)
Beats Mobius on: symbolic simplification, limits, derivatives, integrals,
                 ODEs, matrix algebra, piecewise, statistics, roots.
Beats Excel on:  anything symbolic.

Usage:
  python math_engine.py simplify "x**2 + 2*x + 1"
  python math_engine.py limit "sin(x)/x" x 0
  python math_engine.py diff "x**3 + 2*x" x
  python math_engine.py diff "x**3 + 2*x" x 3          # 3rd derivative
  python math_engine.py integrate "x**2" x
  python math_engine.py integrate "x**2" x 0 1          # definite
  python math_engine.py solve "x**2 - 4"
  python math_engine.py solve-system "x+y=5" "x-y=1"
  python math_engine.py matrix "[[1,2],[3,4]]" det
  python math_engine.py matrix "[[1,2],[3,4]]" inv
  python math_engine.py stats normal 1.96
  python math_engine.py plot "sin(x)" -10 10
  python math_engine.py piece "x < 0: -x, x >= 0: x" 3
"""

from __future__ import annotations
import sys, re
from typing import Any

try:
    import sympy as sp
    from sympy import (
        symbols, sympify, simplify, factor, expand, limit, diff, integrate,
        solve, Matrix, Symbol, Piecewise, oo, pi, E, I,
        sin, cos, tan, exp, log, sqrt, Abs,
        dsolve, Function,
        S, latex, pretty,
    )
    from sympy.stats import Normal, cdf, density
    SYMPY_OK = True
except ImportError:
    SYMPY_OK = False


def _sym(expr_str: str) -> Any:
    """Parse expression string — auto-declare single-letter symbols."""
    local_dict = {
        "x": symbols("x"), "y": symbols("y"), "t": symbols("t"),
        "n": symbols("n"), "a": symbols("a"), "b": symbols("b"),
        "sin": sin, "cos": cos, "tan": tan, "exp": exp,
        "log": log, "ln": log, "sqrt": sqrt, "pi": pi, "e": E,
        "oo": oo, "inf": oo,
    }
    return sympify(expr_str, locals=local_dict)


def _print(expr, label: str = ""):
    if label:
        print(f"  {label}:")
    if SYMPY_OK:
        print(f"    {pretty(expr, use_unicode=True)}")
        print(f"    LaTeX: {latex(expr)}")
    else:
        print(f"    {expr}")


# ── ERU wrapper — every operation emits ERU ──────────────────────────────────

def _eru(operation: str, expected: str, actual: Any, variance: Any = None):
    print(f"\n  ╔═ ERU ══════════════════════════════════════╗")
    print(f"  ║ Operation : {operation}")
    print(f"  ║ Expected  : {expected}")
    print(f"  ║ Actual    : {actual}")
    if variance is not None:
        print(f"  ║ Variance  : {variance}")
    print(f"  ╚════════════════════════════════════════════╝")


# ── Operations ───────────────────────────────────────────────────────────────

def op_simplify(expr_str: str) -> Any:
    expr = _sym(expr_str)
    result = simplify(expr)
    factored = factor(expr)
    expanded = expand(expr)
    print(f"\n  Simplify: {expr_str}")
    print(f"  simplified : {pretty(result)}")
    print(f"  factored   : {pretty(factored)}")
    print(f"  expanded   : {pretty(expanded)}")
    print(f"  LaTeX      : {latex(result)}")
    _eru("simplify", f"simplified form of {expr_str}", str(result),
         "none" if str(result) == str(expr) else f"reduced from {expr_str}")
    return result


def op_limit(expr_str: str, var: str, to: str) -> Any:
    x   = symbols(var)
    to_ = _sym(to)
    expr= _sym(expr_str)
    result = limit(expr, x, to_)
    print(f"\n  lim({expr_str}, {var}→{to}) = {pretty(result)}")
    print(f"  LaTeX: \\lim_{{{var}\\to {latex(to_)}}} {latex(expr)} = {latex(result)}")
    _eru(f"limit as {var}→{to}", f"finite or ±∞ limit exists", str(result))
    return result


def op_diff(expr_str: str, var: str = "x", order: int = 1) -> Any:
    x    = symbols(var)
    expr = _sym(expr_str)
    result = diff(expr, x, order)
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(order, f"{order}th")
    print(f"\n  d^{order}/d{var}^{order} ({expr_str})")
    print(f"  {ordinal} derivative : {pretty(result)}")
    print(f"  LaTeX: {latex(result)}")
    _eru(f"{ordinal} derivative wrt {var}", "derivative exists and is closed-form",
         str(result))
    return result


def op_integrate(expr_str: str, var: str = "x",
                 lower: str = None, upper: str = None) -> Any:
    x    = symbols(var)
    expr = _sym(expr_str)
    if lower is not None and upper is not None:
        a, b = _sym(lower), _sym(upper)
        result = integrate(expr, (x, a, b))
        print(f"\n  ∫[{lower},{upper}] {expr_str} d{var} = {pretty(result)}")
    else:
        result = integrate(expr, x)
        print(f"\n  ∫ {expr_str} d{var} = {pretty(result)} + C")
    print(f"  LaTeX: {latex(result)}")
    _eru("integrate", "closed-form antiderivative or definite value", str(result))
    return result


def op_solve(expr_str: str, var: str = "x") -> Any:
    x    = symbols(var)
    # Support "f(x) = g(x)" form
    if "=" in expr_str:
        lhs, rhs = expr_str.split("=", 1)
        expr = _sym(lhs) - _sym(rhs)
    else:
        expr = _sym(expr_str)
    result = solve(expr, x)
    print(f"\n  Solve: {expr_str} = 0")
    print(f"  Solutions: {result}")
    for r in result:
        print(f"    {var} = {pretty(r)}  (LaTeX: {latex(r)})")
    _eru("solve", "all roots found", str(result))
    return result


def op_solve_system(*equations: str) -> Any:
    syms = symbols("x y z w")
    eqs  = []
    for eq_str in equations:
        if "=" in eq_str:
            lhs, rhs = eq_str.split("=", 1)
            eqs.append(_sym(lhs) - _sym(rhs))
        else:
            eqs.append(_sym(eq_str))
    used = list(syms[:len(eqs)])
    result = solve(eqs, used)
    print(f"\n  Solve system:")
    for eq in equations:
        print(f"    {eq}")
    print(f"  Solution: {result}")
    _eru("solve-system", "unique solution or solution set", str(result))
    return result


def op_matrix(mat_str: str, operation: str = "det") -> Any:
    import ast
    rows = ast.literal_eval(mat_str)
    M    = Matrix(rows)
    print(f"\n  Matrix:")
    print(f"  {pretty(M)}")
    if operation == "det":
        result = M.det()
        print(f"  det = {result}")
    elif operation == "inv":
        result = M.inv()
        print(f"  inv =\n  {pretty(result)}")
    elif operation == "eigenvalues":
        result = M.eigenvals()
        print(f"  eigenvalues = {result}")
    elif operation == "rref":
        result, pivots = M.rref()
        print(f"  rref =\n  {pretty(result)}")
        print(f"  pivots = {pivots}")
    else:
        result = M
    _eru(f"matrix.{operation}", "well-defined result", str(result))
    return result


def op_stats(distribution: str, *args) -> Any:
    if distribution == "normal":
        # args: [mean, std, x] or [x] (assume N(0,1))
        if len(args) == 1:
            mean, std, x_val = 0.0, 1.0, float(args[0])
        elif len(args) == 3:
            mean, std, x_val = float(args[0]), float(args[1]), float(args[2])
        else:
            mean, std, x_val = 0.0, 1.0, float(args[0])

        X      = Normal("X", mean, std)
        p_val  = float(cdf(X)(x_val).evalf())
        z_pdf  = float(density(X)(x_val).evalf())
        print(f"\n  Normal({mean}, {std})")
        print(f"  P(X ≤ {x_val}) = {p_val:.6f}")
        print(f"  pdf({x_val})   = {z_pdf:.6f}")
        _eru("stats.normal.cdf", f"CDF value for x={x_val}", f"{p_val:.6f}")
        return p_val
    else:
        print(f"  Unknown distribution: {distribution}")


def op_plot(expr_str: str, x_min: float = -10, x_max: float = 10,
            width: int = 60, height: int = 12) -> None:
    """ASCII plot."""
    import math
    x  = symbols("x")
    expr = _sym(expr_str)
    fn   = sp.lambdify(x, expr, "math")

    xs = [x_min + (x_max - x_min) * i / (width - 1) for i in range(width)]
    ys = []
    for xi in xs:
        try:
            yi = fn(xi)
            ys.append(yi if math.isfinite(yi) else None)
        except Exception:
            ys.append(None)

    valid = [y for y in ys if y is not None]
    if not valid:
        print("  Cannot plot — no valid values in range")
        return
    y_min, y_max = min(valid), max(valid)
    if y_min == y_max:
        y_min -= 1; y_max += 1

    print(f"\n  Plot: {expr_str}  x∈[{x_min},{x_max}]")
    print(f"  {'─'*width}")
    grid = [[" "] * width for _ in range(height)]
    for col, y in enumerate(ys):
        if y is None:
            continue
        row = int((y_max - y) / (y_max - y_min) * (height - 1))
        row = max(0, min(height - 1, row))
        grid[row][col] = "█"
    for row in grid:
        print("  │" + "".join(row) + "│")
    print(f"  {'─'*width}")
    print(f"  y ∈ [{y_min:.3g}, {y_max:.3g}]")


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    op   = args[0].lower()
    rest = args[1:]

    if not SYMPY_OK:
        print("  ERROR: sympy not installed. Run: pip install sympy")
        return

    if op == "simplify" and rest:
        op_simplify(rest[0])
    elif op == "limit" and len(rest) >= 3:
        op_limit(rest[0], rest[1], rest[2])
    elif op == "diff" and rest:
        order = int(rest[2]) if len(rest) >= 3 else 1
        var   = rest[1] if len(rest) >= 2 else "x"
        op_diff(rest[0], var, order)
    elif op == "integrate" and rest:
        if len(rest) >= 4:
            op_integrate(rest[0], rest[1], rest[2], rest[3])
        else:
            var = rest[1] if len(rest) >= 2 else "x"
            op_integrate(rest[0], var)
    elif op == "solve" and rest:
        op_solve(rest[0])
    elif op == "solve-system" and rest:
        op_solve_system(*rest)
    elif op == "matrix" and len(rest) >= 2:
        op_matrix(rest[0], rest[1])
    elif op == "stats" and rest:
        op_stats(rest[0], *rest[1:])
    elif op == "plot" and rest:
        x_min = float(rest[1]) if len(rest) > 1 else -10
        x_max = float(rest[2]) if len(rest) > 2 else 10
        op_plot(rest[0], x_min, x_max)
    else:
        print(f"  Unknown operation: {op}")
        print(__doc__)


if __name__ == "__main__":
    main()
