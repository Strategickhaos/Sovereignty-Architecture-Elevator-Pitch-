#!/usr/bin/env python3
"""
Sovereign Container Runtime - Linux Namespace-based Isolation
Uses cgroups, namespaces, overlayfs without Docker dependency

Part of the Sovereignty Architecture - Phase 1 Implementation
"""

import os
import subprocess
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignContainer:
    """
    Sovereign Container Runtime
    Provides container isolation using Linux kernel primitives directly
    No dependency on Docker Engine or containerd
    """
    
    def __init__(self, name: str, rootfs_path: str, glyph: Optional[str] = None):
        self.name = name
        self.rootfs = Path(rootfs_path)
        self.container_dir = Path(f"/var/lib/sovereign/containers/{name}")
        self.glyph = glyph or "[001]"  # Default: Aether Prime
        self.container_id = self._generate_id()
        
        # Ensure directories exist
        self.container_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_id(self) -> str:
        """Generate unique container ID"""
        content = f"{self.name}{self.rootfs}{os.getpid()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]
        
    def create_namespaces(self, command: str = "/bin/sh") -> int:
        """
        Create isolated namespaces (PID, NET, MNT, UTS, IPC)
        Uses unshare() system call for container isolation
        
        Returns:
            Process ID of the container init process
        """
        logger.info(f"[{self.glyph}] Creating namespaces for container {self.name}")
        
        try:
            # Create namespace isolation
            result = subprocess.Popen([
                "unshare",
                "--fork",           # Fork to create new PID namespace
                "--pid",            # New PID namespace
                "--mount",          # New mount namespace
                "--uts",            # New UTS namespace (hostname)
                "--ipc",            # New IPC namespace
                "--net",            # New network namespace
                f"--root={self.rootfs}",  # Change root to container filesystem
                command
            ])
            
            logger.info(f"Container {self.name} started with PID {result.pid}")
            return result.pid
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create namespaces: {e}")
            raise
            
    def setup_cgroups(self, memory_limit: str = "512M", cpu_limit: str = "1") -> None:
        """
        Setup cgroups for resource limits without Docker
        
        Args:
            memory_limit: Memory limit (e.g., "512M", "1G")
            cpu_limit: CPU limit (number of CPUs)
        """
        logger.info(f"[{self.glyph}] Setting up cgroups for {self.name}")
        
        cgroup_base = Path("/sys/fs/cgroup")
        if not cgroup_base.exists():
            logger.warning("cgroups v2 not available, skipping resource limits")
            return
            
        cgroup_path = cgroup_base / f"sovereign_{self.name}"
        
        try:
            cgroup_path.mkdir(exist_ok=True)
            
            # Memory limit (cgroups v2)
            memory_max = cgroup_path / "memory.max"
            if memory_max.parent.exists():
                memory_bytes = self._parse_memory_limit(memory_limit)
                memory_max.write_text(str(memory_bytes))
                logger.info(f"Memory limit set to {memory_limit}")
            
            # CPU limit (cgroups v2)
            cpu_max = cgroup_path / "cpu.max"
            if cpu_max.parent.exists():
                cpu_quota = int(float(cpu_limit) * 100000)
                cpu_max.write_text(f"{cpu_quota} 100000")
                logger.info(f"CPU limit set to {cpu_limit} cores")
                
        except PermissionError:
            logger.warning("Insufficient permissions for cgroup setup - run as root")
        except Exception as e:
            logger.error(f"Failed to setup cgroups: {e}")
            
    def _parse_memory_limit(self, limit: str) -> int:
        """Convert memory limit string to bytes"""
        units = {'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}
        
        if limit[-1] in units:
            return int(limit[:-1]) * units[limit[-1]]
        return int(limit)
        
    def mount_overlay(self, lower: str, upper: str, work: str, merged: str) -> None:
        """
        Setup OverlayFS for layered filesystems
        Enables copy-on-write container layers
        
        Args:
            lower: Lower (read-only) layer directory
            upper: Upper (writable) layer directory
            work: Work directory for overlayfs
            merged: Merged mount point
        """
        logger.info(f"[{self.glyph}] Mounting overlay filesystem")
        
        # Ensure directories exist
        for path in [lower, upper, work, merged]:
            Path(path).mkdir(parents=True, exist_ok=True)
        
        try:
            subprocess.run([
                "mount", "-t", "overlay", "overlay",
                "-o", f"lowerdir={lower},upperdir={upper},workdir={work}",
                merged
            ], check=True)
            
            logger.info(f"Overlay mounted at {merged}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to mount overlay: {e}")
            raise
            
    def start(self, command: List[str], volumes: Optional[Dict[str, str]] = None) -> int:
        """
        Start the sovereign container
        
        Args:
            command: Command to run in container
            volumes: Dict of host_path: container_path volume mounts
            
        Returns:
            Container process ID
        """
        logger.info(f"[{self.glyph}] Starting sovereign container: {self.name}")
        
        # Setup overlay filesystem
        lower = self.rootfs / "lower"
        upper = self.container_dir / "upper"
        work = self.container_dir / "work"
        merged = self.container_dir / "merged"
        
        self.mount_overlay(str(lower), str(upper), str(work), str(merged))
        
        # Setup cgroups for resource limits
        self.setup_cgroups()
        
        # Create namespaces and start container
        cmd_str = " ".join(command)
        pid = self.create_namespaces(cmd_str)
        
        # Save container metadata
        self._save_metadata(pid, command)
        
        return pid
        
    def _save_metadata(self, pid: int, command: List[str]) -> None:
        """Save container metadata to disk"""
        metadata = {
            "id": self.container_id,
            "name": self.name,
            "glyph": self.glyph,
            "pid": pid,
            "command": command,
            "rootfs": str(self.rootfs),
            "status": "running"
        }
        
        metadata_file = self.container_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
    def stop(self) -> None:
        """Stop the container"""
        logger.info(f"Stopping container {self.name}")
        
        metadata_file = self.container_dir / "metadata.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            pid = metadata.get("pid")
            
            if pid:
                try:
                    os.kill(pid, 15)  # SIGTERM
                    logger.info(f"Sent SIGTERM to PID {pid}")
                except ProcessLookupError:
                    logger.warning(f"Process {pid} not found")
                    
    def status(self) -> Dict:
        """Get container status"""
        metadata_file = self.container_dir / "metadata.json"
        
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        
        return {"status": "not_found"}


class SovereignRuntime:
    """
    Main Sovereign Container Runtime Manager
    Manages multiple containers and provides CLI interface
    """
    
    def __init__(self):
        self.base_dir = Path("/var/lib/sovereign")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def list_containers(self) -> List[Dict]:
        """List all containers"""
        containers = []
        containers_dir = self.base_dir / "containers"
        
        if not containers_dir.exists():
            return containers
            
        for container_dir in containers_dir.iterdir():
            if container_dir.is_dir():
                metadata_file = container_dir / "metadata.json"
                if metadata_file.exists():
                    containers.append(json.loads(metadata_file.read_text()))
                    
        return containers
        
    def get_container(self, name_or_id: str) -> Optional[SovereignContainer]:
        """Get container by name or ID"""
        for container_data in self.list_containers():
            if container_data["name"] == name_or_id or container_data["id"].startswith(name_or_id):
                return SovereignContainer(
                    container_data["name"],
                    container_data["rootfs"],
                    container_data.get("glyph")
                )
        return None


if __name__ == "__main__":
    # Example usage
    runtime = SovereignRuntime()
    
    # Create a container
    container = SovereignContainer(
        name="DOMandGrokLoveForever",
        rootfs_path="/var/lib/sovereign/rootfs/alpine",
        glyph="[001]"  # Aether Prime - initialization
    )
    
    print(f"Container ID: {container.container_id}")
    print(f"Container ready at: {container.container_dir}")
    print("\n🔥 Sovereign Container Runtime initialized ⚔️🖤")
