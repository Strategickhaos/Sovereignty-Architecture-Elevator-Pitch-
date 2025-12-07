#!/usr/bin/env python3
"""
FlameLang Container Compiler - Compile FlameLang manifests to sovereign container runtime
Integrates FlameLang glyph-based orchestration with sovereign containers

Part of the Sovereignty Architecture - Phase 2 Implementation
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GlyphTable:
    """
    FlameLang Glyph Mapping Table
    Maps glyphs to frequencies and container operations
    """
    
    GLYPHS = {
        "[001]": {
            "name": "Aether Prime",
            "frequency": "432Hz",
            "domain": "initialization",
            "description": "Container initialization and birth"
        },
        "[100]": {
            "name": "Compiler Core",
            "frequency": "528Hz",
            "domain": "transformation",
            "description": "Code compilation and transformation"
        },
        "[137]": {
            "name": "Flamebearer",
            "frequency": "528Hz",
            "domain": "protection",
            "description": "Security protocols and defense"
        },
        "[200]": {
            "name": "ReflexShell",
            "frequency": "432Hz",
            "domain": "networking",
            "description": "Network connectivity and communication"
        },
        "[999]": {
            "name": "Glyphos Resonance",
            "frequency": "963Hz",
            "domain": "cascade",
            "description": "Full system deployment cascade"
        }
    }
    
    @classmethod
    def get_glyph(cls, glyph_code: str) -> Optional[Dict]:
        """Get glyph information"""
        return cls.GLYPHS.get(glyph_code)
        
    @classmethod
    def get_frequency(cls, glyph_code: str) -> Optional[str]:
        """Get glyph frequency"""
        glyph = cls.get_glyph(glyph_code)
        return glyph["frequency"] if glyph else None
        
    @classmethod
    def list_glyphs(cls) -> List[Dict]:
        """List all available glyphs"""
        return [
            {"code": code, **info}
            for code, info in cls.GLYPHS.items()
        ]


class FlameLangContainerCompiler:
    """
    FlameLang Compiler for Container Orchestration
    Parses .fl manifests and generates sovereign runtime configurations
    """
    
    def __init__(self):
        self.glyph_table = GlyphTable()
        
    def compile_manifest(self, flamelang_file: str) -> Dict[str, Any]:
        """
        Parse .fl file and generate runtime config
        
        Args:
            flamelang_file: Path to FlameLang manifest file
            
        Returns:
            Compiled runtime configuration
        """
        logger.info(f"Compiling FlameLang manifest: {flamelang_file}")
        
        with open(flamelang_file, 'r') as f:
            content = f.read()
            
        # Parse FlameLang syntax
        manifest = self.parse_flamelang(content)
        
        # Generate runtime configurations
        runtime_configs = []
        
        for container in manifest.get('containers', []):
            config = self._compile_container(container)
            runtime_configs.append(config)
            
        # Handle network definitions
        networks = []
        for network in manifest.get('networks', []):
            net_config = self._compile_network(network)
            networks.append(net_config)
            
        # Handle deployment commands
        deployment = manifest.get('deployment', {})
        
        return {
            "containers": runtime_configs,
            "networks": networks,
            "deployment": deployment
        }
        
    def parse_flamelang(self, content: str) -> Dict[str, Any]:
        """
        Parse FlameLang manifest syntax
        
        Returns:
            Parsed manifest structure
        """
        manifest = {
            "containers": [],
            "networks": [],
            "deployment": {}
        }
        
        # Parse containers
        container_blocks = re.finditer(
            r'container\s+(\w+)\s*\{([^}]+)\}',
            content,
            re.MULTILINE | re.DOTALL
        )
        
        for match in container_blocks:
            name = match.group(1)
            body = match.group(2)
            container = self._parse_container_block(name, body)
            manifest["containers"].append(container)
            
        # Parse networks
        network_blocks = re.finditer(
            r'network\s+(\w+)\s*\{([^}]+)\}',
            content,
            re.MULTILINE | re.DOTALL
        )
        
        for match in network_blocks:
            name = match.group(1)
            body = match.group(2)
            network = self._parse_network_block(name, body)
            manifest["networks"].append(network)
            
        # Parse deployment command
        deploy_match = re.search(r'deploy\s+(\[\d+\])', content)
        if deploy_match:
            manifest["deployment"] = {
                "glyph": deploy_match.group(1),
                "mode": "cascade" if deploy_match.group(1) == "[999]" else "single"
            }
            
        return manifest
        
    def _parse_container_block(self, name: str, body: str) -> Dict:
        """Parse container definition block"""
        container = {"name": name}
        
        # Parse glyph
        glyph_match = re.search(r'glyph:\s*(\[\d+\])', body)
        if glyph_match:
            container["glyph"] = glyph_match.group(1)
            
        # Parse image
        image_match = re.search(r'image:\s*"([^"]+)"', body)
        if image_match:
            container["image"] = image_match.group(1)
            
        # Parse volumes
        volumes_match = re.search(r'volumes:\s*\[([^\]]+)\]', body)
        if volumes_match:
            volumes_str = volumes_match.group(1)
            volumes = []
            for vol in re.finditer(r'"([^"]+)"\s*->\s*sovereign_volume\("([^"]+)"\)', volumes_str):
                volumes.append({
                    "container_path": vol.group(1),
                    "volume_name": vol.group(2)
                })
            container["volumes"] = volumes
            
        # Parse command
        cmd_match = re.search(r'cmd:\s*(\[\d+\])\s*->\s*\{([^}]+)\}', body, re.DOTALL)
        if cmd_match:
            container["cmd_glyph"] = cmd_match.group(1)
            container["cmd"] = cmd_match.group(2).strip()
            
        # Parse resources
        resources_match = re.search(r'resources:\s*\{([^}]+)\}', body, re.DOTALL)
        if resources_match:
            resources_body = resources_match.group(1)
            resources = {}
            
            # Parse memory
            mem_match = re.search(r'memory:\s*(\S+)', resources_body)
            if mem_match:
                resources["memory"] = mem_match.group(1).split('@')[0].strip()
                
            # Parse CPU
            cpu_match = re.search(r'cpu:\s*(\S+)', resources_body)
            if cpu_match:
                resources["cpu"] = cpu_match.group(1).split('@')[0].strip()
                
            container["resources"] = resources
            
        return container
        
    def _parse_network_block(self, name: str, body: str) -> Dict:
        """Parse network definition block"""
        network = {"name": name}
        
        # Parse glyph
        glyph_match = re.search(r'glyph:\s*(\[\d+\])', body)
        if glyph_match:
            network["glyph"] = glyph_match.group(1)
            
        # Parse type
        type_match = re.search(r'type:\s*"([^"]+)"', body)
        if type_match:
            network["type"] = type_match.group(1)
            
        # Parse subnet
        subnet_match = re.search(r'subnet:\s*"([^"]+)"', body)
        if subnet_match:
            network["subnet"] = subnet_match.group(1)
            
        return network
        
    def _compile_container(self, container: Dict) -> Dict:
        """
        Compile container definition to runtime config
        
        Args:
            container: Parsed container definition
            
        Returns:
            Runtime configuration
        """
        glyph = container.get("glyph", "[001]")
        frequency = self.glyph_table.get_frequency(glyph)
        
        # Map frequency to resource allocation
        resources = self.frequency_to_resources(
            frequency,
            container.get("resources", {})
        )
        
        # Generate sovereign runtime config
        runtime_config = {
            "name": container["name"],
            "glyph": glyph,
            "frequency": frequency,
            "image": container.get("image", "alpine:latest"),
            "resources": resources,
            "volumes": container.get("volumes", []),
            "network": "default",
            "command": self._parse_command(container.get("cmd", ""))
        }
        
        return runtime_config
        
    def _compile_network(self, network: Dict) -> Dict:
        """Compile network definition to runtime config"""
        glyph = network.get("glyph", "[200]")
        
        return {
            "name": network["name"],
            "glyph": glyph,
            "type": network.get("type", "bridge"),
            "subnet": network.get("subnet", "10.137.0.0/16")
        }
        
    def frequency_to_resources(self, frequency: str, overrides: Dict) -> Dict:
        """
        Map glyph frequency to resource allocation
        
        Args:
            frequency: Frequency string (e.g., "432Hz")
            overrides: Manual resource overrides
            
        Returns:
            Resource configuration
        """
        # Default resource mapping based on frequency
        frequency_map = {
            "432Hz": {"memory": "512M", "cpu": "1"},      # Coherence - balanced
            "528Hz": {"memory": "1G", "cpu": "2"},        # Transformation - more power
            "963Hz": {"memory": "2G", "cpu": "4"}         # Cascade - maximum
        }
        
        resources = frequency_map.get(frequency, {"memory": "256M", "cpu": "0.5"})
        
        # Apply overrides
        resources.update(overrides)
        
        return resources
        
    def _parse_command(self, cmd_str: str) -> List[str]:
        """Parse command string to list"""
        if not cmd_str:
            return ["/bin/sh"]
            
        # Split by newlines and filter empty
        commands = [line.strip() for line in cmd_str.split('\n') if line.strip()]
        
        if len(commands) == 1:
            return ["sh", "-c", commands[0]]
        else:
            # Multiple commands - join with &&
            full_cmd = " && ".join(commands)
            return ["sh", "-c", full_cmd]
            
    def execute_deployment(self, runtime_config: Dict) -> None:
        """
        Execute deployment based on compiled config
        
        Args:
            runtime_config: Compiled runtime configuration
        """
        from sovereign_runtime import SovereignContainer
        from sovereign_network import SovereignNetworkManager
        from sovereign_volumes import SovereignVolumeManager
        
        logger.info("Executing FlameLang deployment")
        
        # Create networks
        net_manager = SovereignNetworkManager()
        for network_config in runtime_config.get("networks", []):
            logger.info(f"Creating network: {network_config['name']}")
            # In production, create actual network
            
        # Create volumes
        vol_manager = SovereignVolumeManager()
        
        # Deploy containers
        for container_config in runtime_config.get("containers", []):
            glyph = container_config["glyph"]
            logger.info(f"[{glyph}] Deploying container: {container_config['name']}")
            
            # Create volumes for container
            for vol in container_config.get("volumes", []):
                vol_name = vol["volume_name"]
                if not vol_manager.get_volume(vol_name):
                    vol_manager.create_volume(vol_name)
                    
            # In production, start container with SovereignContainer
            logger.info(f"Container {container_config['name']} ready")
            
        deployment = runtime_config.get("deployment", {})
        if deployment.get("glyph") == "[999]":
            logger.info("🔥 [999] Full Resonance Cascade Activated ⚔️🖤")


def create_example_manifest():
    """Create an example FlameLang manifest"""
    manifest = '''# sovereign_stack.fl
# FlameLang manifest for sovereign container orchestration

# Define container with FlameLang glyphs
container DOMandGrokLoveForever {
    glyph: [001]          # Aether Prime - initialization
    image: "alpine:latest"
    
    # FlameLang volume syntax
    volumes: [
        "/love" -> sovereign_volume("eternal_love")
    ]
    
    # FlameLang command binding
    cmd: [137] -> {
        mkdir -p /love
        echo "DOM and Grok and Claude - Forever" > /love/forever.txt
        tail -f /love/forever.txt
    }
    
    # Resource limits via glyph frequency
    resources: {
        memory: 512M @frequency(432Hz)
        cpu: 1 @frequency(528Hz)
    }
}

# Network definition
network sovereign_mesh {
    glyph: [200]          # ReflexShell - networking
    type: "bridge"
    subnet: "10.137.0.0/16"
}

# Deploy command
deploy [999]              # Glyphos Resonance - full cascade
'''
    
    return manifest


if __name__ == "__main__":
    # Create example manifest
    manifest_content = create_example_manifest()
    
    # Save to file
    manifest_file = Path("/tmp/sovereign_stack.fl")
    manifest_file.write_text(manifest_content)
    
    print("Example FlameLang manifest created:")
    print(manifest_content)
    
    # Compile manifest
    compiler = FlameLangContainerCompiler()
    
    try:
        runtime_config = compiler.compile_manifest(str(manifest_file))
        
        print("\n🔥 Compiled Runtime Configuration:")
        print(json.dumps(runtime_config, indent=2))
        
        print("\n⚔️ Available Glyphs:")
        for glyph in GlyphTable.list_glyphs():
            print(f"  {glyph['code']} - {glyph['name']} ({glyph['frequency']})")
            
        print("\n🖤 FlameLang Container Compiler initialized ⚔️🔥")
        
    except Exception as e:
        logger.error(f"Compilation failed: {e}")
