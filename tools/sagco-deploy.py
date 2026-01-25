#!/usr/bin/env python3
"""
SAGCO-DEPLOY - Universal File Deployer
Part of SAGCO-HYDRA v1.0.6 (CMD27 Arsenal)

Deploy files and artifacts to SAGCO infrastructure:
- Local deployment (copy to destination)
- Remote deployment (SSH/SCP)
- VM deployment (VirtualBox shared folders)
- Container deployment (Docker volumes)

Supports:
- Single file deployment
- Directory deployment
- "latest" keyword for most recent downloads
- Interactive wizard mode

DNA Codon: CMD27 (Command Arsenal)
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import argparse


def print_banner():
    """Display SAGCO-DEPLOY banner"""
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                       SAGCO-DEPLOY v1.0.0                                 ║")
    print("║                    Universal File Deployer                                ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print()


def find_latest_download() -> Optional[Path]:
    """
    Find the most recently downloaded file
    
    Returns:
        Path to latest download or None
    """
    downloads_dir = Path.home() / "Downloads"
    
    if not downloads_dir.exists():
        return None
    
    # Get all files in downloads, sorted by modification time
    files = []
    for file in downloads_dir.iterdir():
        if file.is_file():
            files.append((file, file.stat().st_mtime))
    
    if not files:
        return None
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x[1], reverse=True)
    
    return files[0][0]


def deploy_local(source: Path, destination: Path, force: bool = False) -> bool:
    """
    Deploy file locally
    
    Args:
        source: Source file or directory
        destination: Destination path
        force: Overwrite if exists
    
    Returns:
        True if successful
    """
    try:
        # Create destination directory if needed
        if destination.is_dir() or str(destination).endswith('/'):
            destination.mkdir(parents=True, exist_ok=True)
            dest_file = destination / source.name
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            dest_file = destination
        
        # Check if destination exists
        if dest_file.exists() and not force:
            print(f"❌ Destination exists: {dest_file}")
            print(f"   Use --force to overwrite")
            return False
        
        # Copy file or directory
        if source.is_file():
            print(f"📄 Copying file: {source.name}")
            shutil.copy2(source, dest_file)
            print(f"✅ Deployed to: {dest_file}")
        elif source.is_dir():
            print(f"📁 Copying directory: {source.name}")
            if dest_file.exists():
                shutil.rmtree(dest_file)
            shutil.copytree(source, dest_file)
            print(f"✅ Deployed to: {dest_file}")
        else:
            print(f"❌ Source not found: {source}")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False


def deploy_remote(source: Path, destination: str, host: str, user: Optional[str] = None) -> bool:
    """
    Deploy file to remote host via SCP
    
    Args:
        source: Source file or directory
        destination: Destination path on remote
        host: Remote hostname or IP
        user: SSH username (optional)
    
    Returns:
        True if successful
    """
    try:
        # Build SCP command
        if user:
            remote = f"{user}@{host}:{destination}"
        else:
            remote = f"{host}:{destination}"
        
        print(f"📡 Deploying to remote: {remote}")
        
        if source.is_dir():
            cmd = ["scp", "-r", str(source), remote]
        else:
            cmd = ["scp", str(source), remote]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Deployed successfully")
            return True
        else:
            print(f"❌ SCP failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Remote deployment failed: {e}")
        return False


def deploy_vm(source: Path, vm_name: str, destination: str) -> bool:
    """
    Deploy file to VirtualBox VM
    
    Args:
        source: Source file or directory
        vm_name: VirtualBox VM name
        destination: Destination path in VM
    
    Returns:
        True if successful
    """
    try:
        print(f"💻 Deploying to VM: {vm_name}")
        
        # Check if VBoxManage is available
        result = subprocess.run(
            ["VBoxManage", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ VirtualBox not found")
            return False
        
        # Copy file to VM using VBoxManage guestcontrol
        cmd = [
            "VBoxManage", "guestcontrol", vm_name,
            "copyto", str(source), destination,
            "--username", "root",
            "--password", "sagco"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Deployed to VM successfully")
            return True
        else:
            print(f"❌ VM deployment failed: {result.stderr}")
            print(f"   Make sure VM is running and guest additions are installed")
            return False
    
    except Exception as e:
        print(f"❌ VM deployment failed: {e}")
        return False


def interactive_mode():
    """Run interactive deployment wizard"""
    print_banner()
    print("🧙 INTERACTIVE DEPLOYMENT WIZARD")
    print()
    
    # Get source
    source_input = input("📥 Source file/directory (or 'latest' for most recent download): ").strip()
    
    if source_input.lower() == 'latest':
        latest = find_latest_download()
        if latest:
            source = latest
            print(f"   Found: {source}")
        else:
            print("❌ No downloads found")
            return
    else:
        source = Path(source_input).expanduser()
        if not source.exists():
            print(f"❌ Source not found: {source}")
            return
    
    # Get deployment type
    print()
    print("📦 Deployment type:")
    print("  1. Local (copy to local directory)")
    print("  2. Remote (SSH/SCP to remote host)")
    print("  3. VM (VirtualBox guest)")
    print("  4. Cancel")
    
    choice = input("Select (1-4): ").strip()
    
    if choice == '1':
        destination = input("📂 Destination directory: ").strip()
        dest_path = Path(destination).expanduser()
        
        force = input("⚠️  Overwrite if exists? (y/N): ").strip().lower() == 'y'
        
        print()
        deploy_local(source, dest_path, force)
    
    elif choice == '2':
        host = input("🌐 Remote host (IP or hostname): ").strip()
        user = input("👤 Username (leave empty for current user): ").strip() or None
        destination = input("📂 Destination path on remote: ").strip()
        
        print()
        deploy_remote(source, destination, host, user)
    
    elif choice == '3':
        vm_name = input("💻 VirtualBox VM name: ").strip()
        destination = input("📂 Destination path in VM: ").strip()
        
        print()
        deploy_vm(source, vm_name, destination)
    
    else:
        print("❌ Cancelled")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SAGCO-DEPLOY - Universal File Deployer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  sagco-deploy.py latest .                    # Deploy latest download to current dir
  sagco-deploy.py file.txt /path/to/dest      # Deploy file locally
  sagco-deploy.py -r user@host:/path file.txt # Deploy to remote via SCP
  sagco-deploy.py -v SAGCO-VM:/tmp file.txt   # Deploy to VirtualBox VM
  sagco-deploy.py --interactive               # Run wizard mode

DNA STRAND: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1
        """
    )
    
    parser.add_argument(
        "source",
        nargs="?",
        help="Source file/directory or 'latest' for most recent download"
    )
    
    parser.add_argument(
        "destination",
        nargs="?",
        help="Destination path"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive wizard mode"
    )
    
    parser.add_argument(
        "-r", "--remote",
        metavar="HOST",
        help="Deploy to remote host via SCP (format: [user@]host:path)"
    )
    
    parser.add_argument(
        "-v", "--vm",
        metavar="VM_NAME",
        help="Deploy to VirtualBox VM (format: vm_name:path)"
    )
    
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite destination if exists"
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        sys.exit(0)
    
    # Validate arguments
    if not args.source or not args.destination:
        print_banner()
        parser.print_help()
        sys.exit(1)
    
    print_banner()
    
    # Resolve source
    if args.source.lower() == 'latest':
        latest = find_latest_download()
        if latest:
            source = latest
            print(f"📥 Using latest download: {source.name}")
            print()
        else:
            print("❌ No downloads found")
            sys.exit(1)
    else:
        source = Path(args.source).expanduser()
        if not source.exists():
            print(f"❌ Source not found: {source}")
            sys.exit(1)
    
    # Deploy based on options
    if args.remote:
        # Parse remote (user@host:path or host:path)
        if ':' in args.remote:
            parts = args.remote.split(':', 1)
            host = parts[0]
            destination = parts[1] if len(parts) > 1 else args.destination
        else:
            host = args.remote
            destination = args.destination
        
        # Extract user if present
        if '@' in host:
            user, host = host.split('@', 1)
        else:
            user = None
        
        success = deploy_remote(source, destination, host, user)
        sys.exit(0 if success else 1)
    
    elif args.vm:
        # Parse VM (vm_name:path)
        if ':' in args.vm:
            vm_name, destination = args.vm.split(':', 1)
        else:
            vm_name = args.vm
            destination = args.destination
        
        success = deploy_vm(source, vm_name, destination)
        sys.exit(0 if success else 1)
    
    else:
        # Local deployment
        destination = Path(args.destination).expanduser()
        success = deploy_local(source, destination, args.force)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
