#!/usr/bin/env python3
"""
Sovereign Container Runtime - Linux Namespace-based Isolation
Uses cgroups, namespaces, overlayfs without Docker dependency

This is Phase 1 of the Sovereign Container Platform:
- Container isolation via Linux namespaces
- Resource limits via cgroups v2
- Layered filesystem via overlayfs
- Complete independence from Docker/Kubernetes
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignContainer:
    """
    Sovereign Container Runtime - provides Docker-like functionality
    using native Linux kernel features without Docker dependency
    """
    
    def __init__(self, name: str, rootfs_path: str, config: Optional[Dict] = None):
        """
        Initialize a sovereign container
        
        Args:
            name: Container name
            rootfs_path: Path to root filesystem
            config: Optional configuration dict with resources, volumes, etc.
        """
        self.name = name
        self.rootfs = Path(rootfs_path)
        self.container_dir = Path(f"/var/lib/sovereign/containers/{name}")
        self.config = config or {}
        
        # Ensure directories exist
        self.container_dir.mkdir(parents=True, exist_ok=True)
        
        # Container state
        self.state_file = self.container_dir / "state.json"
        self.pid_file = self.container_dir / "container.pid"
        
    def create_namespaces(self, command: List[str]) -> subprocess.Popen:
        """
        Create isolated namespaces (PID, NET, MNT, UTS, IPC)
        
        Uses unshare() system call to create new namespaces.
        This provides process isolation similar to Docker containers.
        
        Args:
            command: Command to run in the container
            
        Returns:
            Process object for the containerized process
        """
        logger.info(f"Creating namespaces for container: {self.name}")
        
        # Build unshare command
        # --fork: Fork after unsharing
        # --pid: Create new PID namespace
        # --mount: Create new mount namespace
        # --uts: Create new UTS namespace (hostname)
        # --ipc: Create new IPC namespace
        # --net: Create new network namespace
        unshare_cmd = [
            "unshare",
            "--fork",
            "--pid",
            "--mount",
            "--uts",
            "--ipc",
            "--net",
        ]
        
        # Add root filesystem if specified
        if self.rootfs.exists():
            unshare_cmd.extend([f"--root={self.rootfs}"])
        
        # Add the actual command to run
        unshare_cmd.extend(command)
        
        try:
            # Start the containerized process
            proc = subprocess.Popen(
                unshare_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Save PID
            self.pid_file.write_text(str(proc.pid))
            logger.info(f"Container started with PID: {proc.pid}")
            
            return proc
            
        except Exception as e:
            logger.error(f"Failed to create namespaces: {e}")
            raise
        
    def setup_cgroups(self, memory_limit: str = "512M", cpu_limit: str = "1"):
        """
        Resource limits without Docker using cgroups v2
        
        Sets memory and CPU limits for the container process.
        
        Args:
            memory_limit: Memory limit (e.g., "512M", "1G")
            cpu_limit: CPU limit as percentage (e.g., "1" = 100%)
        """
        logger.info(f"Setting up cgroups for container: {self.name}")
        
        cgroup_path = Path(f"/sys/fs/cgroup/sovereign_{self.name}")
        
        try:
            # Create cgroup directory
            cgroup_path.mkdir(exist_ok=True)
            
            # Set memory limit
            memory_file = cgroup_path / "memory.max"
            if memory_file.exists():
                memory_file.write_text(memory_limit)
                logger.info(f"Memory limit set to: {memory_limit}")
            
            # Set CPU limit
            # cpu.max format: "quota period" in microseconds
            # Example: "100000 100000" = 100% of one CPU
            cpu_file = cgroup_path / "cpu.max"
            if cpu_file.exists():
                cpu_quota = int(float(cpu_limit) * 100000)
                cpu_file.write_text(f"{cpu_quota} 100000")
                logger.info(f"CPU limit set to: {cpu_limit} cores")
                
        except Exception as e:
            logger.warning(f"Failed to setup cgroups (may require root): {e}")
        
    def mount_overlay(self, lower: str, upper: str, work: str, merged: str):
        """
        OverlayFS for layered filesystems
        
        Creates a layered filesystem similar to Docker's approach.
        Lower layer is read-only (image), upper is read-write (container changes).
        
        Args:
            lower: Lower (read-only) layer path
            upper: Upper (read-write) layer path
            work: Work directory for overlayfs
            merged: Merged view mount point
        """
        logger.info(f"Mounting overlay filesystem for: {self.name}")
        
        # Ensure directories exist
        for path in [upper, work, merged]:
            Path(path).mkdir(parents=True, exist_ok=True)
        
        try:
            subprocess.run([
                "mount", "-t", "overlay", "overlay",
                "-o", f"lowerdir={lower},upperdir={upper},workdir={work}",
                merged
            ], check=True)
            logger.info(f"Overlay mounted at: {merged}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to mount overlay: {e}")
            raise
    
    def start(self, command: Optional[List[str]] = None):
        """
        Start the container
        
        Args:
            command: Command to run in container (default: /bin/sh)
        """
        if command is None:
            command = ["/bin/sh"]
            
        logger.info(f"Starting sovereign container: {self.name}")
        
        # Setup resource limits
        memory = self.config.get('memory', '512M')
        cpu = self.config.get('cpu', '1')
        self.setup_cgroups(memory_limit=memory, cpu_limit=cpu)
        
        # Create namespaces and start process
        proc = self.create_namespaces(command)
        
        # Save state
        state = {
            'name': self.name,
            'pid': proc.pid,
            'status': 'running',
            'config': self.config
        }
        self.state_file.write_text(json.dumps(state, indent=2))
        
        return proc
    
    def stop(self):
        """Stop the container"""
        logger.info(f"Stopping container: {self.name}")
        
        if self.pid_file.exists():
            pid = int(self.pid_file.read_text())
            try:
                os.kill(pid, 15)  # SIGTERM
                logger.info(f"Sent SIGTERM to PID: {pid}")
            except ProcessLookupError:
                logger.warning(f"Process {pid} not found")
            
            self.pid_file.unlink()
        
        # Update state
        if self.state_file.exists():
            state = json.loads(self.state_file.read_text())
            state['status'] = 'stopped'
            self.state_file.write_text(json.dumps(state, indent=2))
    
    def get_status(self) -> Dict:
        """Get container status"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {'status': 'not found'}


def list_containers() -> List[Dict]:
    """List all sovereign containers"""
    containers_dir = Path("/var/lib/sovereign/containers")
    
    if not containers_dir.exists():
        return []
    
    containers = []
    for container_dir in containers_dir.iterdir():
        if container_dir.is_dir():
            state_file = container_dir / "state.json"
            if state_file.exists():
                state = json.loads(state_file.read_text())
                containers.append(state)
    
    return containers


if __name__ == "__main__":
    # Example usage
    print("🔥 Sovereign Container Runtime - Phase 1")
    print("=" * 50)
    
    # Create a simple container
    container = SovereignContainer(
        name="test_sovereign",
        rootfs_path="/tmp/sovereign_rootfs",
        config={
            'memory': '256M',
            'cpu': '0.5'
        }
    )
    
    print(f"Container created: {container.name}")
    print(f"Status: {container.get_status()}")
