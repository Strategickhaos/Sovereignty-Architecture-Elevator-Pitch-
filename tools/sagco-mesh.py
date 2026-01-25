#!/usr/bin/env python3
"""
SAGCO-MESH v1.0.0
Network mesh discovery and health monitoring

Scans all nodes defined in mesh/hosts/*.yaml and reports their status.
"""

import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)

# Determine repository root
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
HOST_DIR = REPO_ROOT / "mesh" / "hosts"


def ping(ip: str, count: int = 1, timeout: int = 1) -> bool:
    """
    Ping a host to check if it's reachable.
    
    Args:
        ip: IP address to ping
        count: Number of ping attempts
        timeout: Timeout in seconds
        
    Returns:
        True if host is reachable, False otherwise
    """
    # Windows vs POSIX ping command differences
    if os.name == "nt":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(timeout), ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False


def scan_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """
    Check if a specific port is open on a host.
    
    Args:
        ip: IP address to scan
        port: Port number
        timeout: Connection timeout in seconds
        
    Returns:
        True if port is open, False otherwise
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except (socket.timeout, socket.error, OSError):
        return False


def load_hosts() -> List[Dict[str, Any]]:
    """
    Load all host configurations from mesh/hosts/*.yaml
    
    Returns:
        List of host configuration dictionaries
    """
    hosts = []
    
    if not HOST_DIR.exists():
        print(f"Warning: Host directory not found: {HOST_DIR}")
        return hosts
    
    yaml_files = list(HOST_DIR.glob("*.yaml")) + list(HOST_DIR.glob("*.yml"))
    
    for path in yaml_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                data["file"] = path.name
                hosts.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {path.name}: {e}")
    
    return hosts


def scan_host(host: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scan a single host for availability and services.
    
    Args:
        host: Host configuration dictionary
        
    Returns:
        Dictionary with scan results
    """
    ip = host.get("ip", "")
    name = host.get("name", "Unknown")
    role = host.get("role", "")
    
    # Check if host is up
    is_up = ping(ip)
    
    # Scan common ports
    services = []
    if is_up:
        if scan_port(ip, 22):
            services.append("ssh")
        if scan_port(ip, 3389):
            services.append("rdp")
        if scan_port(ip, 80):
            services.append("http")
        if scan_port(ip, 443):
            services.append("https")
    
    return {
        "name": name,
        "ip": ip,
        "role": role,
        "up": "UP" if is_up else "DOWN",
        "services": ",".join(services) if services else "-"
    }


def print_topology(results: List[Dict[str, Any]]) -> None:
    """
    Print the mesh topology in a formatted table.
    
    Args:
        results: List of scan results
    """
    print("\n{:<12} {:<16} {:<14} {:<6} {:<15}".format(
        "NAME", "IP", "ROLE", "STATE", "SERVICES"
    ))
    print("=" * 70)
    
    for r in results:
        print("{:<12} {:<16} {:<14} {:<6} {:<15}".format(
            r["name"][:12], 
            r["ip"][:16], 
            r["role"][:14], 
            r["up"], 
            r["services"][:15]
        ))
    
    # Summary
    up_count = sum(1 for r in results if r["up"] == "UP")
    total = len(results)
    print("\n" + "=" * 70)
    print(f"Mesh Health: {up_count}/{total} nodes online ({up_count/total*100:.0f}%)")
    print()


def main():
    """Main entry point for sagco-mesh"""
    print("SAGCO-MESH v1.0.0 - Network Discovery & Health Monitor")
    print("=" * 70)
    
    hosts = load_hosts()
    
    if not hosts:
        print("Error: No host configurations found.")
        print(f"Expected location: {HOST_DIR}")
        sys.exit(1)
    
    print(f"Scanning {len(hosts)} host(s)...\n")
    
    results = []
    for host in hosts:
        result = scan_host(host)
        results.append(result)
    
    print_topology(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
