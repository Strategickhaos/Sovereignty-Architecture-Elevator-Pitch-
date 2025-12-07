#!/usr/bin/env python3
"""
Sovereign Network Stack - Linux bridge + veth pairs
No dependency on Docker networking

This provides container networking without Docker:
- Linux bridge for container connectivity
- veth pairs for container network interfaces
- IP address management
- Port forwarding
- Network isolation
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, List
import logging
import ipaddress

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignNetwork:
    """
    Sovereign Network Management - Docker-free networking
    """
    
    def __init__(self, network_name: str, subnet: str = "10.137.0.0/16"):
        """
        Initialize sovereign network
        
        Args:
            network_name: Network name
            subnet: Network subnet in CIDR notation
        """
        self.name = network_name
        self.bridge = f"svr-{network_name[:8]}"  # Limit bridge name length
        self.subnet = ipaddress.ip_network(subnet)
        
        # Network configuration directory
        self.network_dir = Path(f"/var/lib/sovereign/networks/{network_name}")
        self.network_dir.mkdir(parents=True, exist_ok=True)
        
        # Network metadata
        self.metadata_file = self.network_dir / "metadata.json"
        
        # IP allocation tracking
        self.ip_allocation_file = self.network_dir / "ip_allocation.json"
        self.allocated_ips = self._load_ip_allocation()
        
    def _load_ip_allocation(self) -> Dict:
        """Load IP allocation state"""
        if self.ip_allocation_file.exists():
            return json.loads(self.ip_allocation_file.read_text())
        return {}
    
    def _save_ip_allocation(self):
        """Save IP allocation state"""
        self.ip_allocation_file.write_text(json.dumps(self.allocated_ips, indent=2))
    
    def create_bridge(self):
        """
        Create Linux bridge for container networking
        """
        logger.info(f"Creating network bridge: {self.bridge}")
        
        try:
            # Check if bridge exists
            result = subprocess.run(
                ["ip", "link", "show", self.bridge],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Bridge {self.bridge} already exists")
            else:
                # Create bridge
                subprocess.run([
                    "ip", "link", "add", self.bridge, "type", "bridge"
                ], check=True)
                logger.info(f"Bridge created: {self.bridge}")
            
            # Bring bridge up
            subprocess.run([
                "ip", "link", "set", self.bridge, "up"
            ], check=True)
            
            # Assign IP to bridge (gateway)
            gateway_ip = list(self.subnet.hosts())[0]
            subprocess.run([
                "ip", "addr", "add",
                f"{gateway_ip}/{self.subnet.prefixlen}",
                "dev", self.bridge
            ], check=False)  # May already exist
            
            # Save metadata
            metadata = {
                'name': self.name,
                'bridge': self.bridge,
                'subnet': str(self.subnet),
                'gateway': str(gateway_ip)
            }
            self.metadata_file.write_text(json.dumps(metadata, indent=2))
            
            logger.info(f"Network ready - Gateway: {gateway_ip}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create bridge: {e}")
            raise
    
    def delete_bridge(self):
        """Delete the network bridge"""
        logger.info(f"Deleting network bridge: {self.bridge}")
        
        try:
            # Bring bridge down
            subprocess.run([
                "ip", "link", "set", self.bridge, "down"
            ], check=False)
            
            # Delete bridge
            subprocess.run([
                "ip", "link", "delete", self.bridge
            ], check=True)
            
            logger.info(f"Bridge deleted: {self.bridge}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to delete bridge: {e}")
            raise
    
    def allocate_ip(self, container_id: str) -> str:
        """
        Allocate an IP address for a container
        
        Args:
            container_id: Container ID
            
        Returns:
            Allocated IP address
        """
        # Get list of available IPs
        available_ips = list(self.subnet.hosts())[1:]  # Skip gateway
        
        # Find first available IP
        for ip in available_ips:
            ip_str = str(ip)
            if ip_str not in self.allocated_ips.values():
                self.allocated_ips[container_id] = ip_str
                self._save_ip_allocation()
                logger.info(f"Allocated IP {ip_str} to {container_id}")
                return ip_str
        
        raise RuntimeError("No available IP addresses in subnet")
    
    def release_ip(self, container_id: str):
        """
        Release IP address for a container
        
        Args:
            container_id: Container ID
        """
        if container_id in self.allocated_ips:
            ip = self.allocated_ips.pop(container_id)
            self._save_ip_allocation()
            logger.info(f"Released IP {ip} from {container_id}")
    
    def attach_container(self, container_id: str, namespace_pid: int) -> str:
        """
        Create veth pair for container and attach to bridge
        
        Args:
            container_id: Container ID
            namespace_pid: PID of container process (for network namespace)
            
        Returns:
            IP address assigned to container
        """
        logger.info(f"Attaching container {container_id} to network {self.name}")
        
        veth_host = f"veth{container_id[:8]}"
        veth_container = "eth0"
        
        try:
            # Create veth pair
            subprocess.run([
                "ip", "link", "add", veth_host,
                "type", "veth",
                "peer", "name", veth_container
            ], check=True)
            
            # Attach host side to bridge
            subprocess.run([
                "ip", "link", "set", veth_host, "master", self.bridge
            ], check=True)
            
            # Bring up host side
            subprocess.run([
                "ip", "link", "set", veth_host, "up"
            ], check=True)
            
            # Move container side into container namespace
            subprocess.run([
                "ip", "link", "set", veth_container,
                "netns", str(namespace_pid)
            ], check=True)
            
            # Allocate IP for container
            container_ip = self.allocate_ip(container_id)
            
            # Configure IP inside container namespace
            subprocess.run([
                "nsenter", "-t", str(namespace_pid), "-n",
                "ip", "addr", "add",
                f"{container_ip}/{self.subnet.prefixlen}",
                "dev", veth_container
            ], check=True)
            
            # Bring up interface inside container
            subprocess.run([
                "nsenter", "-t", str(namespace_pid), "-n",
                "ip", "link", "set", veth_container, "up"
            ], check=True)
            
            # Set default route inside container
            gateway = list(self.subnet.hosts())[0]
            subprocess.run([
                "nsenter", "-t", str(namespace_pid), "-n",
                "ip", "route", "add", "default",
                "via", str(gateway)
            ], check=True)
            
            logger.info(f"Container attached with IP: {container_ip}")
            return container_ip
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to attach container: {e}")
            raise
    
    def detach_container(self, container_id: str):
        """
        Remove container from network
        
        Args:
            container_id: Container ID
        """
        logger.info(f"Detaching container {container_id} from network")
        
        veth_host = f"veth{container_id[:8]}"
        
        try:
            # Delete veth pair (also removes peer)
            subprocess.run([
                "ip", "link", "delete", veth_host
            ], check=True)
            
            # Release IP
            self.release_ip(container_id)
            
            logger.info(f"Container detached from network")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to detach container: {e}")
            raise
    
    def setup_port_forward(self, container_ip: str, host_port: int, container_port: int):
        """
        Setup port forwarding from host to container
        
        Args:
            container_ip: Container IP address
            host_port: Port on host
            container_port: Port in container
        """
        logger.info(f"Setting up port forward: {host_port} -> {container_ip}:{container_port}")
        
        try:
            # Use iptables for port forwarding
            subprocess.run([
                "iptables", "-t", "nat", "-A", "PREROUTING",
                "-p", "tcp", "--dport", str(host_port),
                "-j", "DNAT", "--to-destination",
                f"{container_ip}:{container_port}"
            ], check=True)
            
            logger.info(f"Port forward configured")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to setup port forward: {e}")
            raise
    
    def get_info(self) -> Dict:
        """Get network information"""
        info = {
            'name': self.name,
            'bridge': self.bridge,
            'subnet': str(self.subnet),
            'allocated_ips': len(self.allocated_ips),
            'available_ips': self.subnet.num_addresses - len(self.allocated_ips) - 2,
            'containers': list(self.allocated_ips.keys())
        }
        
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
            info.update(metadata)
        
        return info


def list_networks() -> List[Dict]:
    """List all sovereign networks"""
    networks_dir = Path("/var/lib/sovereign/networks")
    
    if not networks_dir.exists():
        return []
    
    networks = []
    for network_dir in networks_dir.iterdir():
        if network_dir.is_dir():
            metadata_file = network_dir / "metadata.json"
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text())
                networks.append(metadata)
    
    return networks


if __name__ == "__main__":
    print("🔥 Sovereign Network Management - Phase 1")
    print("=" * 50)
    
    # Example usage
    network = SovereignNetwork("test_network", "10.137.0.0/16")
    print(f"Network initialized: {network.name}")
    print(f"Subnet: {network.subnet}")
