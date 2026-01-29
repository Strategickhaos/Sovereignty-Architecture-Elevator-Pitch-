#!/usr/bin/env python3
"""
TRIG6 Proof Generator

MIT License
Copyright (c) 2025 Strategickhaos

Generates cryptographic proof bundles for sovereignty verification.
"""

import os
import sys
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path


def get_git_commit():
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "UNKNOWN"


def get_environment_info():
    """Capture environment information for auditing."""
    env_info = []
    
    # Python version
    try:
        result = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True
        )
        env_info.append(("Python Version", result.stdout.strip() or result.stderr.strip()))
    except Exception as e:
        env_info.append(("Python Version", f"ERROR: {e}"))
    
    # System information
    try:
        result = subprocess.run(
            ["uname", "-a"],
            capture_output=True,
            text=True
        )
        env_info.append(("System", result.stdout.strip()))
    except Exception as e:
        env_info.append(("System", f"ERROR: {e}"))
    
    # Pip packages (if any dependencies are used)
    try:
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True
        )
        pip_output = result.stdout.strip()
        if pip_output:
            env_info.append(("Dependencies", pip_output))
        else:
            env_info.append(("Dependencies", "None (zero-dependency core)"))
    except Exception:
        env_info.append(("Dependencies", "None (zero-dependency core)"))
    
    return env_info


def hash_file(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"


def scan_directory(base_path: Path, scan_patterns: list) -> list:
    """Scan directories for files matching patterns."""
    files = []
    for pattern in scan_patterns:
        # Check if it's a specific file
        file_path = base_path / pattern
        if file_path.exists() and file_path.is_file():
            files.append(file_path)
            continue
        
        # Support both glob patterns and directory names
        if "/" in pattern or "*" in pattern:
            # It's a glob pattern
            matches = list(base_path.glob(pattern))
        else:
            # It's a directory name - scan recursively
            dir_path = base_path / pattern
            if dir_path.exists() and dir_path.is_dir():
                matches = list(dir_path.rglob("*.py")) + list(dir_path.rglob("*.md"))
            else:
                matches = []
        
        for filepath in matches:
            if filepath.is_file():
                files.append(filepath)
    
    return sorted(set(files))


def generate_proof(output_dir: Path, scan_all: bool = False):
    """Generate sovereignty proof bundle."""
    print("=== TRIG6 Sovereignty Proof Generator ===")
    print()
    
    # Get repository root
    repo_root = Path(__file__).parent
    
    # Get commit hash
    commit_hash = get_git_commit()
    print(f"Commit: {commit_hash}")
    
    # Get environment
    env_info = get_environment_info()
    print("\nEnvironment:")
    for key, value in env_info:
        print(f"  {key}: {value}")
    
    # Define scan patterns - expanded to include games/ and sagco/
    scan_patterns = [
        "trig6.py",
        "proof.py",
        "core/*.py",
        "core",
        "domains",
        "packs",
        "games",
        "sagco"
    ]
    
    print(f"\nScanning directories: {', '.join(scan_patterns)}")
    files = scan_directory(repo_root, scan_patterns)
    
    print(f"\nFound {len(files)} files to verify")
    
    # Generate hashes
    file_hashes = []
    for filepath in files:
        rel_path = filepath.relative_to(repo_root)
        file_hash = hash_file(filepath)
        file_hashes.append((str(rel_path), file_hash))
        print(f"  {rel_path}: {file_hash[:16]}...")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate proof summary
    timestamp = datetime.now().astimezone().isoformat()
    summary_path = output_dir / "proof_summary.txt"
    
    with open(summary_path, 'w') as f:
        f.write("TRIG6 Sovereignty Proof Bundle\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Commit: {commit_hash}\n\n")
        
        f.write("Environment:\n")
        for key, value in env_info:
            f.write(f"  {key}: {value}\n")
        f.write("\n")
        
        f.write(f"Files Verified: {len(file_hashes)}\n\n")
        
        f.write("File Integrity Hashes:\n")
        for rel_path, file_hash in file_hashes:
            f.write(f"  {rel_path}\n")
            f.write(f"    SHA256: {file_hash}\n")
        
        # Compute bundle hash
        bundle_data = "\n".join([f"{path}:{hash}" for path, hash in file_hashes])
        bundle_hash = hashlib.sha256(bundle_data.encode()).hexdigest()
        
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Bundle Hash: {bundle_hash}\n")
    
    print(f"\nProof bundle written to: {summary_path}")
    print(f"Bundle Hash: {bundle_hash}")
    
    # Generate machine-readable manifest
    manifest_path = output_dir / "manifest.json"
    import json
    manifest = {
        "timestamp": timestamp,
        "commit": commit_hash,
        "environment": dict(env_info),
        "files": [{"path": p, "hash": h} for p, h in file_hashes],
        "bundle_hash": bundle_hash
    }
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Machine-readable manifest: {manifest_path}")
    print("\n[SUCCESS] Proof bundle generated")
    
    return 0


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TRIG6 Sovereignty Proof Generator")
    parser.add_argument("--all", action="store_true", help="Scan all directories")
    parser.add_argument("--bundle", action="store_true", help="Generate proof bundle")
    parser.add_argument("--output", type=str, default="./proof_bundle", 
                        help="Output directory for proof bundle")
    
    args = parser.parse_args()
    
    if not (args.all or args.bundle):
        parser.print_help()
        return 1
    
    output_dir = Path(args.output)
    return generate_proof(output_dir, scan_all=args.all)


if __name__ == "__main__":
    sys.exit(main())
