#!/usr/bin/env python3
"""
SOPHIA MIND Brain Visualizer - Sync Engine
Sovereign sync across nodes without vendor lock-in

Supports: Proton Drive, Git, and custom sync targets
Part of the Strategickhaos Sovereignty Architecture
"""

import hashlib
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class SophiaSync:
    """Sovereign sync engine for multi-node knowledge graph synchronization"""
    
    def __init__(self, local_vault: str, sync_targets: Dict[str, str]):
        self.local_vault = Path(local_vault)
        self.sync_targets = sync_targets
        self.state_file = self.local_vault / '.sophia_state.json'
        
    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of file content"""
        content = filepath.read_bytes()
        return hashlib.sha256(content).hexdigest()
        
    def detect_changes(self) -> Dict[str, List[str]]:
        """Detect file changes since last sync"""
        current_state = {}
        
        # Build current state
        for md_file in self.local_vault.glob("**/*.md"):
            rel_path = str(md_file.relative_to(self.local_vault))
            current_state[rel_path] = {
                'hash': self.calculate_hash(md_file),
                'mtime': md_file.stat().st_mtime
            }
            
        # Load previous state
        previous_state = self.load_state()
        
        # Detect changes
        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }
        
        for path, info in current_state.items():
            if path not in previous_state:
                changes['added'].append(path)
            elif info['hash'] != previous_state[path]['hash']:
                changes['modified'].append(path)
                
        for path in previous_state:
            if path not in current_state:
                changes['deleted'].append(path)
                
        # Save current state
        self.save_state(current_state)
        
        return changes
        
    def load_state(self) -> Dict:
        """Load previous sync state"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except json.JSONDecodeError:
                print(f"Warning: Corrupted state file, creating new one")
        return {}
        
    def save_state(self, state: Dict) -> None:
        """Save current sync state"""
        self.state_file.write_text(json.dumps(state, indent=2))
        
    def sync_to_proton(self, changes: Dict[str, List[str]]) -> None:
        """Sync changes to Proton Drive folder"""
        if 'proton' not in self.sync_targets:
            print("⚠️  Proton Drive sync target not configured")
            return
            
        proton_path = Path(self.sync_targets['proton'])
        
        if not proton_path.exists():
            print(f"⚠️  Proton Drive path does not exist: {proton_path}")
            return
            
        synced_count = 0
        
        # Sync added and modified files
        for filepath in changes['added'] + changes['modified']:
            src = self.local_vault / filepath
            dst = proton_path / filepath
            
            # Create parent directories
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            dst.write_bytes(src.read_bytes())
            synced_count += 1
            
        # Handle deleted files
        for filepath in changes['deleted']:
            dst = proton_path / filepath
            if dst.exists():
                dst.unlink()
                synced_count += 1
                
        print(f"✅ Proton Drive: Synced {synced_count} files")
        
    def sync_to_git(self, changes: Dict[str, List[str]]) -> bool:
        """Commit and push changes to Git repository"""
        if 'git' not in self.sync_targets:
            print("⚠️  Git sync target not configured")
            return False
            
        git_dir = Path(self.sync_targets['git'])
        
        if not (git_dir / '.git').exists():
            print(f"⚠️  Not a Git repository: {git_dir}")
            return False
            
        total_changes = len(changes['added']) + len(changes['modified']) + len(changes['deleted'])
        
        if total_changes == 0:
            print("ℹ️  No changes to commit")
            return True
            
        try:
            # Stage added and modified files
            for filepath in changes['added'] + changes['modified']:
                subprocess.run(
                    ['git', 'add', filepath],
                    cwd=git_dir,
                    check=True,
                    capture_output=True
                )
                
            # Stage deleted files
            for filepath in changes['deleted']:
                subprocess.run(
                    ['git', 'rm', filepath],
                    cwd=git_dir,
                    check=True,
                    capture_output=True
                )
                
            # Create FlameLang-style commit message
            timestamp = datetime.now().isoformat()
            msg = (
                f"[GR1] SOPHIA sync | {timestamp}\n\n"
                f"Changes: {len(changes['added'])} added, "
                f"{len(changes['modified'])} modified, "
                f"{len(changes['deleted'])} deleted"
            )
            
            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', msg],
                cwd=git_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"⚠️  Git commit failed: {result.stderr}")
                return False
                
            # Push to remote
            push_result = subprocess.run(
                ['git', 'push'],
                cwd=git_dir,
                capture_output=True,
                text=True
            )
            
            if push_result.returncode != 0:
                print(f"⚠️  Git push failed: {push_result.stderr}")
                return False
                
            print(f"✅ Git: Committed and pushed {total_changes} changes")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git sync error: {e}")
            return False
            
    def full_sync(self) -> Dict[str, bool]:
        """Perform full sync to all configured targets"""
        print("🔄 SOPHIA MIND Sync Engine - Starting sync...")
        print(f"📂 Vault: {self.local_vault}")
        
        # Detect changes
        changes = self.detect_changes()
        
        total_changes = len(changes['added']) + len(changes['modified']) + len(changes['deleted'])
        print(f"\n📊 Changes detected: {total_changes}")
        if total_changes > 0:
            print(f"   Added: {len(changes['added'])}")
            print(f"   Modified: {len(changes['modified'])}")
            print(f"   Deleted: {len(changes['deleted'])}")
        
        # Sync to all targets
        results = {}
        
        if 'proton' in self.sync_targets:
            try:
                self.sync_to_proton(changes)
                results['proton'] = True
            except Exception as e:
                print(f"❌ Proton sync failed: {e}")
                results['proton'] = False
                
        if 'git' in self.sync_targets:
            results['git'] = self.sync_to_git(changes)
            
        print("\n✨ Sync complete!")
        return results


def main():
    """CLI interface for SOPHIA sync"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='SOPHIA MIND Sync Engine - Zero vendor lock-in knowledge sync'
    )
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--proton', help='Path to Proton Drive sync folder')
    parser.add_argument('--git', help='Path to Git repository')
    parser.add_argument('--check', action='store_true', help='Only check for changes, do not sync')
    
    args = parser.parse_args()
    
    # Build sync targets
    sync_targets = {}
    if args.proton:
        sync_targets['proton'] = args.proton
    if args.git:
        sync_targets['git'] = args.git
        
    if not sync_targets:
        print("❌ No sync targets specified. Use --proton and/or --git")
        sys.exit(1)
        
    print("🧠 SOPHIA MIND Sync Engine")
    print("   Part of Strategickhaos Sovereignty Architecture")
    print("   Zero Vendor Lock-in | Own Your Data")
    print()
    
    sync = SophiaSync(args.vault_path, sync_targets)
    
    if args.check:
        changes = sync.detect_changes()
        total = len(changes['added']) + len(changes['modified']) + len(changes['deleted'])
        print(f"Changes detected: {total}")
        print(f"  Added: {len(changes['added'])}")
        print(f"  Modified: {len(changes['modified'])}")
        print(f"  Deleted: {len(changes['deleted'])}")
    else:
        results = sync.full_sync()
        
        # Exit with error if any sync failed
        if not all(results.values()):
            sys.exit(1)


if __name__ == '__main__':
    main()
