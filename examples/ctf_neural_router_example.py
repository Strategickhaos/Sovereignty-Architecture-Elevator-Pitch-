#!/usr/bin/env python3
"""
Example: Using the CTF Neural Router
=====================================

Demonstrates basic usage of the CTF Brain for query classification
and next move prediction.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctf_neural_router import CTFBrain


async def example_query_classification():
    """Example 1: Classify various CTF queries"""
    print("="*60)
    print("EXAMPLE 1: Query Classification")
    print("="*60)
    
    brain = CTFBrain()
    
    queries = [
        "I need to scan the network for open ports",
        "Let's enumerate web directories with gobuster",
        "Test the web app for SQL injection",
        "We got a shell! Now let's escalate privileges",
        "Need to crack these password hashes",
        "How do I pivot to the internal network?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        result = await brain.classify_query(query)
        print(f"  → Phase: {result['name']}")
        print(f"  → Node: {result['node']}")
        print(f"  → Confidence: {result['classification']['confidence']:.0%}")
        print(f"  → Suggested Tools: {', '.join(result['tools'][:3])}")


def example_next_moves():
    """Example 2: Predict next moves based on context"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Next Move Prediction")
    print("="*60)
    
    brain = CTFBrain()
    
    # Scenario: Just finished reconnaissance
    current_node = "01-Ua-Recon"
    context = {
        "available_tools": ["nmap", "gobuster", "burpsuite", "nikto"],
        "findings": ["web server on port 80", "ssh on port 22", "directory listing enabled"],
        "historical_success": {
            "02-Ub-Enum": 0.85,
            "03-H-WebApp": 0.75
        },
        "time_constraints": 30
    }
    
    print(f"\nCurrent Phase: {current_node}")
    print(f"Available Tools: {', '.join(context['available_tools'])}")
    print(f"Findings: {', '.join(context['findings'])}")
    
    moves = brain.suggest_next_moves(current_node, context)
    
    print(f"\nSuggested Next Moves:")
    for i, move in enumerate(moves, 1):
        node_name = brain.nodes_data[move.node_id]['name']
        print(f"{i}. {node_name} ({move.node_id})")
        print(f"   Total Score: {move.total_score:.3f}")
        print(f"   └─ Tool Ready: {move.tool_ready:.2f} | Context Match: {move.context_match:.2f}")
        print(f"      Success Rate: {move.success_rate:.2f} | Efficiency: {move.efficiency:.2f}")


def example_path_finding():
    """Example 3: Find paths between methodology phases"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Path Finding")
    print("="*60)
    
    brain = CTFBrain()
    
    paths = [
        ("01-Ua-Recon", "06-Ab-PrivEsc"),
        ("03-H-WebApp", "08-T-Exfil"),
        ("01-Ua-Recon", "10-V-Cleanup")
    ]
    
    for start, end in paths:
        path = brain.visualize_path(start, end)
        if path:
            start_name = brain.nodes_data[start]['name']
            end_name = brain.nodes_data[end]['name']
            print(f"\nPath from {start_name} to {end_name}:")
            print(f"  {' → '.join(p['name'] for p in path)}")
        else:
            print(f"\nNo path found from {start} to {end}")


def example_graph_stats():
    """Example 4: Display graph statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Graph Statistics")
    print("="*60)
    
    brain = CTFBrain()
    stats = brain.get_graph_stats()
    
    print(f"\nGraph: {stats['metadata']['name']}")
    print(f"Version: {stats['metadata']['version']}")
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Edges: {stats['total_edges']}")
    
    print("\nAll Methodology Nodes:")
    for node_id in stats['nodes']:
        node_data = brain.nodes_data[node_id]
        out_degree = brain.graph.out_degree(node_id)
        in_degree = brain.graph.in_degree(node_id)
        print(f"  {node_id}: {node_data['name']}")
        print(f"    Tools: {len(node_data['tools'])} | In: {in_degree} | Out: {out_degree}")


async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("CTF NEURAL ROUTER - USAGE EXAMPLES")
    print("="*60)
    
    await example_query_classification()
    example_next_moves()
    example_path_finding()
    example_graph_stats()
    
    print("\n" + "="*60)
    print("Examples complete! Try the interactive CLI:")
    print("  python3 ctf_neural_router.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
