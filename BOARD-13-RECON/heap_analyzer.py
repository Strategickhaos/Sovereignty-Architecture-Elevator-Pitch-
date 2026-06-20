#!/usr/bin/env python3
"""
SAGCO Heap Snapshot Analyzer — BOARD-13-RECON memory intelligence

Parses Chrome V8 .heapsnapshot files (JSON format) and maps findings
into SAGCO ERU case studies. Detects memory leaks, detached DOM nodes,
large retained objects — all classified into SAGCO districts.

Usage:
  heap_analyzer.py --file Heap-20260606T164726.heapsnapshot
  heap_analyzer.py --file HEAP.heapsnapshot --top 20
  heap_analyzer.py --file HEAP.heapsnapshot --leaks
  heap_analyzer.py --file HEAP.heapsnapshot --emit-citizens
  heap_analyzer.py --file HEAP.heapsnapshot --eru

Typical path (Windows):
  C:\\Users\\garza\\Downloads\\Heap-20260606T164726.heapsnapshot
"""
import argparse, json, sys, time
from pathlib import Path
from collections import defaultdict, Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS   = REPO_ROOT / "BOARD-13-RECON" / "reports"
CITIZENS  = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
REPORTS.mkdir(parents=True, exist_ok=True)

GENESIS_INCREMENT = 3449
PID_BASE = 9600

# Node type → SAGCO district
NODE_DISTRICT = {
    "closure":      "compiler_city",
    "regexp":       "compiler_city",
    "code":         "compiler_city",
    "array":        "memory_palace",
    "string":       "memory_palace",
    "object":       "eru",
    "hidden":       "eru",
    "native":       "industrial",
    "synthetic":    "genesis",
    "concatenated": "memory_palace",
    "sliced":       "memory_palace",
}

LEAK_MARKERS = [
    "Detached", "detached", "leak", "Leak",
    "EventListener", "Observer", "listener",
    "Timer", "Interval", "timeout",
]


def load_snapshot(path: Path) -> dict:
    print(f"  Loading heap snapshot: {path.name}  ({path.stat().st_size / 1024 / 1024:.1f} MB)")
    with open(path) as f:
        return json.load(f)


def parse_nodes(snap: dict) -> list[dict]:
    meta      = snap.get("snapshot", {}).get("meta", {})
    node_fields = meta.get("node_fields", [])
    node_types  = meta.get("node_types", [[]])[0]  # first element is the array of type names
    raw_nodes   = snap.get("nodes", [])
    strings     = snap.get("strings", [])

    nf = len(node_fields)
    if nf == 0:
        return []

    # field indices
    fi = {f: i for i, f in enumerate(node_fields)}

    nodes = []
    for i in range(0, len(raw_nodes), nf):
        chunk = raw_nodes[i:i+nf]
        if len(chunk) < nf:
            break
        type_idx = chunk[fi.get("type", 0)]
        name_idx = chunk[fi.get("name", 1)]
        node_type = (node_types[type_idx] if isinstance(node_types, list)
                     and type_idx < len(node_types) else str(type_idx))
        name = strings[name_idx] if name_idx < len(strings) else ""
        self_size = chunk[fi.get("self_size", 3)] if "self_size" in fi else 0
        nodes.append({
            "idx":       i // nf,
            "type":      node_type,
            "name":      name,
            "self_size": self_size,
            "district":  NODE_DISTRICT.get(node_type, "memory_palace"),
        })
    return nodes


def top_by_size(nodes: list[dict], n: int = 20) -> list[dict]:
    return sorted(nodes, key=lambda x: x["self_size"], reverse=True)[:n]


def find_leaks(nodes: list[dict]) -> list[dict]:
    return [n for n in nodes
            if any(m in n["name"] for m in LEAK_MARKERS) and n["self_size"] > 0]


def eru_analysis(nodes: list[dict], snap: dict) -> dict:
    total_size = sum(n["self_size"] for n in nodes)
    by_type    = defaultdict(int)
    by_district= defaultdict(int)
    type_count = Counter(n["type"] for n in nodes)

    for n in nodes:
        by_type[n["type"]]       += n["self_size"]
        by_district[n["district"]] += n["self_size"]

    leaks = find_leaks(nodes)
    top   = top_by_size(nodes, 10)

    expected = "Heap usage under 100MB with no detached DOM nodes or listener leaks"
    actual_mb = total_size / 1024 / 1024
    actual = f"Heap total {actual_mb:.1f} MB  |  {len(leaks)} potential leak node(s)  |  {len(nodes):,} total nodes"

    variance = []
    if actual_mb > 200:
        variance.append(f"heap size {actual_mb:.0f}MB exceeds 200MB threshold")
    if leaks:
        variance.append(f"{len(leaks)} detached/listener nodes found")
    if not variance:
        variance.append("within normal parameters")

    return {
        "total_nodes":       len(nodes),
        "total_size_bytes":  total_size,
        "total_size_mb":     round(actual_mb, 2),
        "by_type":           dict(sorted(by_type.items(), key=lambda x: -x[1])[:10]),
        "by_district":       dict(sorted(by_district.items(), key=lambda x: -x[1])),
        "node_type_counts":  dict(type_count.most_common(10)),
        "leak_nodes":        len(leaks),
        "leak_samples":      [{"name": l["name"], "type": l["type"],
                                "size": l["self_size"]} for l in leaks[:10]],
        "top_10_by_size":    [{"name": t["name"], "type": t["type"],
                                "size": t["self_size"], "district": t["district"]}
                               for t in top],
        "eru": {
            "expected": expected,
            "actual":   actual,
            "variance": " | ".join(variance),
            "understanding": (
                "Heap snapshot from Sequence browser session. Memory footprint is the "
                "organism's RAM wafer. Large closures = compiler_city bloat. "
                "Detached nodes = ghost citizens still in memory after DOM removal. "
                "EventListener leaks = pad routes that never closed."
            ),
        }
    }


def print_report(result: dict, snapshot_name: str):
    eru = result["eru"]
    print(f"\n  ╔══════════════════════════════════════════════════════╗")
    print(f"  ║  SAGCO Heap Analyzer — {snapshot_name[:28]:28s} ║")
    print(f"  ╚══════════════════════════════════════════════════════╝\n")
    print(f"  Total nodes:   {result['total_nodes']:,}")
    print(f"  Total size:    {result['total_size_mb']:.2f} MB")
    print(f"  Leak signals:  {result['leak_nodes']}")

    print(f"\n  Memory by district:")
    for dist, sz in result["by_district"].items():
        bar = "█" * min(30, int(sz / result["total_size_bytes"] * 30))
        print(f"    {dist:25s}  {bar:30s}  {sz/1024/1024:.2f} MB")

    print(f"\n  Top 10 nodes by size:")
    for i, t in enumerate(result["top_10_by_size"]):
        print(f"    {i+1:2d}.  [{t['type']:12s}]  {t['name'][:40]:40s}  {t['size']:>8,} B  [{t['district']}]")

    if result["leak_samples"]:
        print(f"\n  ⚠  Leak signals ({result['leak_nodes']}):")
        for l in result["leak_samples"]:
            print(f"       [{l['type']:10s}]  {l['name'][:50]}  ({l['size']:,} B)")

    print(f"\n  ERU Analysis:")
    print(f"    Expected:   {eru['expected']}")
    print(f"    Actual:     {eru['actual']}")
    print(f"    Variance:   {eru['variance']}")


def emit_citizens(result: dict, snapshot_name: str):
    if not CITIZENS.exists():
        print("  Citizen registry not found"); return
    raw = json.loads(CITIZENS.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
    existing = {c["cid"] for c in citizens}

    added = 0
    tick  = int(time.time() * 1000)
    for i, node in enumerate(result["top_10_by_size"]):
        cid = f"sgc-artifact-{tick+i}-{(tick+i) % GENESIS_INCREMENT}"
        if cid in existing:
            continue
        citizens.append({
            "cid":      cid,
            "name":     f"heap.{node['type']}.{node['name'][:30]}",
            "kind":     "artifact",
            "born_in":  "genesis",
            "district": node["district"],
            "status":   "observed",
            "payload":  node,
            "tags":     ["heap", "memory", "browser", snapshot_name],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        added += 1

    if isinstance(raw, dict):
        raw["citizens"] = citizens
        CITIZENS.write_text(json.dumps(raw, indent=2))
    else:
        CITIZENS.write_text(json.dumps(citizens, indent=2))
    print(f"  Registered {added} heap nodes as citizens")


def main():
    parser = argparse.ArgumentParser(description="SAGCO Heap Snapshot Analyzer")
    parser.add_argument("--file",          required=True, help=".heapsnapshot file path")
    parser.add_argument("--top",           type=int, default=10)
    parser.add_argument("--leaks",         action="store_true")
    parser.add_argument("--eru",           action="store_true")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"  ERROR: {path} not found")
        print(f"  Tip (Windows): python heap_analyzer.py --file \"C:\\Users\\garza\\Downloads\\Heap-20260606T164726.heapsnapshot\"")
        sys.exit(1)

    snap   = load_snapshot(path)
    nodes  = parse_nodes(snap)
    result = eru_analysis(nodes, snap)

    print_report(result, path.name)

    # Write report
    report_path = REPORTS / f"heap_{int(time.time())}.json"
    with open(report_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Report saved: {report_path.relative_to(REPO_ROOT)}")

    if args.leaks:
        leaks = find_leaks(nodes)
        print(f"\n  All leak signals ({len(leaks)}):")
        for l in leaks[:args.top]:
            print(f"    [{l['type']:12s}]  {l['name'][:60]}  ({l['self_size']:,} B)")

    if args.emit_citizens:
        emit_citizens(result, path.name)

if __name__ == "__main__":
    main()
