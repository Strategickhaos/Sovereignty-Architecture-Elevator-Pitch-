#!/usr/bin/env python3
import sys
import yaml
import json
import os
from difflib import get_close_matches  # For fuzzy search

SPM_PATH = "/opt/sagco/spm.yml"
STATE_PATH = "/var/lib/sagco/menu_state.json"  # Recently used (global for v1; per-user future)

def load_spm():
    with open(SPM_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"recent": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def categories(spm):
    tools = spm.get("tools", {}) or {}
    order = tools.get("order", list(tools.keys()))  # Use order or default to keys
    out = []
    for key in order:
        if key in tools:
            cat = tools[key]
            icon = cat.get("icon", "")
            desc = cat.get("description", "")
            out.append((key, icon, desc))
    return out

def items(spm, category_key, search=""):
    cat = (spm.get("tools", {}) or {}).get(category_key, {}) or {}
    items = cat.get("items", []) or []
    out = []
    for it in items:
        name = str(it.get("name", "")).strip()
        icon = str(it.get("icon", "")).strip()
        desc = str(it.get("description", "")).strip()
        cmd = str(it.get("command", "")).strip()
        if name and cmd:
            out.append((name, icon, desc, cmd))
    if search:
        out = [it for it in out if search.lower() in it[0].lower() or search.lower() in it[2].lower()]  # Fuzzy-ish match
    return out

def recent(spm, state, limit=5):
    recent = state.get("recent", [])[-limit:]  # Last N
    out = []
    for entry in recent:
        cat, name = entry.split(":", 1)  # "category:name"
        for it in items(spm, cat):
            if it[0] == name:
                out.append(it)
                break
    return out

def add_recent(state, category, name):
    entry = f"{category}:{name}"
    recent = state.get("recent", [])
    if entry in recent:
        recent.remove(entry)
    recent.append(entry)
    state["recent"] = recent
    save_state(state)

def main():
    if len(sys.argv) < 2:
        print("usage: sagco-menu.py categories|items|recent|add_recent <args?>", file=sys.stderr)
        sys.exit(2)

    spm = load_spm()
    state = load_state()
    mode = sys.argv[1].lower()

    if mode == "categories":
        for k, icon, d in categories(spm):
            print(f"{k}\t{icon}\t{d}")
        return

    if mode == "items":
        if len(sys.argv) < 3:
            print("usage: sagco-menu.py items <category> [search]", file=sys.stderr)
            sys.exit(2)
        cat = sys.argv[2]
        search = sys.argv[3] if len(sys.argv) > 3 else ""
        for name, icon, desc, cmd in items(spm, cat, search):
            print(f"{name}\t{icon}\t{desc}\t{cmd}")
        return

    if mode == "recent":
        for name, icon, desc, cmd in recent(spm, state):
            print(f"{name}\t{icon}\t{desc}\t{cmd}")
        return

    if mode == "add_recent":
        if len(sys.argv) < 4:
            print("usage: sagco-menu.py add_recent <category> <name>", file=sys.stderr)
            sys.exit(2)
        add_recent(state, sys.argv[2], sys.argv[3])
        return

    print(f"unknown mode: {mode}", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
