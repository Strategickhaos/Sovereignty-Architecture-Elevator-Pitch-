#!/usr/bin/env python3
"""
SAGCO Hub Navigator — Docker Desktop sidebar equivalent, SAGCO-native.

Mirrors the Docker Desktop sidebar:
  Containers · Images · Logs · Volumes · Kubernetes · Builds · Models · Extensions

Usage:
  agent_hub.py --containers  [--running]
  agent_hub.py --images
  agent_hub.py --volumes
  agent_hub.py --kubernetes  [--namespace NS]
  agent_hub.py --builds
  agent_hub.py --models
  agent_hub.py --extensions
  agent_hub.py --logs        [--container NAME]
  agent_hub.py --all
"""
import argparse, json, subprocess, sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
K8S_CLUSTER = "10.96.0.1:443"

SAGCO_NAMESPACES = [
    "sagco-genesis", "sagco-eru", "sagco-trinity",
    "sagco-industrial", "sagco-frequency",
]

# District color markers
DISTRICT_MARK = {
    "genesis": "⚪", "eru": "🟣", "trinity": "🔵",
    "industrial": "🟠", "frequency_coast": "🟢",
    "contradiction_forest": "🔴", "memory_palace": "🟡",
}

def _docker(args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["docker"] + args, stderr=subprocess.DEVNULL, timeout=15
        ).decode()
    except Exception:
        return None

def _kubectl(args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["kubectl"] + args, stderr=subprocess.DEVNULL, timeout=15
        ).decode()
    except Exception:
        return None

# ── SAGCO district classifier ─────────────────────────────────────────────────

def _classify_container(name: str) -> str:
    name = name.lower()
    if "sentinel" in name or "blue" in name:   return "trinity"
    if "red" in name or "chaos" in name:        return "contradiction_forest"
    if "purple" in name or "eru" in name:       return "eru"
    if "observer" in name or "recon" in name:   return "industrial"
    if "mcp" in name or "frequency" in name:    return "frequency_coast"
    if "self" in name or "genesis" in name:     return "genesis"
    if "daemon" in name:                        return "industrial"
    return "memory_palace"

# ── Sidebar tabs ──────────────────────────────────────────────────────────────

def show_containers(running_only: bool = False):
    fmt = '{{json .}}'
    args = ["ps", "--format", fmt]
    if not running_only:
        args.append("-a")
    out = _docker(args)
    if not out:
        print("  Docker not reachable"); return

    print(f"\n  SAGCO Hub — Containers {'(running)' if running_only else '(all)'}\n")
    print(f"  {'District':15s}  {'Name':35s}  {'Status':10s}  {'CPU':8s}  {'Memory'}")
    print("  " + "─" * 85)

    containers = [json.loads(l) for l in out.splitlines() if l.strip()]
    for c in containers:
        name   = c.get("Names", "?").lstrip("/")
        status = c.get("Status", "?")[:10]
        dist   = _classify_container(name)
        mark   = DISTRICT_MARK.get(dist, "⚫")
        print(f"  {mark} {dist:13s}  {name:35s}  {status:10s}")

    print(f"\n  {len(containers)} container(s)")


def show_images():
    out = _docker(["images", "--format", "{{json .}}"])
    if not out:
        print("  Docker not reachable"); return

    print(f"\n  SAGCO Hub — Images\n")
    print(f"  {'Name':50s}  {'Tag':10s}  {'Size':10s}  {'Created'}")
    print("  " + "─" * 85)

    images = [json.loads(l) for l in out.splitlines() if l.strip()]
    for img in images:
        repo = img.get("Repository", "?")
        tag  = img.get("Tag", "?")[:10]
        size = img.get("Size", "?")
        cre  = img.get("CreatedSince", "?")
        mark = "🟢" if any(s in repo for s in ("sagco-os", "sagco-controls", "sagco-core")) else "⚫"
        print(f"  {mark} {repo:48s}  {tag:10s}  {size:10s}  {cre}")

    print(f"\n  {len(images)} image(s)  |  kernel: sagco-os  |  controls: sagco-controls-v2")


def show_volumes():
    out = _docker(["volume", "ls", "--format", "{{json .}}"])
    if not out:
        print("  Docker not reachable"); return

    print(f"\n  SAGCO Hub — Volumes\n")
    KNOWN = {
        "mobiledevices_sagco-reports": ("39GB",  "memory_palace"),
        "mobiledevices_sagco-data":    ("7.8MB", "industrial"),
        "mobiledevices_sagco-ledger":  ("0B",    "genesis"),
        "sagco-neuron":                ("0B",    "eru"),
        "sagco-neuron-cloned":         ("0B",    "eru"),
        "soscclomfleet":               ("0B",    "frequency_coast"),
        "soscclomfleet-cloned":        ("0B",    "frequency_coast"),
    }
    volumes = [json.loads(l) for l in out.splitlines() if l.strip()]
    for v in volumes:
        name = v.get("Name", "?")
        size, dist = KNOWN.get(name, ("?", "memory_palace"))
        mark = DISTRICT_MARK.get(dist, "⚫")
        print(f"  {mark} {dist:20s}  {name:45s}  {size}")
    print(f"\n  {len(volumes)} volume(s)")


def show_kubernetes(namespace: str | None = None):
    print(f"\n  SAGCO Hub — Kubernetes  [{K8S_CLUSTER}]\n")
    ns_list = [namespace] if namespace else SAGCO_NAMESPACES

    for ns in ns_list:
        dist = ns.replace("sagco-", "").replace("-", "_")
        if dist == "frequency": dist = "frequency_coast"
        mark = DISTRICT_MARK.get(dist, "⚫")
        print(f"  {mark}  Namespace: {ns}  (district={dist})")

        pods = _kubectl(["get", "pods", "-n", ns, "--no-headers", "2>/dev/null"])
        if pods and pods.strip():
            for line in pods.strip().splitlines():
                parts = line.split()
                name = parts[0] if parts else "?"
                status = parts[2] if len(parts) > 2 else "?"
                print(f"       pod  {name:45s}  [{status}]")
        else:
            print(f"       (no pods — apply k8s/ manifests to populate)")
        print()


def show_builds():
    out = _docker(["buildx", "ls"])
    print(f"\n  SAGCO Hub — Builds\n")
    if out:
        print(out)
    else:
        print("  No active buildx builders")

    build_dir = REPO_ROOT
    dockerfiles = list(build_dir.glob("Dockerfile*"))
    print(f"\n  SAGCO Dockerfiles ({len(dockerfiles)}):")
    for df in sorted(dockerfiles):
        print(f"  · {df.name}")


def show_models():
    print(f"\n  SAGCO Hub — Models  (sagco-os LLM layer)\n")
    models_dir = REPO_ROOT / "sagco-agents"
    known_models = [
        ("sagco-os:latest",            "kernel LLM — self-awareness"),
        ("dom101/sagco-codex:latest",  "code synthesis model"),
        ("dom101/sagco-dojo:latest",   "training / dojo model"),
        ("sagco-android:latest",       "mobile agent model"),
    ]
    for img, role in known_models:
        print(f"  🧠  {img:45s}  {role}")
    print(f"\n  MCP Extension: MCP Toolkit (Beta) → localhost:3000")
    print(f"  LLM District:  frequency_coast")


def show_extensions():
    print(f"\n  SAGCO Hub — Extensions\n")
    extensions = [
        ("MCP Toolkit", "Beta",   "MCP server management + LLM tool routing", "frequency_coast"),
        ("Kubernetes",  "Active", "K8s cluster at 10.96.0.1:443",             "eru"),
        ("Gordon",      "Active", "Docker AI assistant (sidebar)",             "memory_palace"),
    ]
    for name, ver, desc, dist in extensions:
        mark = DISTRICT_MARK.get(dist, "⚫")
        print(f"  {mark}  [{ver:6s}]  {name:20s}  {desc}")


def show_logs(container: str | None):
    if container:
        out = _docker(["logs", "--tail", "50", container])
        if out:
            print(f"\n  Logs: {container}\n")
            print(out)
        else:
            print(f"  Could not get logs for {container}")
    else:
        out = _docker(["ps", "--format", "{{.Names}}\t{{.Status}}"])
        if out:
            running = [l.split("\t")[0] for l in out.splitlines() if l.strip()]
            print(f"\n  Running containers ({len(running)}) — use --logs --container NAME")
            for r in running:
                print(f"  · {r}")


def show_all():
    show_containers(running_only=True)
    show_images()
    show_volumes()
    show_kubernetes()
    show_models()
    show_extensions()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SAGCO Hub Navigator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--containers",  action="store_true")
    group.add_argument("--images",      action="store_true")
    group.add_argument("--volumes",     action="store_true")
    group.add_argument("--kubernetes",  action="store_true")
    group.add_argument("--builds",      action="store_true")
    group.add_argument("--models",      action="store_true")
    group.add_argument("--extensions",  action="store_true")
    group.add_argument("--logs",        action="store_true")
    group.add_argument("--all",         action="store_true")
    parser.add_argument("--running",    action="store_true")
    parser.add_argument("--namespace",  default=None)
    parser.add_argument("--container",  default=None)
    args = parser.parse_args()

    if args.containers:   show_containers(args.running)
    elif args.images:     show_images()
    elif args.volumes:    show_volumes()
    elif args.kubernetes: show_kubernetes(args.namespace)
    elif args.builds:     show_builds()
    elif args.models:     show_models()
    elif args.extensions: show_extensions()
    elif args.logs:       show_logs(args.container)
    elif args.all:        show_all()

if __name__ == "__main__":
    main()
