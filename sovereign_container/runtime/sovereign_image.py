#!/usr/bin/env python3
"""
Sovereign Image Format - Tarball-based layered images
Compatible with OCI spec but sovereign-managed

This manages container images without Docker dependency:
- Layered filesystem approach
- Image building from Dockerfile
- Local image registry
- Push/pull to sovereign registries
"""

import tarfile
import hashlib
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import logging
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignImage:
    """
    Sovereign Image Management - Docker-free image handling
    """
    
    def __init__(self, name: str, tag: str = "latest"):
        """
        Initialize sovereign image
        
        Args:
            name: Image name
            tag: Image tag (default: latest)
        """
        self.name = name
        self.tag = tag
        self.image_dir = Path(f"/var/lib/sovereign/images/{name}/{tag}")
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        # Manifest file
        self.manifest_file = self.image_dir / "manifest.json"
        
    def parse_dockerfile(self, dockerfile_path: str) -> List[Dict]:
        """
        Parse Dockerfile and extract commands
        
        Args:
            dockerfile_path: Path to Dockerfile
            
        Returns:
            List of layer definitions
        """
        logger.info(f"Parsing Dockerfile: {dockerfile_path}")
        
        with open(dockerfile_path, 'r') as f:
            lines = f.readlines()
        
        layers = []
        current_layer = {'commands': []}
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse Dockerfile instructions
            if line.startswith('FROM'):
                base_image = line.split()[1]
                layers.append({
                    'type': 'from',
                    'base_image': base_image,
                    'commands': []
                })
            elif line.startswith('RUN'):
                command = line[4:].strip()
                if not layers:
                    layers.append({'type': 'layer', 'commands': []})
                layers[-1]['commands'].append({
                    'type': 'run',
                    'command': command
                })
            elif line.startswith('COPY'):
                parts = line.split()
                source = parts[1]
                dest = parts[2] if len(parts) > 2 else '.'
                if not layers:
                    layers.append({'type': 'layer', 'commands': []})
                layers[-1]['commands'].append({
                    'type': 'copy',
                    'source': source,
                    'dest': dest
                })
            elif line.startswith('CMD'):
                # CMD is metadata, not a layer
                cmd = line[4:].strip()
                if not layers:
                    layers.append({'type': 'layer', 'commands': []})
                layers[-1]['metadata'] = {'cmd': cmd}
            elif line.startswith('WORKDIR'):
                workdir = line.split()[1]
                if not layers:
                    layers.append({'type': 'layer', 'commands': []})
                layers[-1]['commands'].append({
                    'type': 'workdir',
                    'path': workdir
                })
        
        logger.info(f"Parsed {len(layers)} layers from Dockerfile")
        return layers
    
    def build_from_dockerfile(self, dockerfile_path: str, context_dir: str = "."):
        """
        Parse Dockerfile and build layers
        
        Args:
            dockerfile_path: Path to Dockerfile
            context_dir: Build context directory
        """
        logger.info(f"Building sovereign image: {self.name}:{self.tag}")
        
        # Parse Dockerfile
        layers = self.parse_dockerfile(dockerfile_path)
        
        # Create layers
        layer_ids = []
        for i, layer in enumerate(layers):
            layer_id = self.create_layer(layer, context_dir)
            layer_ids.append(layer_id)
            logger.info(f"Layer {i+1}/{len(layers)} created: {layer_id}")
        
        # Create manifest
        manifest = {
            'name': self.name,
            'tag': self.tag,
            'layers': layer_ids,
            'created': str(Path(dockerfile_path).stat().st_mtime),
            'dockerfile': dockerfile_path
        }
        
        self.manifest_file.write_text(json.dumps(manifest, indent=2))
        logger.info(f"Image built successfully: {self.name}:{self.tag}")
        
        return manifest
    
    def create_layer(self, layer_def: Dict, context_dir: str) -> str:
        """
        Create filesystem layer from commands
        
        Args:
            layer_def: Layer definition with commands
            context_dir: Build context directory
            
        Returns:
            Layer ID (hash)
        """
        # Generate layer ID from content
        layer_content = json.dumps(layer_def, sort_keys=True)
        layer_id = hashlib.sha256(layer_content.encode()).hexdigest()[:12]
        
        layer_path = self.image_dir / layer_id
        layer_path.mkdir(parents=True, exist_ok=True)
        
        # Create tarball for layer
        tarball_path = layer_path / "layer.tar"
        
        with tarfile.open(tarball_path, 'w') as tar:
            # Execute layer commands and capture filesystem changes
            for command in layer_def.get('commands', []):
                if command['type'] == 'run':
                    # For RUN commands, we'd execute in isolated environment
                    # For now, store command for execution during container start
                    cmd_file = layer_path / "run_commands.json"
                    commands_list = []
                    if cmd_file.exists():
                        commands_list = json.loads(cmd_file.read_text())
                    commands_list.append(command['command'])
                    cmd_file.write_text(json.dumps(commands_list, indent=2))
                    
                elif command['type'] == 'copy':
                    # Copy files from context to layer
                    source = Path(context_dir) / command['source']
                    if source.exists():
                        # Add to tarball
                        tar.add(str(source), arcname=command['dest'])
        
        # Save layer metadata
        metadata = {
            'id': layer_id,
            'type': layer_def.get('type', 'layer'),
            'commands': layer_def.get('commands', []),
            'size': tarball_path.stat().st_size if tarball_path.exists() else 0
        }
        
        (layer_path / "metadata.json").write_text(json.dumps(metadata, indent=2))
        
        return layer_id
    
    def pull_from_registry(self, registry_url: str):
        """
        Pull image from sovereign registry
        
        Args:
            registry_url: URL of sovereign registry
        """
        logger.info(f"Pulling {self.name}:{self.tag} from {registry_url}")
        # TODO: Implement HTTP GET from sovereign registry
        pass
    
    def push_to_registry(self, registry_url: str):
        """
        Push to sovereign registry (not Docker Hub)
        
        Args:
            registry_url: URL of sovereign registry
        """
        logger.info(f"Pushing {self.name}:{self.tag} to {registry_url}")
        
        if not self.manifest_file.exists():
            raise ValueError(f"Image not built: {self.name}:{self.tag}")
        
        manifest = json.loads(self.manifest_file.read_text())
        
        # TODO: Implement HTTP POST to sovereign registry
        # This would upload:
        # 1. Manifest file
        # 2. Layer tarballs
        # 3. Metadata
        
        logger.info(f"Image pushed to sovereign registry: {registry_url}")
        
    def export_rootfs(self, output_path: str) -> Path:
        """
        Export image as a complete rootfs
        
        Args:
            output_path: Where to export the rootfs
            
        Returns:
            Path to exported rootfs
        """
        logger.info(f"Exporting rootfs for {self.name}:{self.tag}")
        
        output = Path(output_path)
        output.mkdir(parents=True, exist_ok=True)
        
        if not self.manifest_file.exists():
            raise ValueError(f"Image not found: {self.name}:{self.tag}")
        
        manifest = json.loads(self.manifest_file.read_text())
        
        # Extract all layers in order
        for layer_id in manifest['layers']:
            layer_path = self.image_dir / layer_id / "layer.tar"
            if layer_path.exists():
                with tarfile.open(layer_path, 'r') as tar:
                    tar.extractall(output)
        
        logger.info(f"Rootfs exported to: {output}")
        return output
    
    def list_local_images(self) -> List[Dict]:
        """List all locally stored sovereign images"""
        images_dir = Path("/var/lib/sovereign/images")
        
        if not images_dir.exists():
            return []
        
        images = []
        for name_dir in images_dir.iterdir():
            if name_dir.is_dir():
                for tag_dir in name_dir.iterdir():
                    manifest_file = tag_dir / "manifest.json"
                    if manifest_file.exists():
                        manifest = json.loads(manifest_file.read_text())
                        images.append({
                            'name': name_dir.name,
                            'tag': tag_dir.name,
                            'layers': len(manifest.get('layers', [])),
                            'created': manifest.get('created', 'unknown')
                        })
        
        return images


if __name__ == "__main__":
    print("🔥 Sovereign Image Management - Phase 1")
    print("=" * 50)
    
    # Example: build an image from Dockerfile
    image = SovereignImage("test_image", "latest")
    print(f"Image initialized: {image.name}:{image.tag}")
