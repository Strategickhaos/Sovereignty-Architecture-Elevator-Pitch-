"""
SAGCO-UNIVERSITY
bond_engine.py — Computes conceptual bonds between atoms.

Bond order formula (from molecular orbital theory):
  Bond Order = (Bonding Electrons - Antibonding Electrons) / 2
Applied here as:
  Bond Order = (supporting_links - contradicting_links) / 2
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import List

from atom_builder import Atom


@dataclass
class Bond:
    bond_id: str
    source: str        # atom_id
    target: str        # atom_id
    bond_type: str     # prerequisite, similarity, dependency, contradiction, reinforcement
    bond_order: float  # (supporting - contradicting) / 2
    strength: str      # single, double, triple, antibond

    def to_dict(self) -> dict:
        return {
            "bond_id": self.bond_id,
            "source": self.source,
            "target": self.target,
            "bond_type": self.bond_type,
            "bond_order": self.bond_order,
            "strength": self.strength,
        }


# ── Bond-type heuristics ──────────────────────────────────────────────────────

_TYPE_ORDER = {
    # (source_type, target_type) -> bond_type, supporting_links, contradicting_links
    ("definition", "question"):   ("prerequisite",   2, 0),
    ("formula",    "question"):   ("dependency",     2, 0),
    ("definition", "formula"):   ("prerequisite",   1, 0),
    ("formula",    "example"):   ("reinforcement",  2, 0),
    ("example",    "question"):  ("reinforcement",  1, 0),
    ("question",   "question"):  ("similarity",     1, 0),
    ("proof",      "formula"):   ("dependency",     3, 0),
    ("proof",      "definition"):("reinforcement",  2, 0),
    ("question",   "proof"):     ("dependency",     1, 0),
    ("definition", "definition"): ("similarity",   1, 0),
}

_DEFAULT = ("similarity", 1, 0)


def _type_pair_info(src: Atom, tgt: Atom):
    key = (src.atom_type, tgt.atom_type)
    return _TYPE_ORDER.get(key, _DEFAULT)


def _shared_tags(src: Atom, tgt: Atom) -> int:
    return len(set(src.tags) & set(tgt.tags))


# ── Public API ────────────────────────────────────────────────────────────────

def bond_order(source: Atom, target: Atom) -> float:
    """
    Compute bond order between two atoms.

    Bond Order = (supporting_links - contradicting_links) / 2

    supporting_links = base from type-pair + shared tag count
    contradicting_links = 1 if same atom_type and no shared tags (competing)
    """
    bond_type, base_support, base_contra = _type_pair_info(source, target)
    shared = _shared_tags(source, target)

    supporting = base_support + shared
    contradicting = base_contra

    # Atoms of same type with no shared tags slightly repel
    if source.atom_type == target.atom_type and shared == 0:
        contradicting += 1

    # Contradiction bond if explicitly typed
    if bond_type == "contradiction":
        contradicting += 2

    order = (supporting - contradicting) / 2.0
    return round(order, 4)


def classify_strength(order: float) -> str:
    """
    Map a bond order to a strength label.

    order < 0     -> antibond
    0 <= order < 1 -> single
    1 <= order < 2 -> double
    >= 2           -> triple
    """
    if order < 0:
        return "antibond"
    if order < 1.0:
        return "single"
    if order < 2.0:
        return "double"
    return "triple"


def compute_bonds(atoms: list[Atom]) -> list[Bond]:
    """
    Compute all meaningful bonds between a list of atoms.

    Only bonds with order >= 0 (no net antibonds) are emitted, except
    when bond_type is 'contradiction' (antibonds are kept to show conflict).

    Args:
        atoms: list of Atom objects from atom_builder.text_to_atoms().
    Returns:
        list of Bond objects.
    """
    bonds: list[Bond] = []

    for i, src in enumerate(atoms):
        for j, tgt in enumerate(atoms):
            if i >= j:
                continue  # no self-bonds, no duplicate pairs

            order = bond_order(src, tgt)
            bond_type, _, _ = _type_pair_info(src, tgt)
            strength = classify_strength(order)

            # Skip weak no-context bonds (order == 0, single, no shared tags)
            if order == 0 and _shared_tags(src, tgt) == 0 and bond_type == "similarity":
                continue

            bonds.append(Bond(
                bond_id=f"BOND-{uuid.uuid4().hex[:6].upper()}",
                source=src.atom_id,
                target=tgt.atom_id,
                bond_type=bond_type,
                bond_order=order,
                strength=strength,
            ))

    return bonds
