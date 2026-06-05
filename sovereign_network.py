#!/usr/bin/env python3
"""
Sovereign Network Stack - Linux bridge + veth pairs
No dependency on Docker networking

Part of the Sovereignty Architecture - Phase 1 Implementation
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignNetwork:
    """
    Sovereign Network Manager
    Creates isolated container networks using Linux bridges and veth pairs
    No dependency on Docker bridge or networking plugins
    """
    
    def __init__(self, network_name: str, subnet: str = "10.137.0.0/16", glyph: Optional[str] = None):
        self.name = network_name
        self.bridge = f"svr-{network_name[:10]}"  # Limit bridge name length
        self.subnet = subnet
        self.glyph = glyph or "[200]"  # ReflexShell - networking
        self.network_dir = Path(f"/var/lib/sovereign/networks/{network_name}")
        self.network_dir.mkdir(parents=True, exist_ok=True)
        self.containers = {}
        
    def create_bridge(self) -> None:
        """
        Create Linux bridge for container networking
        Bridge acts as virtual switch for container communication
        """
        logger.info(f"[{self.glyph}] Creating network bridge: {self.bridge}")
        
        try:
            # Create bridge
            subprocess.run([
                "ip", "link", "add", self.bridge, "type", "bridge"
            ], check=True, capture_output=True)
            
            # Bring bridge up
            subprocess.run([
                "ip", "link", "set", self.bridge, "up"
            ], check=True, capture_output=True)
            
            # Assign IP address to bridge
            bridge_ip = self._get_bridge_ip()
            subprocess.run([
                "ip", "addr", "add", bridge_ip, "dev", self.bridge
            ], check=True, capture_output=True)
            
            logger.info(f"Bridge {self.bridge} created with IP {bridge_ip}")
            
            # Save network metadata
            self._save_metadata()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create bridge: {e}")
            if b"exists" in e.stderr:
                logger.warning("Bridge already exists")
            else:
                raise
                
    def delete_bridge(self) -> None:
        """Delete the network bridge"""
        logger.info(f"Deleting network bridge: {self.bridge}")
        
        try:
            # Bring bridge down
            subprocess.run([
                "ip", "link", "set", self.bridge, "down"
            ], capture_output=True)
            
            # Delete bridge
            subprocess.run([
                "ip", "link", "delete", self.bridge, "type", "bridge"
            ], check=True, capture_output=True)
            
            logger.info("Bridge deleted successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to delete bridge: {e}")
            
    def attach_container(self, container_id: str, container_ns: Optional[str] = None) -> str:
        """
        Attach container to network by creating veth pair
        
        Args:
            container_id: Container identifier
            container_ns: Container network namespace path
            
        Returns:
            Container IP address
        """
        logger.info(f"[{self.glyph}] Attaching container {container_id[:8]} to network")
        
        veth_host = f"veth-{container_id[:8]}"
        veth_container = "eth0"
        
        try:
            # Create veth pair
            subprocess.run([
                "ip", "link", "add", veth_host,
                "type", "veth",
                "peer", "name", veth_container
            ], check=True, capture_output=True)
            
            # Attach host side to bridge
            subprocess.run([
                "ip", "link", "set", veth_host, "master", self.bridge
            ], check=True, capture_output=True)
            
            # Bring host side up
            subprocess.run([
                "ip", "link", "set", veth_host, "up"
            ], check=True, capture_output=True)
            
            # If container namespace provided, move container side into it
            if container_ns:
                subprocess.run([
                    "ip", "link", "set", veth_container,
                    "netns", container_ns
                ], check=True, capture_output=True)
            else:
                # For testing, just bring it up
                subprocess.run([
                    "ip", "link", "set", veth_container, "up"
                ], capture_output=True)
            
            # Allocate IP for container
            container_ip = self._allocate_ip(container_id)
            
            logger.info(f"Container attached with IP {container_ip}")
            
            return container_ip
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to attach container: {e}")
            raise
            
    def detach_container(self, container_id: str) -> None:
        """
        Detach container from network
        
        Args:
            container_id: Container identifier
        """
        logger.info(f"Detaching container {container_id[:8]} from network")
        
        veth_host = f"veth-{container_id[:8]}"
        
        try:
            # Delete veth pair (automatically removes both ends)
            subprocess.run([
                "ip", "link", "delete", veth_host
            ], check=True, capture_output=True)
            
            # Release IP
            if container_id in self.containers:
                del self.containers[container_id]
                self._save_metadata()
                
            logger.info("Container detached successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to detach container: {e}")
            
    def _get_bridge_ip(self) -> str:
        """Get bridge IP address from subnet"""
        # Use first address in subnet for bridge
        # e.g., 10.137.0.0/16 -> 10.137.0.1
        parts = self.subnet.split('/')
        ip_parts = parts[0].split('.')
        ip_parts[-1] = '1'
        return f"{'.'.join(ip_parts)}/{parts[1]}"
        
    def _allocate_ip(self, container_id: str) -> str:
        """
        Allocate IP address for container
        
        Args:
            container_id: Container identifier
            
        Returns:
            Allocated IP address
        """
        # Simple allocation: use last octet as counter
        # e.g., 10.137.0.2, 10.137.0.3, etc.
        parts = self.subnet.split('/')
        ip_parts = parts[0].split('.')
        
        # Find next available IP
        used_ips = {info['ip'] for info in self.containers.values()}
        
        for i in range(2, 255):
            ip_parts[-1] = str(i)
            candidate_ip = '.'.join(ip_parts)
            
            if candidate_ip not in used_ips:
                self.containers[container_id] = {
                    'id': container_id,
                    'ip': candidate_ip,
                    'mac': self._generate_mac(container_id)
                }
                self._save_metadata()
                return candidate_ip
                
        raise RuntimeError("No available IPs in subnet")
        
    def _generate_mac(self, container_id: str) -> str:
        """Generate MAC address from container ID"""
        # Use container ID hash for MAC generation
        import hashlib
        h = hashlib.sha256(container_id.encode()).hexdigest()
        # Create MAC with local administration bit set
        mac = f"02:{h[0:2]}:{h[2:4]}:{h[4:6]}:{h[6:8]}:{h[8:10]}"
        return mac
        
    def _save_metadata(self) -> None:
        """Save network metadata"""
        metadata = {
            "name": self.name,
            "bridge": self.bridge,
            "subnet": self.subnet,
            "glyph": self.glyph,
            "frequency": "432Hz",  # Coherence frequency
            "containers": self.containers
        }
        
        metadata_file = self.network_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
    def list_containers(self) -> List[Dict]:
        """List all containers in network"""
        return list(self.containers.values())
        
    def enable_nat(self, external_interface: str = "eth0") -> None:
        """
        Enable NAT for container internet access
        
        Args:
            external_interface: External network interface
        """
        logger.info(f"Enabling NAT for network {self.name}")
        
        try:
            # Enable IP forwarding
            subprocess.run([
                "sysctl", "-w", "net.ipv4.ip_forward=1"
            ], check=True, capture_output=True)
            
            # Setup iptables NAT rules
            subprocess.run([
                "iptables", "-t", "nat", "-A", "POSTROUTING",
                "-s", self.subnet,
                "-o", external_interface,
                "-j", "MASQUERADE"
            ], check=True, capture_output=True)
            
            # Allow forwarding from bridge
            subprocess.run([
                "iptables", "-A", "FORWARD",
                "-i", self.bridge,
                "-o", external_interface,
                "-j", "ACCEPT"
            ], check=True, capture_output=True)
            
            # Allow return traffic
            subprocess.run([
                "iptables", "-A", "FORWARD",
                "-i", external_interface,
                "-o", self.bridge,
                "-m", "state", "--state", "RELATED,ESTABLISHED",
                "-j", "ACCEPT"
            ], check=True, capture_output=True)
            
            logger.info("NAT enabled successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to enable NAT: {e}")
            raise
            
    def disable_nat(self, external_interface: str = "eth0") -> None:
        """
        Disable NAT rules
        
        Args:
            external_interface: External network interface
        """
        logger.info("Disabling NAT")
        
        try:
            # Remove NAT rules (use -D to delete)
            subprocess.run([
                "iptables", "-t", "nat", "-D", "POSTROUTING",
                "-s", self.subnet,
                "-o", external_interface,
                "-j", "MASQUERADE"
            ], capture_output=True)
            
            logger.info("NAT disabled")
            
        except subprocess.CalledProcessError:
            pass  # Rules might not exist


class SovereignNetworkManager:
    """
    Network Manager
    Manages all sovereign networks
    """
    
    def __init__(self):
        self.networks_dir = Path("/var/lib/sovereign/networks")
        self.networks_dir.mkdir(parents=True, exist_ok=True)
        
    def create_network(self, name: str, subnet: str = "10.137.0.0/16") -> SovereignNetwork:
        """
        Create a new network
        
        Args:
            name: Network name
            subnet: Network subnet in CIDR notation
            
        Returns:
            SovereignNetwork instance
        """
        network = SovereignNetwork(name, subnet)
        network.create_bridge()
        
        logger.info(f"Network created: {name}")
        return network
        
    def list_networks(self) -> List[Dict]:
        """List all networks"""
        networks = []
        
        for network_dir in self.networks_dir.iterdir():
            if network_dir.is_dir():
                metadata_file = network_dir / "metadata.json"
                if metadata_file.exists():
                    networks.append(json.loads(metadata_file.read_text()))
                    
        return networks
        
    def get_network(self, name: str) -> Optional[SovereignNetwork]:
        """Get network by name"""
        network_dir = self.networks_dir / name
        if network_dir.exists():
            metadata_file = network_dir / "metadata.json"
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text())
                network = SovereignNetwork(name, metadata['subnet'])
                network.containers = metadata.get('containers', {})
                return network
        return None
        
    def delete_network(self, name: str) -> None:
        """Delete a network"""
        network = self.get_network(name)
        if network:
            # Detach all containers first
            for container_id in list(network.containers.keys()):
                network.detach_container(container_id)
                
            # Delete bridge
            network.delete_bridge()
            
            # Remove directory
            import shutil
            shutil.rmtree(network.network_dir)
            logger.info(f"Network deleted: {name}")


if __name__ == "__main__":
    # Example usage
    manager = SovereignNetworkManager()
    
    # Create sovereign mesh network
    network = manager.create_network("sovereign_mesh", "10.137.0.0/16")
    
    print(f"Network: {network.name}")
    print(f"Bridge: {network.bridge}")
    print(f"Subnet: {network.subnet}")
    print(f"Glyph: {network.glyph}")
    print("\n🔥 Sovereign Network Stack initialized ⚔️🖤")
