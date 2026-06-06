#!/usr/bin/env python3
"""
MISSING-LINKS Classifier — labels a raw seed with contradiction type + severity.

Usage:
  python classifier.py --seed seeds/ML-<ts>-seed.yaml
  python classifier.py --text "Some raw signal text"
"""

from __future__ import annotations
import yaml, sys, re
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
ML_ROOT   = REPO_ROOT / "MISSING-LINKS"

TAXONOMY_FILE = ML_ROOT / "manifests" / "contradiction_types.yaml"


def load_taxonomy() -> list[dict]:
    if not TAXONOMY_FILE.exists():
        return []
    return yaml.safe_load(TAXONOMY_FILE.read_text()).get("contradiction_taxonomy", [])


KEYWORD_MAP = {
    "IDENTITY_MISMATCH":    ["duplicate", "same cid", "same pid", "collision"],
    "CITIZEN_NO_DISTRICT":  ["no district", "missing district", "district: null"],
    "CITIZEN_NO_PID":       ["no pid", "missing pid", "pid: null"],
    "PHANTOM_MAC":          ["mac", "arp", "phantom", "unregistered device"],
    "RECON_DRIFT":          ["ip changed", "drift", "stale", "moved"],
    "PORT_GHOST":           ["open port", "no owner", "port ghost"],
    "TOKEN_IN_URL":         ["access_token", "id_token", "bearer", "auth_token", "token in url"],
    "PII_IN_PIXEL":         ["phone_number", "email", "tracking pixel", "gtm", "sha-256 hash"],
    "DISTRICT_ORPHAN":      ["wrong district", "orphan", "misrouted"],
    "BOARD_MISSING":        ["board not found", "board missing", "no board"],
    "RAT_GAP":              ["no antibody", "undetected", "coverage gap", "rat gap"],
    "ERU_UNRESOLVED":       ["eru", "no understanding", "no antibody", "unresolved case"],
}


def classify_text(text: str) -> Optional[dict]:
    text_lower = text.lower()
    taxonomy   = load_taxonomy()
    tax_by_id  = {t["id"]: t for t in taxonomy}

    for ct_id, keywords in KEYWORD_MAP.items():
        if any(k in text_lower for k in keywords):
            ct = tax_by_id.get(ct_id, {"id": ct_id, "severity": "MEDIUM"})
            return {
                "contradiction_type": ct_id,
                "severity":   ct.get("severity", "MEDIUM"),
                "domain":     ct.get("domain", "unknown"),
                "law":        ct.get("law", "unknown"),
                "escalates_to": ct.get("escalates_to"),
                "auto_resolve": ct.get("auto_resolve", False),
                "matched_keyword": next(k for k in keywords if k in text_lower),
            }
    return {
        "contradiction_type": "UNKNOWN",
        "severity": "LOW",
        "domain": "unknown",
        "law": "unknown",
        "escalates_to": None,
        "auto_resolve": False,
        "matched_keyword": None,
    }


def classify_seed(seed_path: Path) -> dict:
    seed       = yaml.safe_load(seed_path.read_text())
    probe_text = " ".join([
        str(seed.get("description", "")),
        str(seed.get("actual", "")),
        str(seed.get("variance", "")),
        str(seed.get("raw", "")),
    ])
    result = classify_text(probe_text)
    seed.update(result)
    seed_path.write_text(yaml.dump(seed, sort_keys=False))
    print(f"  Classified {seed_path.name} → {result['contradiction_type']} [{result['severity']}]")
    return seed


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", help="Path to seed YAML file")
    ap.add_argument("--text", help="Raw text to classify")
    args = ap.parse_args()

    if args.seed:
        classify_seed(Path(args.seed))
    elif args.text:
        result = classify_text(args.text)
        print(yaml.dump(result, sort_keys=False))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
