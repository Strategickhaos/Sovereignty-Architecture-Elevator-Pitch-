#!/usr/bin/env python3
"""
BOARD-31 ERU Runner — runs ERU case studies on a parsed Mobius AST.

For each equation → {expected, actual, variance, understanding, antibody_candidate}
Writes reports/<number>_exam.yaml
Links CRITICAL variances to MISSING-LINKS seeds.
"""

from __future__ import annotations
import yaml, sys, time
from pathlib import Path

BOARD_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT  = BOARD_ROOT.parent
ML_SEEDS   = REPO_ROOT / "MISSING-LINKS" / "seeds"

GENESIS_INCREMENT = 3449
_tick = 0


def _next_id() -> str:
    global _tick
    ts   = int(time.time() * 1000)
    tick = _tick % GENESIS_INCREMENT
    _tick += 1
    return f"ERU-31-{ts}-{tick}"


def run_equation(eq) -> dict:
    kind = eq.kind if hasattr(eq, "kind") else eq.get("kind", "?")
    name = eq.name if hasattr(eq, "name") else eq.get("name", "?")
    args = eq.args if hasattr(eq, "args") else eq.get("args", [])
    body = eq.body if hasattr(eq, "body") else eq.get("body", "")

    eru = {"id": _next_id(), "equation": name, "kind": kind}

    if kind == "LIMIT":
        eru["expected"]           = f"Function converges as x → {args[2] if len(args)>2 else '?'}"
        eru["actual"]             = f"lim({args[0] if args else '?'}) = {body}"
        eru["variance"]           = "delta between expected convergence and observed value"
        eru["understanding"]      = "Boundary behavior tells us the steady-state of this signal"
        eru["antibody_candidate"] = None
        eru["severity"]           = "LOW"
    elif kind == "DERIV":
        eru["expected"]           = f"Rate of change = {body} per cycle"
        eru["actual"]             = "measured rate from citizen delta"
        eru["variance"]           = "slope divergence from expected rate"
        eru["understanding"]      = "Rate change invariant — if actual diverges > 10%, open drift case"
        eru["antibody_candidate"] = "ORGANISM_RATE_DRIFT" if body else None
        eru["severity"]           = "MEDIUM"
    elif kind == "PIECE":
        eru["expected"]           = "Piecewise condition fires correctly at boundary"
        eru["actual"]             = f"piece({', '.join(str(a) for a in args[:2])})"
        eru["variance"]           = "condition boundary mismatch — wrong branch taken"
        eru["understanding"]      = "Branch logic must be verified against all severity thresholds"
        eru["antibody_candidate"] = None
        eru["severity"]           = "MEDIUM"
    elif kind == "ASSERT":
        eru["expected"]           = "Assertion passes for all matching events"
        eru["actual"]             = f"assertion: {body}"
        eru["variance"]           = "assertion failure — event matched trigger but action not taken"
        eru["understanding"]      = "if/when/then must be tested against live event stream"
        eru["antibody_candidate"] = str(args[1]) if len(args) > 1 else None
        eru["severity"]           = "CRITICAL"
    else:
        eru["expected"]           = body
        eru["actual"]             = "not measured"
        eru["variance"]           = "unknown"
        eru["understanding"]      = "equation type not yet modeled"
        eru["antibody_candidate"] = None
        eru["severity"]           = "LOW"

    return eru


def run_ast(ast, number: str) -> list[dict]:
    equations = ast.equations if hasattr(ast, "equations") else []
    eru_cases = [run_equation(eq) for eq in equations]

    out = BOARD_ROOT / "reports" / f"{number}_exam.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.dump({
        "cellphone": number,
        "eru_cases": eru_cases,
        "total": len(eru_cases),
        "critical": sum(1 for e in eru_cases if e["severity"] == "CRITICAL"),
    }, sort_keys=False))
    print(f"  ERU report → {out}")

    # Emit MISSING-LINKS seeds for CRITICAL cases
    for case in eru_cases:
        if case["severity"] == "CRITICAL":
            _emit_seed(case, number)

    return eru_cases


def _emit_seed(case: dict, number: str):
    ML_SEEDS.mkdir(parents=True, exist_ok=True)
    seed_id = f"INV-MOBIUS-{number}-{case['id']}"
    path    = ML_SEEDS / f"{seed_id}-seed.yaml"
    if path.exists():
        return
    seed = {
        "seed_id":    seed_id,
        "title":      f"Mobius ASSERT variance — {case['equation']}",
        "status":     "OPEN",
        "created":    time.strftime("%Y-%m-%d"),
        "district":   "compiler_city",
        "owner":      "BOARD-31-CELLPHONE-MOBIUS-LAB",
        "expected":   case["expected"],
        "actual":     case["actual"],
        "variance":   case["variance"],
        "understanding": case["understanding"],
        "antibody_candidate": case.get("antibody_candidate"),
        "pmi_delta_estimate": 0.04,
    }
    path.write_text(yaml.dump(seed, sort_keys=False))
    print(f"  MISSING-LINKS seed → {path.name}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BOARD_ROOT / "src"))
    from parser import parse_file
    mobius = sys.argv[1] if len(sys.argv) > 1 else \
             str(BOARD_ROOT / "cellphones" / "5127739959" / "equations.mobius")
    number = Path(mobius).parent.name
    ast    = parse_file(mobius)
    cases  = run_ast(ast, number)
    print(f"\n  {len(cases)} ERU cases  |  "
          f"{sum(1 for c in cases if c['severity']=='CRITICAL')} CRITICAL")
    for c in cases:
        print(f"  [{c['severity']:8s}] {c['equation']:<25} {c['variance'][:60]}")
