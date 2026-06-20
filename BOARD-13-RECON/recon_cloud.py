"""
SAGCO Cloud Recon — captures GCP reality into nodes + citizens.

Requires: google-cloud-resource-manager, google-cloud-run, google-cloud-container
          google-cloud-pubsub, google-cloud-logging  (all optional — graceful fallback)
          gcloud CLI (used as fallback via subprocess)

Usage:
  python recon_cloud.py --project my-gcp-project
  python recon_cloud.py --auto           # reads PROJECT from gcloud config
  python recon_cloud.py --project X --emit-citizens
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
MANIFESTS   = Path(__file__).resolve().parent / "manifests"
CITIZENS    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

# ── helpers ──────────────────────────────────────────────────────────────────

def _gcloud(args: list[str], project: str | None = None) -> list[dict] | str:
    cmd = ["gcloud"] + args + ["--format=json"]
    if project:
        cmd += ["--project", project]
    try:
        raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=30).decode()
        return json.loads(raw)
    except subprocess.CalledProcessError as e:
        return []
    except json.JSONDecodeError as e:
        return []
    except FileNotFoundError:
        return []

def _gcloud_text(args: list[str]) -> str:
    try:
        return subprocess.check_output(["gcloud"] + args, stderr=subprocess.DEVNULL, timeout=15).decode().strip()
    except Exception:
        return ""

def _auto_project() -> str | None:
    v = _gcloud_text(["config", "get-value", "project"])
    return v if v else None

# ── scanners ─────────────────────────────────────────────────────────────────

def scan_project_info(project: str) -> dict:
    raw = _gcloud(["projects", "describe", project])
    if isinstance(raw, dict):
        return raw
    return {"projectId": project, "note": "gcloud describe failed — using id only"}

def scan_cloud_run(project: str) -> list[dict]:
    services = _gcloud(["run", "services", "list", "--platform=managed"], project)
    if not isinstance(services, list):
        return []
    results = []
    for s in services:
        meta = s.get("metadata", {})
        spec = s.get("status", {})
        results.append({
            "name":      meta.get("name", "unknown"),
            "namespace": meta.get("namespace", ""),
            "region":    meta.get("labels", {}).get("cloud.googleapis.com/location", ""),
            "url":       spec.get("url", ""),
            "ready":     any(
                c.get("type") == "Ready" and c.get("status") == "True"
                for c in spec.get("conditions", [])
            ),
            "kind": "cloud_run_service",
        })
    return results

def scan_gke_clusters(project: str) -> list[dict]:
    clusters = _gcloud(["container", "clusters", "list"], project)
    if not isinstance(clusters, list):
        return []
    results = []
    for c in clusters:
        results.append({
            "name":         c.get("name", "unknown"),
            "zone":         c.get("zone") or c.get("location", ""),
            "status":       c.get("status", ""),
            "node_count":   c.get("currentNodeCount", 0),
            "k8s_version":  c.get("currentMasterVersion", ""),
            "endpoint":     c.get("endpoint", ""),
            "kind":         "gke_cluster",
        })
    return results

def scan_pubsub(project: str) -> list[dict]:
    topics = _gcloud(["pubsub", "topics", "list"], project)
    if not isinstance(topics, list):
        return []
    return [{"name": t.get("name", "").split("/")[-1], "kind": "pubsub_topic"} for t in topics]

def scan_iam_service_accounts(project: str) -> list[dict]:
    accounts = _gcloud(["iam", "service-accounts", "list"], project)
    if not isinstance(accounts, list):
        return []
    results = []
    for a in accounts:
        results.append({
            "email":        a.get("email", ""),
            "display_name": a.get("displayName", ""),
            "disabled":     a.get("disabled", False),
            "kind":         "iam_service_account",
        })
    return results

def scan_artifact_registry(project: str) -> list[dict]:
    repos = _gcloud(["artifacts", "repositories", "list"], project)
    if not isinstance(repos, list):
        return []
    results = []
    for r in repos:
        results.append({
            "name":   r.get("name", "").split("/")[-1],
            "format": r.get("format", ""),
            "region": r.get("name", "").split("/")[3] if "/" in r.get("name", "") else "",
            "kind":   "artifact_registry",
        })
    return results

def scan_k8s_events(project: str, clusters: list[dict]) -> list[dict]:
    """Pull recent Warning events from each GKE cluster."""
    all_events = []
    for cluster in clusters[:2]:  # cap at 2 clusters to avoid timeout
        name = cluster["name"]
        zone = cluster["zone"]
        try:
            subprocess.run(
                ["gcloud", "container", "clusters", "get-credentials",
                 name, "--zone", zone, "--project", project],
                capture_output=True, timeout=20
            )
            raw = subprocess.check_output(
                ["kubectl", "get", "events", "--all-namespaces",
                 "--field-selector=type=Warning", "-o=json"],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode()
            items = json.loads(raw).get("items", [])
            for item in items[:20]:
                all_events.append({
                    "cluster":  name,
                    "reason":   item.get("reason", ""),
                    "message":  item.get("message", "")[:200],
                    "object":   item.get("involvedObject", {}).get("name", ""),
                    "kind":     "k8s_warning_event",
                })
        except Exception:
            pass
    return all_events

# ── citizen registration ──────────────────────────────────────────────────────

def _make_citizen(name: str, kind: str, district: str, payload: dict, tags: list[str]) -> dict:
    tick = int(time.time() * 1000)
    return {
        "cid":        f"sgc-artifact-{tick}-{tick % 3449}",
        "name":       name,
        "kind":       "artifact",
        "born_in":    "genesis",
        "district":   district,
        "status":     "active",
        "travel_log": [],
        "payload":    payload,
        "proofs":     [],
        "tags":       tags + ["cloud", "recon"],
        "links":      [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def register_citizens(resources: dict) -> list[dict]:
    if not CITIZENS.exists():
        print("  citizen registry not found — skipping")
        return []

    registry = json.loads(CITIZENS.read_text())
    new_citizens = []

    for svc in resources.get("cloud_run", []):
        c = _make_citizen(
            f"Cloud Run — {svc['name']}", "artifact", "compiler_city",
            svc, ["cloud_run", "service"]
        )
        new_citizens.append(c)

    for cluster in resources.get("gke_clusters", []):
        c = _make_citizen(
            f"GKE — {cluster['name']}", "artifact", "eru",
            cluster, ["gke", "kubernetes", "cluster"]
        )
        new_citizens.append(c)

    for topic in resources.get("pubsub", []):
        c = _make_citizen(
            f"Pub/Sub — {topic['name']}", "artifact", "frequency_coast",
            topic, ["pubsub", "messaging"]
        )
        new_citizens.append(c)

    for sa in resources.get("service_accounts", []):
        c = _make_citizen(
            f"IAM SA — {sa['display_name'] or sa['email']}", "artifact", "trinity",
            sa, ["iam", "service_account"]
        )
        new_citizens.append(c)

    registry.extend(new_citizens)
    CITIZENS.write_text(json.dumps(registry, indent=2))
    print(f"  registered {len(new_citizens)} cloud citizens in 08-CITIZENS")
    return new_citizens

# ── manifest writer ───────────────────────────────────────────────────────────

def write_manifest(project: str, resources: dict) -> Path:
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    nodes = []
    pid = 6000
    for kind_key, district in [
        ("cloud_run", "compiler_city"),
        ("gke_clusters", "eru"),
        ("pubsub", "frequency_coast"),
        ("service_accounts", "trinity"),
        ("artifact_repos", "memory_palace"),
    ]:
        for item in resources.get(kind_key, []):
            name = item.get("name") or item.get("email", "unknown")
            nodes.append({
                "pid":      pid,
                "canonical": f"CLOUD.{kind_key.upper()}.{name.upper().replace('-','_')}",
                "kind":     item.get("kind", kind_key),
                "district": district,
                "project":  project,
                "source":   item,
            })
            pid += 1

    out = MANIFESTS / f"cloud_nodes_{project}.yaml"
    import yaml
    out.write_text(yaml.dump({"project": project, "nodes": nodes}, sort_keys=False, allow_unicode=True))
    print(f"  node manifest → {out}  ({len(nodes)} nodes)")
    return out

# ── main ─────────────────────────────────────────────────────────────────────

def scan(project: str, emit_citizens: bool = False) -> dict:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nSAGCO Cloud Recon — project: {project}")
    print("---")

    resources = {}

    print("  scanning Cloud Run services...")
    resources["cloud_run"] = scan_cloud_run(project)
    print(f"    → {len(resources['cloud_run'])} service(s)")

    print("  scanning GKE clusters...")
    resources["gke_clusters"] = scan_gke_clusters(project)
    print(f"    → {len(resources['gke_clusters'])} cluster(s)")

    print("  scanning Pub/Sub topics...")
    resources["pubsub"] = scan_pubsub(project)
    print(f"    → {len(resources['pubsub'])} topic(s)")

    print("  scanning IAM service accounts...")
    resources["service_accounts"] = scan_iam_service_accounts(project)
    print(f"    → {len(resources['service_accounts'])} account(s)")

    print("  scanning Artifact Registry...")
    resources["artifact_repos"] = scan_artifact_registry(project)
    print(f"    → {len(resources['artifact_repos'])} repo(s)")

    if resources["gke_clusters"]:
        print("  scanning Kubernetes Warning events...")
        resources["k8s_events"] = scan_k8s_events(project, resources["gke_clusters"])
        print(f"    → {len(resources['k8s_events'])} warning event(s)")

    out = REPORTS_DIR / f"cloud_resources_{project}.json"
    out.write_text(json.dumps(resources, indent=2))
    print(f"\n  report → {out}")

    try:
        import yaml  # noqa: F401
        write_manifest(project, resources)
    except ImportError:
        print("  (install pyyaml for node manifest output)")

    if emit_citizens:
        register_citizens(resources)

    return resources


def main():
    parser = argparse.ArgumentParser(description="SAGCO Cloud Recon")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", help="GCP project ID")
    group.add_argument("--auto",    action="store_true", help="Read project from gcloud config")
    parser.add_argument("--emit-citizens", action="store_true", help="Write cloud resources to citizen registry")
    args = parser.parse_args()

    project = args.project
    if args.auto:
        project = _auto_project()
        if not project:
            print("ERROR: no project in gcloud config. Run: gcloud config set project <id>")
            sys.exit(1)
        print(f"  auto-detected project: {project}")

    scan(project, emit_citizens=args.emit_citizens)
    print("\nDone.")


if __name__ == "__main__":
    main()
