"""
citizen_emitter.py — emits a SAGCO citizen record for each verified board.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional

from priority_queue import SeedPriority

REPO_ROOT        = Path(__file__).resolve().parent.parent.parent
CITIZENS_DIR     = REPO_ROOT / "08-CITIZENS"
REGISTRY_JSON    = CITIZENS_DIR / "citizen_registry.json"


# ── CID generator ─────────────────────────────────────────────────────────────

def _make_cid() -> str:
    ts_ms = int(time.time() * 1000)
    tick  = ts_ms % 3449
    return f"sgc-board-{ts_ms}-{tick}"


# ── Registry helpers ──────────────────────────────────────────────────────────

def _load_registry() -> list:
    if REGISTRY_JSON.exists():
        try:
            data = json.loads(REGISTRY_JSON.read_text())
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []


def _save_registry(records: list):
    CITIZENS_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY_JSON.write_text(json.dumps(records, indent=2))


# ── Emitter ───────────────────────────────────────────────────────────────────

def emit_citizen(board_path: Path, seed: SeedPriority) -> dict:
    """
    Create a citizen entry in 08-CITIZENS/citizen_registry.json.

    CID format: sgc-board-{timestamp_ms}-{tick%3449}
    """
    board_path = Path(board_path)

    # Derive district from board content if possible
    district = "genesis"
    board_yaml_path = board_path / "board.yaml"
    if board_yaml_path.exists():
        try:
            import yaml
            data = yaml.safe_load(board_yaml_path.read_text())
            district = data.get("district", "genesis")
        except Exception:
            pass

    cid = _make_cid()
    citizen: dict = {
        "cid":          cid,
        "name":         seed.title,
        "kind":         "auto_board",
        "district":     district,
        "source_seed":  seed.seed_id,
        "board_path":   str(board_path),
        "board_name":   board_path.name,
        "priority_score": seed.priority_score,
        "invention_prob": seed.invention_prob,
        "bond_order_gap": seed.bond_order_gap,
        "emitted_at":   _iso_now(),
    }

    records = _load_registry()
    records.append(citizen)
    _save_registry(records)

    print(f"  CITIZEN EMITTED: {cid} → {seed.title}")
    return citizen


def _iso_now() -> str:
    import datetime
    return datetime.datetime.utcnow().isoformat() + "Z"


if __name__ == "__main__":
    # Quick smoke test
    from priority_queue import SeedPriority
    sp = SeedPriority(
        seed_id="TEST-001", title="demo board", source="missing_links",
        invention_prob=0.8, bond_order_gap=0.7,
    )
    result = emit_citizen(Path("/tmp/demo_board"), sp)
    print(result)
