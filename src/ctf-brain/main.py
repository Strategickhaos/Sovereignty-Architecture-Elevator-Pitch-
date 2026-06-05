#!/usr/bin/env python3
"""
StrategicKhaos CTF Brain - Distributed Cognitive Orchestration Engine
Maps Rubik's Cube PLL algorithms to penetration testing methodologies
"""

import json
import os
import sys
from typing import Dict, List, Optional, Tuple
import networkx as nx


class CTFBrain:
    """Main CTF Brain orchestration engine"""
    
    def __init__(self, graph_path: Optional[str] = None):
        """Initialize CTF Brain with methodology graph"""
        if graph_path is None:
            graph_path = os.path.join(
                os.path.dirname(__file__), 
                "methodology_graph.json"
            )
        
        with open(graph_path, 'r') as f:
            self.graph_data = json.load(f)
        
        self.graph = self._build_graph()
        self.current_node = None
        self.history = []
        
    def _build_graph(self) -> nx.DiGraph:
        """Build NetworkX directed graph from methodology data"""
        G = nx.DiGraph()
        
        # Add nodes with attributes
        for node in self.graph_data['nodes']:
            G.add_node(
                node['id'],
                name=node['name'],
                pll=node['pll_algorithm'],
                description=node['description'],
                tools=node['tools'],
                keywords=node['keywords']
            )
        
        # Add edges (transitions between nodes)
        for node in self.graph_data['nodes']:
            for next_node in node['next_nodes']:
                G.add_edge(node['id'], next_node)
        
        return G
    
    def classify_query(self, query: str) -> Tuple[str, float, str]:
        """
        Classify user query to appropriate methodology node
        Returns: (node_id, confidence, method)
        """
        query_lower = query.lower()
        
        # Keyword matching
        best_match = None
        best_score = 0
        
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            keywords = node_data['keywords']
            
            # Calculate match score
            matches = sum(1 for kw in keywords if kw in query_lower)
            if matches > best_score:
                best_score = matches
                best_match = node_id
        
        # Calculate confidence percentage
        if best_match:
            max_keywords = len(self.graph.nodes[best_match]['keywords'])
            confidence = (best_score / max_keywords) * 100
            return best_match, confidence, "keyword"
        
        # Default to reconnaissance if no match
        return "01-Ua-Recon", 50.0, "default"
    
    def score_next_moves(self, current_node_id: str) -> List[Tuple[str, float, Dict]]:
        """
        Score potential next moves using 4-quadrant scoring
        Returns list of (node_id, score, breakdown)
        """
        if current_node_id not in self.graph:
            return []
        
        successors = list(self.graph.successors(current_node_id))
        scored_moves = []
        
        for next_node_id in successors:
            node_data = self.graph.nodes[next_node_id]
            
            # 4-Quadrant Scoring
            # 1. Tool availability (assume 0.7 for demo)
            tool_score = 0.70
            
            # 2. Context match (based on common transitions)
            context_score = 0.85
            
            # 3. Success rate (historical, assume 0.80 for demo)
            success_score = 0.80
            
            # 4. Efficiency (time/resources, assume 0.75 for demo)
            efficiency_score = 0.75
            
            # Weighted average
            total_score = (
                tool_score * 0.3 +
                context_score * 0.3 +
                success_score * 0.2 +
                efficiency_score * 0.2
            )
            
            breakdown = {
                'tools': tool_score,
                'context': context_score,
                'success': success_score,
                'efficiency': efficiency_score
            }
            
            scored_moves.append((next_node_id, total_score, breakdown))
        
        # Sort by score descending
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return scored_moves
    
    def display_node_info(self, node_id: str, confidence: Optional[float] = None, 
                         method: Optional[str] = None):
        """Display formatted node information"""
        if node_id not in self.graph:
            print(f"❌ Node {node_id} not found")
            return
        
        node_data = self.graph.nodes[node_id]
        
        print("\n╭" + "─" * 66 + "╮")
        print(f"│ 📍 Node: {node_id:<56}│")
        print(f"│ 📛 Name: {node_data['name']:<56}│")
        print(f"│ 🎲 PLL:  {node_data['pll']:<56}│")
        print("├" + "─" * 66 + "┤")
        
        # Tools
        tools_str = ", ".join(node_data['tools'][:7])
        if len(node_data['tools']) > 7:
            tools_str += "..."
        print(f"│ 🛠️  Tools: {tools_str:<54}│")
        
        # Next nodes
        successors = list(self.graph.successors(node_id))
        if successors:
            next_str = ", ".join(successors[:3])
            print(f"│ ➡️  Next:  {next_str:<54}│")
        
        # Confidence if provided
        if confidence is not None and method is not None:
            print(f"│ 🎯 Confidence: {confidence:.0f}% ({method}){' ' * (43 - len(str(int(confidence))))}│")
        
        print("╰" + "─" * 66 + "╯")
    
    def handle_query(self, query: str):
        """Process and handle user query"""
        node_id, confidence, method = self.classify_query(query)
        self.current_node = node_id
        self.history.append(node_id)
        self.display_node_info(node_id, confidence, method)
    
    def show_next_moves(self):
        """Display scored next moves from current node"""
        if not self.current_node:
            print("❌ No current node set. Run a query first.")
            return
        
        scored_moves = self.score_next_moves(self.current_node)
        
        if not scored_moves:
            print(f"🏁 No next moves from {self.current_node} (final node)")
            return
        
        print(f"\n➡️  Next moves from {self.current_node}:")
        for node_id, score, breakdown in scored_moves:
            node_data = self.graph.nodes[node_id]
            print(f"  {node_id}: {score:.2f} (tools:{breakdown['tools']:.2f} ctx:{breakdown['context']:.2f})")
    
    def show_help(self):
        """Display help information"""
        print("""
Available Commands:
  <query>          - Classify query and show recommended node
  next             - Show scored next moves from current node
  nodes            - List all methodology nodes
  history          - Show navigation history
  help             - Show this help message
  exit             - Exit CTF Brain

Examples:
  scan for open ports
  enumerate web directories
  exploit sql injection
  privilege escalation linux
        """)
    
    def list_nodes(self):
        """List all available methodology nodes"""
        print("\n📊 Methodology Nodes:\n")
        for node_id in sorted(self.graph.nodes()):
            node_data = self.graph.nodes[node_id]
            print(f"  {node_id:<15} {node_data['name']:<30} {node_data['pll']}")


def print_banner():
    """Print CTF Brain banner"""
    print("╔" + "═" * 66 + "╗")
    print("║" + " " * 15 + "STRATEGICKHAOS CTF BRAIN v1.0" + " " * 22 + "║")
    print("║" + " " * 9 + "Distributed Cognitive Orchestration Engine" + " " * 15 + "║")
    print("╚" + "═" * 66 + "╝")
    print()


def main():
    """Main CLI loop"""
    print_banner()
    
    try:
        brain = CTFBrain()
    except FileNotFoundError:
        print("❌ Error: methodology_graph.json not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing methodology_graph.json: {e}")
        sys.exit(1)
    
    print("Type 'help' for available commands, 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("ctf> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Exiting CTF Brain")
                break
            elif user_input.lower() == 'help':
                brain.show_help()
            elif user_input.lower() == 'next':
                brain.show_next_moves()
            elif user_input.lower() == 'nodes':
                brain.list_nodes()
            elif user_input.lower() == 'history':
                print(f"\n📜 History: {' → '.join(brain.history)}")
            else:
                # Treat as query
                brain.handle_query(user_input)
                
        except KeyboardInterrupt:
            print("\n👋 Exiting CTF Brain")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
