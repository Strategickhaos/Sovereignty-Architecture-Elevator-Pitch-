# SAGCO Menu System v1.1

A YAML-driven terminal menu system for tool catalog management, featuring search/filter, ordered categories, icons, and recently used tracking.

## Features

- **YAML-Driven Configuration**: Single source of truth in `spm.yml`
- **Search/Filter**: Type-to-search across all tools (fuzzy match on name/description)
- **Category Ordering**: YAML-defined order via `order` key
- **Icons**: Simple emoji/ASCII per category and item
- **Recently Used**: Tracks last 5 used tools
- **Zero Dependencies**: Python 3 + whiptail (standard on most Linux distros)

## Architecture

### File Structure

```
opt/sagco/
├── spm.yml                    # YAML tool catalog (source of truth)
├── menu_state.json            # Recently used tools (auto-created)
└── bin/
    ├── sagco-menu.py          # Python CLI for menu operations
    └── sagco-menu.sh          # Bash/whiptail UI wrapper

etc/profile.d/
└── sagco-menu.sh              # Auto-launch on interactive login (optional)
```

## Configuration

### spm.yml Structure

```yaml
tools:
  order: ["core-tools", "security-tools", "ops-tools"]  # Category order
  core-tools:
    icon: "🛠️"                                           # Category icon
    description: "Core Utilities"
    items:
      - name: "Git"
        icon: "📂"                                       # Item icon
        command: "git --version"
        description: "Version control"
```

### Adding New Tools

Edit `opt/sagco/spm.yml`:

1. Add category to `tools.order` (if new)
2. Create category section with icon and description
3. Add items with name, icon, command, and description

## Usage

### CLI Interface

```bash
# List categories
python3 opt/sagco/bin/sagco-menu.py categories

# List items in a category
python3 opt/sagco/bin/sagco-menu.py items core-tools

# Search/filter items
python3 opt/sagco/bin/sagco-menu.py items security-tools nmap

# Show recently used
python3 opt/sagco/bin/sagco-menu.py recent

# Add to recent (called automatically by menu)
python3 opt/sagco/bin/sagco-menu.py add_recent core-tools Git
```

### Interactive Menu (Whiptail)

```bash
# Run the interactive menu
./opt/sagco/bin/sagco-menu.sh
```

The menu will:
1. Show category selection (with icons, ordered as configured)
2. Prompt for search term (optional)
3. Show tool selection (filtered by search)
4. Execute selected tool
5. Add to recently used

### Auto-Launch on Login

To auto-launch the menu on interactive login:

```bash
# Set REPO_ROOT environment variable (if needed)
export REPO_ROOT=/path/to/repository

# Source the profile.d script
source etc/profile.d/sagco-menu.sh
```

Or copy to system profile.d:

```bash
sudo cp etc/profile.d/sagco-menu.sh /etc/profile.d/
```

## Testing

```bash
# Test categories
python3 opt/sagco/bin/sagco-menu.py categories

# Test items
python3 opt/sagco/bin/sagco-menu.py items core-tools

# Test search
python3 opt/sagco/bin/sagco-menu.py items security-tools network

# Test recent tracking
python3 opt/sagco/bin/sagco-menu.py add_recent core-tools Git
python3 opt/sagco/bin/sagco-menu.py recent
```

## CAPSTONE

> "SAGCO provides a YAML-defined tool catalog (SPM) that drives a post-login terminal UI. On interactive login, a menu reads spm.yml and presents Kali-like tool categories, launching selected tools deterministically without hardcoding the menu structure."

## v1.1 Features

- ✅ YAML-driven configuration
- ✅ Fuzzy search/filter
- ✅ Icons for categories and items
- ✅ Ordered categories
- ✅ Recently used tracking (last 5)
- ✅ Zero new dependencies
- ✅ Whiptail UI integration

## Future Enhancements (v1.2+)

- Per-user state (vs global)
- Better fuzzy search (difflib thresholds)
- Favorites/pinning
- Tool metadata (tags, categories)
- Command history
