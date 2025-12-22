#!/usr/bin/env python3
"""
StrategicKhaos CTF Brain - Distributed Cognitive Orchestration Engine

Maps Rubik's Cube PLL algorithms to penetration testing methodologies.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import networkx as nx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class CTFBrain:
    """Main CTF Brain orchestration engine."""

    def __init__(self, graph_path: Optional[str] = None):
        """Initialize CTF Brain with methodology graph."""
        if graph_path is None:
            # Default to methodology_graph.json in same directory as this file
            graph_path = Path(__file__).parent / "methodology_graph.json"
        
        self.graph_path = Path(graph_path)
        self.graph = nx.DiGraph()
        self.nodes_data = {}
        self.current_node = None
        self._load_graph()

    def _load_graph(self):
        """Load methodology graph from JSON file."""
        try:
            with open(self.graph_path, 'r') as f:
                data = json.load(f)
            
            # Add nodes
            for node in data['nodes']:
                self.graph.add_node(node['id'], **node)
                self.nodes_data[node['id']] = node
            
            # Add edges
            for edge in data['edges']:
                self.graph.add_edge(edge['from'], edge['to'], weight=edge['weight'])
            
            console.print(f"[green]✓[/green] Loaded {len(self.nodes_data)} nodes and {len(data['edges'])} edges")
        except FileNotFoundError:
            console.print(f"[red]✗[/red] Graph file not found: {self.graph_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            console.print(f"[red]✗[/red] Invalid JSON in graph file: {e}")
            sys.exit(1)

    def classify_query(self, query: str) -> Tuple[Optional[str], float, str]:
        """
        Classify user query to methodology node.
        
        Returns:
            Tuple of (node_id, confidence, method)
            method can be 'keyword', 'llm', or 'none'
        """
        query_lower = query.lower()
        best_match = None
        best_score = 0.0
        
        # Keyword matching
        for node_id, node_data in self.nodes_data.items():
            keywords = node_data.get('keywords', [])
            matches = sum(1 for kw in keywords if kw in query_lower)
            
            if matches > 0:
                # Score based on number of keyword matches and node weight
                score = (matches / len(keywords)) * node_data.get('confidence_weight', 0.5)
                if score > best_score:
                    best_score = score
                    best_match = node_id
        
        if best_match:
            return best_match, best_score, 'keyword'
        
        return None, 0.0, 'none'

    def get_next_moves(self, node_id: str, top_n: int = 5) -> List[Dict]:
        """
        Get recommended next nodes from current node.
        
        Uses 4-quadrant scoring:
        - Tool availability
        - Context match
        - Success rate (edge weight)
        - Efficiency
        """
        if node_id not in self.graph:
            return []
        
        next_moves = []
        for successor in self.graph.successors(node_id):
            edge_data = self.graph.get_edge_data(node_id, successor)
            node_data = self.nodes_data[successor]
            
            # 4-quadrant scoring
            tool_score = len(node_data.get('tools', [])) / 10.0  # Normalize
            context_score = node_data.get('confidence_weight', 0.5)
            success_score = edge_data.get('weight', 0.5)
            efficiency_score = 1.0 - (self.graph.out_degree(successor) / 10.0)  # Fewer outgoing = more focused
            
            # Combined score
            combined_score = (
                tool_score * 0.25 +
                context_score * 0.30 +
                success_score * 0.35 +
                efficiency_score * 0.10
            )
            
            next_moves.append({
                'node_id': successor,
                'node_data': node_data,
                'score': combined_score,
                'tool_score': tool_score,
                'context_score': context_score,
                'success_score': success_score
            })
        
        # Sort by score and return top N
        next_moves.sort(key=lambda x: x['score'], reverse=True)
        return next_moves[:top_n]

    def display_node(self, node_id: str):
        """Display node information in rich format."""
        if node_id not in self.nodes_data:
            console.print(f"[red]✗[/red] Node not found: {node_id}")
            return
        
        node = self.nodes_data[node_id]
        
        # Create panel content
        content = []
        content.append(f"[bold cyan]📍 Node:[/bold cyan] {node_id}")
        content.append(f"[bold cyan]📛 Name:[/bold cyan] {node['name']}")
        content.append(f"[bold cyan]🎲 PLL:[/bold cyan]  {node['pll_algorithm']}")
        content.append("")
        content.append(f"[bold cyan]🛠️  Tools:[/bold cyan] {', '.join(node['tools'])}")
        
        # Get next moves
        next_moves = self.get_next_moves(node_id, top_n=3)
        if next_moves:
            next_nodes = [f"{m['node_id']}" for m in next_moves]
            content.append(f"[bold cyan]➡️  Next:[/bold cyan]  {', '.join(next_nodes)}")
        
        panel = Panel(
            "\n".join(content),
            title=f"[bold green]{node['name']}[/bold green]",
            border_style="cyan"
        )
        console.print(panel)

    def display_next_moves(self, node_id: str):
        """Display next move recommendations."""
        next_moves = self.get_next_moves(node_id)
        
        if not next_moves:
            console.print("[yellow]No next moves available[/yellow]")
            return
        
        console.print(f"\n[bold]➡️  Next moves from {node_id}:[/bold]")
        for move in next_moves:
            node_data = move['node_data']
            score = move['score']
            tool_score = move['tool_score']
            context_score = move['context_score']
            
            console.print(
                f"  [cyan]{move['node_id']}[/cyan]: "
                f"[green]{score:.2f}[/green] "
                f"(tools:[yellow]{tool_score:.2f}[/yellow] "
                f"ctx:[yellow]{context_score:.2f}[/yellow])"
            )

    def list_nodes(self):
        """List all available methodology nodes."""
        table = Table(title="CTF Brain Methodology Nodes", show_header=True, header_style="bold cyan")
        table.add_column("Node", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("PLL Analog", style="yellow")
        table.add_column("Key Tools", style="magenta")
        
        for node_id, node_data in self.nodes_data.items():
            tools = ", ".join(node_data['tools'][:3])
            if len(node_data['tools']) > 3:
                tools += "..."
            
            table.add_row(
                node_id,
                node_data['name'],
                node_data['pll_algorithm'].split(' - ')[0],
                tools
            )
        
        console.print(table)

    def run_cli(self):
        """Run interactive CLI."""
        console.print(Panel.fit(
            "[bold cyan]STRATEGICKHAOS CTF BRAIN v1.0[/bold cyan]\n"
            "[green]Distributed Cognitive Orchestration Engine[/green]",
            border_style="cyan"
        ))
        console.print()
        console.print("[dim]Commands: query <text>, next, list, exit, help[/dim]")
        console.print()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]ctf[/bold cyan]>").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command in ['exit', 'quit', 'q']:
                    console.print("[yellow]Exiting CTF Brain...[/yellow]")
                    break
                
                elif command == 'help':
                    self._show_help()
                
                elif command == 'list':
                    self.list_nodes()
                
                elif command == 'next':
                    if self.current_node:
                        self.display_next_moves(self.current_node)
                    else:
                        console.print("[yellow]No current node. Use 'query' to classify a task.[/yellow]")
                
                elif command == 'query' or command not in ['exit', 'quit', 'q', 'help', 'list', 'next']:
                    # Treat entire input as query if command not recognized
                    query = args if command == 'query' else user_input
                    
                    if not query:
                        console.print("[yellow]Usage: query <your question>[/yellow]")
                        continue
                    
                    # Classify query
                    node_id, confidence, method = self.classify_query(query)
                    
                    if node_id:
                        self.current_node = node_id
                        self.display_node(node_id)
                        console.print(f"[dim]🎯 Confidence: {confidence:.0%} ({method})[/dim]")
                    else:
                        console.print("[yellow]Could not classify query. Try being more specific.[/yellow]")
                        console.print("[dim]Hint: Use keywords like 'scan', 'exploit', 'web', 'privilege'[/dim]")
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                break

    def _show_help(self):
        """Display help information."""
        help_text = """
[bold]Available Commands:[/bold]

  [cyan]query <text>[/cyan]     - Classify a query and get tool recommendations
  [cyan]<text>[/cyan]           - Shorthand for query (just type your question)
  [cyan]next[/cyan]             - Show next recommended moves from current node
  [cyan]list[/cyan]             - List all methodology nodes
  [cyan]help[/cyan]             - Show this help message
  [cyan]exit[/cyan]             - Exit CTF Brain

[bold]Examples:[/bold]

  ctf> scan for open ports
  ctf> enumerate web directories
  ctf> exploit sql injection
  ctf> next
"""
        console.print(Panel(help_text, title="[bold]CTF Brain Help[/bold]", border_style="cyan"))


def main():
    """Main entry point."""
    # Check for custom graph path
    graph_path = os.environ.get('GRAPH_CONFIG')
    
    try:
        brain = CTFBrain(graph_path=graph_path)
        brain.run_cli()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
