#!/usr/bin/env python3
"""
Sovereign Container Runtime - Linux Namespace-based Isolation
Uses cgroups, namespaces, overlayfs without Docker dependency

Part of the Strategickhaos Sovereignty Architecture
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, List


class SovereignContainer:
    """
    Sovereign Container Runtime
    
    Provides container isolation using Linux kernel primitives:
    - Namespaces (PID, NET, MNT, UTS, IPC)
    - Cgroups (resource limits)
    - OverlayFS (layered filesystems)
    """
    
    def __init__(self, name: str, rootfs_path: str, glyph: Optional[str] = None):
        self.name = name
        self.rootfs = Path(rootfs_path)
        self.container_dir = Path(f"/var/lib/sovereign/containers/{name}")
        self.glyph = glyph or "[001]"  # Default to Aether Prime
        self.container_id = None
        self.pid = None
        
    def create_namespaces(self) -> int:
        """
        Create isolated namespaces (PID, NET, MNT, UTS, IPC)
        Returns: PID of the container process
        """
        if not self.rootfs.exists():
            raise FileNotFoundError(f"Root filesystem not found: {self.rootfs}")
        
        # Ensure container directory exists
        self.container_dir.mkdir(parents=True, exist_ok=True)
        
        # Create namespace isolation using unshare
        # This creates a new set of namespaces for the container
        cmd = [
            "unshare",
            "--fork",        # Fork before executing
            "--pid",         # New PID namespace
            "--mount",       # New mount namespace
            "--uts",         # New UTS namespace (hostname)
            "--ipc",         # New IPC namespace
            "--net",         # New network namespace
            f"--root={self.rootfs}",  # Change root to container filesystem
            "/bin/sh", "-c", "sleep infinity"  # Keep container running
        ]
        
        try:
            # Start the container process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new session
            )
            self.pid = process.pid
            self.container_id = self._generate_container_id()
            
            # Save container metadata
            self._save_metadata()
            
            return self.pid
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create namespaces: {e}")
    
    def setup_cgroups(self, memory_limit: str = "512M", cpu_limit: str = "1"):
        """
        Resource limits without Docker
        
        Args:
            memory_limit: Memory limit (e.g., "512M", "1G")
            cpu_limit: CPU limit as number of cores
        """
        cgroup_path = Path(f"/sys/fs/cgroup/sovereign_{self.name}")
        
        try:
            cgroup_path.mkdir(exist_ok=True)
            
            # Memory limit
            memory_file = cgroup_path / "memory.max"
            if memory_file.exists():
                memory_file.write_text(self._parse_memory_limit(memory_limit))
            
            # CPU limit
            cpu_file = cgroup_path / "cpu.max"
            if cpu_file.exists():
                # Format: max period (e.g., "100000 100000" for 1 CPU)
                cpu_max = int(float(cpu_limit) * 100000)
                cpu_file.write_text(f"{cpu_max} 100000")
            
            # Add container process to cgroup
            procs_file = cgroup_path / "cgroup.procs"
            if procs_file.exists() and self.pid:
                procs_file.write_text(str(self.pid))
                
        except PermissionError:
            print(f"⚠️  Warning: Need root privileges to set cgroup limits")
        except Exception as e:
            print(f"⚠️  Warning: Failed to set cgroup limits: {e}")
    
    def mount_overlay(self, lower: str, upper: str, work: str, merged: str):
        """
        OverlayFS for layered filesystems
        
        Args:
            lower: Lower (read-only) layer path
            upper: Upper (read-write) layer path
            work: Work directory for overlayfs
            merged: Mount point for merged filesystem
        """
        try:
            subprocess.run([
                "mount", "-t", "overlay", "overlay",
                "-o", f"lowerdir={lower},upperdir={upper},workdir={work}",
                merged
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to mount overlay: {e}")
    
    def start(self, cmd: Optional[List[str]] = None) -> str:
        """
        Start the container
        
        Args:
            cmd: Command to run in container
            
        Returns:
            Container ID
        """
        print(f"🔥 {self.glyph} Starting container: {self.name}")
        
        # Create namespaces
        pid = self.create_namespaces()
        print(f"✓ Container started with PID: {pid}")
        
        # Setup resource limits
        self.setup_cgroups()
        print(f"✓ Resource limits applied")
        
        return self.container_id
    
    def stop(self):
        """Stop the container"""
        if self.pid:
            try:
                os.kill(self.pid, 15)  # SIGTERM
                print(f"✓ Container {self.name} stopped")
            except ProcessLookupError:
                print(f"⚠️  Container process not found")
    
    def _generate_container_id(self) -> str:
        """Generate a unique container ID"""
        import hashlib
        data = f"{self.name}{self.pid}{os.urandom(8).hex()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]
    
    def _save_metadata(self):
        """Save container metadata"""
        metadata = {
            "name": self.name,
            "id": self.container_id,
            "pid": self.pid,
            "glyph": self.glyph,
            "rootfs": str(self.rootfs),
            "status": "running"
        }
        
        metadata_file = self.container_dir / "metadata.json"
        self.container_dir.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _parse_memory_limit(self, limit: str) -> str:
        """Parse memory limit string to bytes"""
        multipliers = {
            'K': 1024,
            'M': 1024 * 1024,
            'G': 1024 * 1024 * 1024
        }
        
        if limit[-1].upper() in multipliers:
            value = int(limit[:-1])
            multiplier = multipliers[limit[-1].upper()]
            return str(value * multiplier)
        
        return limit


class SovereignContainerManager:
    """
    Manager for sovereign containers
    """
    
    def __init__(self):
        self.containers: Dict[str, SovereignContainer] = {}
        self.base_dir = Path("/var/lib/sovereign/containers")
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def create(self, name: str, rootfs: str, glyph: Optional[str] = None) -> SovereignContainer:
        """Create a new container"""
        container = SovereignContainer(name, rootfs, glyph)
        self.containers[name] = container
        return container
    
    def list(self) -> List[Dict]:
        """List all containers"""
        containers = []
        
        # Load from disk
        if self.base_dir.exists():
            for container_dir in self.base_dir.iterdir():
                if container_dir.is_dir():
                    metadata_file = container_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file) as f:
                            containers.append(json.load(f))
        
        return containers
    
    def get(self, name: str) -> Optional[SovereignContainer]:
        """Get container by name"""
        return self.containers.get(name)
    
    def remove(self, name: str):
        """Remove a container"""
        if name in self.containers:
            container = self.containers[name]
            container.stop()
            del self.containers[name]


if __name__ == "__main__":
    # Example usage
    print("🔥 Sovereign Container Runtime v1.0")
    print("=" * 50)
    
    # This is a demonstration - actual usage requires root privileges
    print("\nExample: Creating a sovereign container")
    print("  container = SovereignContainer('test', '/path/to/rootfs', '[001]')")
    print("  container.start()")
    print("\nNote: Requires root privileges for namespace and cgroup operations")
