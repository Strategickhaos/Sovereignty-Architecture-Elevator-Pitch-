#!/usr/bin/env python3
"""
StrategicKhaos CTF Neural Router
================================
Distributed Cognitive Orchestration Engine

Rubik's PLL Algorithm Pattern → Pentest Methodology Mapping

Philosophy: See state → Recognize pattern → Execute algorithm → Objective achieved

Author: Dom (Me10101) - Strategickhaos DAO LLC
License: Sovereign - No vendor lock-in
"""

import json
import asyncio
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    from ollama import Client as OllamaClient
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from kubernetes import client, config
    from kubernetes.stream import stream
    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False

import networkx as nx


@dataclass
class Classification:
    """Result of query classification"""
    phase: str
    confidence: float
    keywords: list
    reasoning: str = ""


@dataclass  
class MoveScore:
    """Scored next move with quadrant breakdown"""
    node_id: str
    total_score: float
    tool_ready: float
    context_match: float
    success_rate: float
    efficiency: float


class CTFBrain:
    """
    Distributed Cognitive Orchestration Engine
    
    Maps user queries to pentest methodology nodes (like recognizing PLL cases),
    dispatches appropriate tools, and predicts optimal next moves.
    """
    
    PHASE_MAP = {
        "Recon": "01-Ua-Recon",
        "Reconnaissance": "01-Ua-Recon",
        "Enum": "02-Ub-Enum",
        "Enumeration": "02-Ub-Enum",
        "WebApp": "03-H-WebApp",
        "Web": "03-H-WebApp",
        "Exploit": "04-Z-Exploit",
        "Exploitation": "04-Z-Exploit",
        "Creds": "05-Aa-Creds",
        "Credentials": "05-Aa-Creds",
        "PrivEsc": "06-Ab-PrivEsc",
        "Privilege Escalation": "06-Ab-PrivEsc",
        "Persist": "07-E-Persist",
        "Persistence": "07-E-Persist",
        "Exfil": "08-T-Exfil",
        "Exfiltration": "08-T-Exfil",
        "Pivot": "09-F-Pivot",
        "Pivoting": "09-F-Pivot",
        "Cleanup": "10-V-Cleanup"
    }
    
    def __init__(self, graph_path: Optional[str] = None, ollama_host: str = "http://localhost:11434"):
        self.graph = nx.DiGraph()
        self.nodes_data = {}
        self.metadata = {}
        self.weights = {}
        
        # Load graph from JSON
        if graph_path is None:
            graph_path = Path(__file__).parent / "methodology_graph.json"
        self.load_methodology_graph(graph_path)
        
        # Initialize Ollama client if available
        self.ollama = None
        if OLLAMA_AVAILABLE:
            try:
                self.ollama = OllamaClient(host=ollama_host)
            except Exception as e:
                print(f"[WARN] Ollama not available: {e}")
        
        # Initialize Kubernetes client if available
        self.k8s_v1 = None
        if K8S_AVAILABLE:
            try:
                config.load_kube_config()
                self.k8s_v1 = client.CoreV1Api()
            except Exception:
                try:
                    config.load_incluster_config()
                    self.k8s_v1 = client.CoreV1Api()
                except Exception as e:
                    print(f"[WARN] Kubernetes not available: {e}")
    
    def load_methodology_graph(self, path: str):
        """Load the Obsidian-style methodology graph from JSON"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.metadata = data.get('metadata', {})
        self.weights = data.get('quadrant_weights', {
            'tool_ready': 0.3,
            'context_match': 0.3,
            'success_rate': 0.25,
            'efficiency': 0.15
        })
        
        # Build nodes
        for node_id, node_data in data['nodes'].items():
            self.graph.add_node(node_id, **node_data)
            self.nodes_data[node_id] = node_data
        
        # Build edges
        for edge in data['edges']:
            self.graph.add_edge(edge[0], edge[1])
        
        print(f"[INFO] Loaded {len(self.nodes_data)} nodes, {len(data['edges'])} edges")
    
    async def classify_query(self, query: str) -> dict:
        """
        Analyze query → Assign to methodology node
        Like recognizing a PLL case from the cube state
        """
        query_lower = query.lower()
        
        # First try: keyword matching (fast path)
        matched_node = self._keyword_match(query_lower)
        if matched_node:
            node_data = self.nodes_data[matched_node]
            return {
                "node": matched_node,
                "name": node_data.get('name', matched_node),
                "tools": node_data['tools'],
                "next_moves": list(self.graph.successors(matched_node)),
                "pll_analog": node_data.get('pll_analog', ''),
                "classification": Classification(
                    phase=node_data.get('name', matched_node),
                    confidence=0.85,
                    keywords=[t for t in node_data['triggers'] if t in query_lower]
                ).__dict__,
                "method": "keyword"
            }
        
        # Second try: LLM classification (if available)
        if self.ollama:
            try:
                classification = await self._llm_classify(query)
                node_id = self.PHASE_MAP.get(classification.phase, "01-Ua-Recon")
                node_data = self.nodes_data.get(node_id, self.nodes_data["01-Ua-Recon"])
                
                return {
                    "node": node_id,
                    "name": node_data.get('name', node_id),
                    "tools": node_data['tools'],
                    "next_moves": list(self.graph.successors(node_id)),
                    "pll_analog": node_data.get('pll_analog', ''),
                    "classification": classification.__dict__,
                    "method": "llm"
                }
            except Exception as e:
                print(f"[WARN] LLM classification failed: {e}")
        
        # Fallback: default to Recon
        node_data = self.nodes_data["01-Ua-Recon"]
        return {
            "node": "01-Ua-Recon",
            "name": "Reconnaissance",
            "tools": node_data['tools'],
            "next_moves": list(self.graph.successors("01-Ua-Recon")),
            "pll_analog": node_data.get('pll_analog', ''),
            "classification": Classification(
                phase="Recon",
                confidence=0.5,
                keywords=[],
                reasoning="Fallback - no clear match"
            ).__dict__,
            "method": "fallback"
        }
    
    def _keyword_match(self, query: str) -> Optional[str]:
        """Fast keyword-based classification"""
        best_match = None
        best_score = 0
        
        for node_id, node_data in self.nodes_data.items():
            triggers = node_data.get('triggers', [])
            score = sum(1 for t in triggers if t in query)
            if score > best_score:
                best_score = score
                best_match = node_id
        
        return best_match if best_score > 0 else None
    
    async def _llm_classify(self, query: str) -> Classification:
        """Use local LLM for semantic classification"""
        system_prompt = '''You are a CTF/pentest methodology classifier.
Given a query, identify which phase it belongs to:
- Recon (scanning, discovery, network mapping)
- Enum (enumeration, directory busting, user listing)
- WebApp (web vulnerabilities, injection, XSS, SQLi)
- Exploit (gaining access, shells, RCE)
- Creds (password attacks, hash cracking, credential theft)
- PrivEsc (privilege escalation, root, admin)
- Persist (maintaining access, backdoors, implants)
- Exfil (data extraction, file transfer)
- Pivot (lateral movement, tunneling, proxying)
- Cleanup (log clearing, evidence removal)

Return ONLY valid JSON: {"phase": "...", "confidence": 0.0-1.0, "keywords": [...], "reasoning": "..."}'''
        
        response = self.ollama.chat(
            model='qwen2.5:7b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': query}
            ]
        )
        
        content = response['message']['content']
        # Extract JSON from response
        import re
        json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return Classification(**data)
        
        raise ValueError("Could not parse LLM response")
    
    def suggest_next_moves(self, current_node: str, context: Optional[dict] = None) -> list[MoveScore]:
        """
        Quadrilateral collapse: 4 perspectives → optimal next actions
        
        Like choosing the next algorithm after solving OLL based on resulting PLL case
        """
        if context is None:
            context = {}
        
        successors = list(self.graph.successors(current_node))
        scored_moves = []
        
        for next_node in successors:
            scores = self._calculate_quadrant_scores(next_node, context)
            total = sum(scores[k] * self.weights[k] for k in self.weights)
            
            scored_moves.append(MoveScore(
                node_id=next_node,
                total_score=total,
                **scores
            ))
        
        return sorted(scored_moves, key=lambda x: x.total_score, reverse=True)
    
    def _calculate_quadrant_scores(self, node_id: str, context: dict) -> dict:
        """
        4-quadrant scoring system:
        1. Tool availability (do we have the tools?)
        2. Context relevance (does it fit current state?)
        3. Success probability (historical data)
        4. Time efficiency (how long does it take?)
        """
        node_data = self.nodes_data.get(node_id, {})
        available_tools = context.get('available_tools', [])
        findings = context.get('findings', [])
        historical = context.get('historical_success', {})
        time_pressure = context.get('time_constraints', 0)
        
        # Tool readiness
        required_tools = node_data.get('tools', [])
        if available_tools:
            tool_ready = sum(1 for t in required_tools if t in available_tools) / len(required_tools) if required_tools else 1.0
        else:
            tool_ready = 0.7  # Assume most tools available by default
        
        # Context match (semantic overlap with findings)
        triggers = node_data.get('triggers', [])
        findings_str = ' '.join(str(f).lower() for f in findings)
        context_match = sum(1 for t in triggers if t in findings_str) / len(triggers) if triggers else 0.5
        
        # Historical success rate
        success_rate = historical.get(node_id, 0.7)
        
        # Efficiency (inverse of time pressure impact)
        efficiency = max(0.1, 1.0 - (time_pressure / 100))
        
        return {
            'tool_ready': tool_ready,
            'context_match': context_match,
            'success_rate': success_rate,
            'efficiency': efficiency
        }
    
    async def execute_on_cluster(self, node_id: str, target: str, namespace: str = "ctf-tools") -> str:
        """
        Dispatch methodology to GKE pod with appropriate tools
        """
        if not self.k8s_v1:
            return "[ERROR] Kubernetes not available"
        
        node_data = self.nodes_data.get(node_id, {})
        tools = node_data.get('tools', [])
        
        # Find or create pod with required tools
        pod_name = f"ctf-worker-{node_id.split('-')[0].lower()}"
        
        # Build command based on node type
        commands = {
            "01-Ua-Recon": f"nmap -sV -sC {target}",
            "02-Ub-Enum": f"gobuster dir -u {target} -w /usr/share/wordlists/common.txt",
            "03-H-WebApp": f"nikto -h {target}",
            "04-Z-Exploit": f"echo 'Manual exploit selection required for {target}'",
        }
        
        cmd = commands.get(node_id, f"echo 'No auto-command for {node_id}'")
        
        try:
            exec_command = ['/bin/bash', '-c', cmd]
            resp = stream(
                self.k8s_v1.connect_get_namespaced_pod_exec,
                pod_name, namespace,
                command=exec_command,
                stderr=True, stdin=False, stdout=True, tty=False
            )
            return resp
        except Exception as e:
            return f"[ERROR] Execution failed: {e}"
    
    def get_graph_stats(self) -> dict:
        """Return graph statistics for monitoring"""
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "nodes": list(self.nodes_data.keys()),
            "metadata": self.metadata
        }
    
    def visualize_path(self, start: str, end: str) -> list:
        """Find shortest path between methodology nodes"""
        try:
            path = nx.shortest_path(self.graph, start, end)
            return [{"node": n, "name": self.nodes_data[n].get('name', n)} for n in path]
        except nx.NetworkXNoPath:
            return []


async def interactive_cli():
    """Interactive CLI for the CTF Brain"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           STRATEGICKHAOS CTF BRAIN v1.0                         ║
║     Distributed Cognitive Orchestration Engine                   ║
║                                                                  ║
║  "See state → Recognize pattern → Execute algorithm"             ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    brain = CTFBrain()
    stats = brain.get_graph_stats()
    print(f"[LOADED] {stats['total_nodes']} methodology nodes, {stats['total_edges']} transitions\n")
    
    current_node = None
    context = {"available_tools": [], "findings": []}
    
    while True:
        try:
            query = input("ctf> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[EXIT] Sovereign operations complete.")
            break
        
        if not query:
            continue
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("[EXIT] Sovereign operations complete.")
            break
        
        if query.lower() == 'help':
            print("""
Commands:
  <query>       - Classify query and get methodology
  graph         - Show graph statistics
  nodes         - List all methodology nodes
  path A B      - Show path from node A to node B
  next          - Suggest next moves from current node
  tools <list>  - Set available tools (comma-separated)
  help          - Show this help
  exit/quit     - Exit
            """)
            continue
        
        if query.lower() == 'graph':
            stats = brain.get_graph_stats()
            print(f"\n📊 Graph: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
            print(f"📋 Metadata: {stats['metadata'].get('name', 'Unknown')}\n")
            continue
        
        if query.lower() == 'nodes':
            print("\n📍 Methodology Nodes:")
            for node_id, data in brain.nodes_data.items():
                print(f"  {node_id}: {data.get('name', 'Unknown')} - {len(data.get('tools', []))} tools")
            print()
            continue
        
        if query.lower().startswith('path '):
            parts = query.split()
            if len(parts) >= 3:
                path = brain.visualize_path(parts[1], parts[2])
                if path:
                    print(f"\n🛤️  Path: {' → '.join(p['name'] for p in path)}\n")
                else:
                    print("\n[ERROR] No path found\n")
            continue
        
        if query.lower() == 'next' and current_node:
            moves = brain.suggest_next_moves(current_node, context)
            print(f"\n➡️  Next moves from {current_node}:")
            for move in moves:
                print(f"  {move.node_id}: {move.total_score:.2f} (tools:{move.tool_ready:.2f} ctx:{move.context_match:.2f})")
            print()
            continue
        
        if query.lower().startswith('tools '):
            tools = [t.strip() for t in query[6:].split(',')]
            context['available_tools'] = tools
            print(f"[SET] Available tools: {tools}\n")
            continue
        
        # Default: classify the query
        result = await brain.classify_query(query)
        current_node = result['node']
        
        print(f"""
╭──────────────────────────────────────────────────────────────────╮
│ 📍 Node: {result['node']:<54}│
│ 📛 Name: {result['name']:<54}│
│ 🎲 PLL:  {result['pll_analog'][:54]:<54}│
├──────────────────────────────────────────────────────────────────┤
│ 🛠️  Tools: {', '.join(result['tools'][:5]):<52}│
│ ➡️  Next:  {', '.join(result['next_moves'][:3]):<52}│
│ 🎯 Confidence: {result['classification']['confidence']:.0%} ({result['method']})                              │
╰──────────────────────────────────────────────────────────────────╯
        """)


def main():
    """Entry point"""
    asyncio.run(interactive_cli())


if __name__ == "__main__":
    main()
