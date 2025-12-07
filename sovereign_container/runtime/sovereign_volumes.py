#!/usr/bin/env python3
"""
Sovereign Volume Management - Direct filesystem mounts
No dependency on Docker volume drivers

This provides persistent storage for sovereign containers:
- Named volumes
- Bind mounts
- Encrypted volumes (LUKS)
- Backup and restore
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Optional, List
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignVolume:
    """
    Sovereign Volume Management - Docker-free volume handling
    """
    
    def __init__(self, name: str):
        """
        Initialize sovereign volume
        
        Args:
            name: Volume name
        """
        self.name = name
        self.volume_path = Path(f"/var/lib/sovereign/volumes/{name}")
        self.volume_path.mkdir(parents=True, exist_ok=True)
        
        # Volume metadata
        self.metadata_file = self.volume_path / "metadata.json"
        
    def mount_to_container(self, container_path: str):
        """
        Bind mount volume into container namespace
        
        Args:
            container_path: Path inside container to mount volume
        """
        logger.info(f"Mounting volume {self.name} to {container_path}")
        
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
    
    def unmount(self, container_path: str):
        """
        Unmount volume from container
        
        Args:
            container_path: Path inside container where volume is mounted
        """
        logger.info(f"Unmounting volume from {container_path}")
        
        try:
            subprocess.run([
                "umount", container_path
            ], check=True)
            logger.info(f"Volume unmounted successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to unmount volume: {e}")
            raise
    
    def create_encrypted_volume(self, passphrase: str, size_mb: int = 1024):
        """
        LUKS-encrypted sovereign volumes
        
        Creates an encrypted volume using dm-crypt/LUKS for data at rest encryption.
        
        Args:
            passphrase: Encryption passphrase
            size_mb: Volume size in MB
        """
        logger.info(f"Creating encrypted volume: {self.name}")
        
        # Create backing file
        backing_file = self.volume_path / "encrypted.img"
        
        try:
            # Create sparse file
            subprocess.run([
                "dd", "if=/dev/zero",
                f"of={backing_file}",
                "bs=1M",
                f"count={size_mb}",
                "status=none"
            ], check=True)
            
            # Setup loop device
            result = subprocess.run([
                "losetup", "--find", "--show", str(backing_file)
            ], capture_output=True, text=True, check=True)
            
            loop_device = result.stdout.strip()
            logger.info(f"Loop device created: {loop_device}")
            
            # Format with LUKS
            # Security note: Using temporary key file with restricted permissions
            # to avoid exposing passphrase in process arguments or stdin
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.key') as keyfile:
                keyfile_path = keyfile.name
                keyfile.write(passphrase)
            
            try:
                # Restrict key file permissions
                os.chmod(keyfile_path, 0o600)
                
                subprocess.run([
                    "cryptsetup", "luksFormat",
                    loop_device,
                    f"--key-file={keyfile_path}"
                ], check=True)
                
                # Open LUKS volume
                subprocess.run([
                    "cryptsetup", "open",
                    loop_device,
                    f"sovereign_{self.name}",
                    f"--key-file={keyfile_path}"
                ], check=True)
            finally:
                # Securely delete key file
                if os.path.exists(keyfile_path):
                    os.remove(keyfile_path)
            
            # Create filesystem
            subprocess.run([
                "mkfs.ext4",
                f"/dev/mapper/sovereign_{self.name}"
            ], check=True)
            
            # Mount it
            mount_point = self.volume_path / "data"
            mount_point.mkdir(exist_ok=True)
            
            subprocess.run([
                "mount",
                f"/dev/mapper/sovereign_{self.name}",
                str(mount_point)
            ], check=True)
            
            # Save metadata
            metadata = {
                'name': self.name,
                'encrypted': True,
                'backing_file': str(backing_file),
                'loop_device': loop_device,
                'size_mb': size_mb,
                'mount_point': str(mount_point)
            }
            
            self.metadata_file.write_text(json.dumps(metadata, indent=2))
            logger.info(f"Encrypted volume created and mounted")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create encrypted volume: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating encrypted volume: {e}")
            raise
    
    def backup(self, backup_path: str):
        """
        Backup volume to tarball
        
        Args:
            backup_path: Path to save backup
        """
        logger.info(f"Backing up volume: {self.name}")
        
        import tarfile
        
        with tarfile.open(backup_path, 'w:gz') as tar:
            tar.add(str(self.volume_path), arcname=self.name)
        
        logger.info(f"Volume backed up to: {backup_path}")
    
    def restore(self, backup_path: str):
        """
        Restore volume from tarball
        
        Args:
            backup_path: Path to backup file
        """
        logger.info(f"Restoring volume: {self.name}")
        
        import tarfile
        
        # Remove existing volume
        if self.volume_path.exists():
            shutil.rmtree(self.volume_path)
        
        # Extract backup
        with tarfile.open(backup_path, 'r:gz') as tar:
            tar.extractall(self.volume_path.parent)
        
        logger.info(f"Volume restored from: {backup_path}")
    
    def get_info(self) -> Dict:
        """Get volume information"""
        info = {
            'name': self.name,
            'path': str(self.volume_path),
            'exists': self.volume_path.exists(),
        }
        
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
            info.update(metadata)
        
        # Get size
        if self.volume_path.exists():
            total_size = sum(
                f.stat().st_size 
                for f in self.volume_path.rglob('*') 
                if f.is_file()
            )
            info['size_bytes'] = total_size
            info['size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return info
    
    def delete(self):
        """Delete the volume"""
        logger.info(f"Deleting volume: {self.name}")
        
        # Check if it's encrypted and needs cleanup
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
            if metadata.get('encrypted'):
                # Unmount and close LUKS
                try:
                    subprocess.run([
                        "umount",
                        metadata['mount_point']
                    ], check=False)
                    
                    subprocess.run([
                        "cryptsetup", "close",
                        f"sovereign_{self.name}"
                    ], check=False)
                    
                    subprocess.run([
                        "losetup", "-d",
                        metadata['loop_device']
                    ], check=False)
                except Exception as e:
                    logger.warning(f"Cleanup warning: {e}")
        
        # Remove volume directory
        if self.volume_path.exists():
            shutil.rmtree(self.volume_path)
        
        logger.info(f"Volume deleted: {self.name}")


def list_volumes() -> List[Dict]:
    """List all sovereign volumes"""
    volumes_dir = Path("/var/lib/sovereign/volumes")
    
    if not volumes_dir.exists():
        return []
    
    volumes = []
    for volume_dir in volumes_dir.iterdir():
        if volume_dir.is_dir():
            volume = SovereignVolume(volume_dir.name)
            volumes.append(volume.get_info())
    
    return volumes


if __name__ == "__main__":
    print("🔥 Sovereign Volume Management - Phase 1")
    print("=" * 50)
    
    # Example usage
    volume = SovereignVolume("test_volume")
    print(f"Volume created: {volume.name}")
    print(f"Info: {volume.get_info()}")
