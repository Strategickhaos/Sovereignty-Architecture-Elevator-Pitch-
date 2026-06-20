"""
Molecule = atoms + bonds.
"""
from dataclasses import dataclass, field
from typing import List, Dict
from .atoms import Atom, PERIODIC_TABLE
from .bonds import Bond, bond_order


@dataclass
class Molecule:
    name: str
    formula: str
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)
    molecular_weight: float = 0.0
    notes: str = ""

    def __post_init__(self):
        if self.atoms and self.molecular_weight == 0.0:
            self.molecular_weight = sum(a.atomic_mass for a in self.atoms)

    def add_atom(self, symbol: str):
        atom = PERIODIC_TABLE.get(symbol)
        if atom:
            self.atoms.append(atom)
            self.molecular_weight += atom.atomic_mass

    def add_bond(self, bond: Bond):
        self.bonds.append(bond)

    def total_valence_electrons(self) -> int:
        return sum(a.valence_electrons for a in self.atoms)

    def __repr__(self):
        return f"Molecule({self.name}, formula={self.formula}, MW={self.molecular_weight:.3f})"


def parse_formula(formula: str) -> Dict[str, int]:
    """
    Parse a molecular formula like H2O, CO2, C6H12O6.
    Returns dict of {symbol: count}.
    """
    import re
    pattern = re.compile(r"([A-Z][a-z]?)(\d*)")
    result = {}
    for symbol, count_str in pattern.findall(formula):
        count = int(count_str) if count_str else 1
        result[symbol] = result.get(symbol, 0) + count
    return result


def build_molecule(name: str, formula: str) -> Molecule:
    """Build a Molecule from name and formula string."""
    mol = Molecule(name=name, formula=formula)
    atom_counts = parse_formula(formula)
    for symbol, count in atom_counts.items():
        for _ in range(count):
            mol.add_atom(symbol)
    return mol


# Common molecules reference
COMMON_MOLECULES = {
    "water":     build_molecule("Water", "H2O"),
    "co2":       build_molecule("Carbon Dioxide", "CO2"),
    "glucose":   build_molecule("Glucose", "C6H12O6"),
    "ammonia":   build_molecule("Ammonia", "NH3"),
    "methane":   build_molecule("Methane", "CH4"),
    "ethanol":   build_molecule("Ethanol", "C2H6O"),
    "nacl":      build_molecule("Sodium Chloride", "NaCl"),
    "o2":        build_molecule("Oxygen", "O2"),
    "n2":        build_molecule("Nitrogen", "N2"),
    "h2":        build_molecule("Hydrogen", "H2"),
}
