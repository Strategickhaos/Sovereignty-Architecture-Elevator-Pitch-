#!/usr/bin/env python3
"""
sagco catpush — universal node constructor

Takes ANYTHING and turns it into:
  node + PID + YAML manifest + citizen + recon artifact

Usage:
  python catpush.py <path>                     # file or directory
  python catpush.py <path> --kind proof        # explicit kind
  python catpush.py <path> --district eru      # explicit district
  python catpush.py --docker <container>       # running container
  python catpush.py --url <url>                # browser tab / URL
  python catpush.py --pid-file pid.lock        # load existing PID state
  python catpush.py --list                     # show all registered nodes
"""

import argparse, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
REGISTRY    = Path(__file__).resolve().parent / "citizen_registry.json"
MANIFESTS   = Path(__file__).resolve().parent / "catpush_manifests"
PID_LOCK    = Path(__file__).resolve().parent / "catpush_pid.lock"

DISTRICTS = [
    "genesis", "compiler_city", "c64", "eru", "trinity",
    "frequency_coast", "industrial", "memory_palace", "contradiction_forest",
]
KINDS = ["proof", "invention", "artifact", "contradiction", "deploy_packet", "midi", "trig6_state"]

GENESIS_INCREMENT = 3449

# ── PID allocator ─────────────────────────────────────────────────────────────

def _load_pid_state() -> dict:
    if PID_LOCK.exists():
        return json.loads(PID_LOCK.read_text())
    return {"next_pid": 7000, "allocated": {}}

def _save_pid_state(state: dict):
    PID_LOCK.write_text(json.dumps(state, indent=2))

def allocate_pid(canonical: str) -> int:
    state = _load_pid_state()
    if canonical in state["allocated"]:
        return state["allocated"][canonical]
    pid = state["next_pid"]
    state["allocated"][canonical] = pid
    state["next_pid"] = pid + 1
    _save_pid_state(state)
    return pid

# ── CID generator ─────────────────────────────────────────────────────────────

def make_cid(kind: str) -> str:
    tick = int(time.time() * 1000)
    return f"sgc-{kind}-{tick}-{tick % GENESIS_INCREMENT}"

# ── Classifier — auto-detect kind and district from a path ───────────────────

EXT_MAP = {
    ".rs":    ("artifact", "compiler_city"),
    ".py":    ("artifact", "compiler_city"),
    ".ts":    ("artifact", "compiler_city"),
    ".js":    ("artifact", "compiler_city"),
    ".go":    ("artifact", "compiler_city"),
    ".flame": ("artifact", "compiler_city"),
    ".yaml":  ("artifact", "memory_palace"),
    ".yml":   ("artifact", "memory_palace"),
    ".json":  ("artifact", "memory_palace"),
    ".toml":  ("artifact", "memory_palace"),
    ".md":    ("artifact", "memory_palace"),
    ".txt":   ("artifact", "memory_palace"),
    ".pdf":   ("proof",    "memory_palace"),
    ".mid":   ("midi",     "frequency_coast"),
    ".midi":  ("midi",     "frequency_coast"),
    ".wav":   ("midi",     "frequency_coast"),
    ".sh":    ("deploy_packet", "industrial"),
    ".ps1":   ("deploy_packet", "industrial"),
    ".dockerfile": ("deploy_packet", "industrial"),
}

NAME_HINTS = {
    "antibod":    ("artifact",     "trinity"),
    "proof":      ("proof",        "genesis"),
    "citizen":    ("artifact",     "genesis"),
    "deploy":     ("deploy_packet","industrial"),
    "recon":      ("artifact",     "compiler_city"),
    "docker":     ("deploy_packet","industrial"),
    "daemon":     ("deploy_packet","industrial"),
    "contradict": ("contradiction","contradiction_forest"),
    "midi":       ("midi",         "frequency_coast"),
    "flame":      ("artifact",     "compiler_city"),
    "genome":     ("artifact",     "genesis"),
    "dna":        ("artifact",     "genesis"),
    "governance": ("artifact",     "eru"),
    "legal":      ("proof",        "eru"),
}

def classify(path: Path) -> tuple[str, str]:
    name_lower = path.name.lower()
    for hint, (kind, district) in NAME_HINTS.items():
        if hint in name_lower:
            return kind, district
    if path.is_dir():
        return "artifact", "memory_palace"
    ext = path.suffix.lower()
    return EXT_MAP.get(ext, ("artifact", "genesis"))

# ── Payload builders ──────────────────────────────────────────────────────────

def _hash_file(p: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(p.read_bytes())
    except Exception:
        pass
    return h.hexdigest()[:16]

def build_payload_path(path: Path) -> dict:
    payload = {
        "type":  "directory" if path.is_dir() else "file",
        "path":  str(path.resolve()),
        "name":  path.name,
        "ext":   path.suffix,
    }
    if path.is_file():
        try:
            payload["size_bytes"] = path.stat().st_size
            payload["sha256_short"] = _hash_file(path)
        except Exception:
            pass
    elif path.is_dir():
        try:
            children = list(path.iterdir())
            payload["child_count"] = len(children)
            payload["sample"] = [c.name for c in children[:8]]
        except Exception:
            pass
    return payload

def build_payload_docker(container: str) -> dict:
    try:
        raw = subprocess.check_output(
            ["docker", "inspect", container, "--format", "{{json .}}"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode()
        data = json.loads(raw)
        if isinstance(data, list):
            data = data[0]
        return {
            "type":   "docker_container",
            "id":     data.get("Id", "")[:12],
            "name":   data.get("Name", "").lstrip("/"),
            "image":  data.get("Config", {}).get("Image", ""),
            "status": data.get("State", {}).get("Status", ""),
            "ports":  data.get("NetworkSettings", {}).get("Ports", {}),
        }
    except Exception as e:
        return {"type": "docker_container", "name": container, "error": str(e)}

def build_payload_url(url: str) -> dict:
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        return {
            "type":   "url",
            "url":    url,
            "host":   p.netloc,
            "scheme": p.scheme,
            "path":   p.path,
        }
    except Exception:
        return {"type": "url", "url": url}

# ── Canonical name generator ──────────────────────────────────────────────────

def make_canonical(name: str, kind: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").upper()
    return f"CATPUSH.{kind.upper()}.{clean}"

# ── YAML manifest writer ──────────────────────────────────────────────────────

def write_manifest(node: dict) -> Path:
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "_", node["canonical"])
    out = MANIFESTS / f"{safe}.yaml"
    try:
        import yaml
        out.write_text(yaml.dump(node, sort_keys=False, allow_unicode=True))
    except ImportError:
        out.with_suffix(".json").write_text(json.dumps(node, indent=2))
        out = out.with_suffix(".json")
    return out

# ── Citizen registry ──────────────────────────────────────────────────────────

def register_citizen(node: dict) -> str:
    if REGISTRY.exists():
        raw = json.loads(REGISTRY.read_text())
        if isinstance(raw, list):
            doc, registry = None, raw
        else:
            doc, registry = raw, raw.get("citizens", [])
    else:
        doc, registry = None, []

    citizen = {
        "cid":        node["cid"],
        "name":       node["name"],
        "kind":       node["kind"],
        "born_in":    "genesis",
        "district":   node["district"],
        "status":     "active",
        "travel_log": [],
        "payload":    node["payload"],
        "proofs":     [],
        "tags":       node.get("tags", []) + ["catpush"],
        "links":      [],
        "created_at": node["created_at"],
    }
    existing_cids = {c["cid"] for c in registry}
    if node["cid"] not in existing_cids:
        registry.append(citizen)
        if doc is not None:
            doc["citizens"] = registry
            REGISTRY.write_text(json.dumps(doc, indent=2))
        else:
            REGISTRY.write_text(json.dumps(registry, indent=2))
    return node["cid"]

# ── Core push ─────────────────────────────────────────────────────────────────

def catpush(
    name: str,
    payload: dict,
    kind: str,
    district: str,
    tags: list[str] | None = None,
) -> dict:
    canonical = make_canonical(name, kind)
    pid       = allocate_pid(canonical)
    cid       = make_cid(kind)
    now       = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    node = {
        "cid":        cid,
        "pid":        pid,
        "canonical":  canonical,
        "name":       name,
        "kind":       kind,
        "district":   district,
        "status":     "active",
        "payload":    payload,
        "tags":       (tags or []),
        "created_at": now,
    }

    manifest_path = write_manifest(node)
    citizen_cid   = register_citizen(node)

    print(f"\n  ✓ CATPUSH")
    print(f"    cid       : {cid}")
    print(f"    pid       : {pid}")
    print(f"    canonical : {canonical}")
    print(f"    kind      : {kind}  →  district: {district}")
    print(f"    manifest  : {manifest_path}")
    print(f"    citizen   : {citizen_cid}")

    return node

# ── List command ──────────────────────────────────────────────────────────────

def list_nodes():
    state = _load_pid_state()
    allocated = state.get("allocated", {})
    if not allocated:
        print("  No catpush nodes registered yet.")
        return
    print(f"\n  CATPUSH REGISTRY  ({len(allocated)} node(s))\n")
    print(f"  {'PID':<8} {'CANONICAL'}")
    print(f"  {'---':<8} {'---------'}")
    for canonical, pid in sorted(allocated.items(), key=lambda x: x[1]):
        print(f"  {pid:<8} {canonical}")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="catpush",
        description="SAGCO catpush — universal node constructor",
        epilog="Everything becomes a node.",
    )

    source = parser.add_mutually_exclusive_group()
    source.add_argument("path",      nargs="?", help="File or directory path")
    source.add_argument("--docker",  metavar="CONTAINER", help="Docker container name/id")
    source.add_argument("--url",     help="URL (browser tab, API, etc.)")
    source.add_argument("--list",    action="store_true", help="List all registered nodes")

    parser.add_argument("--kind",     choices=KINDS,     help="Override kind classification")
    parser.add_argument("--district", choices=DISTRICTS, help="Override district routing")
    parser.add_argument("--name",     help="Override display name")
    parser.add_argument("--tag",      action="append",   dest="tags", help="Tag (can repeat)")

    args = parser.parse_args()

    if args.list:
        list_nodes()
        return

    # ── resolve source + payload
    if args.docker:
        payload  = build_payload_docker(args.docker)
        name     = args.name or args.docker
        kind     = args.kind or "deploy_packet"
        district = args.district or "industrial"

    elif args.url:
        payload  = build_payload_url(args.url)
        name     = args.name or payload.get("host", args.url)
        kind     = args.kind or "artifact"
        district = args.district or "memory_palace"

    elif args.path:
        p = Path(args.path)
        if not p.exists():
            print(f"ERROR: path does not exist: {p}")
            sys.exit(1)
        payload  = build_payload_path(p)
        auto_kind, auto_district = classify(p)
        name     = args.name or p.name
        kind     = args.kind or auto_kind
        district = args.district or auto_district

    else:
        parser.print_help()
        sys.exit(0)

    catpush(name=name, payload=payload, kind=kind, district=district, tags=args.tags or [])


if __name__ == "__main__":
    main()
