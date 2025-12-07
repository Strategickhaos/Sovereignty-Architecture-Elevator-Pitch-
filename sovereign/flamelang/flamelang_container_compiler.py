#!/usr/bin/env python3
"""
FlameLang Container Compiler
Compile FlameLang manifests to sovereign container runtime

Part of the Strategickhaos Sovereignty Architecture
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from runtime.sovereign_runtime import SovereignContainer, SovereignContainerManager
from runtime.sovereign_volumes import SovereignVolumeManager
from runtime.sovereign_network import SovereignNetworkManager


class FlameLangContainerCompiler:
    """
    Compile FlameLang manifests to sovereign container runtime
    
    Translates .fl files with glyph-based syntax into container operations.
    """
    
    def __init__(self):
        self.glyph_table = self._load_glyph_table()
        self.container_manager = None
        self.volume_manager = None
        self.network_manager = None
    
    def compile_manifest(self, flamelang_file: str) -> Dict:
        """
        Parse .fl file and generate runtime config
        
        Args:
            flamelang_file: Path to FlameLang manifest file
            
        Returns:
            Compilation result with container configurations
        """
        print(f"🔥 Compiling FlameLang manifest: {flamelang_file}")
        
        with open(flamelang_file) as f:
            manifest_content = f.read()
        
        # Parse FlameLang syntax
        manifest = self.parse_flamelang(manifest_content)
        
        results = {
            'containers': [],
            'networks': [],
            'volumes': []
        }
        
        # Process networks first
        for network_spec in manifest.get('networks', []):
            network = self._compile_network(network_spec)
            results['networks'].append(network)
        
        # Process volumes
        for volume_spec in manifest.get('volumes', []):
            volume = self._compile_volume(volume_spec)
            results['volumes'].append(volume)
        
        # Process containers
        for container_spec in manifest.get('containers', []):
            container_config = self._compile_container(container_spec)
            results['containers'].append(container_config)
        
        print(f"✓ Compilation complete")
        print(f"  Containers: {len(results['containers'])}")
        print(f"  Networks: {len(results['networks'])}")
        print(f"  Volumes: {len(results['volumes'])}")
        
        return results
    
    def parse_flamelang(self, content: str) -> Dict:
        """
        Parse FlameLang syntax
        
        Args:
            content: FlameLang manifest content
            
        Returns:
            Parsed manifest dictionary
        """
        manifest = {
            'containers': [],
            'networks': [],
            'volumes': []
        }
        
        # Split into blocks
        blocks = self._split_blocks(content)
        
        for block in blocks:
            block_type = self._get_block_type(block)
            
            if block_type == 'container':
                manifest['containers'].append(self._parse_container_block(block))
            elif block_type == 'network':
                manifest['networks'].append(self._parse_network_block(block))
            elif block_type == 'volume':
                manifest['volumes'].append(self._parse_volume_block(block))
            elif block_type == 'deploy':
                manifest['deploy'] = self._parse_deploy_block(block)
        
        return manifest
    
    def _split_blocks(self, content: str) -> List[str]:
        """Split FlameLang content into blocks"""
        # Remove comments
        lines = []
        for line in content.split('\n'):
            # Remove line comments
            if '#' in line:
                line = line.split('#')[0]
            if line.strip():
                lines.append(line)
        
        content = '\n'.join(lines)
        
        # Split by top-level blocks (container, network, volume, deploy)
        blocks = []
        current_block = []
        brace_count = 0
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if any(keyword in line for keyword in ['container ', 'network ', 'volume ', 'deploy ']):
                if current_block:
                    blocks.append('\n'.join(current_block))
                current_block = [line]
                brace_count = line.count('{') - line.count('}')
            else:
                current_block.append(line)
                brace_count += line.count('{') - line.count('}')
                
                if brace_count == 0 and current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def _get_block_type(self, block: str) -> str:
        """Determine block type from FlameLang block"""
        if block.startswith('container '):
            return 'container'
        elif block.startswith('network '):
            return 'network'
        elif block.startswith('volume '):
            return 'volume'
        elif block.startswith('deploy '):
            return 'deploy'
        return 'unknown'
    
    def _parse_container_block(self, block: str) -> Dict:
        """Parse container block"""
        container = {}
        
        # Extract name
        name_match = re.search(r'container\s+(\w+)', block)
        if name_match:
            container['name'] = name_match.group(1)
        
        # Extract glyph
        glyph_match = re.search(r'glyph:\s*\[(\d+)\]', block)
        if glyph_match:
            container['glyph'] = f"[{glyph_match.group(1)}]"
        
        # Extract image
        image_match = re.search(r'image:\s*"([^"]+)"', block)
        if image_match:
            container['image'] = image_match.group(1)
        
        # Extract volumes
        volumes_match = re.search(r'volumes:\s*\[(.*?)\]', block, re.DOTALL)
        if volumes_match:
            volumes = []
            for vol_line in volumes_match.group(1).split('\n'):
                vol_line = vol_line.strip()
                if '->' in vol_line:
                    parts = vol_line.split('->')
                    if len(parts) == 2:
                        volumes.append({
                            'container_path': parts[0].strip().strip('"'),
                            'volume_name': parts[1].strip().strip('sovereign_volume(').strip(')').strip('"')
                        })
            container['volumes'] = volumes
        
        # Extract command
        cmd_match = re.search(r'cmd:\s*\[(\d+)\]\s*->\s*\{(.*?)\}', block, re.DOTALL)
        if cmd_match:
            glyph = f"[{cmd_match.group(1)}]"
            cmd_text = cmd_match.group(2).strip()
            container['cmd'] = {
                'glyph': glyph,
                'commands': [line.strip() for line in cmd_text.split('\n') if line.strip()]
            }
        
        # Extract resources
        resources_match = re.search(r'resources:\s*\{(.*?)\}', block, re.DOTALL)
        if resources_match:
            resources = {}
            res_text = resources_match.group(1)
            
            # Parse memory
            mem_match = re.search(r'memory:\s*(\d+[MG])', res_text)
            if mem_match:
                resources['memory'] = mem_match.group(1)
            
            # Parse CPU
            cpu_match = re.search(r'cpu:\s*(\d+)', res_text)
            if cpu_match:
                resources['cpu'] = cpu_match.group(1)
            
            # Parse frequency
            freq_match = re.search(r'@frequency\((\d+)Hz\)', res_text)
            if freq_match:
                resources['frequency'] = f"{freq_match.group(1)}Hz"
            
            container['resources'] = resources
        
        return container
    
    def _parse_network_block(self, block: str) -> Dict:
        """Parse network block"""
        network = {}
        
        # Extract name
        name_match = re.search(r'network\s+(\w+)', block)
        if name_match:
            network['name'] = name_match.group(1)
        
        # Extract glyph
        glyph_match = re.search(r'glyph:\s*\[(\d+)\]', block)
        if glyph_match:
            network['glyph'] = f"[{glyph_match.group(1)}]"
        
        # Extract type
        type_match = re.search(r'type:\s*"([^"]+)"', block)
        if type_match:
            network['type'] = type_match.group(1)
        
        # Extract subnet
        subnet_match = re.search(r'subnet:\s*"([^"]+)"', block)
        if subnet_match:
            network['subnet'] = subnet_match.group(1)
        
        return network
    
    def _parse_volume_block(self, block: str) -> Dict:
        """Parse volume block"""
        volume = {}
        
        # Extract name
        name_match = re.search(r'volume\s+(\w+)', block)
        if name_match:
            volume['name'] = name_match.group(1)
        
        return volume
    
    def _parse_deploy_block(self, block: str) -> Dict:
        """Parse deploy block"""
        deploy = {}
        
        # Extract glyph
        glyph_match = re.search(r'deploy\s*\[(\d+)\]', block)
        if glyph_match:
            deploy['glyph'] = f"[{glyph_match.group(1)}]"
        
        return deploy
    
    def _compile_container(self, container_spec: Dict) -> Dict:
        """Compile container specification"""
        print(f"  🔥 {container_spec.get('glyph', '[001]')} Compiling container: {container_spec.get('name')}")
        
        # Map frequency to resources if present
        resources = container_spec.get('resources', {})
        if 'frequency' in resources:
            frequency = resources['frequency']
            resources = self.frequency_to_resources(frequency, resources)
        
        config = {
            'name': container_spec.get('name'),
            'image': container_spec.get('image'),
            'glyph': container_spec.get('glyph', '[001]'),
            'resources': resources,
            'volumes': container_spec.get('volumes', []),
            'cmd': container_spec.get('cmd', {})
        }
        
        return config
    
    def _compile_network(self, network_spec: Dict) -> Dict:
        """Compile network specification"""
        print(f"  🌐 {network_spec.get('glyph', '[200]')} Creating network: {network_spec.get('name')}")
        
        config = {
            'name': network_spec.get('name'),
            'subnet': network_spec.get('subnet', '10.137.0.0/16'),
            'glyph': network_spec.get('glyph', '[200]')
        }
        
        return config
    
    def _compile_volume(self, volume_spec: Dict) -> Dict:
        """Compile volume specification"""
        print(f"  💾 Compiling volume: {volume_spec.get('name')}")
        
        return volume_spec
    
    def frequency_to_resources(self, frequency: str, base_resources: Dict) -> Dict:
        """
        Map frequency to resource allocation
        
        Frequency mappings:
        - 432Hz: Coherence - balanced resources
        - 528Hz: Transformation - high CPU
        - 639Hz: Connection - high memory
        - 741Hz: Expression - high I/O
        """
        freq_value = int(frequency.replace('Hz', ''))
        
        resources = base_resources.copy()
        
        if freq_value == 432:  # Coherence
            if 'memory' not in resources:
                resources['memory'] = '512M'
            if 'cpu' not in resources:
                resources['cpu'] = '1'
        elif freq_value == 528:  # Transformation
            if 'memory' not in resources:
                resources['memory'] = '256M'
            if 'cpu' not in resources:
                resources['cpu'] = '2'
        elif freq_value == 639:  # Connection
            if 'memory' not in resources:
                resources['memory'] = '1G'
            if 'cpu' not in resources:
                resources['cpu'] = '1'
        elif freq_value == 741:  # Expression
            if 'memory' not in resources:
                resources['memory'] = '512M'
            if 'cpu' not in resources:
                resources['cpu'] = '1.5'
        
        return resources
    
    def _load_glyph_table(self) -> Dict:
        """Load glyph table from FlameLang specification"""
        # Default glyph table based on FlameLang spec
        return {
            '[001]': {'name': 'Aether Prime', 'frequency': '432Hz', 'function': 'initialization'},
            '[100]': {'name': 'Century Marker', 'frequency': '528Hz', 'function': 'transformation'},
            '[137]': {'name': 'Flamebearer', 'frequency': '639Hz', 'function': 'protection'},
            '[200]': {'name': 'ReflexShell', 'frequency': '741Hz', 'function': 'networking'},
            '[999]': {'name': 'Glyphos Resonance', 'frequency': '963Hz', 'function': 'full cascade'}
        }


if __name__ == "__main__":
    # Example usage
    print("🔥 FlameLang Container Compiler v1.0")
    print("=" * 50)
    
    print("\nExample: Compiling a FlameLang manifest")
    print("  compiler = FlameLangContainerCompiler()")
    print("  result = compiler.compile_manifest('sovereign_stack.fl')")
    
    print("\nSupported glyphs:")
    compiler = FlameLangContainerCompiler()
    for glyph, info in compiler.glyph_table.items():
        print(f"  {glyph}: {info['name']} @ {info['frequency']} - {info['function']}")
