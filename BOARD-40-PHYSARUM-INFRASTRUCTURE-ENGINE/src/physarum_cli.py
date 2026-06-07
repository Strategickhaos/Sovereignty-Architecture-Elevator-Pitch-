#!/usr/bin/env python3
"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — physarum_cli.py
Biological network optimizer CLI.

Usage:
  python physarum_cli.py --optimize       # run 20 steps, print report
  python physarum_cli.py --steps 50       # custom steps
  python physarum_cli.py --eru            # ERU proof
  python physarum_cli.py --demo           # demo with SAGCO board graph
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

REPO_ROOT  = Path(__file__).resolve().parent.parent
INPUTS_DIR = REPO_ROOT / "inputs"
REPORTS_DIR = REPO_ROOT / "reports"
EXPORTS_DIR = REPO_ROOT / "exports"


def _load_graph():
    """Load nodes and build initial edges from nodes.yaml + signal_weights."""
    import yaml
    from physarum_graph import PhysarumGraph, PhysarumNode, PhysarumEdge

    nodes_path = INPUTS_DIR / "nodes.yaml"
    weights_path = INPUTS_DIR / "signal_weights.yaml"

    raw_nodes = yaml.safe_load(nodes_path.read_text())["nodes"]
    weights   = yaml.safe_load(weights_path.read_text()).get("signal_weights", {})

    nodes = []
    for n in raw_nodes:
        nutrient = weights.get(n["id"], n.get("nutrient", 0.5))
        nodes.append(PhysarumNode(
            node_id  = n["id"],
            name     = n["name"],
            district = n["district"],
            nutrient = nutrient,
        ))

    # Build edges: connect boards in the same district + key cross-district bonds
    edges = []
    node_ids = [n.node_id for n in nodes]
    district_map: dict = {}
    for n in nodes:
        district_map.setdefault(n.district, []).append(n.node_id)

    # Same-district edges
    for district, members in district_map.items():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                edges.append(PhysarumEdge(
                    source=members[i], target=members[j],
                    conductance=0.5, edge_type="bond",
                ))

    # Cross-district dependency edges (key SAGCO topology)
    cross_deps = [
        ("SAGCO-UNIVERSITY", "BOARD-36", "prerequisite"),
        ("SAGCO-UNIVERSITY", "BOARD-37", "prerequisite"),
        ("SAGCO-UNIVERSITY", "BOARD-38", "prerequisite"),
        ("SAGCO-UNIVERSITY", "BOARD-39", "prerequisite"),
        ("BOARD-36", "BOARD-40-SOLVER", "dependency"),
        ("BOARD-37", "BOARD-40-SOLVER", "dependency"),
        ("BOARD-38", "BOARD-40-SOLVER", "dependency"),
        ("BOARD-39", "BOARD-40-SOLVER", "dependency"),
        ("BOARD-36", "BOARD-33", "dependency"),
        ("BOARD-36", "BOARD-34", "dependency"),
        ("BOARD-25", "BOARD-26", "dependency"),
        ("BOARD-25", "BOARD-27", "dependency"),
        ("BOARD-25", "BOARD-32", "dependency"),
        ("BOARD-13", "BOARD-11", "dependency"),
        ("BOARD-11", "BOARD-26", "dependency"),
        ("BOARD-21", "BOARD-36", "dependency"),
        ("BOARD-24", "BOARD-25", "dependency"),
        ("BOARD-29", "BOARD-30", "bond"),
        ("BOARD-29", "BOARD-31", "bond"),
        ("BOARD-40-SOLVER", "BOARD-40-PHYSARUM", "bond"),
    ]
    existing = {(e.source, e.target) for e in edges}
    for src, tgt, etype in cross_deps:
        if src in node_ids and tgt in node_ids:
            if (src, tgt) not in existing:
                edges.append(PhysarumEdge(
                    source=src, target=tgt,
                    conductance=0.6, edge_type=etype,
                ))

    return PhysarumGraph(nodes, edges)


def _load_hazards() -> list:
    import yaml
    hazards_path = INPUTS_DIR / "hazards.yaml"
    raw = yaml.safe_load(hazards_path.read_text()).get("hazards", [])
    affected = []
    for h in raw:
        boards = h.get("boards_affected", [])
        if boards == ["all"]:
            continue  # skip global hazards for node targeting
        affected.extend(boards)
    return list(set(affected))


def cmd_optimize(steps: int = 20, with_eru: bool = False):
    graph = _load_graph()
    hazards = _load_hazards()

    initial_state = {
        "alive_nodes": sum(1 for n in graph.nodes.values() if n.alive),
        "alive_edges": sum(1 for e in graph.edges if e.alive),
    }

    print(f"\n  Physarum optimizer — {steps} steps")
    print(f"  Nodes: {initial_state['alive_nodes']}  Edges: {initial_state['alive_edges']}")
    print(f"  Hazards: {hazards}\n")

    food_sources = [nid for nid, n in graph.nodes.items() if n.nutrient >= 0.85]
    for i in range(steps):
        graph.step(food_sources, hazards)
        if (i + 1) % 5 == 0:
            snap = graph._history[-1]
            print(f"  step {snap['step']:>3}: nodes={snap['alive_nodes']}  "
                  f"edges={snap['alive_edges']}  flow={snap['total_flow']:.4f}")

    report = graph.report()
    _print_report(report)

    # Write outputs
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    import yaml
    opt_path = REPORTS_DIR / "optimized_network.yaml"
    with open(opt_path, "w") as f:
        yaml.dump(report, f, default_flow_style=False)
    print(f"\n  Optimized network written → {opt_path}")

    # Export JSON for visualization
    net_map = {
        "nodes": [
            {
                "id":       nid,
                "name":     n.name,
                "district": n.district,
                "nutrient": n.nutrient,
                "flow":     round(n.flow, 4),
                "alive":    n.alive,
            }
            for nid, n in graph.nodes.items()
        ],
        "edges": [
            {
                "source":      e.source,
                "target":      e.target,
                "conductance": round(e.conductance, 4),
                "flow":        round(e.flow, 4),
                "type":        e.edge_type,
                "alive":       e.alive,
            }
            for e in graph.edges
        ],
    }
    map_path = EXPORTS_DIR / "network_map.json"
    with open(map_path, "w") as f:
        json.dump(net_map, f, indent=2)
    print(f"  Network map (JSON) written → {map_path}")

    if with_eru:
        from eru_network_report import build_eru
        eru = build_eru(graph, initial_state, report)
        eru_path = REPORTS_DIR / "physarum_eru.yaml"
        with open(eru_path, "w") as f:
            yaml.dump(eru, f, default_flow_style=False)
        _print_eru(eru)
        print(f"  ERU report written → {eru_path}")


def cmd_eru():
    graph = _load_graph()
    hazards = _load_hazards()
    initial_state = {
        "alive_nodes": sum(1 for n in graph.nodes.values() if n.alive),
        "alive_edges": sum(1 for e in graph.edges if e.alive),
    }
    food_sources = [nid for nid, n in graph.nodes.items() if n.nutrient >= 0.85]
    graph.optimize(steps=20, food_sources=food_sources, hazards=hazards)
    final = graph.report()

    from eru_network_report import build_eru
    eru = build_eru(graph, initial_state, final)

    import yaml
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    eru_path = REPORTS_DIR / "physarum_eru.yaml"
    with open(eru_path, "w") as f:
        yaml.dump(eru, f, default_flow_style=False)

    _print_eru(eru)
    print(f"\n  ERU report written → {eru_path}")


def _print_report(report: dict):
    print("\n" + "=" * 60)
    print("  PHYSARUM NETWORK REPORT")
    print("=" * 60)
    print(f"  Steps run:     {report['steps_run']}")
    print(f"  Alive nodes:   {report['alive_nodes']}")
    print(f"  Dead nodes:    {report['dead_nodes']}")
    print(f"  Alive edges:   {report['alive_edges']}")
    print(f"  Pruned edges:  {report['pruned_edges']}")
    iso = report.get("isolated_nodes", [])
    print(f"  Isolated:      {iso or 'none'}")
    print(f"\n  Strongest paths:")
    for p in report.get("strongest_paths", [])[:5]:
        print(f"    {p['source']:>25} → {p['target']:<25} "
              f"cond={p['conductance']:.4f}  flow={p['flow']:.4f}  [{p['type']}]")
    print("=" * 60)


def _print_eru(eru: dict):
    e = eru.get("eru", {})
    print("\n" + "=" * 60)
    print("  PHYSARUM ERU PROOF")
    print("=" * 60)
    print(f"  Status:        {e.get('status', '?')}")
    print(f"  Steps run:     {e.get('steps_run', '?')}")
    act = e.get("actual", {})
    exp = e.get("expected", {})
    print(f"  Alive nodes:   {act.get('alive_nodes', '?')} / {exp.get('alive_nodes', '?')} expected")
    print(f"  Node variance: {act.get('node_variance', '?')}")
    print(f"  Isolated:      {act.get('isolated_nodes', []) or 'none'}")
    print(f"  Notes:         {e.get('notes', '')}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="SAGCO Physarum Infrastructure Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--optimize", action="store_true", help="Run 20-step optimization")
    parser.add_argument("--steps", type=int, default=20, help="Number of simulation steps")
    parser.add_argument("--eru", action="store_true", help="Generate ERU proof")
    parser.add_argument("--demo", action="store_true", help="Run full demo with SAGCO board graph")

    args = parser.parse_args()

    if args.demo or args.optimize:
        cmd_optimize(steps=args.steps, with_eru=args.eru or args.demo)
    elif args.eru:
        cmd_eru()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
