"""
GKE Fleet Orchestrator — BOARD-21-PHYSICS-FLEET

Treats each GKE cluster as a physical system node.
Reads cluster manifests, queries live state via kubectl/gcloud,
and produces bloodwork panels (metric reports).

Usage:
  python gke_fleet_orchestrator.py --status          # fleet health summary
  python gke_fleet_orchestrator.py --bloodwork        # full metric panels
  python gke_fleet_orchestrator.py --cluster <name>  # single cluster deep dive
"""
import argparse, json, subprocess, time
from pathlib import Path

BOARD     = Path(__file__).resolve().parent.parent
MANIFESTS = BOARD / "manifests"
REPORTS   = BOARD / "reports"

def _kubectl(cmd: list[str]) -> dict | list | None:
    try:
        raw = subprocess.check_output(
            ["kubectl"] + cmd + ["-o", "json"],
            stderr=subprocess.DEVNULL, timeout=15
        ).decode()
        return json.loads(raw)
    except Exception:
        return None

def _gcloud(cmd: list[str]) -> list | None:
    try:
        raw = subprocess.check_output(
            ["gcloud"] + cmd + ["--format=json"],
            stderr=subprocess.DEVNULL, timeout=20
        ).decode()
        return json.loads(raw)
    except Exception:
        return None

def load_clusters() -> list[dict]:
    try:
        import yaml
        data = yaml.safe_load((MANIFESTS / "gke-clusters.yaml").read_text())
        return data.get("clusters", [])
    except Exception:
        return []

def bloodwork_panel(cluster: dict) -> dict:
    """Produce a metric panel (bloodwork) for a cluster."""
    name = cluster["name"]
    panel = {
        "cluster":   name,
        "role":      cluster.get("role", "unknown"),
        "team":      cluster.get("team", "purple"),
        "district":  cluster.get("district", "eru"),
        "physics":   cluster.get("physics_analog", ""),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metrics":   {},
        "warnings":  [],
        "status":    "pending_claim",
    }

    # Try live kubectl
    nodes = _kubectl(["get", "nodes"])
    if nodes:
        node_list = nodes.get("items", [])
        panel["metrics"]["node_count"] = len(node_list)
        not_ready = [
            n["metadata"]["name"]
            for n in node_list
            if any(
                c.get("type") == "Ready" and c.get("status") != "True"
                for c in n.get("status", {}).get("conditions", [])
            )
        ]
        if not_ready:
            panel["warnings"].append(f"Nodes not ready: {not_ready}")
        panel["status"] = "online"

    pods = _kubectl(["get", "pods", "--all-namespaces"])
    if pods:
        pod_list = pods.get("items", [])
        panel["metrics"]["pod_count"] = len(pod_list)
        failed = [
            p["metadata"]["name"]
            for p in pod_list
            if p.get("status", {}).get("phase") in ("Failed", "Unknown")
        ]
        if failed:
            panel["warnings"].append(f"Failed pods: {failed[:5]}")

    # Physics interpretation
    if panel["metrics"].get("node_count", 0) == 0:
        panel["physics_state"] = "dark_matter — cluster exists in manifest but not yet observable"
    else:
        cpu_warn = len(panel["warnings"]) > 0
        panel["physics_state"] = "high_entropy" if cpu_warn else "stable"

    return panel

def fleet_status() -> list[dict]:
    clusters = load_clusters()
    panels = []
    print(f"\n  SAGCO Physics Fleet — {len(clusters)} cluster(s)\n")
    for c in clusters:
        panel = bloodwork_panel(c)
        panels.append(panel)
        state_sym = {"online": "✓", "high_entropy": "⚠", "pending_claim": "…", "dark_matter": "?"}
        sym = state_sym.get(panel.get("physics_state", "pending_claim"), "?")
        print(f"  {sym} [{panel['team'].upper():6}] {c['name']:<30} {panel.get('physics_state','pending_claim')}")
        if panel["warnings"]:
            for w in panel["warnings"]:
                print(f"         ⚠  {w}")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "physics_fleet_runtime_report.json"
    out.write_text(json.dumps(panels, indent=2))
    print(f"\n  report → {out}")
    return panels

def main():
    parser = argparse.ArgumentParser(description="SAGCO GKE Fleet Orchestrator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status",    action="store_true", help="Fleet health summary")
    group.add_argument("--bloodwork", action="store_true", help="Full metric panels")
    group.add_argument("--cluster",   help="Single cluster deep dive")
    args = parser.parse_args()

    if args.status or args.bloodwork:
        fleet_status()
    elif args.cluster:
        clusters = load_clusters()
        c = next((x for x in clusters if x["name"] == args.cluster), None)
        if not c:
            print(f"ERROR: cluster {args.cluster} not in manifests/gke-clusters.yaml")
            return
        panel = bloodwork_panel(c)
        print(json.dumps(panel, indent=2))

if __name__ == "__main__":
    main()
