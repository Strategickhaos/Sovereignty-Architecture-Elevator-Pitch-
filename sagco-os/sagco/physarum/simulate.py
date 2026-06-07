"""
Physarum Polycephalum simulation.
Implements Poiseuille flow, reinforcement, and pruning on a Graph.
"""
from .graph import Graph


def poiseuille_flow(conductivity: float, pressure_diff: float, length: float = 1.0) -> float:
    """
    Compute flow using Poiseuille's law: Q = (D * dP) / L
    where D = conductivity, dP = pressure difference, L = length.
    """
    return (conductivity * pressure_diff) / max(length, 1e-9)


def simulate(graph: Graph, source: str, sink: str, iterations: int = 50,
             reinforce: float = 1.2, decay: float = 0.9, prune_threshold: float = 0.1) -> Graph:
    """
    Run Physarum simulation on graph.
    - source: node with high pressure (1.0)
    - sink: node with low pressure (0.0)
    - Reinforces edges with high flow, prunes weak edges.
    """
    if source not in graph.nodes or sink not in graph.nodes:
        return graph

    # Initialize pressures
    pressures = {nid: 0.5 for nid in graph.nodes}
    pressures[source] = 1.0
    pressures[sink] = 0.0

    for iteration in range(iterations):
        # Compute flow on each edge
        for edge in graph.edges:
            dp = abs(pressures.get(edge.src, 0.5) - pressures.get(edge.dst, 0.5))
            cond = graph.nodes[edge.src].conductivity
            edge.flow = poiseuille_flow(cond, dp)

        # Update conductivities
        for edge in graph.edges:
            if edge.flow > 0:
                graph.nodes[edge.src].conductivity *= reinforce * edge.flow
                graph.nodes[edge.src].conductivity = min(graph.nodes[edge.src].conductivity, 10.0)
            else:
                graph.nodes[edge.src].conductivity *= decay

        # Update pressures (simple averaging)
        new_pressures = {}
        for nid in graph.nodes:
            if nid == source:
                new_pressures[nid] = 1.0
            elif nid == sink:
                new_pressures[nid] = 0.0
            else:
                neighbors = graph.neighbors(nid)
                if neighbors:
                    new_pressures[nid] = sum(pressures.get(n, 0.5) for n in neighbors) / len(neighbors)
                else:
                    new_pressures[nid] = pressures.get(nid, 0.5) * decay
        pressures = new_pressures

    # Prune weak edges
    graph.edges = [e for e in graph.edges if e.flow >= prune_threshold]

    return graph


def run_simulation(rows: list, output_dir: str = "outputs/") -> dict:
    """Run full physarum simulation on data rows."""
    graph = Graph()
    graph.from_rows(rows)

    node_ids = list(graph.nodes.keys())
    if len(node_ids) < 2:
        return {"nodes": len(node_ids), "edges": 0, "total_flow": 0}

    source = node_ids[0]
    sink = node_ids[-1]
    simulate(graph, source, sink)

    return {
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
        "total_flow": round(graph.total_flow(), 4),
        "source": source,
        "sink": sink,
    }
