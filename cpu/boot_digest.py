#!/usr/bin/env python3
"""
Boot Digest - CPU Recovery Protocol
====================================

A deterministic state restoration tool that mounts persistent artifacts
before letting volatile interpretation run.

This is your brain's "GitHub screenshot recovery" but automated.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class BootDigest:
    """Boot-time self-linking system for CPU recovery."""
    
    def __init__(self, repo_root: Optional[str] = None):
        """Initialize boot digest with repo root."""
        self.repo_root = Path(repo_root) if repo_root else self._find_repo_root()
        self.manifest_path = self.repo_root / "boot_manifest.json"
        self.manifest = self._load_manifest()
        self.confidence_ok = False
        
    def _find_repo_root(self) -> Path:
        """Find repository root by walking up for .git directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _load_manifest(self) -> Dict:
        """Load boot manifest configuration."""
        if not self.manifest_path.exists():
            # Return default manifest if file doesn't exist
            return {
                "version": "BOOT-MANIFEST-1.0",
                "anchors": ["README.md"],
                "globs": ["docs/**/*.md"],
                "max_files": 25,
                "max_chars_per_file": 12000
            }
        
        with open(self.manifest_path, 'r') as f:
            return json.load(f)
    
    def _run_git_command(self, args: List[str]) -> Tuple[str, int]:
        """Run a git command and return output and exit code."""
        try:
            result = subprocess.run(
                ["git", "--no-pager"] + args,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip(), result.returncode
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return f"Error: {e}", 1
    
    def _get_commit_count(self) -> int:
        """Get total commit count."""
        output, code = self._run_git_command(["rev-list", "--count", "HEAD"])
        if code == 0:
            try:
                return int(output)
            except ValueError:
                pass
        return 0
    
    def _get_last_commit_info(self) -> Tuple[str, str]:
        """Get last commit time and message."""
        output, code = self._run_git_command([
            "log", "-1", "--format=%cd|%s", "--date=short"
        ])
        if code == 0 and "|" in output:
            date, msg = output.split("|", 1)
            return date, msg
        return "unknown", "No commits"
    
    def _get_branch_name(self) -> str:
        """Get current branch name."""
        output, code = self._run_git_command(["branch", "--show-current"])
        if code == 0:
            return output
        return "unknown"
    
    def _count_recent_changes(self, days: int = 7) -> int:
        """Count files changed in last N days."""
        since_date = f"{days}.days.ago"
        output, code = self._run_git_command([
            "log", f"--since={since_date}", "--name-only", "--format="
        ])
        if code == 0:
            files = set(line.strip() for line in output.split('\n') if line.strip())
            return len(files)
        return 0
    
    def _get_recent_modules(self, limit: int = 5) -> List[str]:
        """Get recently modified Python modules."""
        output, code = self._run_git_command([
            "log", "-10", "--name-only", "--format=", "--", "*.py"
        ])
        if code == 0:
            files = []
            seen = set()
            for line in output.split('\n'):
                line = line.strip()
                if line and line.endswith('.py') and line not in seen:
                    seen.add(line)
                    files.append(os.path.basename(line))
                    if len(files) >= limit:
                        break
            return files
        return []
    
    def _count_local_branches(self) -> int:
        """Count local branches."""
        output, code = self._run_git_command(["branch", "--list"])
        if code == 0:
            return len([line for line in output.split('\n') if line.strip()])
        return 0
    
    def _load_anchor_files(self, fast_mode: bool = False) -> List[Tuple[str, int]]:
        """Load anchor files and return (filename, char_count) tuples."""
        if fast_mode:
            return []
        
        anchors = []
        max_chars = self.manifest.get("max_chars_per_file", 12000)
        
        for anchor in self.manifest.get("anchors", []):
            anchor_path = self.repo_root / anchor
            if anchor_path.exists():
                try:
                    content = anchor_path.read_text(encoding='utf-8')
                    char_count = min(len(content), max_chars)
                    anchors.append((anchor, char_count))
                except Exception:
                    pass
        
        return anchors
    
    def generate_digest(self, fast_mode: bool = False) -> str:
        """Generate boot digest report."""
        # Compute metrics
        commit_count = self._get_commit_count()
        last_commit_date, last_commit_msg = self._get_last_commit_info()
        branch = self._get_branch_name()
        recent_files = self._count_recent_changes(7) if not fast_mode else 0
        recent_modules = self._get_recent_modules(5) if not fast_mode else []
        local_branches = self._count_local_branches()
        anchors = self._load_anchor_files(fast_mode)
        
        # Set confidence flag
        self.confidence_ok = commit_count > 0
        
        # Build digest
        lines = [
            "=" * 70,
            "SAGCO BOOT DIGEST",
            "=" * 70,
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Repo: {self.repo_root.name}",
            f"Branch: {branch}",
            f"Commits: {commit_count:,}",
            f"Last commit: {last_commit_date}",
            f"  └─ {last_commit_msg}",
        ]
        
        if not fast_mode:
            lines.extend([
                f"Local branches: {local_branches}",
                f"Files changed (7 days): {recent_files}",
            ])
            
            if recent_modules:
                lines.append(f"Recent modules: {', '.join(recent_modules)}")
            
            if anchors:
                lines.append(f"Anchors loaded: {', '.join(f[0] for f in anchors)}")
        
        lines.extend([
            f"STATUS: {'CONFIDENCE_OK' if self.confidence_ok else 'CONFIDENCE_LOW'}",
            "=" * 70,
        ])
        
        if not fast_mode and self.confidence_ok:
            lines.append("")
            lines.append("Next action: Review recent changes and continue development")
        
        return '\n'.join(lines)
    
    def write_boot_report(self, digest: str) -> Path:
        """Write digest to BOOT_REPORT.md."""
        report_path = self.repo_root / "BOOT_REPORT.md"
        
        content = f"""# Boot Report

Generated: {datetime.now().isoformat()}

## Digest

```
{digest}
```

## Purpose

This report provides a quick snapshot of the repository state to help restore
context and confidence when returning to the project.

## Recovery Protocol

1. **Read this file first** - Get oriented before diving into code
2. **Check recent modules** - See what was being worked on
3. **Review last commit** - Understand the last change made
4. **Scan anchor docs** - Refresh on project goals and architecture

---

*Generated by CPU Boot Digest - Deterministic state restoration*
"""
        
        report_path.write_text(content, encoding='utf-8')
        return report_path


def main():
    """CLI entry point for boot digest."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SAGCO Boot Digest - CPU Recovery Protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cpu.boot doctor           # Full boot digest
  python -m cpu.boot doctor --fast    # Quick status check
  python -m cpu.boot panic            # Alias for --fast
        """
    )
    
    parser.add_argument(
        "command",
        choices=["doctor", "panic"],
        help="Command to run (doctor: full digest, panic: fast check)"
    )
    
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip reading docs, only show git stats"
    )
    
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Don't write BOOT_REPORT.md, only print to console"
    )
    
    parser.add_argument(
        "--repo",
        type=str,
        help="Repository root path (auto-detected if not provided)"
    )
    
    args = parser.parse_args()
    
    # Panic mode is always fast
    fast_mode = args.fast or args.command == "panic"
    
    try:
        # Initialize boot digest
        boot = BootDigest(repo_root=args.repo)
        
        # Generate digest
        digest = boot.generate_digest(fast_mode=fast_mode)
        
        # Print to console
        print(digest)
        
        # Write report file unless disabled
        if not args.no_report and not fast_mode:
            report_path = boot.write_boot_report(digest)
            print(f"\n📄 Report written to: {report_path}")
        
        # Exit with success
        sys.exit(0 if boot.confidence_ok else 1)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
