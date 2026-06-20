#!/usr/bin/env python3
"""
sagco connect — Crawl the repo and register every known artifact as a citizen.
Also generates invention stubs for systems we can't reach yet.

Usage:
  python3 sagco_connect.py [--repo-root PATH] [--dry-run]
"""

import argparse
import hashlib
import json
import time
import yaml
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "citizen_registry.json"
REPO_ROOT = Path(__file__).parent.parent

DISTRICTS = {
    "genesis": ["genesis_prime_core.rs", "env_genesis_lock.sh", "ai_constitution.yaml",
                "dao_record.yaml", "dao_record_v1.0.yaml"],
    "compiler_city": ["compiler/", "FLAMELANG_SPECIFICATION.md"],
    "c64": ["SWARM_DNA_v", "physarum_evolution_36.json"],
    "eru": ["governance/", "UNIFIED_SOVEREIGNTY_ARCHITECTURE"],
    "trinity": ["eval_redteam.py", "firewall/", "windows_defender_antibody.py",
                "VAULT_SECURITY_PLAYBOOK.md"],
    "frequency_coast": ["cognitive_architecture.svg", "cognitive_map.dot"],
    "industrial": ["refinory/", "upl_compliance/"],
    "memory_palace": ["obsidian_integration_hub.py", "obsidian_network_antibodies.py",
                      "obsidian_discord_bot.py", "OBSIDIAN_ARSENAL_COMPLETE.md"],
    "contradiction_forest": ["contradictions/", "contradiction-engine.sh"],
}

KIND_MAP = {
    ".rs": "artifact",
    ".py": "artifact",
    ".yaml": "artifact",
    ".json": "artifact",
    ".md": "artifact",
    ".sh": "artifact",
    ".svg": "artifact",
    ".dot": "artifact",
}


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text())
    return {"schema_version": "1.0", "genesis_tick": 1674852049000, "citizens": []}


def save_registry(reg: dict):
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, default=str))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_cid(kind: str) -> str:
    tick = int(time.time() * 1000)
    increment = tick % 3449
    return f"sgc-{kind}-{tick}-{increment}"


def sha256_file(path: Path) -> str:
    try:
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return f"sha256:{h.hexdigest()}"
    except Exception:
        return "sha256:unreadable"


def guess_district(path: Path) -> str:
    rel = str(path.relative_to(REPO_ROOT))
    for district, patterns in DISTRICTS.items():
        for p in patterns:
            if p in rel:
                return district
    return "genesis"


def existing_cids(reg: dict) -> set:
    return {c.get("payload", {}).get("data", {}).get("file_path", "") for c in reg["citizens"]}


# ─── CONNECTORS ───────────────────────────────────────────────────────────────

def connect_contradictions(reg: dict, dry_run: bool):
    """Import all contradictions from contradictions/contradictions.json."""
    src = REPO_ROOT / "contradictions" / "contradictions.json"
    if not src.exists():
        return
    data = json.loads(src.read_text())
    existing = existing_cids(reg)
    count = 0
    for c in data:
        fp = f"contradictions/contradictions.json#id={c['id']}"
        if fp in existing:
            continue
        cid = make_cid("contradiction")
        citizen = {
            "cid": cid,
            "name": c["name"],
            "kind": "contradiction",
            "born_in": "contradiction_forest",
            "born_at": now_iso(),
            "born_from": None,
            "district": "contradiction_forest",
            "status": "active",
            "travel_log": [{"district": "contradiction_forest", "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": c.get("hook", ""),
                "data": {
                    "file_path": fp,
                    "statement_a": c["name"].split(" vs ")[0] if " vs " in c["name"] else c["name"],
                    "statement_b": c["name"].split(" vs ")[1] if " vs " in c["name"] else "",
                    "intersection": c.get("mechanism", ""),
                    "proof": c.get("proof", ""),
                },
                "checksum": sha256_file(src),
            },
            "proofs": [],
            "tags": ["contradiction", "imported"],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [contradiction] {cid[:40]}  {c['name']}")
        count += 1
    print(f"  → {count} contradictions connected")


def connect_swarm_dna(reg: dict, dry_run: bool):
    """Register each SWARM_DNA yaml as a c64 artifact citizen."""
    existing = existing_cids(reg)
    count = 0
    for f in sorted(REPO_ROOT.glob("SWARM_DNA_v*.yaml")):
        fp = str(f.relative_to(REPO_ROOT))
        if fp in existing:
            continue
        cid = make_cid("artifact")
        version = f.stem.split("_Version")[0].replace("SWARM_DNA_", "")
        citizen = {
            "cid": cid,
            "name": f"SWARM DNA {version}",
            "kind": "artifact",
            "born_in": "c64",
            "born_at": now_iso(),
            "born_from": None,
            "district": "c64",
            "status": "active",
            "travel_log": [{"district": "c64", "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": f"SWARM DNA genome version {version} — canonical graph projection",
                "data": {"file_path": fp, "file_type": "yaml",
                         "sha256": sha256_file(f)},
                "checksum": sha256_file(f),
            },
            "proofs": [],
            "tags": ["swarm-dna", "c64", "genome", version],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [c64/swarm-dna] {cid[:40]}  {version}")
        count += 1
    print(f"  → {count} SWARM DNA files connected")


def connect_flamelang(reg: dict, dry_run: bool):
    """Register FlameLang spec + interpreter as compiler_city citizens."""
    targets = [
        ("FLAMELANG_SPECIFICATION.md", "FlameLang Specification v1.0", "compiler_city"),
        ("compiler/flamec.py", "FlameLang Interpreter M1 (flamec.py)", "compiler_city"),
        ("compiler/test_m1.py", "FlameLang M1 Test Suite", "compiler_city"),
    ]
    existing = existing_cids(reg)
    count = 0
    for rel, name, district in targets:
        f = REPO_ROOT / rel
        if not f.exists() or rel in existing:
            continue
        cid = make_cid("artifact")
        citizen = {
            "cid": cid,
            "name": name,
            "kind": "artifact",
            "born_in": district,
            "born_at": now_iso(),
            "born_from": None,
            "district": district,
            "status": "active",
            "travel_log": [{"district": district, "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": name,
                "data": {"file_path": rel, "file_type": f.suffix,
                         "sha256": sha256_file(f), "lines": len(f.read_text().splitlines())},
                "checksum": sha256_file(f),
            },
            "proofs": [],
            "tags": ["flamelang", "compiler", district],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [compiler_city] {cid[:40]}  {name}")
        count += 1
    print(f"  → {count} FlameLang artifacts connected")


def connect_genesis(reg: dict, dry_run: bool):
    """Register genesis_prime_core.rs and constitution as genesis citizens."""
    targets = [
        ("genesis_prime_core.rs", "Genesis Prime Core — Cosmological Lock", "genesis"),
        ("ai_constitution.yaml", "AI Constitution — Sovereign Rules", "genesis"),
        ("dao_record_v1.0.yaml", "DAO Record v1.0 — Origin Charter", "genesis"),
        ("quantum_dna_splicer.rs", "Quantum DNA Splicer — Genome Engine", "genesis"),
    ]
    existing = existing_cids(reg)
    count = 0
    for rel, name, district in targets:
        f = REPO_ROOT / rel
        if not f.exists() or rel in existing:
            continue
        cid = make_cid("artifact")
        citizen = {
            "cid": cid,
            "name": name,
            "kind": "artifact",
            "born_in": district,
            "born_at": now_iso(),
            "born_from": None,
            "district": district,
            "status": "archived",
            "travel_log": [{"district": district, "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": name,
                "data": {"file_path": rel, "file_type": Path(rel).suffix,
                         "sha256": sha256_file(f)},
                "checksum": sha256_file(f),
            },
            "proofs": [{"source": "genesis_prime_core.rs",
                        "hash": "genesis_tick:1674852049000",
                        "verified_at": "2023-01-27T21:00:49Z"}],
            "tags": ["genesis", "sealed"],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [genesis] {cid[:40]}  {name}")
        count += 1
    print(f"  → {count} Genesis artifacts connected")


def connect_governance(reg: dict, dry_run: bool):
    """Register governance artifacts as ERU citizens."""
    targets = [
        ("governance/access_matrix.yaml", "DAO Access Matrix v1.0", "eru"),
        ("governance/article_7_authorized_signers.md", "Article 7 — Authorized Signers", "eru"),
        ("UNIFIED_SOVEREIGNTY_ARCHITECTURE(1).md", "Unified Sovereignty Architecture v1", "eru"),
    ]
    existing = existing_cids(reg)
    count = 0
    for rel, name, district in targets:
        f = REPO_ROOT / rel
        if not f.exists() or rel in existing:
            continue
        cid = make_cid("artifact")
        citizen = {
            "cid": cid,
            "name": name,
            "kind": "artifact",
            "born_in": district,
            "born_at": now_iso(),
            "born_from": None,
            "district": district,
            "status": "active",
            "travel_log": [{"district": district, "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": name,
                "data": {"file_path": rel, "sha256": sha256_file(f)},
                "checksum": sha256_file(f),
            },
            "proofs": [],
            "tags": ["governance", "eru", "dao"],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [eru] {cid[:40]}  {name}")
        count += 1
    print(f"  → {count} Governance artifacts connected")


def connect_memory_palace(reg: dict, dry_run: bool):
    """Register Obsidian + memory palace artifacts."""
    targets = [
        ("obsidian_integration_hub.py", "Obsidian Integration Hub", "memory_palace"),
        ("obsidian_network_antibodies.py", "Obsidian Network Antibodies", "memory_palace"),
        ("obsidian_discord_bot.py", "Obsidian Discord Bot", "memory_palace"),
        ("VAULT_SECURITY_PLAYBOOK.md", "Vault Security Playbook", "memory_palace"),
    ]
    existing = existing_cids(reg)
    count = 0
    for rel, name, district in targets:
        f = REPO_ROOT / rel
        if not f.exists() or rel in existing:
            continue
        cid = make_cid("artifact")
        citizen = {
            "cid": cid,
            "name": name,
            "kind": "artifact",
            "born_in": district,
            "born_at": now_iso(),
            "born_from": None,
            "district": district,
            "status": "active",
            "travel_log": [{"district": district, "entered_at": now_iso(),
                            "gate": None, "result": "passed"}],
            "payload": {
                "summary": name,
                "data": {"file_path": rel, "sha256": sha256_file(f)},
                "checksum": sha256_file(f),
            },
            "proofs": [],
            "tags": ["memory_palace", "obsidian"],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [memory_palace] {cid[:40]}  {name}")
        count += 1
    print(f"  → {count} Memory Palace artifacts connected")


# ─── INVENTIONS (things we can't reach yet) ───────────────────────────────────

INVENTIONS_UNREACHABLE = [
    {
        "name": "FlameLang LLVM Backend",
        "summary": "Compile FlameLang .flm → LLVM IR → native binary. M1 interpreter exists; LLVM codegen does not.",
        "contradiction": "FlameLang runs but can't ship as a native binary",
        "tags": ["flamelang", "llvm", "compiler_city", "invention-stub"],
        "district": "compiler_city",
    },
    {
        "name": "C64 Commutation Verifier",
        "summary": "Verify that DNA/MIDI/TRIG6/Geometry/Glyph projections all commute through the 64-node canonical graph. No verifier exists yet.",
        "contradiction": "5 projections describe same territory but no machine checks they agree",
        "tags": ["c64", "commutation", "verifier", "invention-stub"],
        "district": "c64",
    },
    {
        "name": "SAGCO ERU Command",
        "summary": "CLI command: sagco eru audit <citizen-cid> — runs Expected/Reality/Variance check and attaches result as a proof.",
        "contradiction": "ERU framework documented but not executable from CLI",
        "tags": ["eru", "governance", "cli", "invention-stub"],
        "district": "eru",
    },
    {
        "name": "SAGCO Hardware Serial Bridge",
        "summary": "Host-side Rust driver (sagco-serial) that speaks SSP v1 over USB to Arduino/SAGCO-IO bridge. Arduino sketch exists in concept; host driver does not.",
        "contradiction": "Software kernel built; no physical I/O channel",
        "tags": ["hardware", "serial", "arduino", "industrial", "invention-stub"],
        "district": "industrial",
    },
    {
        "name": "Deploy Gate — Proof Required",
        "summary": "Gate that refuses to move a citizen between districts if proofs list is empty. Currently sagco citizen move has no enforcement.",
        "contradiction": "Citizens can move without evidence",
        "tags": ["deploy-gate", "governance", "invention-stub"],
        "district": "trinity",
    },
    {
        "name": "Obsidian Graph Emitter",
        "summary": "Export citizen_registry.json as Obsidian-compatible markdown graph: one note per citizen, edges as [[wiki-links]].",
        "contradiction": "Citizens exist in JSON; Memory Palace cannot see them",
        "tags": ["obsidian", "memory_palace", "graph", "invention-stub"],
        "district": "memory_palace",
    },
    {
        "name": "SAGCO MIDI Citizen Importer",
        "summary": "Parse .mid files in sagco-sheet-music folder → create midi citizens with C64 node mappings via Circle of Fifths.",
        "contradiction": "Sheet music folder exists on WD_BLACK but no citizen format for MIDI",
        "tags": ["midi", "frequency_coast", "c64", "invention-stub"],
        "district": "frequency_coast",
    },
    {
        "name": "Citizen Travel Visualizer",
        "summary": "HTML/SVG map of SAGCO-WORLD districts with citizen dots moving through them in real time from travel_log data.",
        "contradiction": "Map exists in description; no visual render of citizen movement",
        "tags": ["visualization", "gta-map", "invention-stub"],
        "district": "memory_palace",
    },
]


def create_invention_stubs(reg: dict, dry_run: bool):
    existing_names = {c["name"] for c in reg["citizens"]}
    count = 0
    for inv in INVENTIONS_UNREACHABLE:
        if inv["name"] in existing_names:
            continue
        cid = make_cid("invention")
        citizen = {
            "cid": cid,
            "name": inv["name"],
            "kind": "invention",
            "born_in": "contradiction_forest",
            "born_at": now_iso(),
            "born_from": None,
            "district": inv["district"],
            "status": "embryo",
            "travel_log": [
                {"district": "contradiction_forest", "entered_at": now_iso(),
                 "gate": None, "result": "passed"},
                {"district": inv["district"], "entered_at": now_iso(),
                 "gate": "invention_stub_gate", "result": "passed"},
            ],
            "payload": {
                "summary": inv["summary"],
                "data": {
                    "description": inv["summary"],
                    "contradiction_resolved": inv["contradiction"],
                    "implementation_path": "TBD",
                    "stub": True,
                },
                "checksum": "pending",
            },
            "proofs": [],
            "tags": inv["tags"],
            "links": [],
        }
        if not dry_run:
            reg["citizens"].append(citizen)
        print(f"  [invention-stub] {cid[:40]}  {inv['name']}")
        count += 1
    print(f"  → {count} invention stubs created")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="sagco connect",
                                     description="Connect all known artifacts to the Citizen registry")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    globals()["REPO_ROOT"] = Path(args.repo_root)

    reg = load_registry()
    before = len(reg["citizens"])

    print("\n[SAGCO CONNECT] Scanning repo for connectable artifacts...\n")

    print("── Genesis District ──────────────────────────────────────")
    connect_genesis(reg, args.dry_run)

    print("\n── Compiler City ─────────────────────────────────────────")
    connect_flamelang(reg, args.dry_run)

    print("\n── C64 Ring Road ─────────────────────────────────────────")
    connect_swarm_dna(reg, args.dry_run)

    print("\n── ERU Governance ────────────────────────────────────────")
    connect_governance(reg, args.dry_run)

    print("\n── Memory Palace ─────────────────────────────────────────")
    connect_memory_palace(reg, args.dry_run)

    print("\n── Contradiction Forest → Inventions ─────────────────────")
    connect_contradictions(reg, args.dry_run)

    print("\n── Invention Stubs (unreachable territory) ───────────────")
    create_invention_stubs(reg, args.dry_run)

    after = len(reg["citizens"])
    delta = after - before

    if not args.dry_run:
        save_registry(reg)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}[SAGCO CONNECT] Complete.")
    print(f"  Before: {before} citizens")
    print(f"  After:  {after} citizens")
    print(f"  Added:  {delta} new citizens")
    print(f"\n  Registry: {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
