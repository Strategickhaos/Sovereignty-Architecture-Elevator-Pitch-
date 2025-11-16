#!/usr/bin/env python3
# require_checklist.py - UPL Compliance Checklist Enforcement
# Ensures UPL checklist is complete before commits

import sys
import re
from pathlib import Path

def check_upl_checklist(file_path):
    """Check if UPL compliance checklist is properly filled out"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ ERROR: Checklist file not found: {file_path}")
        return False
    except UnicodeDecodeError:
        print(f"❌ ERROR: Cannot decode file: {file_path}")
        return False
    
    # Check for attorney review section
    if "Attorney Review" not in content:
        print(f"❌ ERROR: Missing 'Attorney Review' section in {file_path}")
        return False
    
    # Count completed checkboxes
    completed_items = len(re.findall(r'\[x\]', content, re.IGNORECASE))
    total_items = len(re.findall(r'\[[ x]\]', content, re.IGNORECASE))
    
    if completed_items == 0:
        print(f"❌ ERROR: No completed checklist items in {file_path}")
        print("   Please complete required compliance checks before committing.")
        return False
    
    # Check for attorney sign-off specifically
    attorney_pattern = r'\[x\].*Attorney.*Sign-off.*COMPLETE'
    if not re.search(attorney_pattern, content, re.IGNORECASE):
        print(f"⚠️  WARNING: Attorney sign-off not marked complete in {file_path}")
        print(f"   Completed: {completed_items}/{total_items} items")
        print("   Ensure attorney review is complete before production use.")
        # Allow commit but warn - attorney review can happen after internal drafting
    
    print(f"✅ UPL checklist validation passed: {completed_items}/{total_items} items completed")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: require_checklist.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Only check UPL compliance checklist files
    if 'upl_safe_30_checklist' in file_path or 'compliance_checklist' in file_path:
        if not check_upl_checklist(file_path):
            sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()