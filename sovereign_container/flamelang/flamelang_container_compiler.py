#!/usr/bin/env python3
"""
FlameLang Container Compiler
Compile FlameLang manifests to sovereign container runtime

This bridges FlameLang with the sovereign container platform:
- Parse .fl files
- Map glyphs to container operations
- Translate frequencies to resource allocation
- Generate sovereign runtime configurations
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FlameLang Glyph Table - maps glyphs to their properties
GLYPH_TABLE = {
    '[001]': {
        'name': 'Aether Prime',
        'frequency': 432,  # Hz - Coherence
        'domain': 'initialization',
        'properties': ['create', 'begin', 'genesis']
    },
    '[100]': {
        'name': 'Resonance Core',
        'frequency': 528,  # Hz - Transformation
        'domain': 'execution',
        'properties': ['transform', 'execute', 'process']
    },
    '[137]': {
        'name': 'Flamebearer',
        'frequency': 639,  # Hz - Connection/Protection
        'domain': 'protection',
        'properties': ['protect', 'shield', 'defend']
    },
    '[200]': {
        'name': 'ReflexShell',
        'frequency': 741,  # Hz - Expression
        'domain': 'networking',
        'properties': ['connect', 'network', 'communicate']
    },
    '[999]': {
        'name': 'Glyphos Resonance',
        'frequency': 963,  # Hz - Activation
        'domain': 'orchestration',
        'properties': ['deploy', 'cascade', 'activate']
    }
}


class FlameLangContainerCompiler:
    """
    Compiler for FlameLang container manifests
    """
    
    def __init__(self):
        """Initialize FlameLang compiler"""
        self.glyph_table = GLYPH_TABLE
        
    def parse_flamelang(self, content: str) -> Dict:
        """
        Parse FlameLang manifest content
        
        Args:
            content: FlameLang manifest as string
            
        Returns:
            Parsed manifest structure
        """
        logger.info("Parsing FlameLang manifest")
        
        manifest = {
            'containers': [],
            'networks': [],
            'volumes': [],
            'deploy_commands': []
        }
        
        # Parse container definitions
        container_pattern = r'container\s+(\w+)\s*{([^}]+)}'
        for match in re.finditer(container_pattern, content):
            container_name = match.group(1)
            container_body = match.group(2)
            
            container = self._parse_container(container_name, container_body)
            manifest['containers'].append(container)
        
        # Parse network definitions
        network_pattern = r'network\s+(\w+)\s*{([^}]+)}'
        for match in re.finditer(network_pattern, content):
            network_name = match.group(1)
            network_body = match.group(2)
            
            network = self._parse_network(network_name, network_body)
            manifest['networks'].append(network)
        
        # Parse deploy commands
        deploy_pattern = r'deploy\s+(\[\d+\])'
        for match in re.finditer(deploy_pattern, content):
            glyph = match.group(1)
            manifest['deploy_commands'].append(glyph)
        
        logger.info(f"Parsed {len(manifest['containers'])} containers, {len(manifest['networks'])} networks")
        return manifest
    
    def _parse_container(self, name: str, body: str) -> Dict:
        """Parse container definition"""
        container = {
            'name': name,
            'glyph': None,
            'image': None,
            'volumes': [],
            'resources': {},
            'network': None,
            'command': []
        }
        
        # Parse glyph
        glyph_match = re.search(r'glyph:\s*(\[\d+\])', body)
        if glyph_match:
            container['glyph'] = glyph_match.group(1)
        
        # Parse image
        image_match = re.search(r'image:\s*"([^"]+)"', body)
        if image_match:
            container['image'] = image_match.group(1)
        
        # Parse volumes
        volumes_match = re.search(r'volumes:\s*\[([^\]]+)\]', body)
        if volumes_match:
            volumes_str = volumes_match.group(1)
            # Parse volume mappings like "/love" -> sovereign_volume("eternal_love")
            vol_pattern = r'"([^"]+)"\s*->\s*sovereign_volume\("([^"]+)"\)'
            for vol_match in re.finditer(vol_pattern, volumes_str):
                container['volumes'].append({
                    'container_path': vol_match.group(1),
                    'volume_name': vol_match.group(2)
                })
        
        # Parse command
        cmd_match = re.search(r'cmd:\s*(\[\d+\])\s*->\s*{([^}]+)}', body, re.DOTALL)
        if cmd_match:
            glyph = cmd_match.group(1)
            commands = cmd_match.group(2).strip().split('\n')
            container['command'] = [cmd.strip() for cmd in commands if cmd.strip()]
            container['cmd_glyph'] = glyph
        
        # Parse resources
        resources_match = re.search(r'resources:\s*{([^}]+)}', body, re.DOTALL)
        if resources_match:
            resources_str = resources_match.group(1)
            
            # Parse memory
            memory_match = re.search(r'memory:\s*(\w+)\s*@frequency\((\d+)Hz\)', resources_str)
            if memory_match:
                container['resources']['memory'] = memory_match.group(1)
                container['resources']['memory_frequency'] = int(memory_match.group(2))
            
            # Parse CPU
            cpu_match = re.search(r'cpu:\s*([\d.]+)\s*@frequency\((\d+)Hz\)', resources_str)
            if cpu_match:
                container['resources']['cpu'] = cpu_match.group(1)
                container['resources']['cpu_frequency'] = int(cpu_match.group(2))
        
        return container
    
    def _parse_network(self, name: str, body: str) -> Dict:
        """Parse network definition"""
        network = {
            'name': name,
            'glyph': None,
            'type': 'bridge',
            'subnet': None
        }
        
        # Parse glyph
        glyph_match = re.search(r'glyph:\s*(\[\d+\])', body)
        if glyph_match:
            network['glyph'] = glyph_match.group(1)
        
        # Parse type
        type_match = re.search(r'type:\s*"([^"]+)"', body)
        if type_match:
            network['type'] = type_match.group(1)
        
        # Parse subnet
        subnet_match = re.search(r'subnet:\s*"([^"]+)"', body)
        if subnet_match:
            network['subnet'] = subnet_match.group(1)
        
        return network
    
    def frequency_to_resources(self, frequency: int) -> Dict:
        """
        Map frequency to resource allocation
        
        FlameLang uses frequencies to encode resource requirements:
        - 432Hz (Coherence) = Balanced resources
        - 528Hz (Transformation) = High compute
        - 639Hz (Connection) = High network
        - 741Hz (Expression) = High I/O
        - 963Hz (Activation) = Maximum resources
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Resource configuration
        """
        if frequency == 432:
            return {'memory': '512M', 'cpu': '1', 'network_priority': 'normal'}
        elif frequency == 528:
            return {'memory': '1G', 'cpu': '2', 'network_priority': 'normal'}
        elif frequency == 639:
            return {'memory': '512M', 'cpu': '1', 'network_priority': 'high'}
        elif frequency == 741:
            return {'memory': '1G', 'cpu': '1', 'network_priority': 'high', 'io_priority': 'high'}
        elif frequency == 963:
            return {'memory': '2G', 'cpu': '4', 'network_priority': 'high', 'io_priority': 'high'}
        else:
            # Default resources
            return {'memory': '256M', 'cpu': '0.5', 'network_priority': 'normal'}
    
    def compile_manifest(self, flamelang_file: str) -> Dict:
        """
        Compile FlameLang manifest to sovereign runtime config
        
        Args:
            flamelang_file: Path to .fl file
            
        Returns:
            Sovereign runtime configuration
        """
        logger.info(f"Compiling FlameLang manifest: {flamelang_file}")
        
        with open(flamelang_file, 'r') as f:
            content = f.read()
        
        # Parse FlameLang
        manifest = self.parse_flamelang(content)
        
        # Generate sovereign runtime configs
        runtime_config = {
            'containers': [],
            'networks': [],
            'volumes': []
        }
        
        # Process containers
        for container in manifest['containers']:
            # Get glyph properties
            glyph = container.get('glyph')
            if glyph and glyph in self.glyph_table:
                glyph_info = self.glyph_table[glyph]
                frequency = glyph_info['frequency']
                
                # Map frequency to resources
                resources = self.frequency_to_resources(frequency)
                
                # Override with explicit resources if provided
                if container.get('resources'):
                    resources.update(container['resources'])
            else:
                resources = container.get('resources', {})
            
            # Build runtime config for container
            container_config = {
                'name': container['name'],
                'image': container.get('image'),
                'glyph': glyph,
                'frequency': self.glyph_table.get(glyph, {}).get('frequency', 432) if glyph else 432,
                'resources': resources,
                'volumes': container.get('volumes', []),
                'command': container.get('command', []),
                'network': container.get('network')
            }
            
            runtime_config['containers'].append(container_config)
        
        # Process networks
        for network in manifest['networks']:
            network_config = {
                'name': network['name'],
                'type': network.get('type', 'bridge'),
                'subnet': network.get('subnet', '10.137.0.0/16'),
                'glyph': network.get('glyph')
            }
            runtime_config['networks'].append(network_config)
        
        logger.info(f"Compilation complete: {len(runtime_config['containers'])} containers configured")
        return runtime_config
    
    def execute_runtime_config(self, runtime_config: Dict):
        """
        Execute compiled runtime configuration
        
        This would integrate with sovereign_runtime.py to actually start containers
        
        Args:
            runtime_config: Compiled runtime configuration
        """
        logger.info("Executing sovereign runtime configuration")
        
        # This would call into sovereign_runtime.py, sovereign_network.py, etc.
        # For now, we just log the configuration
        
        for network in runtime_config['networks']:
            logger.info(f"[Network] {network['name']}: {network['subnet']}")
        
        for container in runtime_config['containers']:
            glyph = container.get('glyph', 'N/A')
            frequency = container.get('frequency', 432)
            logger.info(f"[Container] {container['name']}")
            logger.info(f"  Glyph: {glyph} @ {frequency}Hz")
            logger.info(f"  Resources: {container['resources']}")
            logger.info(f"  Volumes: {len(container['volumes'])}")


def load_glyph_table() -> Dict:
    """Load glyph table (for external use)"""
    return GLYPH_TABLE


if __name__ == "__main__":
    print("🔥 FlameLang Container Compiler - Phase 2")
    print("=" * 50)
    
    compiler = FlameLangContainerCompiler()
    print("Compiler initialized")
    print(f"Loaded {len(compiler.glyph_table)} glyphs")
