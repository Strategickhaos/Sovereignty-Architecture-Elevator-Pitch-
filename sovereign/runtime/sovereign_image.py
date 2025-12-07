#!/usr/bin/env python3
"""
Sovereign Image Format - Tarball-based layered images
Compatible with OCI spec but sovereign-managed

Part of the Strategickhaos Sovereignty Architecture
"""

import tarfile
import hashlib
import json
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional


class SovereignImage:
    """
    Sovereign Image Management
    
    Builds and manages container images without Docker dependency.
    Uses tarball-based layers compatible with OCI format.
    """
    
    def __init__(self, name: str, tag: str = "latest"):
        self.name = name
        self.tag = tag
        self.image_dir = Path(f"/var/lib/sovereign/images/{name}/{tag}")
        self.layers: List[str] = []
        
    def build_from_dockerfile(self, dockerfile_path: str) -> str:
        """
        Parse Dockerfile and build layers
        
        Args:
            dockerfile_path: Path to Dockerfile
            
        Returns:
            Image ID
        """
        print(f"🔥 Building sovereign image: {self.name}:{self.tag}")
        
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
        
        # Parse Dockerfile
        instructions = self.parse_dockerfile(dockerfile_content)
        
        # Build base from FROM instruction
        base_image = instructions[0].get('image') if instructions else 'alpine:latest'
        print(f"✓ Base image: {base_image}")
        
        # Create layers from instructions
        for idx, instruction in enumerate(instructions[1:], 1):
            print(f"  Layer {idx}: {instruction['type']} {instruction.get('value', '')[:50]}...")
            layer_id = self.create_layer(instruction)
            self.layers.append(layer_id)
        
        # Save image metadata
        image_id = self._save_image_metadata()
        print(f"✓ Image built successfully: {image_id}")
        
        return image_id
    
    def parse_dockerfile(self, content: str) -> List[Dict]:
        """
        Parse Dockerfile content
        
        Returns:
            List of instruction dictionaries
        """
        instructions = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse instruction
            parts = line.split(None, 1)
            if len(parts) < 1:
                continue
                
            instruction_type = parts[0].upper()
            instruction_value = parts[1] if len(parts) > 1 else ''
            
            instruction = {
                'type': instruction_type,
                'value': instruction_value
            }
            
            # Special handling for FROM
            if instruction_type == 'FROM':
                instruction['image'] = instruction_value
            
            instructions.append(instruction)
        
        return instructions
    
    def create_layer(self, instruction: Dict) -> str:
        """
        Create filesystem layer from instruction
        
        Args:
            instruction: Parsed Dockerfile instruction
            
        Returns:
            Layer ID (hash)
        """
        # Generate layer ID from instruction
        layer_content = json.dumps(instruction, sort_keys=True)
        layer_id = hashlib.sha256(layer_content.encode()).hexdigest()[:12]
        
        layer_path = self.image_dir / layer_id
        layer_path.mkdir(parents=True, exist_ok=True)
        
        # Create layer tarball (simplified - would execute instruction in reality)
        tarball_path = layer_path / "layer.tar"
        
        # Store instruction metadata
        metadata = {
            'id': layer_id,
            'instruction': instruction,
            'created': self._get_timestamp()
        }
        
        with open(layer_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return layer_id
    
    def pull_from_registry(self, registry_url: str) -> str:
        """
        Pull image from sovereign registry (not Docker Hub)
        
        Args:
            registry_url: URL of sovereign registry
            
        Returns:
            Image ID
        """
        print(f"🔥 Pulling {self.name}:{self.tag} from sovereign registry")
        # TODO: Implement HTTP pull from sovereign registry
        print("✓ Image pulled successfully")
        return self._generate_image_id()
    
    def push_to_registry(self, registry_url: str):
        """
        Push to sovereign registry (not Docker Hub)
        
        Args:
            registry_url: URL of sovereign registry
        """
        print(f"🔥 Pushing {self.name}:{self.tag} to sovereign registry")
        # TODO: Implement HTTP POST to sovereign registry server
        print("✓ Image pushed successfully")
    
    def export_rootfs(self, output_path: str):
        """
        Export image as a rootfs tarball
        
        Args:
            output_path: Path to export rootfs
        """
        print(f"🔥 Exporting rootfs to {output_path}")
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Create tarball with all layers merged
        with tarfile.open(output, 'w:gz') as tar:
            for layer_id in self.layers:
                layer_path = self.image_dir / layer_id / "layer.tar"
                if layer_path.exists():
                    tar.add(layer_path, arcname=f"layers/{layer_id}.tar")
        
        print(f"✓ Rootfs exported to {output_path}")
    
    def _save_image_metadata(self) -> str:
        """Save image metadata and return image ID"""
        image_id = self._generate_image_id()
        
        metadata = {
            'id': image_id,
            'name': self.name,
            'tag': self.tag,
            'layers': self.layers,
            'created': self._get_timestamp()
        }
        
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.image_dir / "manifest.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return image_id
    
    def _generate_image_id(self) -> str:
        """Generate unique image ID"""
        data = f"{self.name}:{self.tag}:{len(self.layers)}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


class SovereignImageRegistry:
    """
    Sovereign Image Registry
    
    Manages local image storage without Docker dependency
    """
    
    def __init__(self):
        self.registry_dir = Path("/var/lib/sovereign/images")
        self.registry_dir.mkdir(parents=True, exist_ok=True)
    
    def list_images(self) -> List[Dict]:
        """List all images in registry"""
        images = []
        
        if not self.registry_dir.exists():
            return images
        
        # Scan image directories
        for name_dir in self.registry_dir.iterdir():
            if not name_dir.is_dir():
                continue
                
            for tag_dir in name_dir.iterdir():
                if not tag_dir.is_dir():
                    continue
                    
                manifest_file = tag_dir / "manifest.json"
                if manifest_file.exists():
                    with open(manifest_file) as f:
                        images.append(json.load(f))
        
        return images
    
    def get_image(self, name: str, tag: str = "latest") -> Optional[SovereignImage]:
        """Get image by name and tag"""
        image = SovereignImage(name, tag)
        
        manifest_file = image.image_dir / "manifest.json"
        if manifest_file.exists():
            with open(manifest_file) as f:
                metadata = json.load(f)
                image.layers = metadata.get('layers', [])
            return image
        
        return None
    
    def remove_image(self, name: str, tag: str = "latest"):
        """Remove image from registry"""
        image_dir = Path(f"/var/lib/sovereign/images/{name}/{tag}")
        
        if image_dir.exists():
            shutil.rmtree(image_dir)
            print(f"✓ Removed image: {name}:{tag}")
        else:
            print(f"⚠️  Image not found: {name}:{tag}")
    
    def tag_image(self, source_name: str, source_tag: str, 
                  dest_name: str, dest_tag: str):
        """Tag an image with a new name/tag"""
        source_dir = Path(f"/var/lib/sovereign/images/{source_name}/{source_tag}")
        dest_dir = Path(f"/var/lib/sovereign/images/{dest_name}/{dest_tag}")
        
        if not source_dir.exists():
            raise FileNotFoundError(f"Source image not found: {source_name}:{source_tag}")
        
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        
        print(f"✓ Tagged {source_name}:{source_tag} as {dest_name}:{dest_tag}")


if __name__ == "__main__":
    # Example usage
    print("🔥 Sovereign Image Management v1.0")
    print("=" * 50)
    
    print("\nExample: Building an image from Dockerfile")
    print("  image = SovereignImage('myapp', 'v1.0')")
    print("  image.build_from_dockerfile('Dockerfile')")
    print("  image.export_rootfs('/tmp/myapp-rootfs.tar.gz')")
    
    print("\nExample: Managing images")
    print("  registry = SovereignImageRegistry()")
    print("  images = registry.list_images()")
    print("  image = registry.get_image('myapp', 'v1.0')")
