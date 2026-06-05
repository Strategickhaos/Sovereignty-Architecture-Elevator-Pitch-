#!/usr/bin/env python3
"""
SAGCO Menu - YAML-Driven Tool Discovery & Navigation
Version 1.3 (TRIG6-verified)

A modular REPL-like tool for navigating the SAGCO/Strategickhaos tool ecosystem.
Loads tool configurations from YAML/JSON, provides fuzzy search, and manages
recent selections with per-user state persistence.

TRIG6 Analysis:
  - ANGLE 1 (Structural): Modular design with distinct loaders, extractors, handlers
  - ANGLE 2 (Narrative): O(n) linear operations, no unbounded loops
  - ANGLE 3 (Emotional): User-focused UX with safe defaults and helpful errors
  - ANGLE 4 (Technical): Safe YAML/JSON, fuzzy matching, bounded state
  - ANGLE 5 (Pedagogical): Clear patterns for learning Python data handling
  - ANGLE 6 (Meta-Narrative): YAML-to-UI bridge making config feel alive
"""

import sys
import os
import json
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Check Python version
if sys.version_info < (3, 7):
    print("Error: Python 3.7+ required", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ============================================================================
# LOADERS: SPM + State (YAML/JSON)
# ============================================================================

def load_spm_config(config_path: str) -> Optional[Dict]:
    """
    Load SPM (System/Tools Package Manager) configuration from YAML/JSON.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Parsed configuration dict or None on error
        
    TRIG6 NOTE: Safe loading with error handling (v1.3 enhancement)
    """
    try:
        path = Path(config_path)
        if not path.exists():
            print(f"Error: Configuration file not found: {config_path}", file=sys.stderr)
            return None
            
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                try:
                    # Safe YAML loading
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"Error: Malformed YAML in {config_path}:", file=sys.stderr)
                    print(f"  {e}", file=sys.stderr)
                    return None
            elif path.suffix == '.json':
                try:
                    config = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error: Malformed JSON in {config_path}:", file=sys.stderr)
                    print(f"  {e}", file=sys.stderr)
                    return None
            else:
                print(f"Error: Unsupported file format: {path.suffix}", file=sys.stderr)
                print("  Supported: .yaml, .yml, .json", file=sys.stderr)
                return None
                
        if not isinstance(config, dict):
            print(f"Error: Configuration must be a dict/object, got {type(config).__name__}", file=sys.stderr)
            return None
            
        return config
        
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        return None


def load_recent_state(state_path: Optional[str] = None) -> List[str]:
    """
    Load recent items from per-user state file.
    
    Args:
        state_path: Optional path to state file (defaults to ~/.sagco_recent.json)
        
    Returns:
        List of recent item names (most recent first)
    """
    if state_path is None:
        home = os.getenv('HOME', os.getenv('USERPROFILE', '/tmp'))
        state_path = os.path.join(home, '.sagco_recent.json')
    
    try:
        path = Path(state_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'recent' in data:
                    return data['recent'][:5]  # Cap at 5
    except Exception:
        # Silent fail - start fresh
        pass
    
    return []


def save_recent_state(recent: List[str], state_path: Optional[str] = None) -> None:
    """
    Save recent items to per-user state file.
    
    Args:
        recent: List of recent item names
        state_path: Optional path to state file
    """
    if state_path is None:
        home = os.getenv('HOME', os.getenv('USERPROFILE', '/tmp'))
        state_path = os.path.join(home, '.sagco_recent.json')
    
    try:
        path = Path(state_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'recent': recent[:5]}, f, indent=2)  # Cap at 5
    except Exception as e:
        print(f"Warning: Could not save recent state: {e}", file=sys.stderr)


# ============================================================================
# EXTRACTORS: Categories + Items (Ordered, Icon'd)
# ============================================================================

def extract_categories(config: Dict) -> List[Dict]:
    """
    Extract categories from SPM configuration.
    
    Args:
        config: Parsed SPM configuration
        
    Returns:
        List of category dicts with 'name', 'icon', 'items' keys
    """
    categories = config.get('categories', [])
    if not isinstance(categories, list):
        return []
    
    result = []
    for cat in categories:
        if isinstance(cat, dict) and 'name' in cat:
            result.append({
                'name': cat.get('name', 'Unknown'),
                'icon': cat.get('icon', '📦'),
                'items': cat.get('items', [])
            })
    
    return result


def extract_all_items(categories: List[Dict]) -> List[Tuple[str, Dict, str]]:
    """
    Extract all items from categories for searching.
    
    Args:
        categories: List of category dicts
        
    Returns:
        List of (item_name, item_dict, category_name) tuples
    """
    items = []
    for cat in categories:
        cat_name = cat['name']
        for item in cat['items']:
            if isinstance(item, dict) and 'name' in item:
                items.append((item['name'], item, cat_name))
    
    return items


# ============================================================================
# HANDLERS: Recent + add_recent (Capped/Deduped)
# ============================================================================

def add_recent(recent: List[str], item_name: str, max_recent: int = 5) -> List[str]:
    """
    Add item to recent list with deduplication and capping.
    
    Args:
        recent: Current recent items list
        item_name: Name of item to add
        max_recent: Maximum items to keep (default 5)
        
    Returns:
        Updated recent list (most recent first)
    """
    # Remove if already exists (dedup)
    if item_name in recent:
        recent.remove(item_name)
    
    # Add to front
    recent.insert(0, item_name)
    
    # Cap at max_recent
    return recent[:max_recent]


# ============================================================================
# SEARCH: Fuzzy Cross-Tool (difflib matches)
# ============================================================================

def fuzzy_search(query: str, items: List[Tuple[str, Dict, str]], 
                cutoff: float = 0.6, limit: int = 5) -> List[Tuple[str, Dict, str]]:
    """
    Perform fuzzy search across all items.
    
    Args:
        query: Search query string
        items: List of (item_name, item_dict, category_name) tuples
        cutoff: Minimum similarity score (0.0-1.0, default 0.6)
        limit: Maximum results to return (default 5)
        
    Returns:
        List of matching items sorted by relevance
    """
    if not query or not items:
        return []
    
    # Get all item names for matching
    item_names = [item[0] for item in items]
    
    # Use difflib for fuzzy matching
    matches = difflib.get_close_matches(query, item_names, n=limit, cutoff=cutoff)
    
    # Return full item tuples for matches
    result = []
    for match in matches:
        for item in items:
            if item[0] == match:
                result.append(item)
                break
    
    return result


# ============================================================================
# OUTPUT: Display Functions
# ============================================================================

def print_header(config: Dict) -> None:
    """Print menu header with configuration info."""
    name = config.get('name', 'SAGCO Menu')
    version = config.get('version', 'unknown')
    desc = config.get('description', '')
    
    print("=" * 70)
    print(f"{name} (v{version})")
    if desc:
        print(f"{desc}")
    print("=" * 70)
    print()


def print_categories(categories: List[Dict]) -> None:
    """Print all categories with their items."""
    for i, cat in enumerate(categories, 1):
        print(f"\n{cat['icon']}  {i}. {cat['name']}")
        print("-" * 70)
        
        items = cat['items']
        if not items:
            print("  (no items)")
            continue
            
        for j, item in enumerate(items, 1):
            if isinstance(item, dict):
                name = item.get('name', 'unknown')
                desc = item.get('description', '')
                print(f"  {i}.{j} {name}")
                if desc:
                    print(f"      → {desc}")


def print_recent(recent: List[str], all_items: List[Tuple[str, Dict, str]]) -> None:
    """Print recent selections."""
    if not recent:
        return
    
    print("\n⏱️  Recent Selections")
    print("-" * 70)
    
    # Find full item info for each recent name
    for i, item_name in enumerate(recent[:5], 1):  # Cap display at 5
        # Find item details
        item_info = None
        for item in all_items:
            if item[0] == item_name:
                item_info = item
                break
        
        if item_info:
            name, item_dict, cat_name = item_info
            desc = item_dict.get('description', '')
            print(f"  R{i}. {name} ({cat_name})")
            if desc:
                print(f"      → {desc}")
        else:
            print(f"  R{i}. {item_name} (not found)")


def print_search_results(results: List[Tuple[str, Dict, str]]) -> None:
    """Print fuzzy search results."""
    if not results:
        print("\nNo matches found.")
        return
    
    print(f"\n🔍 Search Results ({len(results)} matches)")
    print("-" * 70)
    
    for i, (name, item_dict, cat_name) in enumerate(results, 1):
        desc = item_dict.get('description', '')
        cmd = item_dict.get('command', '')
        print(f"  {i}. {name} ({cat_name})")
        if desc:
            print(f"     → {desc}")
        if cmd:
            print(f"     $ {cmd}")


# ============================================================================
# MAIN: Argument Parser & Modes
# ============================================================================

def print_usage():
    """Print usage information."""
    print("Usage: sagco-menu.py [OPTIONS] [CONFIG_PATH]")
    print()
    print("Options:")
    print("  --list, -l              List all categories and items")
    print("  --search QUERY, -s      Search for tools matching QUERY")
    print("  --recent, -r            Show recent selections")
    print("  --help, -h              Show this help message")
    print()
    print("Config Path:")
    print("  Path to SPM configuration file (YAML/JSON)")
    print("  Default: ./spm_tools.yaml")
    print()
    print("Examples:")
    print("  sagco-menu.py --list")
    print("  sagco-menu.py --search deploy")
    print("  sagco-menu.py --recent")
    print("  sagco-menu.py custom_config.yaml --search monitor")


def main():
    """Main entry point with argument parsing."""
    # Parse arguments
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print_usage()
        sys.exit(0)
    
    # Determine mode and config path
    mode = 'list'  # Default mode
    query = None
    config_path = './spm_tools.yaml'  # Default config
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ['--list', '-l']:
            mode = 'list'
        elif arg in ['--search', '-s']:
            mode = 'search'
            if i + 1 < len(args):
                query = args[i + 1]
                i += 1
            else:
                print("Error: --search requires a query argument", file=sys.stderr)
                sys.exit(1)
        elif arg in ['--recent', '-r']:
            mode = 'recent'
        elif not arg.startswith('-'):
            # Assume it's a config path
            config_path = arg
        else:
            print(f"Error: Unknown option: {arg}", file=sys.stderr)
            print_usage()
            sys.exit(1)
        
        i += 1
    
    # Load configuration
    config = load_spm_config(config_path)
    if config is None:
        sys.exit(1)
    
    # Extract categories and items
    categories = extract_categories(config)
    all_items = extract_all_items(categories)
    
    if not categories:
        print("Warning: No categories found in configuration", file=sys.stderr)
    
    # Load recent state
    recent = load_recent_state()
    
    # Execute based on mode
    print_header(config)
    
    if mode == 'list':
        print_categories(categories)
        if recent:
            print()
            print_recent(recent, all_items)
    
    elif mode == 'search':
        if not query:
            print("Error: Search query not provided", file=sys.stderr)
            sys.exit(1)
        
        results = fuzzy_search(query, all_items, cutoff=0.6, limit=5)
        print_search_results(results)
        
        # If exactly one match, add to recent
        if len(results) == 1:
            recent = add_recent(recent, results[0][0])
            save_recent_state(recent)
    
    elif mode == 'recent':
        print_recent(recent, all_items)
    
    print()


if __name__ == '__main__':
    main()
