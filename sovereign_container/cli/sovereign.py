#!/usr/bin/env python3
"""
Sovereign Container CLI
Command-line interface for the sovereign container platform

Commands:
  sovereign run    - Run a container
  sovereign ps     - List containers
  sovereign stop   - Stop a container
  sovereign images - List images
  sovereign build  - Build an image
  sovereign network - Manage networks
  sovereign volume - Manage volumes
  sovereign compile - Compile FlameLang manifest
"""

import sys
import argparse
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sovereign_container.runtime import (
    SovereignContainer, SovereignImage, SovereignVolume, SovereignNetwork,
    list_containers, list_volumes, list_networks
)
from sovereign_container.flamelang import FlameLangContainerCompiler


def cmd_run(args):
    """Run a sovereign container"""
    print(f"🔥 Starting sovereign container: {args.name}")
    
    config = {
        'memory': args.memory,
        'cpu': args.cpu
    }
    
    if args.glyph:
        print(f"   Glyph: {args.glyph}")
        config['glyph'] = args.glyph
    
    container = SovereignContainer(
        name=args.name,
        rootfs_path=args.rootfs or "/tmp/sovereign_rootfs",
        config=config
    )
    
    # Start container
    command = args.command.split() if args.command else ["/bin/sh"]
    proc = container.start(command)
    
    print(f"✓ Container started")
    print(f"  ID: {args.name}")
    print(f"  PID: {proc.pid}")
    print(f"  Status: Running")
    
    if args.frequency:
        print(f"  Frequency: {args.frequency}Hz")


def cmd_ps(args):
    """List sovereign containers"""
    containers = list_containers()
    
    if not containers:
        print("No containers running")
        return
    
    print(f"{'ID':<20} {'NAME':<20} {'STATUS':<10} {'GLYPH':<10}")
    print("-" * 70)
    
    for container in containers:
        container_id = container.get('name', 'unknown')[:20]
        name = container.get('name', 'unknown')[:20]
        status = container.get('status', 'unknown')[:10]
        glyph = container.get('config', {}).get('glyph', 'N/A')[:10]
        
        print(f"{container_id:<20} {name:<20} {status:<10} {glyph:<10}")


def cmd_stop(args):
    """Stop a sovereign container"""
    print(f"Stopping container: {args.name}")
    
    container = SovereignContainer(
        name=args.name,
        rootfs_path="/tmp/sovereign_rootfs"
    )
    
    container.stop()
    print("✓ Container stopped")


def cmd_images(args):
    """List sovereign images"""
    image = SovereignImage("dummy", "dummy")
    images = image.list_local_images()
    
    if not images:
        print("No images found")
        return
    
    print(f"{'NAME':<30} {'TAG':<15} {'LAYERS':<10} {'CREATED':<30}")
    print("-" * 85)
    
    for img in images:
        name = f"{img['name']}"[:30]
        tag = img['tag'][:15]
        layers = str(img['layers'])[:10]
        created = img.get('created', 'unknown')[:30]
        
        print(f"{name:<30} {tag:<15} {layers:<10} {created:<30}")


def cmd_build(args):
    """Build a sovereign image"""
    print(f"🔥 Building sovereign image: {args.tag}")
    print(f"   Dockerfile: {args.file}")
    print(f"   Context: {args.context}")
    
    name, tag = args.tag.split(':') if ':' in args.tag else (args.tag, 'latest')
    
    image = SovereignImage(name, tag)
    manifest = image.build_from_dockerfile(args.file, args.context)
    
    print(f"✓ Image built successfully")
    print(f"  Name: {name}")
    print(f"  Tag: {tag}")
    print(f"  Layers: {len(manifest['layers'])}")


def cmd_network(args):
    """Manage sovereign networks"""
    if args.action == 'create':
        print(f"Creating network: {args.name}")
        network = SovereignNetwork(args.name, args.subnet)
        network.create_bridge()
        print("✓ Network created")
        
    elif args.action == 'list':
        networks = list_networks()
        if not networks:
            print("No networks found")
            return
        
        print(f"{'NAME':<20} {'SUBNET':<20} {'BRIDGE':<15}")
        print("-" * 55)
        
        for net in networks:
            name = net['name'][:20]
            subnet = net.get('subnet', 'N/A')[:20]
            bridge = net.get('bridge', 'N/A')[:15]
            print(f"{name:<20} {subnet:<20} {bridge:<15}")
    
    elif args.action == 'delete':
        print(f"Deleting network: {args.name}")
        network = SovereignNetwork(args.name)
        network.delete_bridge()
        print("✓ Network deleted")


def cmd_volume(args):
    """Manage sovereign volumes"""
    if args.action == 'create':
        print(f"Creating volume: {args.name}")
        volume = SovereignVolume(args.name)
        
        if args.encrypted:
            import getpass
            passphrase = getpass.getpass("Enter encryption passphrase: ")
            volume.create_encrypted_volume(passphrase, args.size)
            print("✓ Encrypted volume created")
        else:
            print("✓ Volume created")
        
    elif args.action == 'list':
        volumes = list_volumes()
        if not volumes:
            print("No volumes found")
            return
        
        print(f"{'NAME':<30} {'SIZE':<15} {'ENCRYPTED':<10}")
        print("-" * 55)
        
        for vol in volumes:
            name = vol['name'][:30]
            size = f"{vol.get('size_mb', 0)} MB"[:15]
            encrypted = "Yes" if vol.get('encrypted') else "No"
            print(f"{name:<30} {size:<15} {encrypted:<10}")
    
    elif args.action == 'delete':
        print(f"Deleting volume: {args.name}")
        volume = SovereignVolume(args.name)
        volume.delete()
        print("✓ Volume deleted")


def cmd_compile(args):
    """Compile FlameLang manifest"""
    print(f"🔥 Compiling FlameLang manifest: {args.file}")
    
    compiler = FlameLangContainerCompiler()
    runtime_config = compiler.compile_manifest(args.file)
    
    print(f"✓ Compilation complete")
    print(f"  Containers: {len(runtime_config['containers'])}")
    print(f"  Networks: {len(runtime_config['networks'])}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(runtime_config, f, indent=2)
        print(f"  Config saved to: {args.output}")
    
    if args.execute:
        print("\n🔥 Executing runtime configuration...")
        compiler.execute_runtime_config(runtime_config)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Sovereign Container Platform - Docker-free container management',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a container')
    run_parser.add_argument('name', help='Container name')
    run_parser.add_argument('--rootfs', help='Root filesystem path')
    run_parser.add_argument('--command', help='Command to run')
    run_parser.add_argument('--memory', default='512M', help='Memory limit (default: 512M)')
    run_parser.add_argument('--cpu', default='1', help='CPU limit (default: 1)')
    run_parser.add_argument('--glyph', help='FlameLang glyph (e.g., [001])')
    run_parser.add_argument('--frequency', type=int, help='Frequency in Hz')
    run_parser.set_defaults(func=cmd_run)
    
    # PS command
    ps_parser = subparsers.add_parser('ps', help='List containers')
    ps_parser.set_defaults(func=cmd_ps)
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop a container')
    stop_parser.add_argument('name', help='Container name')
    stop_parser.set_defaults(func=cmd_stop)
    
    # Images command
    images_parser = subparsers.add_parser('images', help='List images')
    images_parser.set_defaults(func=cmd_images)
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build an image')
    build_parser.add_argument('-t', '--tag', required=True, help='Image name:tag')
    build_parser.add_argument('-f', '--file', default='Dockerfile', help='Dockerfile path')
    build_parser.add_argument('context', nargs='?', default='.', help='Build context')
    build_parser.set_defaults(func=cmd_build)
    
    # Network command
    network_parser = subparsers.add_parser('network', help='Manage networks')
    network_parser.add_argument('action', choices=['create', 'list', 'delete'])
    network_parser.add_argument('--name', help='Network name')
    network_parser.add_argument('--subnet', default='10.137.0.0/16', help='Network subnet')
    network_parser.set_defaults(func=cmd_network)
    
    # Volume command
    volume_parser = subparsers.add_parser('volume', help='Manage volumes')
    volume_parser.add_argument('action', choices=['create', 'list', 'delete'])
    volume_parser.add_argument('--name', help='Volume name')
    volume_parser.add_argument('--encrypted', action='store_true', help='Create encrypted volume')
    volume_parser.add_argument('--size', type=int, default=1024, help='Volume size in MB')
    volume_parser.set_defaults(func=cmd_volume)
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile FlameLang manifest')
    compile_parser.add_argument('file', help='FlameLang manifest file (.fl)')
    compile_parser.add_argument('-o', '--output', help='Output runtime config file')
    compile_parser.add_argument('-e', '--execute', action='store_true', help='Execute after compiling')
    compile_parser.set_defaults(func=cmd_compile)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    print("🔥⚔️🖤 SOVEREIGN CONTAINER PLATFORM 🖤⚔️🔥")
    print("=" * 60)
    sys.exit(main())
