#!/usr/bin/env python3
"""
TRIG6 Neurograph Builder v1
Phase 4.6 Code Contribution

Builds dendritic graph visualizations from TRIG6 configurations.
Dynamically merges trig6.yaml (core config) + trig6_neurograph.yaml (graph extensions).
Outputs DOT (Graphviz) or JSON (Obsidian/NetworkX) formats.

Usage:
    python neurograph_builder.py --output dot --file graph/trig6_neurograph.dot
    python neurograph_builder.py --output json --file graph/trig6_neurograph.json
"""

import yaml
import json
import argparse
import os
import sys


def load_configs(trig_yaml='config/trig6.yaml', neuro_yaml='config/trig6_neurograph.yaml'):
    """Load and parse YAML configuration files."""
    try:
        with open(trig_yaml, 'r') as f:
            trig_config = yaml.safe_load(f)
        with open(neuro_yaml, 'r') as f:
            neuro_config = yaml.safe_load(f)
        return trig_config, neuro_config
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found: {e.filename}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML: {e}", file=sys.stderr)
        sys.exit(1)


def build_dynamic_graph(trig_config, neuro_config):
    """
    Dynamically build graph structure by merging configs.
    
    Auto-generates:
    - Theta topic nodes from trig_config
    - Edges from INTENTION_VECTOR to theta nodes
    - Edges from theta nodes to optimal agents
    - Agent metric nodes and edges
    - Metric to organ connections
    """
    # Base from neuro_yaml
    graph = neuro_config.get('graph', {})
    nodes = list(neuro_config.get('nodes', []))  # Create mutable copy
    edges = list(neuro_config.get('edges', []))  # Create mutable copy
    groups = {g['name']: g['color'] for g in neuro_config.get('groups', [])}

    # Helper to check if node exists
    def node_exists(node_id):
        return any(n['id'] == node_id for n in nodes)
    
    # Helper to check if edge exists
    def edge_exists(from_id, to_id):
        return any(e['from'] == from_id and e['to'] == to_id for e in edges)

    # Auto-add from trig_yaml: theta topics as nodes
    for topic, data in trig_config.get('theta_topics', {}).items():
        node_id = f"theta_{topic}"
        if not node_exists(node_id):
            nodes.append({
                'id': node_id,
                'label': f"θ={data['theta']}\n{topic.capitalize()}",
                'group': 'theta_hub'
            })
        
        # Edges from INTENTION_VECTOR to thetas
        if not edge_exists('INTENTION_VECTOR', node_id):
            edges.append({
                'from': 'INTENTION_VECTOR',
                'to': node_id,
                'weight': data.get('weight', 0.85)
            })
        
        # Edges from theta to optimal_agents
        for opt_agent in data.get('optimal_agents', []):
            # Map agent names to node IDs
            agent_id = map_agent_to_node(opt_agent)
            if agent_id and not edge_exists(node_id, agent_id):
                edges.append({
                    'from': node_id,
                    'to': agent_id,
                    'weight': 0.75
                })

    # Auto-add agent-specific metrics as dendritic fans
    for agent, conf in trig_config.get('agents', {}).items():
        agent_id = f"{conf['model'].split('-')[0]}_{conf['trig']}"  # e.g., GPT_tan
        
        for metric, m_conf in conf.get('metrics', {}).items():
            metric_id = metric
            if not node_exists(metric_id):
                nodes.append({
                    'id': metric_id,
                    'label': f"{metric.capitalize()}\n({m_conf['description'][:20]}...)",
                    'group': 'metrics'
                })
            
            if not edge_exists(agent_id, metric_id):
                edges.append({
                    'from': agent_id,
                    'to': metric_id,
                    'weight': m_conf['weight']
                })
        
        # Metric to organs (specific mappings)
        if 'noise' in conf.get('metrics', {}) and not edge_exists('noise', 'Guardian_core'):
            edges.append({'from': 'noise', 'to': 'Guardian_core', 'weight': 0.6})
        
        if 'innovation' in conf.get('metrics', {}) and not edge_exists('innovation', 'FlameBench_core'):
            edges.append({'from': 'innovation', 'to': 'FlameBench_core', 'weight': 0.7})
        
        if 'focus' in conf.get('metrics', {}) and not edge_exists('focus', 'FlameBench_core'):
            edges.append({'from': 'focus', 'to': 'FlameBench_core', 'weight': 0.65})

    # Clamp weights for aesthetic stability (avoid 0/∞)
    for e in edges:
        e['weight'] = max(0.1, min(0.9, e.get('weight', 0.5)))

    return {'graph': graph, 'nodes': nodes, 'edges': edges, 'groups': groups}


def map_agent_to_node(agent_name):
    """Map agent names from trig config to node IDs."""
    mapping = {
        'angent_tangent': 'Grok_tan',
        'angent_cosine': 'Claude_cos',
        'angent_sine': 'Gemini_sin',
    }
    return mapping.get(agent_name)


def emit_dot(graph_data, output_file):
    """Generate Graphviz DOT format output."""
    dot = 'digraph TRIG6_NEUROGRAPH {\n'
    dot += '  rankdir=LR;\n'
    dot += '  node [shape=circle, style=filled, fontsize=10];\n'
    dot += '  overlap=false;\n'
    dot += '  splines=true;\n\n'

    # Subgraphs for groups
    for group, color in graph_data['groups'].items():
        dot += f'  subgraph cluster_{group} {{\n'
        dot += f'    label="{group.replace("_", " ").title()}";\n'
        dot += f'    color="{color}";\n'
        dot += f'    style=filled;\n'
        dot += f'    fillcolor="{color}20";\n'  # 20% opacity
        for node in [n for n in graph_data['nodes'] if n.get('group') == group]:
            label = node['label'].replace('\n', '\\n')
            dot += f'    {node["id"]} [label="{label}", fillcolor="{color}"];\n'
        dot += '  }\n\n'

    # Edges with weights
    for edge in graph_data['edges']:
        weight = edge.get('weight', 0.5)
        # Vary edge thickness based on weight
        penwidth = 0.5 + (weight * 3.5)  # Range: 0.5 to 4.0
        dot += f'  {edge["from"]} -> {edge["to"]} '
        dot += f'[weight={weight:.2f}, penwidth={penwidth:.2f}, '
        dot += f'label="{weight:.2f}"];\n'

    dot += '}\n'

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(dot)


def emit_json(graph_data, output_file):
    """Generate JSON format output (Obsidian/NetworkX compatible)."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(graph_data, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Build TRIG6 Neurograph from YAML configs.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --output dot --file graph/trig6_neurograph.dot
  %(prog)s --output json --file graph/trig6_neurograph.json
  %(prog)s --trig_yaml config/trig6.yaml --neuro_yaml config/trig6_neurograph.yaml --output dot --file output.dot
        """
    )
    parser.add_argument('--trig_yaml', default='config/trig6.yaml',
                        help='Path to TRIG6 core config (default: config/trig6.yaml)')
    parser.add_argument('--neuro_yaml', default='config/trig6_neurograph.yaml',
                        help='Path to neurograph config (default: config/trig6_neurograph.yaml)')
    parser.add_argument('--output', choices=['dot', 'json'], required=True,
                        help='Output format: dot (Graphviz) or json (Obsidian/NetworkX)')
    parser.add_argument('--file', required=True,
                        help='Output file path')
    
    args = parser.parse_args()

    # Load configurations
    print(f"Loading configurations...")
    print(f"  TRIG config: {args.trig_yaml}")
    print(f"  Neurograph config: {args.neuro_yaml}")
    trig_config, neuro_config = load_configs(args.trig_yaml, args.neuro_yaml)

    # Build dynamic graph
    print(f"Building dynamic graph...")
    graph_data = build_dynamic_graph(trig_config, neuro_config)
    print(f"  Nodes: {len(graph_data['nodes'])}")
    print(f"  Edges: {len(graph_data['edges'])}")
    print(f"  Groups: {len(graph_data['groups'])}")

    # Generate output
    print(f"Generating {args.output.upper()} output...")
    if args.output == 'dot':
        emit_dot(graph_data, args.file)
    elif args.output == 'json':
        emit_json(graph_data, args.file)

    print(f"✓ Generated {args.output} at {args.file}")


if __name__ == '__main__':
    main()
