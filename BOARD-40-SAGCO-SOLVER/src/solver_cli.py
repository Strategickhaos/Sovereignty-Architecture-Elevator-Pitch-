#!/usr/bin/env python3
"""
BOARD-40-SAGCO-SOLVER — solver_cli.py
Universal file solver CLI.

Usage:
  python solver_cli.py <file>
  python solver_cli.py --demo
  python solver_cli.py <file> --passes frequency,flashcards,eru
  python solver_cli.py <file> --out DIR
"""

import argparse
import sys
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

DEMO_FILE = Path(__file__).parent.parent / "demo" / "water_street_menu.yaml"


def main():
    parser = argparse.ArgumentParser(
        description="sagco solve <anything> — universal file pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("file", nargs="?", help="Input file to solve")
    parser.add_argument("--demo", action="store_true", help="Run on built-in Water Street menu demo")
    parser.add_argument("--passes", help="Comma-separated pass names to run (default: all)")
    parser.add_argument("--out", metavar="DIR", help="Custom output directory")

    args = parser.parse_args()

    if not args.file and not args.demo:
        parser.print_help()
        sys.exit(1)

    from solver_pipeline import solve, print_report

    target = str(DEMO_FILE) if args.demo else args.file

    if not Path(target).exists():
        print(f"  ERROR: file not found: {target}")
        sys.exit(1)

    passes = [p.strip() for p in args.passes.split(",")] if args.passes else None

    print(f"\n  sagco solve → {target}")
    print(f"  passes: {passes or 'all'}\n")

    report = solve(target, output_dir=args.out, passes=passes)
    print_report(report)


if __name__ == "__main__":
    main()
