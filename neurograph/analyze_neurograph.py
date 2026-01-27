#!/usr/bin/env python3
"""
Example script demonstrating how to load and analyze the Proto-Elamite neurograph.

This shows basic operations like:
- Loading the JSON
- Querying nodes and edges
- Filtering by classification
- Analyzing mutation patterns
"""

import json
from collections import defaultdict


def load_neurograph(filepath='proto_elamite_pelsim1_dendrites.json'):
    """Load neurograph from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def analyze_symbol_evolution(data, symbol):
    """Analyze evolution pattern for a specific symbol."""
    # Get all nodes for this symbol
    nodes = [n for n in data['nodes'] if n['symbol'] == symbol]
    
    # Get all edges for this symbol
    edges = [e for e in data['edges'] if e['symbol'] == symbol]
    
    print(f"\n=== {symbol.upper()} ===")
    print(f"Nodes: {len(nodes)} (1 initial + {len(nodes)-1} mutations)")
    print(f"Edges: {len(edges)} mutation events")
    
    # Classification breakdown
    classifications = defaultdict(int)
    for edge in edges:
        classifications[edge['classification']] += 1
    
    print(f"Classifications:")
    for cls in ['green', 'yellow', 'red']:
        count = classifications[cls]
        pct = count / len(edges) * 100 if edges else 0
        print(f"  {cls}: {count} ({pct:.1f}%)")
    
    # Find best mutation (highest delta_f with lower danger)
    best_mutations = sorted(
        [e for e in edges if e['delta_f'] > 0 and e['delta_danger'] < 0],
        key=lambda e: e['delta_f'],
        reverse=True
    )
    
    if best_mutations:
        best = best_mutations[0]
        print(f"\nBest mutation:")
        print(f"  {best['from']} -> {best['to']}")
        print(f"  Δf: +{best['delta_f']:.3f}, Δdanger: {best['delta_danger']:.2f}")
        print(f"  Classification: {best['classification']}")


def find_mutation_chains(data, symbol, max_chain_length=5):
    """Find mutation chains (sequences of connected mutations)."""
    edges = [e for e in data['edges'] if e['symbol'] == symbol]
    
    # Build adjacency graph
    graph = defaultdict(list)
    for edge in edges:
        graph[edge['from']].append((edge['to'], edge))
    
    # Find chains starting from initial node
    slug = symbol.lower().replace(" ", "_")
    initial_node = f"{slug}:v1"
    
    chains = []
    
    def find_chains_recursive(current, chain, depth):
        if depth >= max_chain_length:
            chains.append(chain[:])
            return
        
        if current not in graph or not graph[current]:
            chains.append(chain[:])
            return
        
        for next_node, edge in graph[current]:
            chain.append(edge)
            find_chains_recursive(next_node, chain, depth + 1)
            chain.pop()
    
    find_chains_recursive(initial_node, [], 0)
    
    # Find longest chain
    if chains:
        longest = max(chains, key=len)
        print(f"\nLongest mutation chain ({len(longest)} steps):")
        for i, edge in enumerate(longest, 1):
            print(f"  {i}. {edge['from']} -> {edge['to']} "
                  f"({edge['classification']}, Δf={edge['delta_f']:+.3f})")


def filter_by_classification(data, classification):
    """Get all edges with a specific classification."""
    return [e for e in data['edges'] if e['classification'] == classification]


def main():
    """Main analysis demonstration."""
    print("=== Proto-Elamite Neurograph Analysis ===")
    
    # Load data
    data = load_neurograph()
    
    print(f"\nRun: {data['meta']['run_id']}")
    print(f"Total nodes: {len(data['nodes'])}")
    print(f"Total edges: {len(data['edges'])}")
    
    # Analyze each symbol
    for symbol in data['meta']['symbols_scoped']:
        analyze_symbol_evolution(data, symbol)
        find_mutation_chains(data, symbol, max_chain_length=5)
    
    # Overall classification stats
    print("\n=== OVERALL STATISTICS ===")
    classifications = defaultdict(int)
    for edge in data['edges']:
        classifications[edge['classification']] += 1
    
    print(f"\nEdge classifications:")
    for cls in ['green', 'yellow', 'red']:
        count = classifications[cls]
        pct = count / len(data['edges']) * 100 if data['edges'] else 0
        print(f"  {cls}: {count} ({pct:.1f}%)")
    
    # Green edges (best mutations)
    green_edges = filter_by_classification(data, 'green')
    if green_edges:
        avg_delta_f = sum(e['delta_f'] for e in green_edges) / len(green_edges)
        avg_delta_danger = sum(e['delta_danger'] for e in green_edges) / len(green_edges)
        print(f"\nGreen edges (better & safer):")
        print(f"  Average Δf: +{avg_delta_f:.3f}")
        print(f"  Average Δdanger: {avg_delta_danger:.2f}")
    
    # Red edges (risky improvements)
    red_edges = filter_by_classification(data, 'red')
    if red_edges:
        avg_delta_f = sum(e['delta_f'] for e in red_edges) / len(red_edges)
        avg_delta_danger = sum(e['delta_danger'] for e in red_edges) / len(red_edges)
        print(f"\nRed edges (better but riskier):")
        print(f"  Average Δf: +{avg_delta_f:.3f}")
        print(f"  Average Δdanger: +{avg_delta_danger:.2f}")
    
    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main()
