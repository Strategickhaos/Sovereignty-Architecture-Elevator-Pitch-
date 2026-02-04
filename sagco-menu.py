#!/usr/bin/env python3
"""
SAGCO-MENU v1.1 - State Manager
Manages menu state including recent tools with per-user storage
"""

import json
import os
from pathlib import Path

# Per-user state management (Micro-hardening #1)
USER = os.getenv("USER") or "global"
STATE_DIR = "/var/lib/sagco"
STATE_PATH = f"{STATE_DIR}/menu_state_{USER}.json"


def ensure_state_dir():
    """Ensure state directory exists with proper permissions"""
    Path(STATE_DIR).mkdir(parents=True, exist_ok=True)
    # Set permissions to allow all users to write (for multi-user support)
    try:
        os.chmod(STATE_DIR, 0o777)
    except (OSError, PermissionError):
        # If we can't chmod (not root), that's okay - will use fallback
        pass


def load_state():
    """Load menu state from disk"""
    try:
        ensure_state_dir()
        if os.path.exists(STATE_PATH):
            with open(STATE_PATH, 'r') as f:
                return json.load(f)
    except (OSError, PermissionError, json.JSONDecodeError):
        # Fallback to user home directory if /var/lib/sagco isn't writable
        fallback_path = os.path.expanduser(f"~/.sagco_menu_state_{USER}.json")
        try:
            if os.path.exists(fallback_path):
                with open(fallback_path, 'r') as f:
                    return json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    
    return {"recent": []}


def save_state(state):
    """Save menu state to disk"""
    try:
        ensure_state_dir()
        with open(STATE_PATH, 'w') as f:
            json.dump(state, f, indent=2)
    except (OSError, PermissionError):
        # Fallback to user home directory
        fallback_path = os.path.expanduser(f"~/.sagco_menu_state_{USER}.json")
        try:
            with open(fallback_path, 'w') as f:
                json.dump(state, f, indent=2)
        except OSError:
            pass  # Silent fail if we can't save state


def add_recent(tool_name, tool_command):
    """
    Add a tool to recent list
    Micro-hardening #3: Cap recents to 5 unique items
    """
    state = load_state()
    recent = state.get("recent", [])
    
    # Create tool entry
    tool_entry = {
        "name": tool_name,
        "command": tool_command
    }
    
    # Remove if already exists (for deduplication)
    recent = [r for r in recent if r["name"] != tool_name]
    
    # Add to end
    recent.append(tool_entry)
    
    # Cap to last 5 items (Micro-hardening #3)
    recent = recent[-5:]
    
    state["recent"] = recent
    save_state(state)


def get_recent():
    """Get list of recent tools"""
    state = load_state()
    return state.get("recent", [])


def clear_recent():
    """Clear recent tools list"""
    state = {"recent": []}
    save_state(state)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: sagco-menu.py [add|get|clear] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: sagco-menu.py add <name> <command>")
            sys.exit(1)
        add_recent(sys.argv[2], sys.argv[3])
        print(f"Added '{sys.argv[2]}' to recent tools")
    
    elif command == "get":
        recent = get_recent()
        if recent:
            for tool in recent:
                print(f"{tool['name']}\t{tool['command']}")
        else:
            print("No recent tools")
    
    elif command == "clear":
        clear_recent()
        print("Cleared recent tools")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
