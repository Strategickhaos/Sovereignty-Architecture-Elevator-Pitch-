# SAGCO-MENU v1.2

SAGCO-MENU is a YAML-driven, post-login TUI that supports ordered categories, iconography, global fuzzy search across all tools, and a per-user recency list—without hardcoding menu structure.

## Features

- **YAML-driven configuration**: Single source of truth in `spm.yml`
- **Per-user state**: State stored in `${XDG_STATE_HOME:-~/.local/state}/sagco/menu_state.json`
- **Global fuzzy search**: Search across all tools with typo tolerance
- **Ordered categories**: Define custom category order in YAML
- **Iconography**: Full emoji support for categories and tools
- **Recency tracking**: Last 5 used tools, deduplicated
- **Collision-proof**: Unique keys prevent tool name conflicts across categories

## Installation

```bash
# Install to /opt/sagco (recommended)
sudo cp -r opt/sagco /opt/

# Or use custom location
export SAGCO_BIN=/path/to/sagco/bin
export SPM_PATH=/path/to/spm.yml
```

## Usage

```bash
# Launch interactive menu
/opt/sagco/bin/sagco-menu.sh

# CLI commands
/opt/sagco/bin/sagco-menu.py categories           # List categories
/opt/sagco/bin/sagco-menu.py items security-tools # List tools in category
/opt/sagco/bin/sagco-menu.py recent               # Show recent tools
/opt/sagco/bin/sagco-menu.py add_recent networking Ping  # Add to recent
```

## Configuration

Edit `spm.yml` to add/modify tools:

```yaml
tools:
  order:
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

## Fixes in v1.2

### Bug Fix 1: Per-user state (non-root compatible)
✅ State now stored in `${XDG_STATE_HOME:-~/.local/state}/sagco/` instead of `/var/lib/sagco`

### Bug Fix 2: Tool name collision prevention
✅ Internal keys use `category::name` format to prevent collisions when different categories have tools with the same name

### Bug Fix 3: Categories list cleanup
✅ The "order" key is now properly excluded from category listings

## Dependencies

- Python 3.7+
- PyYAML (`pip install pyyaml`)
- whiptail (usually pre-installed on Linux)
- bash

## Capstone Statement

> "SAGCO-MENU is a YAML-driven, post-login TUI that supports ordered categories, iconography, global fuzzy search across all tools, and a per-user recency list—without hardcoding menu structure."
