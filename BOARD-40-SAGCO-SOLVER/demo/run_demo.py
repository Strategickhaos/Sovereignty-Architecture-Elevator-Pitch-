#!/usr/bin/env python3
"""
Run the SAGCO solver on the Water Street Oyster Bar menu demo.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from solver_pipeline import solve, print_report

MENU_FILE = Path(__file__).parent / "water_street_menu.yaml"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "water_street_menu"

print("\n  Water Street Oyster Bar Menu — SAGCO Solver Demo")
print("  " + "=" * 54)

report = solve(str(MENU_FILE), output_dir=str(OUTPUT_DIR))
print_report(report)

print(f"\n  Demo outputs written to: {OUTPUT_DIR}")
