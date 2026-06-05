#!/usr/bin/env python3
"""
Sovereign Image Format - Tarball-based layered images
Compatible with OCI spec but sovereign-managed

Part of the Sovereignty Architecture - Phase 1 Implementation
"""

import tarfile
import hashlib
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SovereignImage:
    """
    Sovereign Image Format Manager
    Handles container image building, layering, and registry operations
    No dependency on Docker daemon or Docker Hub
    """
    
    def __init__(self, name: str, tag: str = "latest"):
        self.name = name
        self.tag = tag
        self.image_dir = Path(f"/var/lib/sovereign/images/{name}/{tag}")
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
    def build_from_dockerfile(self, dockerfile_path: str, context_path: str = ".") -> str:
        """
        Parse Dockerfile and build layers
        
        Args:
            dockerfile_path: Path to Dockerfile
            context_path: Build context directory
            
        Returns:
            Image ID (SHA256 hash)
        """
        logger.info(f"Building image {self.name}:{self.tag} from {dockerfile_path}")
        
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
            
        # Parse Dockerfile into layers
        layers = self.parse_dockerfile(dockerfile_content)
        
        # Build each layer
        for idx, layer in enumerate(layers):
            logger.info(f"Building layer {idx + 1}/{len(layers)}: {layer['instruction']}")
            self.create_layer(layer, context_path)
            
        # Generate image manifest
        image_id = self._generate_manifest(layers)
        
        logger.info(f"Image built successfully: {image_id}")
        return image_id
        
    def parse_dockerfile(self, content: str) -> List[Dict]:
        """
        Parse Dockerfile content into layer instructions
        
        Returns:
            List of layer dictionaries with instruction and args
        """
        layers = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
                
            # Parse instruction
            parts = line.split(None, 1)
            if len(parts) < 1:
                continue
                
            instruction = parts[0].upper()
            args = parts[1] if len(parts) > 1 else ""
            
            # Create layer for instructions that modify filesystem
            if instruction in ['FROM', 'RUN', 'COPY', 'ADD', 'WORKDIR', 'ENV', 'EXPOSE', 'CMD', 'ENTRYPOINT']:
                layers.append({
                    'instruction': instruction,
                    'args': args,
                    'raw': line
                })
                
        return layers
        
    def create_layer(self, layer: Dict, context_path: str) -> str:
        """
        Create filesystem layer from instruction
        
        Args:
            layer: Layer instruction dictionary
            context_path: Build context directory
            
        Returns:
            Layer ID (SHA256 hash)
        """
        instruction = layer['instruction']
        args = layer['args']
        
        # Generate layer ID
        layer_id = hashlib.sha256(layer['raw'].encode()).hexdigest()[:12]
        layer_path = self.image_dir / "layers" / layer_id
        layer_path.mkdir(parents=True, exist_ok=True)
        
        # Execute layer instruction
        if instruction == 'FROM':
            self._handle_from(args, layer_path)
        elif instruction == 'RUN':
            self._handle_run(args, layer_path)
        elif instruction == 'COPY':
            self._handle_copy(args, layer_path, context_path)
        elif instruction == 'ADD':
            self._handle_add(args, layer_path, context_path)
        elif instruction == 'WORKDIR':
            self._handle_workdir(args, layer_path)
        elif instruction == 'ENV':
            self._handle_env(args, layer_path)
        elif instruction == 'CMD':
            self._handle_cmd(args, layer_path)
        elif instruction == 'ENTRYPOINT':
            self._handle_entrypoint(args, layer_path)
            
        # Create layer tarball
        layer_tar = self.image_dir / "layers" / f"{layer_id}.tar"
        with tarfile.open(layer_tar, 'w') as tar:
            tar.add(layer_path, arcname='.')
            
        # Save layer metadata
        layer_metadata = {
            'id': layer_id,
            'instruction': instruction,
            'args': args,
            'size': layer_tar.stat().st_size
        }
        
        metadata_file = self.image_dir / "layers" / f"{layer_id}.json"
        metadata_file.write_text(json.dumps(layer_metadata, indent=2))
        
        return layer_id
        
    def _handle_from(self, args: str, layer_path: Path) -> None:
        """Handle FROM instruction - base image"""
        base_image = args.strip()
        logger.info(f"Base image: {base_image}")
        
        # For now, create empty base or reference existing rootfs
        # In production, this would pull from registry
        (layer_path / "rootfs").mkdir(exist_ok=True)
        
    def _handle_run(self, args: str, layer_path: Path) -> None:
        """Handle RUN instruction - execute command"""
        command = args.strip()
        logger.info(f"Executing: {command}")
        
        # Create script to document the command
        # In production, this would execute in isolated environment
        script_file = layer_path / "run.sh"
        script_file.write_text(f"#!/bin/sh\n{command}\n")
        script_file.chmod(0o755)
        
    def _handle_copy(self, args: str, layer_path: Path, context_path: str) -> None:
        """Handle COPY instruction"""
        parts = args.split()
        if len(parts) >= 2:
            src = parts[0]
            dst = parts[-1]
            
            src_path = Path(context_path) / src
            dst_path = layer_path / dst.lstrip('/')
            
            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                if src_path.is_dir():
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
                    
    def _handle_add(self, args: str, layer_path: Path, context_path: str) -> None:
        """Handle ADD instruction (similar to COPY)"""
        self._handle_copy(args, layer_path, context_path)
        
    def _handle_workdir(self, args: str, layer_path: Path) -> None:
        """Handle WORKDIR instruction"""
        workdir = args.strip()
        workdir_path = layer_path / workdir.lstrip('/')
        workdir_path.mkdir(parents=True, exist_ok=True)
        
    def _handle_env(self, args: str, layer_path: Path) -> None:
        """Handle ENV instruction"""
        env_file = layer_path / "env.sh"
        env_file.write_text(f"export {args}\n")
        
    def _handle_cmd(self, args: str, layer_path: Path) -> None:
        """Handle CMD instruction"""
        cmd_file = layer_path / "cmd.json"
        cmd_file.write_text(json.dumps({"cmd": args}))
        
    def _handle_entrypoint(self, args: str, layer_path: Path) -> None:
        """Handle ENTRYPOINT instruction"""
        entrypoint_file = layer_path / "entrypoint.json"
        entrypoint_file.write_text(json.dumps({"entrypoint": args}))
        
    def _generate_manifest(self, layers: List[Dict]) -> str:
        """Generate image manifest"""
        manifest = {
            "name": self.name,
            "tag": self.tag,
            "layers": [
                hashlib.sha256(layer['raw'].encode()).hexdigest()[:12]
                for layer in layers
            ],
            "config": {
                "glyph": "[001]",  # Aether Prime
                "frequency": "432Hz"  # Coherence
            }
        }
        
        manifest_file = self.image_dir / "manifest.json"
        manifest_file.write_text(json.dumps(manifest, indent=2))
        
        # Generate image ID from manifest
        image_id = hashlib.sha256(json.dumps(manifest).encode()).hexdigest()[:12]
        
        return image_id
        
    def push_to_registry(self, registry_url: str) -> None:
        """
        Push to sovereign registry (not Docker Hub)
        
        Args:
            registry_url: URL of sovereign registry
        """
        logger.info(f"Pushing {self.name}:{self.tag} to {registry_url}")
        
        # In production, this would:
        # 1. Authenticate with sovereign registry
        # 2. Upload layers as tarballs
        # 3. Upload manifest
        # 4. Verify integrity with SHA256
        
        # For now, just log the operation
        manifest_file = self.image_dir / "manifest.json"
        if manifest_file.exists():
            logger.info(f"Manifest ready for push: {manifest_file}")
        else:
            logger.error("No manifest found - build image first")
            
    def pull_from_registry(self, registry_url: str) -> None:
        """
        Pull from sovereign registry
        
        Args:
            registry_url: URL of sovereign registry
        """
        logger.info(f"Pulling {self.name}:{self.tag} from {registry_url}")
        
        # In production, this would:
        # 1. Authenticate with sovereign registry
        # 2. Download manifest
        # 3. Download layers
        # 4. Verify integrity
        # 5. Extract to local storage
        
        logger.info("Pull operation simulated - implement HTTP client in production")
        
    def export_tarball(self, output_path: str) -> None:
        """Export image as tarball"""
        logger.info(f"Exporting image to {output_path}")
        
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(self.image_dir, arcname=f"{self.name}-{self.tag}")
            
        logger.info(f"Image exported to {output_path}")


class SovereignImageRegistry:
    """
    Sovereign Image Registry
    HTTP-based registry for sovereign images
    No dependency on Docker Registry or external services
    """
    
    def __init__(self, registry_dir: str = "/var/lib/sovereign/registry"):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        
    def list_images(self) -> List[Dict]:
        """List all images in registry"""
        images = []
        images_dir = self.registry_dir / "images"
        
        if not images_dir.exists():
            return images
            
        for image_dir in images_dir.iterdir():
            if image_dir.is_dir():
                for tag_dir in image_dir.iterdir():
                    if tag_dir.is_dir():
                        manifest_file = tag_dir / "manifest.json"
                        if manifest_file.exists():
                            manifest = json.loads(manifest_file.read_text())
                            images.append(manifest)
                            
        return images


if __name__ == "__main__":
    # Example usage
    image = SovereignImage("dom-grok-love", "forever")
    
    print(f"Image: {image.name}:{image.tag}")
    print(f"Image directory: {image.image_dir}")
    print("\n🔥 Sovereign Image Format initialized ⚔️🖤")
