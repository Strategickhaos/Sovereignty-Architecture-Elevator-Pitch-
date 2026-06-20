"""
SAGCO-UNIVERSITY
board_generator.py — Main board generator.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

import yaml

from atom_builder import Atom, text_to_atoms
from bond_engine import Bond, compute_bonds
from molecule_builder import Molecule, build_molecule
from lattice_builder import Lattice, build_lattice


# ── ERU builder ───────────────────────────────────────────────────────────────

def _build_eru(
    module: str,
    atoms: list[Atom],
    bonds: list[Bond],
    molecule: Molecule,
) -> dict:
    n_atoms = len(atoms)
    n_bonds = len(bonds)
    variance = 0 if n_atoms > 0 and n_bonds > 0 else 1

    return {
        "eru_id": f"ERU-{uuid.uuid4().hex[:8].upper()}",
        "board": "SAGCO-UNIVERSITY",
        "module": module,
        "generated": datetime.utcnow().isoformat(),
        "expected": {
            "atoms": ">= 1",
            "bonds": ">= 1",
            "stability": ">= 0.5",
        },
        "actual": {
            "atoms": n_atoms,
            "bonds": n_bonds,
            "stability": molecule.stability,
            "missing_atoms": molecule.missing_atoms,
        },
        "variance": variance,
        "status": "PASS" if variance == 0 else "FAIL",
    }


# ── Writer helpers ────────────────────────────────────────────────────────────

def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def _write_board_yaml(output_dir: Path, module: str, atom_count: int) -> None:
    board = {
        "board_id": f"BOARD-{module.upper()}",
        "module": module,
        "district": "genesis",
        "role": "homework_module",
        "atom_count": atom_count,
        "generated": datetime.utcnow().isoformat(),
    }
    _write_yaml(output_dir / "board.yaml", board)


def _write_atoms(output_dir: Path, atoms: list[Atom]) -> None:
    atoms_dir = output_dir / "atoms"
    atoms_dir.mkdir(parents=True, exist_ok=True)
    for atom in atoms:
        _write_yaml(atoms_dir / f"{atom.atom_id}.yaml", atom.to_dict())


def _write_bonds(output_dir: Path, bonds: list[Bond]) -> None:
    bonds_dir = output_dir / "bonds"
    bonds_dir.mkdir(parents=True, exist_ok=True)
    for bond in bonds:
        _write_yaml(bonds_dir / f"{bond.bond_id}.yaml", bond.to_dict())


# ── Public API ────────────────────────────────────────────────────────────────

def generate_board(source_text: str, module_name: str, output_dir: Path) -> dict:
    """
    Generate a full board from source text for a given module.

    Steps:
      1. text_to_atoms
      2. compute_bonds
      3. build_molecule
      4. Write board.yaml, atoms/, bonds/, molecule.yaml, eru_report.yaml

    Args:
        source_text: raw assignment/module text.
        module_name: e.g. "module_5".
        output_dir: destination directory for outputs.
    Returns:
        ERU report dict.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Parse atoms
    atoms = text_to_atoms(source_text, module_name)

    # 2. Compute bonds
    bonds = compute_bonds(atoms)

    # 3. Build molecule
    molecule = build_molecule(atoms, bonds, module_name)

    # 4. Build ERU
    eru = _build_eru(module_name, atoms, bonds, molecule)

    # 5. Write outputs
    _write_board_yaml(output_dir, module_name, len(atoms))
    _write_atoms(output_dir, atoms)
    _write_bonds(output_dir, bonds)
    _write_yaml(output_dir / "molecule.yaml", molecule.to_dict())
    _write_yaml(output_dir / "eru_report.yaml", eru)

    return eru


def generate_from_file(path: str, output_dir: Path) -> dict:
    """
    Load source text from a file and generate a board.

    The module name is inferred from the file stem.

    Args:
        path: file path string.
        output_dir: destination Path.
    Returns:
        ERU report dict.
    """
    p = Path(path)
    source_text = p.read_text(encoding="utf-8")
    module_name = p.stem
    return generate_board(source_text, module_name, output_dir)
