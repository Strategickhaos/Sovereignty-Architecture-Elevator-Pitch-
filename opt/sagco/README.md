# SAGCO-MENU v1.1

**YAML-driven terminal menu system for tool management with search, icons, ordering, and recently used tracking.**

---

## Overview

SAGCO-MENU provides a Kali/Parrot-style terminal menu that:
- Reads tool catalog from YAML (`spm.yml`)
- Presents an interactive whiptail-based UI on login
- Supports search/filter across all tools
- Displays icons for categories and tools
- Maintains recently used tools list
- Requires zero additional dependencies (Python + whiptail + jq)

---

## Features

### 1. YAML Source of Truth
All tools, categories, ordering, and icons are defined in `/opt/sagco/spm.yml`:
- **Category ordering**: Define display order via `order` array
- **Icons**: Emoji/ASCII icons for categories and items
- **Flexible structure**: Add/remove tools without touching menu code

### 2. Search/Filter
Type-to-search functionality:
- Fuzzy matching on tool names and descriptions
- Works across all categories
- Real-time filtering in the UI

### 3. Recently Used
Automatic tracking of launched tools:
- Last 5 tools stored in `/var/lib/sagco/menu_state.json`
- Shows as special "Recently Used" category
- Updates on every tool launch

### 4. Interactive UI
Whiptail-based terminal interface:
- Category selection with icons
- Search prompt per category
- Tool selection and execution
- Clean output formatting

---

## Installation

### 1. Deploy Files

```bash
# Copy YAML configuration
sudo cp opt/sagco/spm.yml /opt/sagco/spm.yml

# Copy Python menu script
sudo cp opt/sagco/bin/sagco-menu.py /opt/sagco/bin/sagco-menu.py
sudo chmod +x /opt/sagco/bin/sagco-menu.py

# Copy Bash wrapper
sudo cp opt/sagco/bin/sagco-menu.sh /opt/sagco/bin/sagco-menu.sh
sudo chmod +x /opt/sagco/bin/sagco-menu.sh

# Copy profile integration
sudo cp etc/profile.d/sagco-menu.sh /etc/profile.d/sagco-menu.sh
sudo chmod +x /etc/profile.d/sagco-menu.sh

# Create state directory
sudo mkdir -p /var/lib/sagco
sudo chmod 755 /var/lib/sagco
```

### 2. Verify Dependencies

```bash
# Check Python 3
python3 --version

# Check PyYAML
python3 -c "import yaml"

# Check whiptail
which whiptail

# Check jq (optional, for future features)
which jq
```

### 3. Test

```bash
# Test categories listing
/opt/sagco/bin/sagco-menu.py categories

# Test items listing
/opt/sagco/bin/sagco-menu.py items core-tools

# Test search
/opt/sagco/bin/sagco-menu.py items security-tools nmap

# Launch interactive menu (requires TTY)
/opt/sagco/bin/sagco-menu.sh
```

### 4. Login Integration

The menu will automatically launch on interactive shell login via `/etc/profile.d/sagco-menu.sh`.

To disable auto-launch, remove or comment out the profile script.

---

## Configuration

### Adding Tools

Edit `/opt/sagco/spm.yml`:

```yaml
tools:
  order: ["core-tools", "security-tools", "ops-tools", "custom-tools"]
  custom-tools:
    icon: "🎯"
    description: "Custom Tools"
    items:
      - name: "MyTool"
        icon: "⚡"
        command: "mytool --help"
        description: "Custom tool description"
```

### Changing Category Order

Update the `order` array:

```yaml
tools:
  order: ["security-tools", "core-tools", "ops-tools"]  # New order
```

### Customizing Icons

Use any emoji or ASCII characters:

```yaml
security-tools:
  icon: "🔐"  # Category icon
  items:
    - name: "Tool"
      icon: "🚀"  # Item icon
```

---

## Architecture

### Components

1. **spm.yml** - YAML source of truth
   - Defines all categories, tools, ordering, icons
   - Single source for menu structure

2. **sagco-menu.py** - Python backend
   - Loads YAML configuration
   - Handles search/filter logic
   - Manages recently used state (JSON)
   - Provides CLI interface for menu operations

3. **sagco-menu.sh** - Bash wrapper
   - Whiptail-based UI
   - Orchestrates user interactions
   - Launches tools in clean environment

4. **sagco-menu.sh (profile.d)** - Login integration
   - Launches menu on interactive login
   - Checks for TTY before running

5. **menu_state.json** - State persistence
   - Recently used tools (last 5)
   - JSON format for easy inspection
   - Global for v1.1 (per-user in v1.2)

### Data Flow

```
Login → /etc/profile.d/sagco-menu.sh
    ↓
sagco-menu.sh (bash wrapper)
    ↓
sagco-menu.py categories → List categories
    ↓
User selects category
    ↓
sagco-menu.py items <category> [search] → List tools
    ↓
User selects tool
    ↓
bash -lc "<command>" → Execute tool
    ↓
sagco-menu.py add_recent <category> <tool> → Update state
```

---

## Usage Examples

### Manual Menu Launch

```bash
/opt/sagco/bin/sagco-menu.sh
```

### Python CLI Examples

```bash
# List all categories
/opt/sagco/bin/sagco-menu.py categories

# List tools in security-tools category
/opt/sagco/bin/sagco-menu.py items security-tools

# Search for "network" in ops-tools
/opt/sagco/bin/sagco-menu.py items ops-tools network

# Show recently used tools
/opt/sagco/bin/sagco-menu.py recent

# Add tool to recent (internal use)
/opt/sagco/bin/sagco-menu.py add_recent security-tools Nmap
```

---

## Troubleshooting

### Menu doesn't launch on login
- Check `/etc/profile.d/sagco-menu.sh` exists and is executable
- Verify interactive shell: `echo $-` should contain 'i'
- Check TTY: `tty` should show a terminal device

### Python script fails
- Verify PyYAML: `python3 -c "import yaml"`
- Check file paths: `/opt/sagco/spm.yml` must exist
- Check permissions: Script must be executable

### Whiptail not found
- Install whiptail: `apt-get install whiptail` (Debian/Ubuntu)
- Or use newt: `apt-get install newt`

### State file errors
- Create directory: `sudo mkdir -p /var/lib/sagco`
- Fix permissions: `sudo chmod 755 /var/lib/sagco`

---

## Future Enhancements (v1.2+)

- Per-user state files (`$HOME/.sagco/menu_state.json`)
- Better fuzzy search with scoring (difflib thresholds)
- Tool descriptions with markdown rendering
- Command history integration
- Bookmarks/favorites
- Multi-column display for large tool lists

---

## CAPSTONE SENTENCE

> "SAGCO provides a YAML-defined tool catalog (SPM) that drives a post-login terminal UI. On interactive login, a menu reads spm.yml and presents Kali-like tool categories, launching selected tools deterministically without hardcoding the menu structure."

**v1.1 Complete.** 🔥💜
