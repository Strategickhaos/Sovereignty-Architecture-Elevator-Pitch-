#!/usr/bin/env python3
"""
SAGCO-DEPLOY - Universal File Deployer
SAGCO-HYDRA v1.0.6
Deploys files to SAGCO infrastructure with version tracking
"""

import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"

def display_banner():
    """Display deployment banner"""
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║              SAGCO-DEPLOY Universal File Deployer v1.0.0                 ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print()

def find_latest_file(pattern=None):
    """Find the latest file matching pattern"""
    cwd = Path.cwd()
    
    if pattern:
        files = list(cwd.glob(pattern))
    else:
        # Look for common SAGCO artifacts
        patterns = [
            "sagco-os-*.iso",
            "sagco-os-*.zip",
            "*.flm",
            "*.sagco"
        ]
        files = []
        for p in patterns:
            files.extend(cwd.glob(p))
    
    if not files:
        return None
    
    # Sort by modification time
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]

def deploy_file(source, destination, verbose=False):
    """Deploy a file to destination"""
    src_path = Path(source)
    
    if not src_path.exists():
        print(f"❌ Error: Source file not found: {source}")
        return False
    
    dest_path = Path(destination)
    
    # If destination is a directory, preserve filename
    if dest_path.is_dir():
        dest_path = dest_path / src_path.name
    else:
        # Ensure parent directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if verbose:
            print(f"📦 Deploying: {src_path}")
            print(f"📍 Target: {dest_path}")
            print(f"📏 Size: {src_path.stat().st_size:,} bytes")
        
        # Copy file
        shutil.copy2(src_path, dest_path)
        
        if verbose:
            print(f"✅ Deployment successful")
            print(f"⏰ Timestamp: {datetime.now().isoformat()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def interactive_mode():
    """Interactive deployment wizard"""
    print("🧙 Interactive Deployment Wizard")
    print("─" * 80)
    print()
    
    # Source selection
    print("Select source file:")
    print("  1. Latest SAGCO ISO")
    print("  2. Latest ZIP archive")
    print("  3. Custom path")
    print()
    
    choice = input("Choice [1-3]: ").strip()
    
    if choice == '1':
        source = find_latest_file("sagco-os-*.iso")
        if not source:
            print("❌ No ISO files found")
            return False
    elif choice == '2':
        source = find_latest_file("*.zip")
        if not source:
            print("❌ No ZIP files found")
            return False
    elif choice == '3':
        source = input("Enter source path: ").strip()
    else:
        print("❌ Invalid choice")
        return False
    
    print()
    
    # Destination selection
    print("Select destination:")
    print("  1. Current directory")
    print("  2. /tmp directory")
    print("  3. Custom path")
    print()
    
    choice = input("Choice [1-3]: ").strip()
    
    if choice == '1':
        destination = Path.cwd()
    elif choice == '2':
        destination = Path("/tmp")
    elif choice == '3':
        destination = input("Enter destination path: ").strip()
    else:
        print("❌ Invalid choice")
        return False
    
    print()
    
    # Confirm
    print(f"Source: {source}")
    print(f"Destination: {destination}")
    print()
    confirm = input("Proceed with deployment? [y/N]: ").strip().lower()
    
    if confirm == 'y':
        return deploy_file(source, destination, verbose=True)
    else:
        print("❌ Deployment cancelled")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SAGCO-DEPLOY Universal File Deployer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sagco-deploy.py latest .             # Deploy latest file to current dir
  sagco-deploy.py file.iso /mnt/iso    # Deploy specific file
  sagco-deploy.py --interactive        # Interactive wizard mode
        """
    )
    
    parser.add_argument('source', nargs='?', help='Source file or "latest"')
    parser.add_argument('destination', nargs='?', help='Destination path')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive wizard mode')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    display_banner()
    
    # Interactive mode
    if args.interactive or (not args.source and not args.destination):
        success = interactive_mode()
        sys.exit(0 if success else 1)
    
    # Check arguments
    if not args.source or not args.destination:
        parser.print_help()
        sys.exit(1)
    
    # Handle "latest" keyword
    if args.source == 'latest':
        source = find_latest_file()
        if not source:
            print("❌ No SAGCO artifacts found in current directory")
            sys.exit(1)
        print(f"📦 Latest file: {source}")
        print()
    else:
        source = args.source
    
    # Deploy
    success = deploy_file(source, args.destination, verbose=args.verbose)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
