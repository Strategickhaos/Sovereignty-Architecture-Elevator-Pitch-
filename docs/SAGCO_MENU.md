# SAGCO-MENU v1.2 Documentation

## Overview

SAGCO-MENU is a post-login TUI (Text User Interface) menu system for SAGCO OS that provides an organized, searchable interface for launching system tools and utilities. The menu is YAML-driven and state-aware, supporting ordered categories, iconography, fuzzy search, and a recency list—without hardcoding menu structure or introducing runtime dependencies.

## Key Features

### ✅ v1.2 Features
- **Global Fuzzy Search**: One search box searches ALL tools across categories (fuzzy matching on name/desc/cmd/category)
- **Per-User State**: Each user gets their own state file (`/var/lib/sagco/menu_state_$USER.json`)
- **Recent Items Tracking**: Maintains a list of the 5 most recently used tools (deduplicated)
- **Empty Result Guard**: Shows a user-friendly message when no tools match the search
- **YAML-Driven**: All tool configuration is in `/opt/sagco/spm.yml` - no code changes needed
- **Zero Dependencies**: Uses only standard Python libraries (yaml, json, difflib) and bash builtins
- **Icon Support**: Tools and categories can have emoji icons for better visual identification
- **Ordered Categories**: Define custom category order in YAML

## Architecture

```
┌─────────────────────────────────────────┐
│      sagco-menu.sh (Bash Frontend)      │
│  - Whiptail TUI                         │
│  - User interaction loop                │
│  - Global search handling               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    sagco-menu.py (Python Backend)       │
│  - YAML parsing                         │
│  - JSON state management                │
│  - Fuzzy search (difflib)               │
│  - Per-user state files                 │
└─────────────────┬───────────────────────┘
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│  spm.yml     │      │  Per-user state  │
│  (Config)    │      │  JSON files      │
└──────────────┘      └──────────────────┘
```

## Files

### `/opt/sagco/bin/sagco-menu.py`
Python backend that handles:
- Loading YAML configuration from `/opt/sagco/spm.yml`
- Managing per-user state in `/var/lib/sagco/menu_state_$USER.json`
- Fuzzy search across all tools using `difflib.get_close_matches()`
- Recent items tracking with cap and deduplication

**CLI Interface:**
```bash
sagco-menu.py categories              # List all categories
sagco-menu.py items <category> [search]  # List items (with optional search)
sagco-menu.py recent                   # List recent items
sagco-menu.py add_recent <cat> <name>  # Add to recent list
```

### `/opt/sagco/bin/sagco-menu.sh`
Bash frontend that provides:
- Interactive whiptail-based menu UI
- Category selection with icons
- Global search prompt
- Empty result handling
- Tool execution and recent updates

### `/opt/sagco/spm.yml`
YAML configuration defining all tools and categories:
```yaml
tools:
  order:  # Optional: define category order
    - security-tools
    - networking
  
  security-tools:
    icon: "🔒"
    description: "Security and penetration testing tools"
    items:
      - name: "Nmap"
        icon: "🌐"
        description: "Network discovery and security auditing"
        command: "nmap --help"
```

## Usage

### Interactive Menu
```bash
# Launch the menu
/opt/sagco/bin/sagco-menu.sh

# Typical workflow:
# 1. Select a category (or "recent" if available)
# 2. Enter optional search term (leave empty to see all)
# 3. Select a tool to launch
# 4. Tool runs, then press Enter to return
```

### Global Search
When you enter a search term, the menu automatically switches to "all" category and searches across:
- Tool names
- Tool descriptions
- Tool commands
- Category names

**Search Algorithm**: Uses fuzzy matching with 0.6 cutoff (60% similarity threshold)

**Example**: Searching "nmap" will find:
- Tools with "nmap" in the name
- Tools with "nmap" in the description
- Tools with "nmap" in the command

### Recent Items
The menu tracks your 5 most recently used tools:
- Automatically added after launching a tool
- Deduplicated (same tool only appears once)
- Displayed as "🕒 Recently Used" category
- Per-user (each user has their own recents)

## Configuration

### Adding a New Tool
Edit `/opt/sagco/spm.yml`:
```yaml
  my-category:
    icon: "🎯"
    description: "My custom category"
    items:
      - name: "My Tool"
        icon: "⚡"
        description: "Does something awesome"
        command: "my-tool --interactive"
```

### Changing Category Order
Edit the `order` list in `/opt/sagco/spm.yml`:
```yaml
tools:
  order:
    - most-used
    - security-tools
    - networking
    - development
```

### Per-User State Location
State files are stored at: `/var/lib/sagco/menu_state_$USER.json`

**Ensure the directory exists:**
```bash
sudo mkdir -p /var/lib/sagco
sudo chmod 755 /var/lib/sagco
```

## Technical Details

### Global Search Implementation
When a search term is provided:
1. `sagco-menu.sh` sets `EFFECTIVE_CHOICE="all"`
2. `sagco-menu.py items` function detects "all" or non-empty search
3. Uses `all_items()` to get tools from ALL categories
4. Applies fuzzy matching with `get_close_matches()`
5. Returns filtered results with category information

### State Management
- **File Format**: JSON with simple structure: `{"recent": ["cat:name", ...]}`
- **Atomicity**: Uses Python's `json.dump()` for atomic writes
- **Deduplication**: Removes duplicates before adding to recent list
- **Cap**: Maintains maximum of 5 recent items

### Empty Result Handling
If no tools match the search:
```bash
whiptail --title "No Results" --msgbox "No tools matched your search." 8 50
```
User returns to category selection to try again.

## Capstone Statement

**The post-login TUI is YAML-driven and state-aware, supporting ordered categories, iconography, fuzzy search, and a recency list—without hardcoding menu structure or introducing runtime dependencies.**

## Deployment

### Quick Deploy
```bash
# 1. Copy files to /opt/sagco/
sudo cp -r opt/sagco /opt/

# 2. Make scripts executable
sudo chmod +x /opt/sagco/bin/*.py /opt/sagco/bin/*.sh

# 3. Ensure state directory exists
sudo mkdir -p /var/lib/sagco
sudo chmod 755 /var/lib/sagco

# 4. Test the menu
/opt/sagco/bin/sagco-menu.sh
```

### Auto-launch on Login
Add to `/etc/profile.d/sagco-menu.sh`:
```bash
#!/bin/bash
if [[ -t 0 ]] && [[ -f /opt/sagco/bin/sagco-menu.sh ]]; then
  /opt/sagco/bin/sagco-menu.sh
fi
```

## Future Enhancements (v1.3+)

Potential features for future versions:
- **Tag Badges**: Add tags to tools (e.g., "beginner", "advanced")
- **Telemetry Log**: Track tool usage statistics
- **Command History**: Show previously used commands
- **Favorites**: Star/favorite specific tools
- **Custom Shortcuts**: Define keyboard shortcuts for common tools
- **Multi-language**: Support for tool descriptions in multiple languages

## Version History

### v1.2 (Current)
- ✅ Global fuzzy search across all tools
- ✅ Per-user state via `$USER`-filed JSON
- ✅ Empty search result message
- ✅ Recent items cap (5) with deduplication
- ✅ ~25 lines of changes from v1.1

### v1.1
- Category-based navigation
- Per-category search
- Basic recent items
- Icon support

### v1.0
- Initial release
- YAML-driven configuration
- Whiptail TUI
- Basic tool launching
