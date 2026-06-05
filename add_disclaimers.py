#!/usr/bin/env python3
"""
Script to add universal STRATEGICKHAOS disclaimer to all code files.
This script intelligently adds disclaimers while preserving shebangs and existing structure.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# Universal disclaimer for different file types
DISCLAIMER_HASH = """# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================
"""

DISCLAIMER_DOCKER = """# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================
"""

DISCLAIMER_RUST = """// ============================================================
// STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
// Copyright © 2025 Domenic G. Garza • All Rights Reserved
// 
// This file is part of the Strategickhaos Autonomous Runtime.
// It may not be copied, modified, distributed, or executed
// except by authorized operators within the Strategickhaos
// governance model and licensing structure.
// 
// Unauthorized use is prohibited. All activity is logged.
// ============================================================
"""

def has_disclaimer(content: str) -> bool:
    """Check if file already has the STRATEGICKHAOS disclaimer."""
    return "STRATEGICKHAOS DAO LLC" in content and "SOVEREIGN SOFTWARE FRAMEWORK" in content

def get_file_type(filepath: Path) -> str:
    """Determine file type based on extension."""
    name = filepath.name.lower()
    suffix = filepath.suffix.lower()
    
    if suffix == ".py":
        return "python"
    elif suffix in [".yaml", ".yml"]:
        return "yaml"
    elif suffix == ".sh":
        return "shell"
    elif suffix == ".rs":
        return "rust"
    elif name.startswith("dockerfile") or "docker-compose" in name:
        return "docker"
    else:
        return "unknown"

def add_disclaimer_to_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Add disclaimer to a file, preserving shebangs and structure.
    Returns (success, message).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False, "Binary file or encoding error"
    except Exception as e:
        return False, f"Read error: {str(e)}"
    
    # Skip if already has disclaimer
    if has_disclaimer(content):
        return False, "Already has disclaimer"
    
    # Skip empty files
    if not content.strip():
        return False, "Empty file"
    
    file_type = get_file_type(filepath)
    
    if file_type == "unknown":
        return False, "Unknown file type"
    
    # Get appropriate disclaimer
    if file_type == "rust":
        disclaimer = DISCLAIMER_RUST
    elif file_type in ["python", "yaml", "shell", "docker"]:
        disclaimer = DISCLAIMER_HASH
    else:
        return False, "Unsupported file type"
    
    lines = content.split('\n')
    new_lines = []
    insert_index = 0
    
    # Preserve shebang if present
    if lines and lines[0].startswith('#!'):
        new_lines.append(lines[0])
        insert_index = 1
    
    # Add disclaimer
    new_lines.append(disclaimer.rstrip())
    new_lines.append("")
    
    # Add remaining content
    for i in range(insert_index, len(lines)):
        new_lines.append(lines[i])
    
    new_content = '\n'.join(new_lines)
    
    if dry_run:
        return True, "Would add disclaimer"
    
    # Write back to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Disclaimer added"
    except Exception as e:
        return False, f"Write error: {str(e)}"

def find_files_to_update(root_dir: Path) -> List[Path]:
    """Find all files that should have disclaimers."""
    patterns = [
        "*.py", "*.yaml", "*.yml", "*.sh", "*.rs",
        "Dockerfile*", "docker-compose*"
    ]
    
    files = []
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
    
    for pattern in patterns:
        for filepath in root_dir.rglob(pattern):
            # Skip excluded directories
            if any(excl in filepath.parts for excl in exclude_dirs):
                continue
            # Skip if it's a directory (shouldn't happen but be safe)
            if filepath.is_dir():
                continue
            files.append(filepath)
    
    return sorted(set(files))

def main():
    """Main function to add disclaimers to all relevant files."""
    repo_root = Path(__file__).parent.resolve()
    
    print(f"🔍 Scanning repository: {repo_root}")
    
    files = find_files_to_update(repo_root)
    print(f"📄 Found {len(files)} files to process")
    
    # Statistics
    stats = {
        "success": 0,
        "skipped": 0,
        "errors": 0
    }
    
    for filepath in files:
        rel_path = filepath.relative_to(repo_root)
        success, message = add_disclaimer_to_file(filepath, dry_run=False)
        
        if success:
            print(f"✅ {rel_path}: {message}")
            stats["success"] += 1
        elif "Already has disclaimer" in message:
            print(f"⏭️  {rel_path}: {message}")
            stats["skipped"] += 1
        else:
            print(f"⚠️  {rel_path}: {message}")
            stats["errors"] += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully added: {stats['success']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"⚠️  Errors: {stats['errors']}")
    print("=" * 60)
    
    return 0 if stats["errors"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
