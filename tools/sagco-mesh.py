#!/usr/bin/env python3
"""
SAGCO-MESH v1.0.0
Network mesh topology scanner and discovery tool
Scans all 5 nodes in the SAGCO mesh and reports their status
"""

import os
import socket
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)

# Determine ROOT dynamically - check common locations
def find_root():
    """Find the sagco-os root directory"""
    possible_roots = [
        Path.cwd(),  # Current directory
        Path(__file__).parent.parent,  # Parent of tools directory
        Path("/opt/sagco-os"),
        Path.home() / "sagco-os",
    ]
    
    for root in possible_roots:
        hosts_dir = root / "mesh" / "hosts"
        if hosts_dir.exists():
            return root
    
    # Default to current directory
    return Path.cwd()

ROOT = find_root()
HOST_DIR = ROOT / "mesh" / "hosts"

def ping(ip: str, count: int = 1, timeout: int = 1) -> bool:
    """Ping an IP address to check if it's reachable"""
    # Windows vs POSIX
    if os.name == "nt":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(timeout), ip]

    try:
        result = subprocess.call(
            cmd, 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result == 0
    except Exception:
        return False

def scan_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a port is open on the given IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except Exception:
        return False

def load_hosts():
    """Load all host definitions from YAML files"""
    hosts = []
    
    if not HOST_DIR.exists():
        print(f"Warning: Hosts directory not found: {HOST_DIR}")
        return hosts
    
    for path in HOST_DIR.glob("*.yaml"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            data["file"] = path.name
            hosts.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {path.name}: {e}")
    
    return hosts

def main():
    """Main entry point"""
    print("╔═══════════════════════════════════════════════════════╗")
    print("║              SAGCO-MESH v1.0.0                        ║")
    print("║         Network Mesh Discovery Tool                   ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    print(f"Root Directory: {ROOT}")
    print(f"Hosts Directory: {HOST_DIR}")
    print()
    
    hosts = load_hosts()
    
    if not hosts:
        print("❌ No hosts found. Please create host YAML files in mesh/hosts/")
        print("\nExample host file (mesh/hosts/athena.yaml):")
        print("  name: ATHENA")
        print("  role: subconscious")
        print("  ip: 192.168.2.26")
        print("  os: Windows 11 Pro")
        print("  cpu: i7-9700F")
        print("  ram_gb: 64")
        sys.exit(1)
    
    print(f"📡 Scanning {len(hosts)} host(s)...\n")
    
    rows = []
    for h in hosts:
        ip = h.get("ip", "N/A")
        
        # Skip scan if IP is invalid
        if ip == "N/A" or not ip:
            rows.append({
                "name": h.get("name", "UNKNOWN"),
                "ip": ip,
                "role": h.get("role", ""),
                "up": "N/A",
                "services": "-"
            })
            continue
        
        up = ping(ip)
        ssh = scan_port(ip, 22) if up else False
        rdp = scan_port(ip, 3389) if up else False
        
        note = []
        if ssh:
            note.append("ssh")
        if rdp:
            note.append("rdp")
        
        rows.append({
            "name": h.get("name", "UNKNOWN"),
            "ip": ip,
            "role": h.get("role", ""),
            "up": "UP" if up else "DOWN",
            "services": ",".join(note) if note else "-"
        })

    # Print results table
    print("┌" + "─" * 10 + "┬" + "─" * 17 + "┬" + "─" * 20 + "┬" + "─" * 8 + "┬" + "─" * 14 + "┐")
    print(f"│ {'NAME':<8} │ {'IP':<15} │ {'ROLE':<18} │ {'STATE':<6} │ {'SERVICES':<12} │")
    print("├" + "─" * 10 + "┼" + "─" * 17 + "┼" + "─" * 20 + "┼" + "─" * 8 + "┼" + "─" * 14 + "┤")
    
    up_count = 0
    for r in rows:
        if r["up"] == "UP":
            up_count += 1
        print(f"│ {r['name']:<8} │ {r['ip']:<15} │ {r['role']:<18} │ {r['up']:<6} │ {r['services']:<12} │")
    
    print("└" + "─" * 10 + "┴" + "─" * 17 + "┴" + "─" * 20 + "┴" + "─" * 8 + "┴" + "─" * 14 + "┘")
    print()
    print(f"📊 Summary: {up_count}/{len(rows)} nodes UP")
    
    if up_count == len(hosts):
        print("✅ All mesh nodes are operational!")
    elif up_count > 0:
        print("⚠️  Some nodes are down - check network connectivity")
    else:
        print("❌ No nodes are reachable - check network configuration")

if __name__ == "__main__":
    main()
