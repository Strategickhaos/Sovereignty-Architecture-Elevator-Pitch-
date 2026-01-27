#!/usr/bin/env python3
"""
DOM Computing Model - Vault Mapper
===================================

Automatically discovers and maps vault-nodes in your filesystem.
Maps the distributed cognition graph of your sovereign computing environment.

Usage:
    python vault_mapper.py --scan ~/ --depth 3 --visualize
    python vault_mapper.py --init
    python vault_mapper.py --cortex ~/sovereignty-cortex
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import subprocess


@dataclass
class VaultNode:
    """Represents a discovered vault-node in the system"""
    path: str
    name: str
    node_type: str  # 'code_vault', 'pure_repo', 'pure_vault', 'hybrid', 'ai_dataset'
    indicators: List[str]  # Which files indicate this type
    tools: List[str]  # Which tools would open this
    size_mb: float
    file_count: int
    last_modified: str
    metadata: Dict[str, any]


class VaultMapper:
    """
    The DCM Vault Mapper discovers and classifies compute nodes.
    
    This is the reconnaissance layer for your distributed cognition engine.
    """
    
    # Indicators that signal different node types
    INDICATORS = {
        'git_repo': ['.git'],
        'obsidian_vault': ['.obsidian'],
        'python_project': ['setup.py', 'pyproject.toml', 'requirements.txt'],
        'node_project': ['package.json', 'node_modules'],
        'rust_project': ['Cargo.toml', 'Cargo.lock'],
        'java_project': ['pom.xml', 'build.gradle', 'gradle.properties'],
        'go_project': ['go.mod', 'go.sum'],
        'docker_project': ['Dockerfile', 'docker-compose.yml'],
        'kubernetes_config': ['k8s/', 'kubernetes/', '*.yaml'],
        'ai_config': ['ai_constitution.yaml', 'jarvis_config.yaml', '*.yaml'],
        'vault_config': ['.vault', 'vault_config.json']
    }
    
    # Tool associations
    TOOL_MAP = {
        'git_repo': ['git', 'GitHub Desktop'],
        'obsidian_vault': ['Obsidian'],
        'python_project': ['PyCharm', 'VS Code'],
        'node_project': ['VS Code', 'WebStorm'],
        'rust_project': ['Fleet', 'VS Code', 'CLion'],
        'java_project': ['IntelliJ IDEA', 'Eclipse'],
        'go_project': ['GoLand', 'VS Code'],
        'docker_project': ['Docker Desktop', 'VS Code'],
    }
    
    def __init__(self):
        self.discovered_nodes: List[VaultNode] = []
        self.stats = defaultdict(int)
    
    def discover_nodes(
        self, 
        root: str, 
        depth: int = 3,
        exclude_patterns: Optional[List[str]] = None
    ) -> List[VaultNode]:
        """
        Recursively discover all vault-nodes starting from root.
        
        Args:
            root: Starting directory path
            depth: How deep to recurse
            exclude_patterns: Patterns to skip (e.g., 'node_modules', '.venv')
        
        Returns:
            List of discovered VaultNode objects
        """
        if exclude_patterns is None:
            exclude_patterns = [
                'node_modules', '.venv', 'venv', '__pycache__',
                '.next', 'dist', 'build', 'target', '.cache'
            ]
        
        root_path = Path(root).expanduser().resolve()
        print(f"🔍 Scanning from: {root_path}")
        print(f"📏 Max depth: {depth}")
        
        self._scan_directory(root_path, depth, exclude_patterns)
        
        print(f"\n✅ Discovery complete!")
        print(f"📊 Found {len(self.discovered_nodes)} vault-nodes")
        self._print_stats()
        
        return self.discovered_nodes
    
    def _scan_directory(
        self, 
        path: Path, 
        depth: int,
        exclude_patterns: List[str]
    ):
        """Recursively scan directory for vault-nodes"""
        if depth < 0:
            return
        
        if not path.is_dir():
            return
        
        # Check if this directory should be excluded
        if any(pattern in path.name for pattern in exclude_patterns):
            return
        
        # Check if this directory is a vault-node
        indicators = self._detect_indicators(path)
        if indicators:
            node = self._create_node(path, indicators)
            self.discovered_nodes.append(node)
            self.stats[node.node_type] += 1
            print(f"  💜 Found {node.node_type}: {node.name}")
        
        # Recurse into subdirectories
        try:
            for subdir in path.iterdir():
                if subdir.is_dir():
                    self._scan_directory(subdir, depth - 1, exclude_patterns)
        except PermissionError:
            pass  # Skip directories we can't access
    
    def _detect_indicators(self, path: Path) -> Dict[str, bool]:
        """Detect which indicators are present in this directory"""
        found_indicators = {}
        
        try:
            items = set(item.name for item in path.iterdir())
            
            for indicator_type, patterns in self.INDICATORS.items():
                for pattern in patterns:
                    if pattern in items or any(item.startswith(pattern.rstrip('*')) for item in items):
                        found_indicators[indicator_type] = True
                        break
        except PermissionError:
            pass
        
        return found_indicators
    
    def _create_node(self, path: Path, indicators: Dict[str, bool]) -> VaultNode:
        """Create a VaultNode from detected indicators"""
        # Classify node type
        node_type = self._classify_node(indicators)
        
        # Determine which tools would open this
        tools = set()
        for indicator_type in indicators.keys():
            tools.update(self.TOOL_MAP.get(indicator_type, []))
        
        # Calculate size and file count
        size_mb, file_count = self._calculate_size(path)
        
        # Get last modified time
        last_modified = self._get_last_modified(path)
        
        # Extract metadata
        metadata = self._extract_metadata(path, indicators)
        
        return VaultNode(
            path=str(path),
            name=path.name,
            node_type=node_type,
            indicators=list(indicators.keys()),
            tools=sorted(list(tools)),
            size_mb=size_mb,
            file_count=file_count,
            last_modified=last_modified,
            metadata=metadata
        )
    
    def _classify_node(self, indicators: Dict[str, bool]) -> str:
        """Classify the type of vault-node based on indicators"""
        has_git = 'git_repo' in indicators
        has_obsidian = 'obsidian_vault' in indicators
        has_code = any(k in indicators for k in [
            'python_project', 'node_project', 'rust_project',
            'java_project', 'go_project'
        ])
        has_ai = 'ai_config' in indicators
        
        if has_git and has_obsidian and has_code:
            return 'code_vault'  # The holy trinity
        elif has_git and has_code:
            return 'pure_repo'
        elif has_obsidian:
            return 'pure_vault'
        elif has_ai:
            return 'ai_dataset'
        elif len(indicators) > 2:
            return 'hybrid_project'
        else:
            return 'compute_node'
    
    def _calculate_size(self, path: Path) -> tuple[float, int]:
        """Calculate total size and file count"""
        total_size = 0
        file_count = 0
        
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
        except (PermissionError, OSError):
            pass
        
        return round(total_size / (1024 * 1024), 2), file_count
    
    def _get_last_modified(self, path: Path) -> str:
        """Get last modification time"""
        try:
            import datetime
            timestamp = path.stat().st_mtime
            return datetime.datetime.fromtimestamp(timestamp).isoformat()
        except Exception:
            return "unknown"
    
    def _extract_metadata(self, path: Path, indicators: Dict[str, bool]) -> Dict:
        """Extract additional metadata from the node"""
        metadata = {}
        
        # Try to read package.json if it exists
        if 'node_project' in indicators:
            package_json = path / 'package.json'
            if package_json.exists():
                try:
                    with open(package_json) as f:
                        data = json.load(f)
                        metadata['package_name'] = data.get('name', '')
                        metadata['version'] = data.get('version', '')
                except Exception:
                    pass
        
        # Try to read Cargo.toml if it exists
        if 'rust_project' in indicators:
            cargo_toml = path / 'Cargo.toml'
            if cargo_toml.exists():
                try:
                    # Simple TOML parsing for package name
                    with open(cargo_toml) as f:
                        for line in f:
                            if line.startswith('name'):
                                metadata['package_name'] = line.split('=')[1].strip().strip('"')
                                break
                except Exception:
                    pass
        
        # Check for README
        for readme_name in ['README.md', 'README.txt', 'README']:
            readme_path = path / readme_name
            if readme_path.exists():
                metadata['has_readme'] = True
                break
        
        return metadata
    
    def _print_stats(self):
        """Print statistics about discovered nodes"""
        print("\n📈 Node Type Distribution:")
        for node_type, count in sorted(self.stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {node_type:20} {count:4} nodes")
    
    def export_json(self, output_file: str):
        """Export discovered nodes to JSON"""
        output_path = Path(output_file).expanduser()
        
        data = {
            'metadata': {
                'total_nodes': len(self.discovered_nodes),
                'scan_timestamp': self._get_last_modified(Path('.')),
                'stats': dict(self.stats)
            },
            'nodes': [asdict(node) for node in self.discovered_nodes]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Exported to: {output_path}")
    
    def visualize_swarm(self, output_file: str = "cortex_graph.svg"):
        """Generate a visual graph of the vault-node swarm"""
        try:
            # Generate DOT format
            dot_content = self._generate_dot()
            
            # Write DOT file
            dot_file = output_file.replace('.svg', '.dot')
            with open(dot_file, 'w') as f:
                f.write(dot_content)
            
            # Try to render with Graphviz
            try:
                subprocess.run(['dot', '-Tsvg', dot_file, '-o', output_file], check=True)
                print(f"\n🎨 Visualization saved to: {output_file}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"\n⚠️  Graphviz not found. DOT file saved to: {dot_file}")
                print("   Install Graphviz to generate SVG: apt-get install graphviz")
        
        except Exception as e:
            print(f"\n❌ Visualization failed: {e}")
    
    def _generate_dot(self) -> str:
        """Generate Graphviz DOT format for the swarm"""
        lines = [
            'digraph VaultSwarm {',
            '  rankdir=LR;',
            '  node [shape=box, style=rounded];',
            '  ',
            '  // Node type color scheme',
        ]
        
        # Color scheme for node types
        colors = {
            'code_vault': '#9B59B6',      # Purple
            'pure_repo': '#3498DB',       # Blue
            'pure_vault': '#E74C3C',      # Red
            'hybrid_project': '#F39C12',  # Orange
            'ai_dataset': '#1ABC9C',      # Teal
            'compute_node': '#95A5A6'     # Gray
        }
        
        # Add nodes
        for i, node in enumerate(self.discovered_nodes):
            color = colors.get(node.node_type, '#95A5A6')
            label = f"{node.name}\\n({node.node_type})"
            lines.append(f'  node{i} [label="{label}", fillcolor="{color}", style="filled,rounded"];')
        
        # Add edges based on parent-child relationships
        path_to_index = {node.path: i for i, node in enumerate(self.discovered_nodes)}
        for i, node in enumerate(self.discovered_nodes):
            node_path = Path(node.path)
            parent_path = str(node_path.parent)
            if parent_path in path_to_index:
                parent_idx = path_to_index[parent_path]
                lines.append(f'  node{parent_idx} -> node{i};')
        
        lines.append('}')
        return '\n'.join(lines)
    
    def generate_report(self, output_file: str = "vault_map_report.md"):
        """Generate a markdown report of the discovery"""
        lines = [
            "# 🟪 Vault-Node Discovery Report",
            "",
            f"**Generated:** {self._get_last_modified(Path('.'))}",
            f"**Total Nodes:** {len(self.discovered_nodes)}",
            "",
            "## 📊 Statistics",
            "",
        ]
        
        # Add statistics table
        lines.append("| Node Type | Count | % of Total |")
        lines.append("|-----------|-------|------------|")
        total = len(self.discovered_nodes)
        for node_type, count in sorted(self.stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            lines.append(f"| {node_type} | {count} | {percentage:.1f}% |")
        
        lines.append("")
        lines.append("## 🗺️ Discovered Nodes")
        lines.append("")
        
        # Group nodes by type
        nodes_by_type = defaultdict(list)
        for node in self.discovered_nodes:
            nodes_by_type[node.node_type].append(node)
        
        for node_type, nodes in sorted(nodes_by_type.items()):
            lines.append(f"### {node_type.replace('_', ' ').title()}")
            lines.append("")
            
            for node in nodes:
                lines.append(f"**{node.name}**")
                lines.append(f"- Path: `{node.path}`")
                lines.append(f"- Size: {node.size_mb} MB ({node.file_count} files)")
                lines.append(f"- Tools: {', '.join(node.tools)}")
                lines.append(f"- Indicators: {', '.join(node.indicators)}")
                if node.metadata:
                    lines.append(f"- Metadata: {json.dumps(node.metadata, indent=2)}")
                lines.append("")
        
        # Write report
        output_path = Path(output_file).expanduser()
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"\n📄 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='DCM Vault Mapper - Discover and map your distributed cognition network'
    )
    parser.add_argument(
        '--scan',
        type=str,
        help='Root directory to scan (e.g., ~/ or ~/projects)'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='Maximum depth to recurse (default: 3)'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize vault mapping for current directory'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate visual graph of vault-nodes'
    )
    parser.add_argument(
        '--report',
        type=str,
        default='vault_map_report.md',
        help='Output file for markdown report'
    )
    parser.add_argument(
        '--json',
        type=str,
        help='Export nodes to JSON file'
    )
    
    args = parser.parse_args()
    
    mapper = VaultMapper()
    
    if args.init:
        # Scan current directory
        nodes = mapper.discover_nodes('.', depth=args.depth)
    elif args.scan:
        # Scan specified directory
        nodes = mapper.discover_nodes(args.scan, depth=args.depth)
    else:
        parser.print_help()
        return
    
    # Generate outputs
    if nodes:
        mapper.generate_report(args.report)
        
        if args.json:
            mapper.export_json(args.json)
        
        if args.visualize:
            mapper.visualize_swarm()


if __name__ == '__main__':
    main()
