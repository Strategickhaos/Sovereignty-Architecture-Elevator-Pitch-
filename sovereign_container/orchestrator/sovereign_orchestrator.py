#!/usr/bin/env python3
"""
Sovereign Orchestrator - FlameLang-based container orchestration
Replaces Kubernetes with sovereign control plane

This is Phase 3 of the Sovereign Container Platform:
- Multi-node orchestration
- FlameLang-based scheduling
- Glyph frequency-aware placement
- Mesh networking
- Zero dependency on Kubernetes
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignOrchestrator:
    """
    FlameLang-based container orchestration
    Replaces Kubernetes with sovereign control plane
    """
    
    def __init__(self):
        """Initialize sovereign orchestrator"""
        self.nodes = {}  # Physical machines in mesh
        self.containers = {}  # Running containers
        self.pending = []  # Pending container specs
        
        # State directory - use home directory if /var/lib not writable
        try:
            self.state_dir = Path("/var/lib/sovereign/orchestrator")
            self.state_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            # Fallback to home directory for non-root users
            home = Path.home()
            self.state_dir = home / ".sovereign" / "orchestrator"
            self.state_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Using fallback state directory: {self.state_dir}")
        
        # Load state if exists
        self._load_state()
        
    def _load_state(self):
        """Load orchestrator state"""
        state_file = self.state_dir / "state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text())
            self.nodes = state.get('nodes', {})
            self.containers = state.get('containers', {})
            logger.info(f"Loaded state: {len(self.nodes)} nodes, {len(self.containers)} containers")
    
    def _save_state(self):
        """Save orchestrator state"""
        state = {
            'nodes': self.nodes,
            'containers': self.containers,
            'timestamp': datetime.now().isoformat()
        }
        state_file = self.state_dir / "state.json"
        state_file.write_text(json.dumps(state, indent=2))
    
    def register_node(self, node_id: str, node_spec: Dict):
        """
        Register physical node in sovereign mesh
        
        Args:
            node_id: Unique node identifier
            node_spec: Node specification with hostname, resources, glyph
        """
        logger.info(f"Registering node: {node_id}")
        
        self.nodes[node_id] = {
            'id': node_id,
            'hostname': node_spec['hostname'],
            'resources': node_spec['resources'],
            'glyph': node_spec.get('glyph', '[001]'),  # Default to Aether Prime
            'authority': self.calculate_authority(node_spec),
            'status': 'ready',
            'containers': []
        }
        
        self._save_state()
        logger.info(f"Node registered with authority: {self.nodes[node_id]['authority']}")
    
    def calculate_authority(self, node_spec: Dict) -> float:
        """
        Calculate node authority based on resources and glyph
        
        Authority determines node's capability to host containers
        
        Args:
            node_spec: Node specification
            
        Returns:
            Authority score (0.0 - 1.0)
        """
        resources = node_spec.get('resources', {})
        
        # Base authority from resources
        memory_gb = self._parse_memory(resources.get('memory', '1G'))
        cpu_cores = float(resources.get('cpu', 1))
        
        # Normalize to 0-1 scale (assuming max 32GB RAM, 16 cores)
        memory_score = min(memory_gb / 32.0, 1.0)
        cpu_score = min(cpu_cores / 16.0, 1.0)
        
        # Weighted average
        base_authority = (memory_score * 0.5) + (cpu_score * 0.5)
        
        # Glyph modifier
        glyph = node_spec.get('glyph')
        glyph_modifiers = {
            '[001]': 1.0,   # Aether Prime - standard
            '[100]': 1.2,   # Resonance Core - enhanced compute
            '[137]': 1.1,   # Flamebearer - enhanced security
            '[200]': 1.15,  # ReflexShell - enhanced networking
            '[999]': 1.3    # Glyphos Resonance - maximum capability
        }
        
        modifier = glyph_modifiers.get(glyph, 1.0)
        authority = base_authority * modifier
        
        return min(authority, 1.0)
    
    def _parse_memory(self, memory_str: str) -> float:
        """Parse memory string to GB"""
        memory_str = memory_str.upper()
        if 'G' in memory_str:
            return float(memory_str.replace('G', ''))
        elif 'M' in memory_str:
            return float(memory_str.replace('M', '')) / 1024.0
        return 1.0
    
    def frequency_matches(self, node_glyph: str, required_frequency: int) -> bool:
        """
        Check if node glyph frequency matches required frequency
        
        Args:
            node_glyph: Node's glyph
            required_frequency: Required frequency in Hz
            
        Returns:
            True if frequencies are compatible
        """
        # Glyph to frequency mapping
        glyph_frequencies = {
            '[001]': 432,
            '[100]': 528,
            '[137]': 639,
            '[200]': 741,
            '[999]': 963
        }
        
        node_freq = glyph_frequencies.get(node_glyph, 432)
        
        # Frequencies are compatible if within 20% range
        tolerance = 0.2
        lower_bound = required_frequency * (1 - tolerance)
        upper_bound = required_frequency * (1 + tolerance)
        
        return lower_bound <= node_freq <= upper_bound
    
    def schedule_container(self, container_spec: Dict) -> Optional[str]:
        """
        Schedule container to node using FlameLang logic
        
        Args:
            container_spec: Container specification
            
        Returns:
            Node ID where container was scheduled, or None if failed
        """
        logger.info(f"Scheduling container: {container_spec['name']}")
        
        # Get required frequency
        required_frequency = container_spec.get('frequency', 432)
        
        # Find compatible nodes
        compatible_nodes = []
        for node_id, node in self.nodes.items():
            if node['status'] != 'ready':
                continue
            
            # Check frequency compatibility
            if self.frequency_matches(node['glyph'], required_frequency):
                # Check resource availability
                if self._has_resources(node, container_spec['resources']):
                    compatible_nodes.append((node_id, node))
        
        if not compatible_nodes:
            logger.warning(f"No compatible nodes for container {container_spec['name']}")
            self.pending.append(container_spec)
            return None
        
        # Select node with highest authority
        compatible_nodes.sort(key=lambda x: x[1]['authority'], reverse=True)
        selected_node_id, selected_node = compatible_nodes[0]
        
        # Deploy to node
        self.deploy_to_node(selected_node_id, container_spec)
        
        return selected_node_id
    
    def _has_resources(self, node: Dict, required: Dict) -> bool:
        """
        Check if node has required resources available
        
        Phase 1: Basic validation
        Phase 2: Will track actual resource usage across containers
        """
        # Basic validation - check if required resources are reasonable
        if not required:
            return True
        
        node_resources = node.get('resources', {})
        
        # Check memory
        required_memory = required.get('memory', '0M')
        node_memory = node_resources.get('memory', '0G')
        
        # Simple validation: ensure we're not requesting more than node total
        # In production, this would track actual allocated resources
        req_mb = self._parse_memory(required_memory)
        node_gb = self._parse_memory(node_memory)
        
        if req_mb > node_gb * 1024:  # Don't exceed total node memory
            return False
        
        # Check CPU
        required_cpu = float(required.get('cpu', 0))
        node_cpu = float(node_resources.get('cpu', 0))
        
        if required_cpu > node_cpu:  # Don't exceed total node CPU
            return False
        
        # TODO Phase 2: Track actual allocated resources and check available capacity
        return True
    
    def deploy_to_node(self, node_id: str, container_spec: Dict):
        """
        Deploy container to specific node
        
        Args:
            node_id: Target node ID
            container_spec: Container specification
        """
        logger.info(f"Deploying {container_spec['name']} to node {node_id}")
        
        container_id = f"{container_spec['name']}-{node_id[:8]}"
        
        # Record deployment
        self.containers[container_id] = {
            'id': container_id,
            'name': container_spec['name'],
            'node_id': node_id,
            'spec': container_spec,
            'status': 'running',
            'deployed_at': datetime.now().isoformat()
        }
        
        # Update node
        self.nodes[node_id]['containers'].append(container_id)
        
        self._save_state()
        
        logger.info(f"Container deployed: {container_id}")
        
        # In production, this would use SSH/API to actually start container on remote node
        # For now, we just track the deployment
    
    def handle_glyph_command(self, glyph_code: str):
        """
        Execute FlameLang orchestration commands
        
        Args:
            glyph_code: FlameLang glyph command
        """
        logger.info(f"Handling glyph command: {glyph_code}")
        
        if glyph_code == "[999]":  # Full Resonance
            logger.info("Activating Full Resonance - deploying all pending containers")
            # Deploy to all nodes
            for container in self.pending:
                self.schedule_container(container)
            self.pending = []
                
        elif glyph_code == "[137]":  # Flamebearer Defense
            logger.info("Activating Flamebearer Defense - security protocols")
            # Activate security protocols
            self.enable_defense_mode()
            
        elif glyph_code == "[001]":  # Aether Prime
            logger.info("Activating Aether Prime - initialization protocols")
            # Initialize all nodes
            for node_id in self.nodes:
                self.nodes[node_id]['status'] = 'ready'
            self._save_state()
    
    def enable_defense_mode(self):
        """Enable security defense mode"""
        logger.info("🔥 Defense mode activated - Flamebearer protection")
        
        # In production, this would:
        # - Enable additional firewall rules
        # - Increase monitoring
        # - Lock down network access
        # - Enable intrusion detection
        
        for node_id in self.nodes:
            self.nodes[node_id]['defense_mode'] = True
        
        self._save_state()
    
    def get_cluster_status(self) -> Dict:
        """Get cluster status"""
        return {
            'nodes': len(self.nodes),
            'containers': len(self.containers),
            'pending': len(self.pending),
            'ready_nodes': sum(1 for n in self.nodes.values() if n['status'] == 'ready'),
            'node_list': list(self.nodes.keys()),
            'container_list': list(self.containers.keys())
        }


if __name__ == "__main__":
    print("🔥 Sovereign Orchestrator - Phase 3")
    print("=" * 50)
    
    orchestrator = SovereignOrchestrator()
    print(f"Cluster status: {orchestrator.get_cluster_status()}")
