"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — test_physarum.py
Unit tests for the Physarum network simulator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from physarum_graph import PhysarumGraph, PhysarumNode, PhysarumEdge


def _make_simple_graph():
    nodes = [
        PhysarumNode("A", "Alpha", "genesis", nutrient=0.9),
        PhysarumNode("B", "Beta",  "genesis", nutrient=0.5),
        PhysarumNode("C", "Gamma", "genesis", nutrient=0.3),
    ]
    edges = [
        PhysarumEdge("A", "B", conductance=0.5, edge_type="bond"),
        PhysarumEdge("B", "C", conductance=0.5, edge_type="bond"),
        PhysarumEdge("A", "C", conductance=0.02, edge_type="bond"),  # weak edge
    ]
    return PhysarumGraph(nodes, edges)


def test_step_runs():
    g = _make_simple_graph()
    g.step(food_sources=["A"], hazards=[])
    assert g._step_count == 1
    print("  [PASS] step() increments step count")


def test_reinforce_increases_conductance():
    from reinforce_paths import reinforce
    g = _make_simple_graph()
    # Set known flow on first edge
    g.edges[0].flow = 0.5
    original = g.edges[0].conductance
    reinforce(g, {"A→B": 0.5}, growth_rate=0.1)
    assert g.edges[0].conductance > original, (
        f"Expected conductance > {original}, got {g.edges[0].conductance}"
    )
    print(f"  [PASS] reinforce: conductance {original:.4f} → {g.edges[0].conductance:.4f}")


def test_prune_removes_weak_edges():
    from prune_routes import prune
    g = _make_simple_graph()
    # Edge A-C has conductance=0.02 which is above 0.01 threshold
    # Force it below threshold
    g.edges[2].conductance = 0.005
    prune(g, threshold=0.01)
    assert not g.edges[2].alive, "Expected weak edge to be pruned"
    print("  [PASS] prune: weak edge (conductance=0.005) correctly pruned")


def test_heal_repairs_hazarded_node():
    from self_heal import heal
    g = _make_simple_graph()
    # Damage node B
    g.nodes["B"].nutrient = 0.1
    g.nodes["B"].alive = False
    # A and C are healthy — should revive B
    heal(g, hazards=["B"])
    assert g.nodes["B"].alive, "Expected node B to be revived"
    print(f"  [PASS] heal: node B revived, nutrient={g.nodes['B'].nutrient:.4f}")


def test_optimize_returns_report():
    g = _make_simple_graph()
    report = g.optimize(steps=5, food_sources=["A"])
    assert "steps_run" in report
    assert report["steps_run"] == 5
    assert "strongest_paths" in report
    print(f"  [PASS] optimize: completed 5 steps, {report['alive_edges']} alive edges")


if __name__ == "__main__":
    print("\n  BOARD-40-PHYSARUM tests\n")
    test_step_runs()
    test_reinforce_increases_conductance()
    test_prune_removes_weak_edges()
    test_heal_repairs_hazarded_node()
    test_optimize_returns_report()
    print("\n  All tests passed.\n")
