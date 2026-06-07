"""
SAGCO-UNIVERSITY
atom_builder.py — Turns homework questions into atoms.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import List


@dataclass
class Atom:
    atom_id: str        # "Q1", "DEF-1", "FORMULA-1", "EX-1", "PROOF-1"
    atom_type: str      # question, formula, definition, example, proof
    content: str
    tags: list[str]
    module: str

    def to_dict(self) -> dict:
        return {
            "atom_id": self.atom_id,
            "atom_type": self.atom_type,
            "content": self.content,
            "tags": self.tags,
            "module": self.module,
        }


# ── Tag extractor ─────────────────────────────────────────────────────────────

_MATH_KEYWORDS = {
    "derivative", "integral", "limit", "critical", "extrema",
    "maximum", "minimum", "saddle", "function", "point",
    "calculus", "formula", "bond", "electron", "bonding",
    "antibonding",
}

_ENGINEERING_KEYWORDS = {
    "pipeline", "compile", "deploy", "scaffold", "module",
    "board", "system", "architecture", "layer",
}


def _extract_tags(text: str) -> list[str]:
    words = set(re.findall(r"[a-zA-Z]+", text.lower()))
    tags: list[str] = []
    for kw in _MATH_KEYWORDS:
        if kw in words:
            tags.append(kw)
    for kw in _ENGINEERING_KEYWORDS:
        if kw in words:
            tags.append(kw)
    return sorted(set(tags))


# ── Public API ────────────────────────────────────────────────────────────────

def parse_questions(text: str) -> list[Atom]:
    """
    Find Q1, Q2, Q3, ... patterns in text and return Atoms of type 'question'.

    Patterns matched:
      Q1: ...text...
      Q1. ...text...
      Question 1: ...text...
    """
    pattern = re.compile(
        r"(?:Q(?:uestion)?\s*(\d+)\s*[:.]\s*)(.+?)(?=(?:Q(?:uestion)?\s*\d+\s*[:.])|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    atoms: list[Atom] = []
    for m in pattern.finditer(text):
        num = m.group(1)
        content = m.group(2).strip()
        if not content:
            continue
        atoms.append(Atom(
            atom_id=f"Q{num}",
            atom_type="question",
            content=content,
            tags=_extract_tags(content),
            module="",
        ))
    return atoms


def parse_definitions(text: str) -> list[Atom]:
    """
    Find 'Definition: ...' patterns in text.

    Patterns matched:
      Definition: ...text...
      Def: ...text...
    """
    pattern = re.compile(
        r"(?:Def(?:inition)?\s*[:.]\s*)(.+?)(?=(?:Def(?:inition)?\s*[:.])|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    atoms: list[Atom] = []
    counter = 1
    for m in pattern.finditer(text):
        content = m.group(1).strip()
        if not content:
            continue
        atoms.append(Atom(
            atom_id=f"DEF-{counter}",
            atom_type="definition",
            content=content,
            tags=_extract_tags(content),
            module="",
        ))
        counter += 1
    return atoms


def parse_formulas(text: str) -> list[Atom]:
    """
    Find lines containing = or := patterns (formulas/equations).

    Heuristic: a line with at least one = and at least one math symbol
    or keyword is treated as a formula atom.
    """
    lines = text.split("\n")
    atoms: list[Atom] = []
    counter = 1

    # Also detect explicit "Formula:" prefix
    prefix_pattern = re.compile(r"Formula\s*[:.]\s*(.+)", re.IGNORECASE)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        pm = prefix_pattern.match(line)
        if pm:
            content = pm.group(1).strip()
            atoms.append(Atom(
                atom_id=f"FORMULA-{counter}",
                atom_type="formula",
                content=content,
                tags=_extract_tags(content),
                module="",
            ))
            counter += 1
            continue

        # Heuristic: line has = or := and looks mathy
        if ("=" in line or ":=" in line) and re.search(r"[a-zA-Z]\s*[\(\^]|[\d]\s*[+\-\*/^]", line):
            atoms.append(Atom(
                atom_id=f"FORMULA-{counter}",
                atom_type="formula",
                content=line,
                tags=_extract_tags(line),
                module="",
            ))
            counter += 1

    return atoms


def parse_examples(text: str) -> list[Atom]:
    """Find 'Example: ...' patterns."""
    pattern = re.compile(
        r"(?:Example\s*[:.]\s*)(.+?)(?=(?:Example\s*[:.])|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    atoms: list[Atom] = []
    counter = 1
    for m in pattern.finditer(text):
        content = m.group(1).strip()
        if not content:
            continue
        atoms.append(Atom(
            atom_id=f"EX-{counter}",
            atom_type="example",
            content=content,
            tags=_extract_tags(content),
            module="",
        ))
        counter += 1
    return atoms


def parse_proofs(text: str) -> list[Atom]:
    """Find 'Proof: ...' patterns."""
    pattern = re.compile(
        r"(?:Proof\s*[:.]\s*)(.+?)(?=(?:Proof\s*[:.])|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    atoms: list[Atom] = []
    counter = 1
    for m in pattern.finditer(text):
        content = m.group(1).strip()
        if not content:
            continue
        atoms.append(Atom(
            atom_id=f"PROOF-{counter}",
            atom_type="proof",
            content=content,
            tags=_extract_tags(content),
            module="",
        ))
        counter += 1
    return atoms


def text_to_atoms(text: str, module: str) -> list[Atom]:
    """
    Parse all atom types from text and stamp them with the module name.

    Args:
        text: raw assignment/module text.
        module: module identifier string (e.g. "module_5").
    Returns:
        Combined list of all Atom types found, de-duplicated by atom_id.
    """
    all_atoms: list[Atom] = (
        parse_questions(text)
        + parse_definitions(text)
        + parse_formulas(text)
        + parse_examples(text)
        + parse_proofs(text)
    )

    # Stamp module and de-duplicate
    seen: set[str] = set()
    result: list[Atom] = []
    for atom in all_atoms:
        atom.module = module
        if atom.atom_id not in seen:
            seen.add(atom.atom_id)
            result.append(atom)

    return result
