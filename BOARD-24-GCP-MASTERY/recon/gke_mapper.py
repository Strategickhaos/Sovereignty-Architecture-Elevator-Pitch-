#!/usr/bin/env python3
"""
GKE Mapper — BOARD-24-GCP-MASTERY recon module

Discovers live GKE clusters and maps them into:
  - SAGCO node manifests
  - BOARD-21-PHYSICS-FLEET cluster list
  - Citizen registry entries

Usage:
  python gke_mapper.py --project my-project
  python gke_mapper.py --auto
  python gke_mapper.py --emit-citizens
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CITIZENS  = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
MANIFESTS = Path(__file__).resolve().parent.parent / "citizens"
PHYSICS   = REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "manifests" / "gke-clusters.yaml"

GENESIS_INCREMENT = 3449
PID_BASE = 8000

def _gcloud(cmd: list[str], project: str | None = None) -> list | None:
    full = ["gcloud"] + cmd + ["--format=json"]
    if project:
        full += ["--project", project]
    try:
        raw = subprocess.check_output(full, stderr=subprocess.DEVNULL, timeout=20).decode()
        return json.loads(raw)
    except Exception:
        return None

def _auto_project() -> str | None:
    try:
        return subprocess.check_output(
            ["gcloud", "config", "get-value", "project"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode().strip() or None
    except Exception:
        return None

def map_clusters(project: str, emit_citizens: bool = False) -> list[dict]:
    raw = _gcloud(["container", "clusters", "list"], project)
    if not isinstance(raw, list):
        print(f"  gcloud returned no clusters (check project={project} and auth)")
        return []

    MANIFESTS.mkdir(parents=True, exist_ok=True)
    nodes = []
    pid = PID_BASE

    for i, c in enumerate(raw):
        name     = c.get("name", f"cluster-{i}")
        zone     = c.get("zone") or c.get("location", "unknown")
        status   = c.get("status", "UNKNOWN")
        version  = c.get("currentMasterVersion", "")
        nodes_n  = c.get("currentNodeCount", 0)
        endpoint = c.get("endpoint", "")

        tick = int(time.time() * 1000) + i
        cid  = f"sgc-artifact-{tick}-{tick % GENESIS_INCREMENT}"
        canonical = f"GKE.CLUSTER.{name.upper().replace('-','_')}"

        node = {
            "pid": pid + i, "cid": cid, "canonical": canonical,
            "name": name, "project": project, "zone": zone,
            "status": status, "k8s_version": version,
            "node_count": nodes_n, "endpoint": endpoint,
            "district": "eru", "kind": "artifact",
            "tags": ["gke", "kubernetes", "cluster"],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        nodes.append(node)

        yaml_out = MANIFESTS / f"{canonical}.yaml"
        yaml_out.write_text(
            f"pid: {node['pid']}\n"
            f"cid: {cid}\n"
            f"canonical: {canonical}\n"
            f"name: {name}\n"
            f"project: {project}\n"
            f"zone: {zone}\n"
            f"status: {status}\n"
            f"k8s_version: {version}\n"
            f"node_count: {nodes_n}\n"
            f"endpoint: {endpoint}\n"
            f"district: eru\n"
            f"team: purple\n"
            f"physics_analog: ERU engine — Expected/Reality/Variance synthesis\n"
        )
        print(f"  → {canonical}  [{status}]  nodes={nodes_n}  zone={zone}")

    if emit_citizens and nodes:
        _register(nodes)

    # Update physics fleet manifest
    _update_physics_fleet(nodes)
    return nodes

def _register(nodes: list[dict]):
    if not CITIZENS.exists():
        return
    raw = json.loads(CITIZENS.read_text())
    if isinstance(raw, list):
        doc, citizens = None, raw
    else:
        doc, citizens = raw, raw.get("citizens", [])
    existing = {c["cid"] for c in citizens}
    added = 0
    for n in nodes:
        if n["cid"] in existing:
            continue
        citizens.append({
            "cid": n["cid"], "name": n["name"], "kind": "artifact",
            "born_in": "genesis", "district": "eru", "status": n["status"].lower(),
            "travel_log": [], "payload": n, "proofs": [],
            "tags": n["tags"] + ["gcp", "board-24"],
            "links": [], "created_at": n["created_at"],
        })
        added += 1
    if doc:
        doc["citizens"] = citizens
        CITIZENS.write_text(json.dumps(doc, indent=2))
    else:
        CITIZENS.write_text(json.dumps(citizens, indent=2))
    print(f"  registered {added} GKE cluster citizens")

def _update_physics_fleet(nodes: list[dict]):
    try:
        import yaml
        existing = yaml.safe_load(PHYSICS.read_text()) if PHYSICS.exists() else {"clusters": []}
        known = {c["name"] for c in existing.get("clusters", [])}
        for n in nodes:
            if n["name"] not in known:
                existing["clusters"].append({
                    "name": n["name"], "type": "gke",
                    "role": "purple_team", "district": "eru",
                    "team": "purple",
                    "physics_analog": "ERU engine",
                    "status": n["status"].lower(),
                })
        PHYSICS.write_text(yaml.dump(existing, sort_keys=False, allow_unicode=True))
        print(f"  updated BOARD-21 cluster manifest")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="SAGCO GKE Mapper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", help="GCP project ID")
    group.add_argument("--auto", action="store_true")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    project = args.project or _auto_project()
    if not project:
        print("ERROR: no project — run gcloud config set project <id>")
        sys.exit(1)

    print(f"\n  GKE Mapper — project={project}")
    clusters = map_clusters(project, emit_citizens=args.emit_citizens)
    print(f"\n  {len(clusters)} cluster(s) mapped")

if __name__ == "__main__":
    main()
