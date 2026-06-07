"""
Bond dataclass and bond order formula.
bond_order = (bonding_electrons - antibonding_electrons) / 2
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Bond:
    atom1: str
    atom2: str
    bond_type: str = "covalent"    # covalent, ionic, metallic, hydrogen
    bond_order: float = 1.0
    bond_length_pm: float = 0.0    # picometers
    bond_energy_kjmol: float = 0.0
    notes: str = ""

    def __repr__(self):
        return f"Bond({self.atom1}-{self.atom2}, order={self.bond_order}, type={self.bond_type})"


def bond_order(bonding_electrons: int, antibonding_electrons: int) -> float:
    """
    Compute molecular orbital bond order.
    Formula: (bonding - antibonding) / 2
    """
    return (bonding_electrons - antibonding_electrons) / 2.0


def classify_bond(electronegativity_diff: float) -> str:
    """
    Classify bond type based on electronegativity difference.
    < 0.5: nonpolar covalent
    0.5 - 1.7: polar covalent
    > 1.7: ionic
    """
    diff = abs(electronegativity_diff)
    if diff < 0.5:
        return "nonpolar_covalent"
    elif diff <= 1.7:
        return "polar_covalent"
    else:
        return "ionic"


def make_bond(atom1_symbol: str, atom2_symbol: str, bonding_e: int = 2, antibonding_e: int = 0) -> Bond:
    """Create a Bond with calculated bond order."""
    from sagco.university.atoms import PERIODIC_TABLE
    a1 = PERIODIC_TABLE.get(atom1_symbol)
    a2 = PERIODIC_TABLE.get(atom2_symbol)
    bo = bond_order(bonding_e, antibonding_e)
    bond_type = "covalent"
    if a1 and a2:
        en_diff = abs(a1.electronegativity - a2.electronegativity)
        bond_type = classify_bond(en_diff)
    return Bond(atom1_symbol, atom2_symbol, bond_type=bond_type, bond_order=bo)


# Common bond data table (bond length in pm, energy in kJ/mol)
BOND_TABLE = {
    ("H", "H"):  Bond("H", "H",  "nonpolar_covalent", 1.0, 74,  436),
    ("C", "C"):  Bond("C", "C",  "nonpolar_covalent", 1.0, 154, 347),
    ("C", "N"):  Bond("C", "N",  "polar_covalent",    1.0, 147, 305),
    ("C", "O"):  Bond("C", "O",  "polar_covalent",    1.0, 143, 360),
    ("O", "H"):  Bond("O", "H",  "polar_covalent",    1.0, 96,  467),
    ("N", "H"):  Bond("N", "H",  "polar_covalent",    1.0, 101, 391),
    ("C", "H"):  Bond("C", "H",  "nonpolar_covalent", 1.0, 109, 413),
    ("N", "N"):  Bond("N", "N",  "nonpolar_covalent", 1.0, 145, 163),
    ("O", "O"):  Bond("O", "O",  "nonpolar_covalent", 1.0, 148, 157),
}
