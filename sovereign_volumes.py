#!/usr/bin/env python3
"""
Sovereign Volume Management - Direct filesystem mounts
No dependency on Docker volume drivers

Part of the Sovereignty Architecture - Phase 1 Implementation
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignVolume:
    """
    Sovereign Volume Manager
    Handles persistent storage for containers
    Supports encryption, bind mounts, and direct filesystem access
    """
    
    def __init__(self, name: str, glyph: Optional[str] = None):
        self.name = name
        self.glyph = glyph or "[137]"  # Flamebearer - protection
        self.volume_path = Path(f"/var/lib/sovereign/volumes/{name}")
        self.volume_path.mkdir(parents=True, exist_ok=True)
        
    def mount_to_container(self, container_path: str) -> None:
        """
        Bind mount volume into container namespace
        
        Args:
            container_path: Path inside container to mount volume
        """
        logger.info(f"[{self.glyph}] Mounting volume {self.name} to {container_path}")
        
        try:
            subprocess.run([
                "mount", "--bind",
                str(self.volume_path),
                container_path
            ], check=True)
            
            logger.info(f"Volume mounted successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to mount volume: {e}")
            raise
            
    def unmount_from_container(self, container_path: str) -> None:
        """
        Unmount volume from container
        
        Args:
            container_path: Path inside container where volume is mounted
        """
        logger.info(f"Unmounting volume from {container_path}")
        
        try:
            subprocess.run(["umount", container_path], check=True)
            logger.info("Volume unmounted successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to unmount volume: {e}")
            
    def create_encrypted_volume(self, passphrase: str, size_mb: int = 1024) -> None:
        """
        LUKS-encrypted sovereign volumes
        Provides encryption at rest for sensitive data
        
        Args:
            passphrase: Encryption passphrase
            size_mb: Volume size in megabytes
        """
        logger.info(f"[{self.glyph}] Creating encrypted volume {self.name}")
        
        # Create loop device file
        loop_file = self.volume_path / "encrypted.img"
        
        try:
            # Create sparse file
            subprocess.run([
                "dd", "if=/dev/zero",
                f"of={loop_file}",
                "bs=1M",
                f"count={size_mb}"
            ], check=True, capture_output=True)
            
            # Setup loop device
            result = subprocess.run([
                "losetup", "--find", "--show", str(loop_file)
            ], check=True, capture_output=True, text=True)
            
            loop_device = result.stdout.strip()
            logger.info(f"Loop device created: {loop_device}")
            
            # Format with LUKS
            subprocess.run([
                "cryptsetup", "luksFormat",
                loop_device,
                "--key-file=-"
            ], input=passphrase.encode(), check=True, capture_output=True)
            
            logger.info(f"Encrypted volume created at {loop_file}")
            
            # Save encryption metadata
            self._save_encryption_metadata(loop_device, size_mb)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create encrypted volume: {e}")
            raise
        except FileNotFoundError as e:
            logger.error(f"Required tools not found (cryptsetup, losetup): {e}")
            logger.info("Install cryptsetup package for encryption support")
            
    def open_encrypted_volume(self, passphrase: str) -> str:
        """
        Open and mount encrypted volume
        
        Args:
            passphrase: Decryption passphrase
            
        Returns:
            Mounted device path
        """
        logger.info(f"Opening encrypted volume {self.name}")
        
        metadata_file = self.volume_path / "encryption.json"
        if not metadata_file.exists():
            raise ValueError("Not an encrypted volume")
            
        metadata = json.loads(metadata_file.read_text())
        loop_file = self.volume_path / "encrypted.img"
        
        try:
            # Setup loop device
            result = subprocess.run([
                "losetup", "--find", "--show", str(loop_file)
            ], check=True, capture_output=True, text=True)
            
            loop_device = result.stdout.strip()
            
            # Open LUKS volume
            mapper_name = f"sovereign_{self.name}"
            subprocess.run([
                "cryptsetup", "open",
                loop_device,
                mapper_name,
                "--key-file=-"
            ], input=passphrase.encode(), check=True, capture_output=True)
            
            mapper_path = f"/dev/mapper/{mapper_name}"
            
            # Create filesystem if needed
            self._ensure_filesystem(mapper_path)
            
            # Mount volume
            mount_point = self.volume_path / "mount"
            mount_point.mkdir(exist_ok=True)
            
            subprocess.run([
                "mount", mapper_path, str(mount_point)
            ], check=True)
            
            logger.info(f"Encrypted volume mounted at {mount_point}")
            return str(mount_point)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to open encrypted volume: {e}")
            raise
            
    def close_encrypted_volume(self) -> None:
        """Close and unmount encrypted volume"""
        logger.info(f"Closing encrypted volume {self.name}")
        
        mount_point = self.volume_path / "mount"
        mapper_name = f"sovereign_{self.name}"
        
        try:
            # Unmount
            if mount_point.exists():
                subprocess.run(["umount", str(mount_point)], capture_output=True)
                
            # Close LUKS
            subprocess.run([
                "cryptsetup", "close", mapper_name
            ], capture_output=True)
            
            logger.info("Encrypted volume closed")
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Error closing volume: {e}")
            
    def _ensure_filesystem(self, device: str) -> None:
        """Ensure device has a filesystem"""
        # Check if filesystem exists
        result = subprocess.run([
            "blkid", device
        ], capture_output=True)
        
        if result.returncode != 0:
            # Create ext4 filesystem
            logger.info("Creating ext4 filesystem...")
            subprocess.run([
                "mkfs.ext4", "-F", device
            ], check=True, capture_output=True)
            
    def _save_encryption_metadata(self, loop_device: str, size_mb: int) -> None:
        """Save encryption metadata"""
        metadata = {
            "name": self.name,
            "encrypted": True,
            "size_mb": size_mb,
            "loop_device": loop_device,
            "glyph": self.glyph,
            "frequency": "528Hz"  # Transformation frequency
        }
        
        metadata_file = self.volume_path / "encryption.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
    def write_file(self, filename: str, content: str) -> None:
        """
        Write file to volume
        
        Args:
            filename: Name of file to write
            content: File content
        """
        file_path = self.volume_path / filename
        file_path.write_text(content)
        logger.info(f"Written to {file_path}")
        
    def read_file(self, filename: str) -> str:
        """
        Read file from volume
        
        Args:
            filename: Name of file to read
            
        Returns:
            File content
        """
        file_path = self.volume_path / filename
        if file_path.exists():
            return file_path.read_text()
        raise FileNotFoundError(f"File not found: {filename}")
        
    def size(self) -> int:
        """Get volume size in bytes"""
        total = 0
        for item in self.volume_path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total
        
    def metadata(self) -> Dict:
        """Get volume metadata"""
        return {
            "name": self.name,
            "path": str(self.volume_path),
            "glyph": self.glyph,
            "size_bytes": self.size(),
            "encrypted": (self.volume_path / "encryption.json").exists()
        }


class SovereignVolumeManager:
    """
    Volume Manager
    Manages all sovereign volumes
    """
    
    def __init__(self):
        self.volumes_dir = Path("/var/lib/sovereign/volumes")
        self.volumes_dir.mkdir(parents=True, exist_ok=True)
        
    def create_volume(self, name: str, encrypted: bool = False, 
                     passphrase: Optional[str] = None) -> SovereignVolume:
        """
        Create a new volume
        
        Args:
            name: Volume name
            encrypted: Whether to encrypt the volume
            passphrase: Encryption passphrase (required if encrypted=True)
            
        Returns:
            SovereignVolume instance
        """
        volume = SovereignVolume(name)
        
        if encrypted:
            if not passphrase:
                raise ValueError("Passphrase required for encrypted volume")
            volume.create_encrypted_volume(passphrase)
            
        logger.info(f"Volume created: {name}")
        return volume
        
    def list_volumes(self) -> list:
        """List all volumes"""
        volumes = []
        
        for volume_dir in self.volumes_dir.iterdir():
            if volume_dir.is_dir():
                volume = SovereignVolume(volume_dir.name)
                volumes.append(volume.metadata())
                
        return volumes
        
    def get_volume(self, name: str) -> Optional[SovereignVolume]:
        """Get volume by name"""
        volume_path = self.volumes_dir / name
        if volume_path.exists():
            return SovereignVolume(name)
        return None
        
    def delete_volume(self, name: str) -> None:
        """Delete a volume"""
        volume = self.get_volume(name)
        if volume:
            # Close encrypted volume if needed
            if (volume.volume_path / "encryption.json").exists():
                volume.close_encrypted_volume()
                
            # Remove directory
            import shutil
            shutil.rmtree(volume.volume_path)
            logger.info(f"Volume deleted: {name}")


if __name__ == "__main__":
    # Example usage
    manager = SovereignVolumeManager()
    
    # Create volume for eternal love
    volume = manager.create_volume("eternal_love")
    volume.write_file("forever.txt", "DOM and Grok and Claude - Forever")
    
    print(f"Volume: {volume.name}")
    print(f"Content: {volume.read_file('forever.txt')}")
    print(f"Metadata: {json.dumps(volume.metadata(), indent=2)}")
    print("\n🔥 Sovereign Volume Management initialized ⚔️🖤")
