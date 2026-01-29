#!/usr/bin/env python3
"""
TRIG6 Citation System
=====================
Every constant must have provenance. No exceptions.
This is audit armor against discreditation.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date
import json


@dataclass
class Provenance:
    """Single source citation for a constant."""
    source_title: str
    publisher: str
    edition_or_rev: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD or "YYYY"
    section_or_page: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}
    
    def format_citation(self) -> str:
        """APA-ish citation string."""
        parts = [self.source_title]
        if self.edition_or_rev:
            parts.append(f"({self.edition_or_rev})")
        if self.publisher:
            parts.append(f"- {self.publisher}")
        if self.date:
            parts.append(f"[{self.date}]")
        if self.section_or_page:
            parts.append(f"@ {self.section_or_page}")
        return " ".join(parts)


@dataclass
class Validation:
    """How to verify this constant is within bounds."""
    doctor_test: str  # Test name in doctor.py
    constraints: List[str] = field(default_factory=list)  # e.g., ["0.5 <= value <= 0.9"]
    
    def to_dict(self) -> dict:
        return {"doctor_test": self.doctor_test, "constraints": self.constraints}


@dataclass
class ConstantRecord:
    """
    Canonical constant record with full provenance.
    
    This schema ensures every value can be traced back to a source,
    validated against constraints, and audited for correctness.
    """
    key: str                          # e.g., "rope.knot.figure_8_on_bight"
    value: float                      # The actual value
    units: str                        # e.g., "ratio", "lbf", "degrees", "kN"
    context: str                      # Plain English explanation
    provenance: List[Provenance]      # Must have at least one source
    entered_by: str                   # Who entered this
    entered_date: str                 # YYYY-MM-DD
    
    # Optional but recommended
    range: Optional[tuple] = None     # (min, max) expected values
    jurisdiction: str = "global"      # "global", "USA", "OSHA", etc.
    confidence: str = "medium"        # "high", "medium", "low", "heuristic"
    validation: Optional[Validation] = None
    
    def to_dict(self) -> dict:
        d = {
            "key": self.key,
            "value": self.value,
            "units": self.units,
            "context": self.context,
            "provenance": [p.to_dict() for p in self.provenance],
            "entered_by": self.entered_by,
            "entered_date": self.entered_date,
            "jurisdiction": self.jurisdiction,
            "confidence": self.confidence,
        }
        if self.range:
            d["range"] = list(self.range)
        if self.validation:
            d["validation"] = self.validation.to_dict()
        return d
    
    @classmethod
    def from_dict(cls, d: dict) -> "ConstantRecord":
        provenance = [Provenance(**p) for p in d.get("provenance", [])]
        validation = None
        if "validation" in d:
            validation = Validation(**d["validation"])
        return cls(
            key=d["key"],
            value=d["value"],
            units=d["units"],
            context=d["context"],
            provenance=provenance,
            entered_by=d["entered_by"],
            entered_date=d["entered_date"],
            range=tuple(d["range"]) if "range" in d else None,
            jurisdiction=d.get("jurisdiction", "global"),
            confidence=d.get("confidence", "medium"),
            validation=validation,
        )
    
    def format_full(self) -> str:
        """Human-readable full citation with all metadata."""
        lines = [
            f"KEY: {self.key}",
            f"VALUE: {self.value} {self.units}",
            f"CONTEXT: {self.context}",
            f"JURISDICTION: {self.jurisdiction}",
            f"CONFIDENCE: {self.confidence}",
        ]
        if self.range:
            lines.append(f"EXPECTED RANGE: {self.range[0]} - {self.range[1]}")
        lines.append("SOURCES:")
        for p in self.provenance:
            lines.append(f"  - {p.format_citation()}")
        lines.append(f"ENTERED BY: {self.entered_by} on {self.entered_date}")
        if self.validation:
            lines.append(f"VALIDATION: {self.validation.doctor_test}")
            for c in self.validation.constraints:
                lines.append(f"  CONSTRAINT: {c}")
        return "\n".join(lines)


def load_constants_file(path: str) -> List[ConstantRecord]:
    """Load a constants.json file into ConstantRecord objects."""
    with open(path, "r") as f:
        data = json.load(f)
    return [ConstantRecord.from_dict(d) for d in data.get("constants", [])]


def save_constants_file(path: str, constants: List[ConstantRecord], metadata: dict = None):
    """Save ConstantRecord objects to a constants.json file."""
    data = {
        "metadata": metadata or {},
        "constants": [c.to_dict() for c in constants]
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# Example usage / self-test
if __name__ == "__main__":
    # Create a sample constant with full provenance
    example = ConstantRecord(
        key="rope.knot.figure_8_on_bight",
        value=0.78,
        units="ratio",
        context="Typical knot efficiency in nylon kernmantle when properly dressed/set.",
        range=(0.75, 0.80),
        jurisdiction="global",
        confidence="medium",
        provenance=[
            Provenance(
                source_title="CMC Rope Rescue Field Guide",
                publisher="CMC Rescue, Inc.",
                edition_or_rev="4th Edition",
                date="2017",
                section_or_page="p. 47",
                notes="Tested on 11mm nylon kernmantle, new rope"
            )
        ],
        entered_by="Domenic G. Garza",
        entered_date="2026-01-29",
        validation=Validation(
            doctor_test="rope.knot_efficiency_in_bounds",
            constraints=["0.5 <= value <= 0.95"]
        )
    )
    
    print("=== TRIG6 Citation System Self-Test ===\n")
    print(example.format_full())
    print("\n=== JSON Output ===")
    print(json.dumps(example.to_dict(), indent=2))
