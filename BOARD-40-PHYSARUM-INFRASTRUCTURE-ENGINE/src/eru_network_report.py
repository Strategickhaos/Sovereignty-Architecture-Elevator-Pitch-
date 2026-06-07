"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — eru_network_report.py
Build ERU proof for the optimized Physarum network.
Expected: all nodes reachable, no isolated boards, variance=0
Actual:   N nodes alive, M edges, K pruned, L healed
"""


def build_eru(graph, initial_state: dict, final_state: dict) -> dict:
    """
    Returns ERU proof dict comparing initial → final network state.
    """
    total_nodes    = len(graph.nodes)
    alive_nodes    = sum(1 for n in graph.nodes.values() if n.alive)
    dead_nodes     = total_nodes - alive_nodes
    alive_edges    = sum(1 for e in graph.edges if e.alive)
    pruned_edges   = sum(1 for e in graph.edges if not e.alive)
    isolated_nodes = final_state.get("isolated_nodes", [])

    expected_alive  = total_nodes
    expected_isolated = 0
    expected_pruned   = 0

    node_variance     = expected_alive - alive_nodes
    isolated_variance = len(isolated_nodes) - expected_isolated

    if node_variance == 0 and isolated_variance == 0:
        status = "PASS"
    elif node_variance <= total_nodes * 0.2:
        status = "PARTIAL"
    else:
        status = "FAIL"

    return {
        "eru": {
            "expected": {
                "alive_nodes":    expected_alive,
                "isolated_nodes": expected_isolated,
                "pruned_edges":   expected_pruned,
                "variance":       0,
            },
            "actual": {
                "alive_nodes":    alive_nodes,
                "dead_nodes":     dead_nodes,
                "alive_edges":    alive_edges,
                "pruned_edges":   pruned_edges,
                "isolated_nodes": isolated_nodes,
                "node_variance":  node_variance,
                "isolation_variance": isolated_variance,
            },
            "status":         status,
            "steps_run":      final_state.get("steps_run", 0),
            "optimization":   {
                "initial_alive_nodes": initial_state.get("alive_nodes", total_nodes),
                "final_alive_nodes":   alive_nodes,
                "initial_alive_edges": initial_state.get("alive_edges", len(graph.edges)),
                "final_alive_edges":   alive_edges,
            },
            "notes": (
                "Network fully connected and optimized."
                if status == "PASS"
                else f"{node_variance} nodes lost, {len(isolated_nodes)} isolated."
            ),
        }
    }
