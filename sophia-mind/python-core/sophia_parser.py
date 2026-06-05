#!/usr/bin/env python3
"""
SOPHIA MIND Brain Visualizer - Markdown Parser
Parse Obsidian-style markdown with FlameLang extensions

Part of the Strategickhaos Sovereignty Architecture
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional


class SophiaParser:
    """Parse Obsidian-compatible markdown files with FlameLang glyph support"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.nodes: Dict[str, Dict] = {}
        self.connections: List[Dict] = []
        
    def parse_vault(self) -> Dict:
        """Parse all .md files in vault"""
        for md_file in self.vault_path.glob("**/*.md"):
            try:
                node = self.parse_file(md_file)
                self.nodes[node['id']] = node
            except Exception as e:
                print(f"Warning: Failed to parse {md_file}: {e}")
                
        return {
            'nodes': list(self.nodes.values()),
            'node_count': len(self.nodes)
        }
        
    def parse_file(self, filepath: Path) -> Dict:
        """Parse single markdown file"""
        content = filepath.read_text(encoding='utf-8')
        
        # Extract YAML frontmatter
        frontmatter = {}
        body = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                except yaml.YAMLError as e:
                    print(f"Warning: Invalid YAML in {filepath}: {e}")
        
        # Extract wiki links [[target]] or [[target|alias]]
        links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', body)
        
        # Extract FlameLang glyph tags #[FL1] or glyph: FL1
        glyphs = re.findall(r'#?\[([A-Z]{2}\d+)\]', body)
        if 'glyph' in frontmatter:
            glyphs.append(frontmatter['glyph'])
        if 'glyphs' in frontmatter:
            if isinstance(frontmatter['glyphs'], list):
                glyphs.extend(frontmatter['glyphs'])
            else:
                glyphs.append(frontmatter['glyphs'])
            
        # Get frequency from frontmatter or glyph lookup
        frequency = frontmatter.get('frequency', self.glyph_to_frequency(glyphs))
        
        return {
            'id': filepath.stem,
            'title': frontmatter.get('title', filepath.stem),
            'path': str(filepath.relative_to(self.vault_path)),
            'glyphs': list(set(glyphs)),  # Remove duplicates
            'frequency': frequency,
            'connections': links,
            'tags': frontmatter.get('tags', []),
            'frontmatter': frontmatter
        }
        
    def glyph_to_frequency(self, glyphs: List[str]) -> int:
        """Map FlameLang glyph codes to Solfeggio frequencies"""
        glyph_freq = {
            # Aegis Engine - Coherence (432Hz base)
            'AE1': 432, 'AE2': 440, 'AE3': 444,
            
            # FlameLang - Transformation (528Hz)
            'FL1': 528, 'FL2': 532, 'FL3': 536,
            
            # Recon/Research - Connection (639Hz)
            'RC1': 639, 'RC2': 643, 'RC3': 647,
            
            # Athena - Oneness/Strategy (963Hz)
            'AT1': 963, 'AT2': 967, 'AT3': 971,
            
            # Flamebearer - Expression/Defense (741Hz)
            'FB1': 741, 'FB2': 745, 'FB3': 749,
            
            # Genesis/Grok - Creation (999Hz)
            'GR1': 999, 'GR2': 1001, 'GR3': 1003,
            
            # Lyra - Harmony (852Hz)
            'LY1': 852, 'LY2': 856, 'LY3': 860,
        }
        
        for g in glyphs:
            if g in glyph_freq:
                return glyph_freq[g]
        
        # Default to 432Hz - coherence frequency
        return 432
        
    def export_to_unity(self, output_path: str) -> None:
        """Export graph data for Unity consumption as JSON"""
        
        # Create edges from connections
        edges = []
        for src_id, node in self.nodes.items():
            for target in node['connections']:
                # Clean target link (remove aliases)
                target_clean = target.strip()
                if target_clean in self.nodes:
                    edges.append({
                        'source': src_id,
                        'target': target_clean
                    })
        
        unity_data = {
            'metadata': {
                'vault_path': str(self.vault_path),
                'node_count': len(self.nodes),
                'edge_count': len(edges),
                'export_version': '1.0'
            },
            'nodes': list(self.nodes.values()),
            'edges': edges
        }
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(unity_data, indent=2, ensure_ascii=False))
        
        print(f"✅ Exported {len(self.nodes)} nodes and {len(edges)} edges to {output_path}")
        
    def get_statistics(self) -> Dict:
        """Get vault statistics"""
        glyph_counts = {}
        for node in self.nodes.values():
            for glyph in node['glyphs']:
                glyph_counts[glyph] = glyph_counts.get(glyph, 0) + 1
                
        return {
            'total_nodes': len(self.nodes),
            'glyph_distribution': glyph_counts,
            'most_connected': self._get_most_connected(5)
        }
        
    def _get_most_connected(self, limit: int = 5) -> List[Dict]:
        """Get nodes with most connections"""
        node_connections = [
            {
                'id': node['id'],
                'title': node['title'],
                'connection_count': len(node['connections'])
            }
            for node in self.nodes.values()
        ]
        
        return sorted(node_connections, key=lambda x: x['connection_count'], reverse=True)[:limit]


def main():
    """CLI interface for SOPHIA parser"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python sophia_parser.py <vault_path> <output_json>")
        print("Example: python sophia_parser.py ~/ObsidianVault ./graph_data.json")
        sys.exit(1)
        
    vault_path = sys.argv[1]
    output_path = sys.argv[2]
    
    print(f"🧠 SOPHIA MIND Parser - Strategickhaos Brain Visualizer")
    print(f"📂 Parsing vault: {vault_path}")
    
    parser = SophiaParser(vault_path)
    result = parser.parse_vault()
    
    print(f"✅ Parsed {result['node_count']} nodes")
    
    # Export to Unity format
    parser.export_to_unity(output_path)
    
    # Print statistics
    stats = parser.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total nodes: {stats['total_nodes']}")
    print(f"   Glyph types: {len(stats['glyph_distribution'])}")
    print(f"\n🔗 Most connected nodes:")
    for node in stats['most_connected']:
        print(f"   - {node['title']}: {node['connection_count']} connections")


if __name__ == '__main__':
    main()
