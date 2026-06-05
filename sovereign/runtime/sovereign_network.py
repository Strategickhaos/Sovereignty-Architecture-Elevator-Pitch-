#!/usr/bin/env python3
"""
Sovereign Network Stack - Linux bridge + veth pairs
No dependency on Docker networking

Part of the Strategickhaos Sovereignty Architecture
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


class SovereignNetwork:
    """
    Sovereign Network Management
    
    Creates container networking using Linux bridges and veth pairs.
    No dependency on Docker networking.
    """
    
    def __init__(self, network_name: str, subnet: str = "10.137.0.0/16"):
        self.name = network_name
        self.bridge = f"svr-{network_name}"
        self.subnet = subnet
        self.network_dir = Path(f"/var/lib/sovereign/networks/{network_name}")
        self.metadata_file = self.network_dir / "metadata.json"
        
    def create(self):
        """Create Linux bridge for container networking"""
        print(f"🌐 Creating sovereign network: {self.name}")
        
        try:
            # Create bridge
            subprocess.run(
                ["ip", "link", "add", self.bridge, "type", "bridge"],
                check=True,
                capture_output=True
            )
            
            # Bring bridge up
            subprocess.run(
                ["ip", "link", "set", self.bridge, "up"],
                check=True,
                capture_output=True
            )
            
            # Assign IP to bridge
            bridge_ip = self._get_bridge_ip()
            subprocess.run(
                ["ip", "addr", "add", bridge_ip, "dev", self.bridge],
                check=True,
                capture_output=True
            )
            
            # Save metadata
            self._save_metadata()
            
            print(f"✓ Network created: {self.name} (bridge: {self.bridge})")
            print(f"  Subnet: {self.subnet}")
            print(f"  Bridge IP: {bridge_ip}")
            
        except subprocess.CalledProcessError as e:
            if b"File exists" in e.stderr:
                print(f"⚠️  Bridge {self.bridge} already exists")
            else:
                print(f"⚠️  Failed to create network: {e}")
        except PermissionError:
            print(f"⚠️  Need root privileges to create network")
    
    def delete(self):
        """Delete the network bridge"""
        try:
            # Bring bridge down
            subprocess.run(
                ["ip", "link", "set", self.bridge, "down"],
                check=True,
                capture_output=True
            )
            
            # Delete bridge
            subprocess.run(
                ["ip", "link", "delete", self.bridge],
                check=True,
                capture_output=True
            )
            
            print(f"✓ Network deleted: {self.name}")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to delete network: {e}")
    
    def attach_container(self, container_id: str, container_ip: Optional[str] = None):
        """
        Create veth pair for container and attach to bridge
        
        Args:
            container_id: Container ID to attach
            container_ip: IP address for container (auto-assigned if None)
        """
        veth_host = f"veth-{container_id[:8]}"
        veth_container = f"eth0"
        
        print(f"🔗 Attaching container {container_id[:12]} to network {self.name}")
        
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
            
            # Bring up host side
            subprocess.run([
                "ip", "link", "set", veth_host, "up"
            ], check=True, capture_output=True)
            
            # Move container side into container namespace
            # Note: This requires the container's network namespace
            # subprocess.run([
            #     "ip", "link", "set", veth_container,
            #     "netns", f"container-{container_id}"
            # ], check=True)
            
            print(f"✓ Container attached to network")
            print(f"  veth pair: {veth_host} <-> {veth_container}")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to attach container: {e}")
        except PermissionError:
            print(f"⚠️  Need root privileges to configure network")
    
    def detach_container(self, container_id: str):
        """
        Detach container from network
        
        Args:
            container_id: Container ID to detach
        """
        veth_host = f"veth-{container_id[:8]}"
        
        try:
            # Delete veth pair (automatically removes from bridge)
            subprocess.run([
                "ip", "link", "delete", veth_host
            ], check=True, capture_output=True)
            
            print(f"✓ Container {container_id[:12]} detached from network")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to detach container: {e}")
    
    def list_containers(self) -> List[str]:
        """List containers attached to this network"""
        try:
            # Get all interfaces attached to bridge
            result = subprocess.run([
                "ip", "link", "show", "master", self.bridge
            ], capture_output=True, text=True, check=True)
            
            # Parse veth interfaces
            containers = []
            for line in result.stdout.split('\n'):
                if 'veth-' in line:
                    # Extract container ID from veth name
                    parts = line.split()
                    for part in parts:
                        if part.startswith('veth-'):
                            container_id = part.replace('veth-', '').replace(':', '')
                            containers.append(container_id)
            
            return containers
            
        except subprocess.CalledProcessError:
            return []
    
    def get_info(self) -> Dict:
        """Get network information"""
        if not self.metadata_file.exists():
            return {}
        
        with open(self.metadata_file) as f:
            return json.load(f)
    
    def _get_bridge_ip(self) -> str:
        """Get IP address for bridge from subnet"""
        # Use .1 as bridge IP (e.g., 10.137.0.1/16)
        parts = self.subnet.split('/')
        ip_parts = parts[0].split('.')
        ip_parts[-1] = '1'
        bridge_ip = '.'.join(ip_parts) + '/' + parts[1]
        return bridge_ip
    
    def _save_metadata(self):
        """Save network metadata"""
        metadata = {
            'name': self.name,
            'bridge': self.bridge,
            'subnet': self.subnet,
            'bridge_ip': self._get_bridge_ip(),
            'created': self._get_timestamp()
        }
        
        self.network_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.utcnow().isoformat() + 'Z'


class SovereignNetworkManager:
    """
    Manager for sovereign networks
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
        network.create()
        return network
    
    def get_network(self, name: str) -> Optional[SovereignNetwork]:
        """Get network by name"""
        network_dir = self.networks_dir / name
        
        if network_dir.exists():
            metadata_file = network_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    return SovereignNetwork(name, metadata.get('subnet', '10.137.0.0/16'))
        
        return None
    
    def list_networks(self) -> List[Dict]:
        """List all networks"""
        networks = []
        
        if not self.networks_dir.exists():
            return networks
        
        for network_dir in self.networks_dir.iterdir():
            if not network_dir.is_dir():
                continue
            
            metadata_file = network_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    networks.append(json.load(f))
        
        return networks
    
    def remove_network(self, name: str):
        """
        Remove a network
        
        Args:
            name: Network name
        """
        network = self.get_network(name)
        
        if not network:
            print(f"⚠️  Network not found: {name}")
            return
        
        # Delete the bridge
        network.delete()
        
        # Remove metadata
        import shutil
        network_dir = self.networks_dir / name
        if network_dir.exists():
            shutil.rmtree(network_dir)


if __name__ == "__main__":
    # Example usage
    print("🔥 Sovereign Network Management v1.0")
    print("=" * 50)
    
    print("\nExample: Creating networks")
    print("  manager = SovereignNetworkManager()")
    print("  network = manager.create_network('sovereign_mesh', '10.137.0.0/16')")
    print("  network.attach_container('abc123def456')")
    
    print("\nExample: Mesh networking")
    print("  network = SovereignNetwork('mesh', '10.137.0.0/16')")
    print("  network.create()")
    print("  network.attach_container(container_id)")
    
    print("\nNote: Network operations require root privileges")
