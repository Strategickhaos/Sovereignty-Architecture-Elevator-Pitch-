#!/usr/bin/env python3
"""
BOARD-43 — MathML Generator CLI
Usage:
  python3 mathml_gen.py gate11          run Gate 11 implicit diff problem
  python3 mathml_gen.py gate11 --compact  single-line output for Mobius paste
  python3 mathml_gen.py --list          list available problems
"""
import sys
import os

PROBLEMS = {
    "gate11": "problems.gate11_implicit_diff",
}

def main():
    args = sys.argv[1:]
    if not args or "--list" in args:
        print("Available problems:")
        for k in PROBLEMS:
            print(f"  {k}")
        return

    name = args[0]
    if name not in PROBLEMS:
        print(f"Unknown problem: {name}")
        print("Run with --list to see available problems.")
        sys.exit(1)

    sys.path.insert(0, os.path.dirname(__file__))
    mod = __import__(PROBLEMS[name], fromlist=["build"])
    tree = mod.build()

    from src.render import render, render_compact
    if "--compact" in args:
        out = render_compact(tree)
    else:
        out = render(tree)

    print(out)
    print(f"\n{'─'*60}", file=sys.stderr)
    print(f"BOARD-43 MathML Generator — {name}", file=sys.stderr)
    print(f"Paste the output above into Mobius → Equation Editor → MathML/LaTeX tab", file=sys.stderr)


if __name__ == "__main__":
    main()
