#!/usr/bin/env python3
"""
SAGCO Kube Agent — Kubernetes / GKE cluster navigator

Usage:
  agent_kube.py --nodes
  agent_kube.py --pods [--namespace NS]
  agent_kube.py --events
  agent_kube.py --district-map
  agent_kube.py --eru-check
"""
import argparse, json, subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def _kubectl(args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["kubectl"] + args, stderr=subprocess.DEVNULL, timeout=15
        ).decode()
    except Exception:
        return None

def show_nodes():
    out = _kubectl(["get", "nodes", "-o", "wide"])
    if out:
        print("\n  GKE/K8s Nodes:")
        print(out)
    else:
        print("  kubectl not reachable — check kubeconfig")

def show_pods(namespace: str | None):
    ns_args = ["-n", namespace] if namespace else ["--all-namespaces"]
    out = _kubectl(["get", "pods"] + ns_args)
    if out:
        print(f"\n  Pods (ns={namespace or 'all'}):")
        print(out)
    else:
        print("  kubectl not reachable — check kubeconfig")

def show_events():
    out = _kubectl(["get", "events", "--all-namespaces", "--sort-by=.metadata.creationTimestamp"])
    if out:
        for line in out.splitlines()[-30:]:
            if any(w in line for w in ("Warning", "Error", "Failed", "OOMKilled", "BackOff")):
                print(f"  ⚠  {line}")
            else:
                print(f"     {line}")
    else:
        print("  kubectl not reachable")

def district_map():
    """Map K8s namespaces → SAGCO districts."""
    mapping = {
        "default":      "genesis",
        "kube-system":  "trinity",
        "monitoring":   "eru",
        "red":          "contradiction_forest",
        "blue":         "memory_palace",
        "purple":       "eru",
        "security":     "trinity",
        "logging":      "industrial",
        "ingress":      "frequency_coast",
    }
    out = _kubectl(["get", "namespaces", "-o", "json"])
    if out:
        ns_list = json.loads(out).get("items", [])
        print("\n  Namespace → SAGCO District Map:")
        print(f"  {'Namespace':30s}  District")
        print("  " + "-" * 50)
        for ns in ns_list:
            name = ns["metadata"]["name"]
            dist = mapping.get(name, "memory_palace")
            print(f"  {name:30s}  {dist}")
    else:
        print("  kubectl not reachable — showing static mapping")
        for ns, dist in mapping.items():
            print(f"  {ns:30s}  {dist}")

def eru_check():
    """Quick ERU health check of the cluster."""
    print("\n  ERU Cluster Health Check\n")
    checks = [
        ("NetworkPolicies", ["get", "networkpolicies", "--all-namespaces"]),
        ("ResourceQuotas",  ["get", "resourcequota",   "--all-namespaces"]),
        ("PodDisruptionBudgets", ["get", "pdb",         "--all-namespaces"]),
        ("ServiceAccounts w/ Workload Identity", [
            "get", "serviceaccounts", "--all-namespaces",
            "-o", "jsonpath={.items[*].metadata.annotations}"
        ]),
    ]
    for label, cmd in checks:
        out = _kubectl(cmd)
        if out and out.strip() and "No resources found" not in out:
            lines = [l for l in out.splitlines() if l.strip()]
            print(f"  ✓  {label}: {len(lines)-1} found")
        else:
            print(f"  ✗  {label}: NONE — see ERU case studies in BOARD-24/eru/eru-gke.yaml")

def main():
    parser = argparse.ArgumentParser(description="SAGCO Kube Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--nodes",      action="store_true")
    group.add_argument("--pods",       action="store_true")
    group.add_argument("--events",     action="store_true")
    group.add_argument("--district-map", action="store_true")
    group.add_argument("--eru-check",  action="store_true")
    parser.add_argument("--namespace", default=None)
    args = parser.parse_args()

    if args.nodes:         show_nodes()
    elif args.pods:        show_pods(args.namespace)
    elif args.events:      show_events()
    elif args.district_map: district_map()
    elif args.eru_check:   eru_check()

if __name__ == "__main__":
    main()
