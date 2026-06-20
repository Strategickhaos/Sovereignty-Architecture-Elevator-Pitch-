"""
SAGCO-UNIVERSITY
sagco_boardgen.py — CLI entry point for the SAGCO University board generator.

Usage:
  python sagco_boardgen.py generate --module "5home2266305sn" --text "..."
  python sagco_boardgen.py generate --file assignment.txt --module "mod5"
  python sagco_boardgen.py demo      # builds a demo board from calc content
  python sagco_boardgen.py lattice   # builds lattice from all modules in homework/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure src/ is importable when called directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml

from atom_builder import text_to_atoms
from bond_engine import compute_bonds
from molecule_builder import build_molecule
from lattice_builder import build_lattice, find_cross_module_bonds
from board_generator import generate_board, generate_from_file


# ── Paths ─────────────────────────────────────────────────────────────────────

SRC_DIR      = Path(__file__).resolve().parent
UNIV_ROOT    = SRC_DIR.parent
HOMEWORK_DIR = UNIV_ROOT / "homework"
OUTPUT_DIR   = UNIV_ROOT / "output"


# ── Demo content ──────────────────────────────────────────────────────────────

DEMO_TEXT = """\
Q1: Find the critical points of f(x) = 10x^(2/3) + x^(5/3)
Q2: Classify each critical point as local max, local min, or saddle point
Q3: Find absolute extrema on [-5, 5]
Definition: A critical point occurs where f'(x) = 0 or f'(x) is undefined
Formula: Bond Order = (Bonding Electrons - Antibonding Electrons) / 2
Example: For f(x) = x^2 - 4, f'(x) = 2x, critical point at x=0
"""


# ── Banner ────────────────────────────────────────────────────────────────────

def _banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║  SAGCO UNIVERSITY — Board Generator                     ║
║  district: genesis  |  role: university_factory         ║
╚══════════════════════════════════════════════════════════╝
""")


# ── Sub-commands ──────────────────────────────────────────────────────────────

def cmd_generate(args):
    """Generate a board from text or file."""
    module = args.module or "unknown_module"

    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"  ERROR: file not found: {p}", file=sys.stderr)
            sys.exit(1)
        out_dir = OUTPUT_DIR / module
        eru = generate_from_file(str(p), out_dir)
        print(f"  Module   : {module}")
    elif args.text:
        out_dir = OUTPUT_DIR / module
        eru = generate_board(args.text, module, out_dir)
    else:
        print("  ERROR: provide --text or --file", file=sys.stderr)
        sys.exit(1)

    print(f"  Output   : {out_dir}")
    print(f"  Atoms    : {eru['actual']['atoms']}")
    print(f"  Bonds    : {eru['actual']['bonds']}")
    print(f"  Stability: {eru['actual']['stability']}")
    print(f"  ERU      : {eru['status']}  (variance={eru['variance']})")
    if eru["actual"].get("missing_atoms"):
        print("  Missing prereqs:")
        for m in eru["actual"]["missing_atoms"]:
            print(f"    → {m}")


def cmd_demo(_args=None):
    """Build a demo board from built-in calculus content."""
    module = "demo_calculus"
    out_dir = OUTPUT_DIR / module
    eru = generate_board(DEMO_TEXT, module, out_dir)

    print("  [demo] Calculus module board generated")
    print(f"  Output   : {out_dir}")
    print(f"  Atoms    : {eru['actual']['atoms']}")
    print(f"  Bonds    : {eru['actual']['bonds']}")
    print(f"  Stability: {eru['actual']['stability']}")
    print(f"  ERU      : {eru['status']}  (variance={eru['variance']})")
    if eru["actual"].get("missing_atoms"):
        print("  Missing prereqs detected:")
        for m in eru["actual"]["missing_atoms"]:
            print(f"    → {m}")
    print(f"\n  Board files written to: {out_dir}\n")


def cmd_lattice(_args=None):
    """Build a lattice from all modules found in homework/."""
    raw_dirs = sorted(HOMEWORK_DIR.glob("*/raw/"))
    if not raw_dirs:
        print("  No homework modules found in homework/*/raw/")
        return

    molecules = []
    for raw_dir in raw_dirs:
        module = raw_dir.parent.name
        txt_files = list(raw_dir.glob("*.txt"))
        if not txt_files:
            continue
        combined = "\n".join(f.read_text() for f in txt_files)
        atoms = text_to_atoms(combined, module)
        bonds = compute_bonds(atoms)
        mol   = build_molecule(atoms, bonds, module)
        molecules.append(mol)
        print(f"  Module: {module:30s}  atoms={len(atoms):3d}  bonds={len(bonds):3d}")

    if not molecules:
        print("  No .txt files found in any homework/*/raw/ directory.")
        return

    lattice = build_lattice(molecules, "SAGCO-University-Course")
    out_path = UNIV_ROOT / "output" / "lattice.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        yaml.dump(lattice.to_dict(), f, default_flow_style=False, allow_unicode=True)

    print(f"\n  Lattice built: {lattice.lattice_id}")
    print(f"  Modules      : {len(molecules)}")
    print(f"  Cross bonds  : {len(lattice.cross_bonds)}")
    print(f"  Stability    : {lattice.overall_stability}")
    print(f"  Written to   : {out_path}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="sagco_boardgen",
        description="SAGCO University — Homework Board Generator",
    )
    sub = parser.add_subparsers(dest="command")

    # generate sub-command
    gen_p = sub.add_parser("generate", help="Generate a board from text or file")
    gen_p.add_argument("--module", default="unknown_module",
                       help="Module identifier (e.g. '5home2266305sn')")
    gen_p.add_argument("--text", help="Raw text to parse")
    gen_p.add_argument("--file", help="Path to a .txt file")

    sub.add_parser("demo",    help="Run built-in calculus demo")
    sub.add_parser("lattice", help="Build lattice from all homework modules")

    args = parser.parse_args()
    _banner()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "demo":
        cmd_demo(args)
    elif args.command == "lattice":
        cmd_lattice(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
