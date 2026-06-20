"""
Atom dataclass and question/definition parsing.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Atom:
    symbol: str
    name: str
    atomic_number: int = 0
    atomic_mass: float = 0.0
    group: str = ""
    period: int = 0
    electronegativity: float = 0.0
    valence_electrons: int = 0
    notes: str = ""

    def __repr__(self):
        return f"Atom({self.symbol}, Z={self.atomic_number}, {self.name})"


# Small built-in periodic table (first 20 elements)
PERIODIC_TABLE = {
    "H":  Atom("H",  "Hydrogen",    1,  1.008,  "1",  1, 2.20, 1),
    "He": Atom("He", "Helium",      2,  4.003,  "18", 1, 0.00, 2),
    "Li": Atom("Li", "Lithium",     3,  6.941,  "1",  2, 0.98, 1),
    "Be": Atom("Be", "Beryllium",   4,  9.012,  "2",  2, 1.57, 2),
    "B":  Atom("B",  "Boron",       5, 10.811,  "13", 2, 2.04, 3),
    "C":  Atom("C",  "Carbon",      6, 12.011,  "14", 2, 2.55, 4),
    "N":  Atom("N",  "Nitrogen",    7, 14.007,  "15", 2, 3.04, 5),
    "O":  Atom("O",  "Oxygen",      8, 15.999,  "16", 2, 3.44, 6),
    "F":  Atom("F",  "Fluorine",    9, 18.998,  "17", 2, 3.98, 7),
    "Ne": Atom("Ne", "Neon",       10, 20.180,  "18", 2, 0.00, 8),
    "Na": Atom("Na", "Sodium",     11, 22.990,  "1",  3, 0.93, 1),
    "Mg": Atom("Mg", "Magnesium",  12, 24.305,  "2",  3, 1.31, 2),
    "Al": Atom("Al", "Aluminum",   13, 26.982,  "13", 3, 1.61, 3),
    "Si": Atom("Si", "Silicon",    14, 28.086,  "14", 3, 1.90, 4),
    "P":  Atom("P",  "Phosphorus", 15, 30.974,  "15", 3, 2.19, 5),
    "S":  Atom("S",  "Sulfur",     16, 32.065,  "16", 3, 2.58, 6),
    "Cl": Atom("Cl", "Chlorine",   17, 35.453,  "17", 3, 3.16, 7),
    "Ar": Atom("Ar", "Argon",      18, 39.948,  "18", 3, 0.00, 8),
    "K":  Atom("K",  "Potassium",  19, 39.098,  "1",  4, 0.82, 1),
    "Ca": Atom("Ca", "Calcium",    20, 40.078,  "2",  4, 1.00, 2),
}


def parse_questions(text: str) -> List[dict]:
    """
    Parse a text block containing Q&A pairs.
    Format: 'Q: ...\\nA: ...'
    Returns list of {'question': ..., 'answer': ...}
    """
    import re
    results = []
    lines = text.strip().splitlines()
    current_q = None
    current_a = None
    for line in lines:
        line = line.strip()
        if re.match(r"^Q[:\.]", line, re.IGNORECASE):
            if current_q is not None:
                results.append({"question": current_q, "answer": current_a or ""})
            current_q = re.sub(r"^Q[:\.]?\s*", "", line, flags=re.IGNORECASE)
            current_a = None
        elif re.match(r"^A[:\.]", line, re.IGNORECASE):
            current_a = re.sub(r"^A[:\.]?\s*", "", line, flags=re.IGNORECASE)
    if current_q:
        results.append({"question": current_q, "answer": current_a or ""})
    return results


def parse_definitions(text: str) -> List[dict]:
    """
    Parse term: definition pairs from text.
    Returns list of {'term': ..., 'definition': ...}
    """
    results = []
    for line in text.strip().splitlines():
        if ":" in line:
            term, _, definition = line.partition(":")
            term = term.strip()
            definition = definition.strip()
            if term:
                results.append({"term": term, "definition": definition})
    return results
