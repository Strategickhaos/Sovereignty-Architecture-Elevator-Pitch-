"""ERU network report for Physarum simulation results."""


def network_report(sim_result: dict, eru_summary: dict = None) -> str:
    """Generate a text report of the physarum network simulation."""
    lines = [
        "# SAGCO Physarum Network Report",
        "",
        "## Network Topology",
        f"- Nodes: {sim_result.get('nodes', 0)}",
        f"- Edges (post-prune): {sim_result.get('edges', 0)}",
        f"- Total flow: {sim_result.get('total_flow', 0)}",
        f"- Source node: {sim_result.get('source', 'N/A')}",
        f"- Sink node: {sim_result.get('sink', 'N/A')}",
        "",
    ]
    if eru_summary:
        lines += [
            "## ERU Overlay",
            f"- PASS nodes: {eru_summary.get('PASS', 0)}",
            f"- PARTIAL nodes: {eru_summary.get('PARTIAL', 0)}",
            f"- FAIL nodes: {eru_summary.get('FAIL', 0)}",
            f"- Pass rate: {eru_summary.get('pass_rate', 0)}%",
            "",
        ]
    return "\n".join(lines)
