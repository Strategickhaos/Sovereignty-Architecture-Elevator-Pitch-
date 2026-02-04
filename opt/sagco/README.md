# SAGCO Menu System v1.2

This directory contains the SAGCO menu system files for installation.

## Directory Structure

```
/opt/sagco/
├── bin/
│   ├── sagco-menu.py  # Python backend (CLI interface)
│   └── sagco-menu.sh  # Bash frontend (TUI menu)
├── spm.yml            # System Package Manager config
└── README.md          # This file
```

## Quick Install

```bash
# From repository root:
sudo cp -r opt/sagco /opt/
sudo chmod +x /opt/sagco/bin/*.py /opt/sagco/bin/*.sh
sudo mkdir -p /var/lib/sagco
sudo chmod 755 /var/lib/sagco
```

## Files

### `bin/sagco-menu.py`
- **Purpose**: Python backend for menu operations
- **Dependencies**: python3, python3-yaml (PyYAML)
- **Functions**: categories, items, recent, add_recent
- **Config**: Uses `/opt/sagco/spm.yml` (or `$SPM_PATH`)
- **State**: Per-user files in `/var/lib/sagco/menu_state_$USER.json`

### `bin/sagco-menu.sh`
- **Purpose**: Interactive whiptail-based TUI
- **Dependencies**: bash, whiptail
- **Features**: 
  - Category selection with icons
  - Global fuzzy search
  - Recent items tracking
  - Empty result handling
  - Tool execution

### `spm.yml`
- **Purpose**: YAML configuration for all tools and categories
- **Format**: Hierarchical structure with ordered categories
- **Fields**: icon, description, name, command per tool
- **Editing**: Modify this file to add/remove tools
- **Validation**: Use `python3 -m yaml` to check syntax

## Usage

### Interactive Menu
```bash
/opt/sagco/bin/sagco-menu.sh
```

### Command Line
```bash
# List categories
/opt/sagco/bin/sagco-menu.py categories

# List tools in category
/opt/sagco/bin/sagco-menu.py items security-tools

# Search all tools
/opt/sagco/bin/sagco-menu.py items all "nmap"

# Show recent
/opt/sagco/bin/sagco-menu.py recent

# Add to recent
/opt/sagco/bin/sagco-menu.py add_recent security-tools Nmap
```

## Configuration

### Environment Variables
- `SPM_PATH`: Path to spm.yml (default: `/opt/sagco/spm.yml`)
- `SAGCO_STATE_DIR`: State directory (default: `/var/lib/sagco`)
- `SAGCO_BIN`: Binary directory (default: `/opt/sagco/bin`)

### Example: Custom Paths
```bash
export SPM_PATH="/custom/path/spm.yml"
export SAGCO_STATE_DIR="/custom/state"
/opt/sagco/bin/sagco-menu.sh
```

## Documentation

See full documentation:
- **Quick Start**: `/docs/SAGCO_MENU_QUICKSTART.md`
- **Full Docs**: `/docs/SAGCO_MENU.md`
- **Main README**: `/README.md` (search for "SAGCO Menu")

## Version

**v1.2** - Global Search + Hardened State
- Global fuzzy search across all tools
- Per-user state with deduplication
- Empty result message handling
- Recent items cap (5 items)
- Environment variable configuration

## License

Same as parent project (MIT License)

## Support

For issues, see the main repository documentation or contact the Strategickhaos team.
