#!/usr/bin/env python3
import sys
import yaml
import json
import os
from difflib import get_close_matches  # Fuzzy search

SPM_PATH = "/opt/sagco/spm.yml"
STATE_PATH = "/var/lib/sagco/menu_state.json"  # Recently used (per-user keys)

def load_spm():
    with open(SPM_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_user_key():
    return os.environ.get("USER", "global")  # Per-user or fallback

def load_state(user_key):
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_key, {"recent": []})
    return {"recent": []}

def save_state(user_key, user_state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[user_key] = user_state
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

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

def all_items(spm):
    out = []
    for cat_key, cat in (spm.get("tools", {}) or {}).items():
        if cat_key == "order": continue
        for it in cat.get("items", []):
            name = str(it.get("name", "")).strip()
            icon = str(it.get("icon", "")).strip()
            desc = str(it.get("description", "")).strip()
            cmd = str(it.get("command", "")).strip()
            if name and cmd:
                out.append((name, icon, desc, cmd, cat_key))  # Add cat_key for recent
    return out

def items(spm, category_key, search=""):
    if category_key == "all" or search:  # Cross-tool for search
        out = all_items(spm)
    else:
        cat = (spm.get("tools", {}) or {}).get(category_key, {}) or {}
        out = []
        for it in cat.get("items", []):
            name = str(it.get("name", "")).strip()
            icon = str(it.get("icon", "")).strip()
            desc = str(it.get("description", "")).strip()
            cmd = str(it.get("command", "")).strip()
            if name and cmd:
                out.append((name, icon, desc, cmd, category_key))
    if search:
        matches = get_close_matches(search.lower(), [f"{n} {d}" for n, _, d, _, _ in out], n=len(out), cutoff=0.6)
        out = [it for it in out if f"{it[0]} {it[2]}".lower() in matches or search.lower() in it[0].lower() or search.lower() in it[2].lower()]
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
    return state

def main():
    if len(sys.argv) < 2:
        print("usage: sagco-menu.py categories|items|recent|add_recent <args?>", file=sys.stderr)
        sys.exit(2)

    spm = load_spm()
    user_key = get_user_key()
    state = load_state(user_key)
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
        for name, icon, desc, cmd, cat_key in items(spm, cat, search):
            print(f"{name}\t{icon}\t{desc}\t{cmd}\t{cat_key}")
        return

    if mode == "recent":
        for name, icon, desc, cmd, cat_key in recent(spm, state):
            print(f"{name}\t{icon}\t{desc}\t{cmd}\t{cat_key}")
        return

    if mode == "add_recent":
        if len(sys.argv) < 4:
            print("usage: sagco-menu.py add_recent <category> <name>", file=sys.stderr)
            sys.exit(2)
        updated_state = add_recent(state, sys.argv[2], sys.argv[3])
        save_state(user_key, updated_state)
        return

    print(f"unknown mode: {mode}", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
