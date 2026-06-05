#!/usr/bin/env python3
"""
neurograph_builder.py

SAGCO-OS Neurograph Cognitive Topology Visualization System

Implements the five-tier neural topology with hierarchical information flow,
activation/inhibition edges, and danger zone indicators.

Part of: Self-Amplifying Generative Cognitive Operating System
DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1-LOM1-TRIG6-WAVE1-HYBRID1-NEURO1-OPS1-BOOT1

Copyright (c) 2026 Strategickhaos DAO LLC
Inventor: Dom Garza
"""

import json
import math
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class EdgeType(Enum):
    """Edge type enumeration"""
    PROJECTION = "projection"
    ACTIVATION = "activation"
    INHIBITION = "inhibition"
    CONTROL = "control"
    MODULATION = "modulation"
    AGGREGATION = "aggregation"
    INPUT = "input"
    OUTPUT = "output"


class NodeTier(Enum):
    """Hierarchical tier assignment"""
    TIER_0 = 0  # Intention Vector
    TIER_1 = 1  # Theta Topics
    TIER_2 = 2  # Agent Neurons
    TIER_2_5 = 2.5  # Blend Control
    TIER_3 = 3  # Metric Dendrites
    TIER_3_5 = 3.5  # Derived Metrics
    TIER_4 = 4  # Organ Effectors
    TIER_5 = 5  # FOCUS Router


@dataclass
class Node:
    """Graph node representing a cognitive element"""
    id: str
    label: str
    tier: NodeTier
    node_type: str
    active: bool = True
    danger_zone: bool = False
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'label': self.label,
            'tier': self.tier.value,
            'node_type': self.node_type,
            'active': bool(self.active),
            'danger_zone': bool(self.danger_zone),
            'metadata': self.metadata
        }


@dataclass
class Edge:
    """Graph edge representing information flow"""
    source: str
    target: str
    edge_type: EdgeType
    weight: float = 1.0
    active: bool = True
    danger_indicator: bool = False
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'source': self.source,
            'target': self.target,
            'edge_type': self.edge_type.value,
            'weight': float(self.weight),
            'active': bool(self.active),
            'danger_indicator': bool(self.danger_indicator),
            'metadata': self.metadata
        }


class NeurographBuilder:
    """
    Neurograph Cognitive Topology Visualization System
    
    Implements Claim 4: Visualization system for multi-agent cognitive architectures
    """
    
    # Domain-specific theta values (in radians)
    THETA_DOMAINS = {
        "hypervisor": 0.1,
        "compiler": math.pi / 6,
        "security": math.pi / 4,
        "academics": math.pi / 3,
        "creative": math.pi / 2,
        "research": 2 * math.pi / 3
    }
    
    # Agent function mappings
    AGENT_FUNCTIONS = {
        "GPT": "sin",
        "Claude": "cos",
        "Grok": "tan",
        "Gemini": "cot",
        "Web": "sec",
        "SAGCO": "csc"
    }
    
    def __init__(self):
        """Initialize the neurograph builder"""
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.current_theta: float = math.pi / 4
        
    def clear(self):
        """Clear all nodes and edges"""
        self.nodes.clear()
        self.edges.clear()
    
    def add_node(self, node: Node) -> Node:
        """Add a node to the graph"""
        self.nodes[node.id] = node
        return node
    
    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge to the graph"""
        self.edges.append(edge)
        return edge
    
    def build_tier_0_intention(self) -> Node:
        """
        Build Tier 0: Intention Vector
        
        Single node representing the task intention
        """
        node = Node(
            id="I_theta",
            label=f"I(θ = {math.degrees(self.current_theta):.1f}°)",
            tier=NodeTier.TIER_0,
            node_type="intention",
            metadata={"theta": self.current_theta}
        )
        return self.add_node(node)
    
    def build_tier_1_topics(self, intention_node: Node) -> List[Node]:
        """
        Build Tier 1: Theta Topics
        
        Domain-specific θ values with projection edges from intention
        """
        topic_nodes = []
        
        for domain, theta_value in self.THETA_DOMAINS.items():
            node = Node(
                id=f"topic_{domain}",
                label=f"{domain.title()}\nθ={math.degrees(theta_value):.1f}°",
                tier=NodeTier.TIER_1,
                node_type="topic",
                active=(abs(theta_value - self.current_theta) < 0.5),
                metadata={"domain": domain, "theta": theta_value}
            )
            topic_nodes.append(self.add_node(node))
            
            # Add projection edge from intention
            edge = Edge(
                source=intention_node.id,
                target=node.id,
                edge_type=EdgeType.PROJECTION,
                weight=1.0 - abs(theta_value - self.current_theta) / math.pi
            )
            self.add_edge(edge)
        
        return topic_nodes
    
    def build_tier_2_agents(self, topic_nodes: List[Node], 
                           agent_weights: Optional[Dict[str, float]] = None) -> List[Node]:
        """
        Build Tier 2: Agent Neurons
        
        Six TRIG6 agents with activation/inhibition edges
        
        Args:
            topic_nodes: Topic nodes from Tier 1
            agent_weights: Optional pre-computed weights for agents
        """
        agent_nodes = []
        
        if agent_weights is None:
            # Default weights based on current theta
            agent_weights = {
                "GPT": abs(math.sin(self.current_theta)),
                "Claude": abs(math.cos(self.current_theta)),
                "Grok": abs(math.tanh(math.tan(self.current_theta))),
                "Gemini": 0.5,
                "Web": 0.3,
                "SAGCO": 1.0
            }
        
        for agent_name, trig_func in self.AGENT_FUNCTIONS.items():
            weight = agent_weights.get(agent_name, 0.5)
            
            # Check for danger zones
            danger = self._check_agent_danger(agent_name, self.current_theta)
            
            node = Node(
                id=f"agent_{agent_name.lower()}",
                label=f"{agent_name}\n({trig_func})\nw={weight:.3f}",
                tier=NodeTier.TIER_2,
                node_type="agent",
                active=(weight > 0.1),
                danger_zone=danger,
                metadata={
                    "agent": agent_name,
                    "function": trig_func,
                    "weight": weight
                }
            )
            agent_nodes.append(self.add_node(node))
            
            # Add edges from topics
            for topic in topic_nodes:
                if topic.active:
                    edge_type = EdgeType.ACTIVATION if weight > 0.5 else EdgeType.INHIBITION
                    edge = Edge(
                        source=topic.id,
                        target=node.id,
                        edge_type=edge_type,
                        weight=weight,
                        danger_indicator=danger
                    )
                    self.add_edge(edge)
        
        return agent_nodes
    
    def build_tier_2_5_blend_control(self, alpha: float, damping: float) -> List[Node]:
        """
        Build Tier 2.5: Blend Control
        
        Alpha and damping nodes with control edges
        """
        control_nodes = []
        
        # Alpha node
        alpha_node = Node(
            id="control_alpha",
            label=f"α = {alpha:.3f}\n{'Hyperbolic' if alpha > 0.5 else 'Trigonometric'}",
            tier=NodeTier.TIER_2_5,
            node_type="control",
            metadata={"alpha": alpha, "mode": "hyperbolic" if alpha > 0.5 else "trigonometric"}
        )
        control_nodes.append(self.add_node(alpha_node))
        
        # Damping node
        damping_node = Node(
            id="control_damping",
            label=f"Damping\n{damping:.3f}",
            tier=NodeTier.TIER_2_5,
            node_type="control",
            metadata={"damping": damping}
        )
        control_nodes.append(self.add_node(damping_node))
        
        return control_nodes
    
    def build_tier_3_metrics(self, agent_nodes: List[Node]) -> List[Node]:
        """
        Build Tier 3: Metric Dendrites
        
        Per-agent metrics (focus, coherence, noise, innovation)
        """
        metric_nodes = []
        metric_types = ["focus", "coherence", "noise", "innovation"]
        
        for agent in agent_nodes:
            agent_name = agent.metadata["agent"]
            for metric_type in metric_types:
                # Simulate metric value
                metric_value = 0.5 + 0.3 * math.sin(hash(agent_name + metric_type) % 100)
                
                node = Node(
                    id=f"metric_{agent_name.lower()}_{metric_type}",
                    label=f"{metric_type.title()}\n{metric_value:.2f}",
                    tier=NodeTier.TIER_3,
                    node_type="metric",
                    active=(metric_value > 0.4),
                    metadata={"agent": agent_name, "metric": metric_type, "value": metric_value}
                )
                metric_nodes.append(self.add_node(node))
                
                # Edge from agent
                edge = Edge(
                    source=agent.id,
                    target=node.id,
                    edge_type=EdgeType.OUTPUT,
                    weight=metric_value
                )
                self.add_edge(edge)
        
        return metric_nodes
    
    def build_tier_3_5_derived_metrics(self, metric_nodes: List[Node],
                                       resonance: float, drift: float, 
                                       noise: float) -> List[Node]:
        """
        Build Tier 3.5: Derived Metrics
        
        Resonance, drift, noise, invention density aggregations
        """
        derived_nodes = []
        
        metrics = [
            ("resonance", resonance),
            ("drift", drift),
            ("noise", noise),
            ("invention_density", 0.5)  # Placeholder
        ]
        
        for metric_name, value in metrics:
            danger = (metric_name == "drift" and value > 0.3) or \
                    (metric_name == "noise" and value > 0.15)
            
            node = Node(
                id=f"derived_{metric_name}",
                label=f"{metric_name.replace('_', ' ').title()}\n{value:.3f}",
                tier=NodeTier.TIER_3_5,
                node_type="derived_metric",
                active=True,
                danger_zone=danger,
                metadata={"metric": metric_name, "value": value}
            )
            derived_nodes.append(self.add_node(node))
            
            # Aggregation edges from tier 3 metrics
            for metric_node in metric_nodes[:3]:  # Just connect a few for clarity
                edge = Edge(
                    source=metric_node.id,
                    target=node.id,
                    edge_type=EdgeType.AGGREGATION,
                    weight=0.5
                )
                self.add_edge(edge)
        
        return derived_nodes
    
    def build_tier_4_organs(self, derived_nodes: List[Node]) -> List[Node]:
        """
        Build Tier 4: Organ Effectors
        
        FlameBench, Guardian, HYDRA Mesh, SAGCO Logs
        """
        organ_nodes = []
        organs = [
            ("flamebench", "FlameBench"),
            ("guardian", "Guardian"),
            ("hydra", "HYDRA Mesh"),
            ("logs", "SAGCO Logs")
        ]
        
        for organ_id, organ_label in organs:
            node = Node(
                id=f"organ_{organ_id}",
                label=organ_label,
                tier=NodeTier.TIER_4,
                node_type="organ",
                active=True,
                metadata={"organ": organ_id}
            )
            organ_nodes.append(self.add_node(node))
            
            # Input edges from derived metrics
            for derived in derived_nodes:
                edge = Edge(
                    source=derived.id,
                    target=node.id,
                    edge_type=EdgeType.INPUT,
                    weight=0.7
                )
                self.add_edge(edge)
        
        return organ_nodes
    
    def build_tier_5_focus_router(self, organ_nodes: List[Node]) -> Node:
        """
        Build Tier 5: FOCUS Router
        
        Central routing node receiving inputs from all organs
        """
        router = Node(
            id="router_focus",
            label="FOCUS Router",
            tier=NodeTier.TIER_5,
            node_type="router",
            active=True,
            metadata={"routes": len(organ_nodes)}
        )
        self.add_node(router)
        
        # Input edges from all organs
        for organ in organ_nodes:
            edge = Edge(
                source=organ.id,
                target=router.id,
                edge_type=EdgeType.INPUT,
                weight=1.0
            )
            self.add_edge(edge)
        
        return router
    
    def _check_agent_danger(self, agent_name: str, theta: float) -> bool:
        """Check if agent is in danger zone based on singularities"""
        danger_threshold = 0.1
        
        if agent_name in ["Grok"]:  # tan
            return abs(theta - math.pi/2) < danger_threshold
        elif agent_name in ["Gemini"]:  # cot
            return abs(theta) < danger_threshold or \
                   abs(theta - math.pi) < danger_threshold
        elif agent_name in ["Web"]:  # sec
            return abs(theta - math.pi/2) < danger_threshold
        elif agent_name in ["SAGCO"]:  # csc
            return abs(theta) < danger_threshold or \
                   abs(theta - math.pi) < danger_threshold
        
        return False
    
    def build_complete_neurograph(self, theta: float = None,
                                 agent_weights: Optional[Dict[str, float]] = None,
                                 alpha: float = 0.0,
                                 damping: float = 1.0,
                                 resonance: float = 0.8,
                                 drift: float = 0.2,
                                 noise: float = 0.1) -> 'NeurographBuilder':
        """
        Build the complete five-tier neurograph
        
        Implements Claim 4: Complete visualization system
        
        Args:
            theta: Task angle (optional, uses current if None)
            agent_weights: Pre-computed agent weights
            alpha: Blend ratio
            damping: Damping factor
            resonance: Resonance score
            drift: Drift score
            noise: Noise score
            
        Returns:
            Self for method chaining
        """
        if theta is not None:
            self.current_theta = theta
        
        # Clear existing graph
        self.clear()
        
        # Build all tiers
        intention = self.build_tier_0_intention()
        topics = self.build_tier_1_topics(intention)
        agents = self.build_tier_2_agents(topics, agent_weights)
        controls = self.build_tier_2_5_blend_control(alpha, damping)
        metrics = self.build_tier_3_metrics(agents)
        derived = self.build_tier_3_5_derived_metrics(metrics, resonance, drift, noise)
        organs = self.build_tier_4_organs(derived)
        router = self.build_tier_5_focus_router(organs)
        
        # Add control edges from drift to blend control
        for control in controls:
            edge = Edge(
                source=derived[1].id,  # drift node
                target=control.id,
                edge_type=EdgeType.CONTROL,
                weight=drift
            )
            self.add_edge(edge)
        
        return self
    
    def to_dot(self) -> str:
        """
        Export graph in Graphviz DOT format
        
        Implements Claim 4(d): DOT format rendering
        
        Returns:
            DOT format string
        """
        lines = ["digraph NeurographCognitiveTopology {"]
        lines.append("  rankdir=TB;")
        lines.append("  node [shape=box, style=rounded];")
        lines.append("")
        
        # Group nodes by tier
        tiers = {}
        for node in self.nodes.values():
            tier_val = node.tier.value
            if tier_val not in tiers:
                tiers[tier_val] = []
            tiers[tier_val].append(node)
        
        # Add nodes tier by tier
        for tier_val in sorted(tiers.keys()):
            lines.append(f"  // Tier {tier_val}")
            lines.append("  {")
            lines.append(f"    rank=same;")
            
            for node in tiers[tier_val]:
                # Node styling
                color = "red" if node.danger_zone else ("green" if node.active else "gray")
                style = "filled" if node.danger_zone else "rounded"
                
                lines.append(f'    {node.id} [label="{node.label}", '
                           f'color="{color}", style="{style}"];')
            
            lines.append("  }")
            lines.append("")
        
        # Add edges
        lines.append("  // Edges")
        for edge in self.edges:
            color = "red" if edge.danger_indicator else "black"
            style = "dashed" if edge.edge_type == EdgeType.INHIBITION else "solid"
            width = max(0.5, min(3.0, edge.weight * 2))
            
            lines.append(f'  {edge.source} -> {edge.target} '
                        f'[color="{color}", style="{style}", penwidth={width:.1f}, '
                        f'label="{edge.edge_type.value}"];')
        
        lines.append("}")
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """
        Export graph in JSON format for interactive viewers
        
        Implements Claim 4(d): JSON format rendering
        
        Returns:
            JSON format string
        """
        data = {
            "metadata": {
                "theta": self.current_theta,
                "theta_degrees": math.degrees(self.current_theta),
                "node_count": len(self.nodes),
                "edge_count": len(self.edges)
            },
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges]
        }
        return json.dumps(data, indent=2)
    
    def get_summary(self) -> Dict:
        """Get a summary of the neurograph"""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "active_nodes": sum(1 for n in self.nodes.values() if n.active),
            "danger_nodes": sum(1 for n in self.nodes.values() if n.danger_zone),
            "theta": self.current_theta,
            "theta_degrees": math.degrees(self.current_theta)
        }


def main():
    """Example usage and demonstration"""
    print("=" * 80)
    print("SAGCO-OS Neurograph Cognitive Topology Visualization System")
    print("=" * 80)
    print()
    
    # Build neurograph at different theta values
    test_cases = [
        {"theta": math.pi / 4, "alpha": 0.1, "drift": 0.15},
        {"theta": math.pi / 2 - 0.05, "alpha": 0.5, "drift": 0.35},
        {"theta": 3 * math.pi / 4, "alpha": 0.3, "drift": 0.25}
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test Case {i}: θ = {math.degrees(params['theta']):.1f}°, "
              f"α = {params['alpha']:.2f}, drift = {params['drift']:.2f}")
        print('=' * 80)
        
        builder = NeurographBuilder()
        builder.build_complete_neurograph(
            theta=params['theta'],
            alpha=params['alpha'],
            drift=params['drift'],
            resonance=0.75,
            noise=0.12
        )
        
        summary = builder.get_summary()
        print(f"\nGraph Summary:")
        print(f"  Nodes: {summary['nodes']} (Active: {summary['active_nodes']}, "
              f"Danger: {summary['danger_nodes']})")
        print(f"  Edges: {summary['edges']}")
        print(f"  Theta: {summary['theta_degrees']:.1f}°")
        
        # Export to DOT
        dot_file = f"/tmp/neurograph_test_{i}.dot"
        with open(dot_file, 'w') as f:
            f.write(builder.to_dot())
        print(f"\n  DOT file written to: {dot_file}")
        
        # Export to JSON
        json_file = f"/tmp/neurograph_test_{i}.json"
        with open(json_file, 'w') as f:
            f.write(builder.to_json())
        print(f"  JSON file written to: {json_file}")
    
    print("\n" + "=" * 80)
    print("Neurograph visualization files generated successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
