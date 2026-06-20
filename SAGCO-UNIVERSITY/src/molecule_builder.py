"""
SAGCO-UNIVERSITY
molecule_builder.py — Assembles atoms+bonds into a module molecule.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List

from atom_builder import Atom
from bond_engine import Bond


@dataclass
class Molecule:
    mol_id: str
    module_name: str
    atoms: list[Atom]
    bonds: list[Bond]
    stability: float       # average bond order across all bonds
    missing_atoms: list[str]  # detected prereqs not present

    def to_dict(self) -> dict:
        return {
            "mol_id": self.mol_id,
            "module_name": self.module_name,
            "atom_count": len(self.atoms),
            "bond_count": len(self.bonds),
            "stability": self.stability,
            "missing_atoms": self.missing_atoms,
            "atoms": [a.to_dict() for a in self.atoms],
            "bonds": [b.to_dict() for b in self.bonds],
        }


# ── Prereq detection ──────────────────────────────────────────────────────────

_PREREQ_TAGS = {
    "derivative": ["limit", "function"],
    "integral":   ["derivative", "function"],
    "critical":   ["derivative"],
    "extrema":    ["critical", "derivative"],
    "saddle":     ["critical", "derivative"],
    "bonding":    ["electron", "formula"],
    "antibonding":["bonding", "electron"],
}


def _detect_missing(atoms: list[Atom]) -> list[str]:
    """
    Scan atom tags for implied prerequisites not present in the atom set.
    Returns list of missing concept strings.
    """
    present_tags: set[str] = set()
    for a in atoms:
        present_tags.update(a.tags)

    missing: list[str] = []
    for tag, prereqs in _PREREQ_TAGS.items():
        if tag in present_tags:
            for prereq in prereqs:
                if prereq not in present_tags:
                    missing.append(f"{prereq} (needed by {tag})")

    return sorted(set(missing))


def _avg_bond_order(bonds: list[Bond]) -> float:
    if not bonds:
        return 0.0
    return round(sum(b.bond_order for b in bonds) / len(bonds), 4)


# ── Public API ────────────────────────────────────────────────────────────────

def build_molecule(atoms: list[Atom], bonds: list[Bond], module: str) -> Molecule:
    """
    Assemble a Molecule from atoms and bonds for a given module.

    Args:
        atoms: list of Atom objects.
        bonds: list of Bond objects computed by bond_engine.compute_bonds().
        module: module name string.
    Returns:
        Molecule dataclass.
    """
    stability = _avg_bond_order(bonds)
    missing   = _detect_missing(atoms)

    return Molecule(
        mol_id=f"MOL-{uuid.uuid4().hex[:8].upper()}",
        module_name=module,
        atoms=atoms,
        bonds=bonds,
        stability=stability,
        missing_atoms=missing,
    )
