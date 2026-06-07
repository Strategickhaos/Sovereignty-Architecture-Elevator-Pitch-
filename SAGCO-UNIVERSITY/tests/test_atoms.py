"""
SAGCO-UNIVERSITY
tests/test_atoms.py — Unit tests for atom_builder, bond_engine, molecule_builder.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from atom_builder import (
    Atom, parse_questions, parse_definitions, parse_formulas,
    parse_examples, text_to_atoms,
)
from bond_engine import Bond, compute_bonds, bond_order, classify_strength
from molecule_builder import build_molecule


# ── Sample text ───────────────────────────────────────────────────────────────

SAMPLE = """\
Q1: Find the critical points of f(x) = 10x^(2/3) + x^(5/3)
Q2: Classify each critical point as local max, local min, or saddle point
Q3: Find absolute extrema on [-5, 5]
Definition: A critical point occurs where f'(x) = 0 or f'(x) is undefined
Formula: Bond Order = (Bonding Electrons - Antibonding Electrons) / 2
Example: For f(x) = x^2 - 4, f'(x) = 2x, critical point at x=0
"""


# ── text_to_atoms ─────────────────────────────────────────────────────────────

def test_text_to_atoms_finds_questions():
    atoms = text_to_atoms(SAMPLE, "module_5")
    questions = [a for a in atoms if a.atom_type == "question"]
    assert len(questions) == 3, f"Expected 3 questions, got {len(questions)}"
    ids = [q.atom_id for q in questions]
    assert "Q1" in ids
    assert "Q2" in ids
    assert "Q3" in ids


def test_text_to_atoms_finds_definition():
    atoms = text_to_atoms(SAMPLE, "module_5")
    defs = [a for a in atoms if a.atom_type == "definition"]
    assert len(defs) >= 1
    assert "DEF-1" in [d.atom_id for d in defs]


def test_text_to_atoms_finds_formula():
    atoms = text_to_atoms(SAMPLE, "module_5")
    formulas = [a for a in atoms if a.atom_type == "formula"]
    assert len(formulas) >= 1


def test_text_to_atoms_finds_example():
    atoms = text_to_atoms(SAMPLE, "module_5")
    examples = [a for a in atoms if a.atom_type == "example"]
    assert len(examples) >= 1
    assert "EX-1" in [e.atom_id for e in examples]


def test_text_to_atoms_stamps_module():
    atoms = text_to_atoms(SAMPLE, "test_module")
    for a in atoms:
        assert a.module == "test_module"


def test_text_to_atoms_returns_atom_instances():
    atoms = text_to_atoms(SAMPLE, "m")
    for a in atoms:
        assert isinstance(a, Atom)
        assert a.atom_type in ("question", "definition", "formula", "example", "proof")


def test_text_to_atoms_empty():
    atoms = text_to_atoms("", "m")
    assert atoms == []


# ── compute_bonds ─────────────────────────────────────────────────────────────

def test_compute_bonds_returns_bonds():
    atoms = text_to_atoms(SAMPLE, "module_5")
    bonds = compute_bonds(atoms)
    assert isinstance(bonds, list)
    for b in bonds:
        assert isinstance(b, Bond)


def test_compute_bonds_no_self_bonds():
    atoms = text_to_atoms(SAMPLE, "module_5")
    bonds = compute_bonds(atoms)
    for b in bonds:
        assert b.source != b.target


def test_compute_bonds_single_atom():
    atom = Atom("Q1", "question", "test content", ["critical"], "m")
    bonds = compute_bonds([atom])
    assert bonds == []


# ── build_molecule ────────────────────────────────────────────────────────────

def test_build_molecule_stability():
    atoms = text_to_atoms(SAMPLE, "module_5")
    bonds = compute_bonds(atoms)
    mol = build_molecule(atoms, bonds, "module_5")
    assert mol.stability >= 0.0
    assert mol.module_name == "module_5"
    assert len(mol.atoms) == len(atoms)
    assert len(mol.bonds) == len(bonds)


def test_build_molecule_empty():
    mol = build_molecule([], [], "empty")
    assert mol.stability == 0.0
    assert mol.atoms == []
    assert mol.bonds == []


# ── bond_order formula ────────────────────────────────────────────────────────

def test_bond_order_definition_question():
    """A definition -> question bond should have positive order."""
    src = Atom("DEF-1", "definition", "critical point where f'(x)=0", ["critical", "derivative"], "m")
    tgt = Atom("Q1",    "question",   "find critical points",          ["critical", "derivative"], "m")
    order = bond_order(src, tgt)
    assert order > 0, f"Expected positive bond order, got {order}"


def test_bond_order_formula():
    """
    Bond Order = (supporting - contradicting) / 2
    For a formula -> question pair with 2 shared tags:
    supporting = 2 (base) + 2 (shared tags) = 4
    contradicting = 0
    order = 4/2 = 2.0
    """
    src = Atom("FORMULA-1", "formula",   "f'(x) derivative calc", ["derivative", "critical"], "m")
    tgt = Atom("Q1",        "question",  "find derivative point",  ["derivative", "critical"], "m")
    order = bond_order(src, tgt)
    assert order == 2.0, f"Expected 2.0, got {order}"


def test_classify_strength_antibond():
    assert classify_strength(-1.0) == "antibond"


def test_classify_strength_single():
    assert classify_strength(0.5) == "single"


def test_classify_strength_double():
    assert classify_strength(1.5) == "double"


def test_classify_strength_triple():
    assert classify_strength(2.5) == "triple"


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import traceback

    tests = [
        test_text_to_atoms_finds_questions,
        test_text_to_atoms_finds_definition,
        test_text_to_atoms_finds_formula,
        test_text_to_atoms_finds_example,
        test_text_to_atoms_stamps_module,
        test_text_to_atoms_returns_atom_instances,
        test_text_to_atoms_empty,
        test_compute_bonds_returns_bonds,
        test_compute_bonds_no_self_bonds,
        test_compute_bonds_single_atom,
        test_build_molecule_stability,
        test_build_molecule_empty,
        test_bond_order_definition_question,
        test_bond_order_formula,
        test_classify_strength_antibond,
        test_classify_strength_single,
        test_classify_strength_double,
        test_classify_strength_triple,
    ]

    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n  {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
