"""
SAGCO-UNIVERSITY
lattice_builder.py — Assembles molecules into a course lattice.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List

from atom_builder import Atom
from bond_engine import Bond, bond_order, classify_strength
from molecule_builder import Molecule


@dataclass
class Lattice:
    lattice_id: str
    course_name: str
    molecules: list[Molecule]
    cross_bonds: list[Bond]      # bonds between different modules
    overall_stability: float

    def to_dict(self) -> dict:
        return {
            "lattice_id": self.lattice_id,
            "course_name": self.course_name,
            "module_count": len(self.molecules),
            "cross_bond_count": len(self.cross_bonds),
            "overall_stability": self.overall_stability,
            "molecules": [m.mol_id for m in self.molecules],
            "cross_bonds": [b.to_dict() for b in self.cross_bonds],
        }


# ── Public API ────────────────────────────────────────────────────────────────

def find_cross_module_bonds(molecules: list[Molecule]) -> list[Bond]:
    """
    Detect bonds between atoms in DIFFERENT modules.

    Two atoms from different modules bond if they share ≥1 tag.

    Args:
        molecules: list of Molecule objects.
    Returns:
        list of cross-module Bond objects.
    """
    cross: list[Bond] = []

    for i, mol_a in enumerate(molecules):
        for j, mol_b in enumerate(molecules):
            if i >= j:
                continue
            for atom_a in mol_a.atoms:
                for atom_b in mol_b.atoms:
                    shared = set(atom_a.tags) & set(atom_b.tags)
                    if not shared:
                        continue
                    order = bond_order(atom_a, atom_b)
                    cross.append(Bond(
                        bond_id=f"XBOND-{uuid.uuid4().hex[:6].upper()}",
                        source=f"{mol_a.module_name}:{atom_a.atom_id}",
                        target=f"{mol_b.module_name}:{atom_b.atom_id}",
                        bond_type="cross_module",
                        bond_order=order,
                        strength=classify_strength(order),
                    ))

    return cross


def build_lattice(molecules: list[Molecule], course_name: str) -> Lattice:
    """
    Build a Lattice from a list of Molecules.

    Args:
        molecules: list of Molecule objects (one per module).
        course_name: e.g. "Calculus I".
    Returns:
        Lattice dataclass.
    """
    cross_bonds = find_cross_module_bonds(molecules)

    all_bond_orders = []
    for mol in molecules:
        all_bond_orders.extend(b.bond_order for b in mol.bonds)
    all_bond_orders.extend(b.bond_order for b in cross_bonds)

    overall_stability = (
        round(sum(all_bond_orders) / len(all_bond_orders), 4)
        if all_bond_orders
        else 0.0
    )

    return Lattice(
        lattice_id=f"LAT-{uuid.uuid4().hex[:8].upper()}",
        course_name=course_name,
        molecules=molecules,
        cross_bonds=cross_bonds,
        overall_stability=overall_stability,
    )
