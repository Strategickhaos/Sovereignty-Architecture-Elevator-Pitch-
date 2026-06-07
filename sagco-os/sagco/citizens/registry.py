"""
Citizen registry — read/write using stdlib json.
Citizens are identified by ID and have metadata fields.
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Citizen:
    citizen_id: str
    name: str
    category: str = ""
    eru_status: str = "UNKNOWN"
    rust_token: str = ""
    notes: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Citizen":
        return cls(
            citizen_id=d.get("citizen_id", d.get("id", "")),
            name=d.get("name", ""),
            category=d.get("category", ""),
            eru_status=d.get("eru_status", "UNKNOWN"),
            rust_token=d.get("rust_token", ""),
            notes=d.get("notes", ""),
            tags=d.get("tags", []),
        )


class CitizenRegistry:
    """Registry that persists citizens as JSON."""

    def __init__(self, path: str = "data/citizens.json"):
        self.path = path
        self._citizens: dict = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for d in data:
                    c = Citizen.from_dict(d)
                    self._citizens[c.citizen_id] = c
            except (json.JSONDecodeError, KeyError, TypeError):
                self._citizens = {}

    def save(self):
        os.makedirs(os.path.dirname(self.path) if os.path.dirname(self.path) else ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self._citizens.values()], f, indent=2)

    def register(self, citizen: Citizen):
        self._citizens[citizen.citizen_id] = citizen

    def get(self, citizen_id: str) -> Optional[Citizen]:
        return self._citizens.get(citizen_id)

    def all(self) -> List[Citizen]:
        return list(self._citizens.values())

    def find_by_category(self, category: str) -> List[Citizen]:
        cat_lower = category.lower()
        return [c for c in self._citizens.values() if c.category.lower() == cat_lower]

    def find_by_eru(self, status: str) -> List[Citizen]:
        return [c for c in self._citizens.values() if c.eru_status == status]

    def import_from_rows(self, rows: list, id_field: str = "ID", name_field: str = "Item",
                         category_field: str = "Category"):
        """Bulk import citizens from data rows."""
        for row in rows:
            cid = str(row.get(id_field, ""))
            name = str(row.get(name_field, ""))
            if not cid:
                continue
            c = Citizen(
                citizen_id=cid,
                name=name,
                category=str(row.get(category_field, "")),
                eru_status=str(row.get("ERU", "UNKNOWN")),
                rust_token=str(row.get("Rust Token", "")),
                notes=str(row.get("Details", "")),
            )
            self.register(c)

    def summary(self) -> dict:
        from collections import Counter
        eru_counts = Counter(c.eru_status for c in self._citizens.values())
        cat_counts = Counter(c.category for c in self._citizens.values())
        return {
            "total": len(self._citizens),
            "eru_distribution": dict(eru_counts),
            "category_distribution": dict(cat_counts),
        }

    def __len__(self):
        return len(self._citizens)

    def __repr__(self):
        return f"CitizenRegistry({len(self._citizens)} citizens, path={self.path!r})"
