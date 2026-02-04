#!/usr/bin/env python3
import sys
import yaml
import json
import os
from difflib import get_close_matches

SPM_PATH = os.getenv("SPM_PATH", "/opt/sagco/spm.yml")

def get_state_path():
    user = os.getenv("USER", "global")
    state_dir = os.getenv("SAGCO_STATE_DIR", "/var/lib/sagco")
    return f"{state_dir}/menu_state_{user}.json"

def load_spm():
    with open(SPM_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_state():
    state_path = get_state_path()
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"recent": []}

def save_state(state):
    state_path = get_state_path()
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def categories(spm):
    tools = spm.get("tools", {}) or {}
    order = tools.get("order", list(tools.keys()))
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
                out.append((name, icon, desc, cmd, cat_key))
    return out

def items(spm, category_key, search=""):
    if category_key == "all" or search:  # Global for search
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
        search_lower = search.lower()
        # First pass: substring matching (exact matches)
        substring_matches = []
        for item in out:
            name, icon, desc, cmd, cat_key = item
            searchable = f"{name} {desc} {cmd} {cat_key}".lower()
            if search_lower in searchable:
                substring_matches.append(item)
        
        # If we have substring matches, use those
        if substring_matches:
            out = substring_matches
        else:
            # Fallback to fuzzy matching for typos
            candidates = [f"{n} {d} {cmd} {cat_key}" for n, _, d, cmd, cat_key in out]
            matches = get_close_matches(search_lower, [c.lower() for c in candidates], n=len(out), cutoff=0.6)
            out = [it for it, cand in zip(out, candidates) if cand.lower() in matches]
    return out

def recent(spm, state, limit=5):
    recent = state.get("recent", [])[-limit:]
    out = []
    for entry in recent:
        cat, name = entry.split(":", 1)
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
    state["recent"] = recent[-5:]  # Cap to 5, deduped
    return state

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
        save_state(updated_state)
        return

    print(f"unknown mode: {mode}", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
