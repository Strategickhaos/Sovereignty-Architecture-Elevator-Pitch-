# SAGCO-MENU v1.2

**Strategic Academic Governance & Cognitive Operations - Terminal Menu System**

SAGCO-MENU provides a YAML-defined tool catalog (SPM) that drives a post-login terminal UI. On interactive login, a menu reads spm.yml and presents Kali-like tool categories (ordered with icons), launching selected tools deterministically without hardcoding the menu structure.

## Features

### v1.2 Enhancements
- ✨ **Cross-Tool Search/Filter**: Type-to-search across ALL tools (fuzzy matching via difflib, matches name/desc/cmd)
- 🎨 **Category Ordering**: YAML "order" array controls menu sequence
- 🎭 **Icons**: Emoji/ASCII per category and item (YAML "icon" field)
- 🕒 **Recently Used**: Stored in `/var/lib/sagco/menu_state.json` (last 5 items, per-user via $USER key)
- 🔍 **Fuzzy Search**: Uses Python's difflib for intelligent matching
- 👤 **Per-User State**: Each user has their own recently used list
- 📦 **Zero New Dependencies**: Python/difflib built-in, whiptail from v1

## Installation

### 1. Copy Files to System Directories

```bash
# From the repository root
sudo cp -r sagco/opt/sagco /opt/
sudo cp sagco/etc/profile.d/sagco-menu.sh /etc/profile.d/

# Make scripts executable
sudo chmod +x /opt/sagco/bin/sagco-menu.py
sudo chmod +x /opt/sagco/bin/sagco-menu.sh
sudo chmod +x /etc/profile.d/sagco-menu.sh

# Create state directory
sudo mkdir -p /var/lib/sagco
sudo chmod 777 /var/lib/sagco  # Or set appropriate permissions
```

### 2. Install Dependencies

```bash
# Python 3 (usually pre-installed)
# PyYAML for YAML parsing
pip3 install pyyaml

# Whiptail (usually pre-installed on Debian/Ubuntu/Kali)
sudo apt-get install whiptail  # If needed
```

## Usage

### Automatic Launch
SAGCO-MENU automatically launches on interactive login (via `/etc/profile.d/sagco-menu.sh`).

### Manual Launch
```bash
/opt/sagco/bin/sagco-menu.sh
```

### Navigation
1. **Select Category**: Use arrow keys and Enter to select a tool category
2. **Search (Optional)**: Enter search term to filter tools across ALL categories (cross-tool search)
3. **Select Tool**: Choose a tool from the filtered list
4. **Execute**: Tool runs, then press Enter to return to menu
5. **Recently Used**: Your recent selections appear at the top for quick access

### Menu Flow
```
[SAGCO Tools Menu]
  🕒 Recently Used (if any)
  🛠️ Core System Utilities
  🔒 Security & Penetration Testing
  ⚙️ DevOps & Operations
  🌐 Network Utilities
  
  ↓ Select category
  
[Search Prompt]
  Enter search term (optional): nmap
  
  ↓ Press Enter (or type to filter)
  
[Tool List - Filtered]
  🔍 Nmap - Network scanner
  ...
  
  ↓ Select tool
  
[Execute]
  SAGCO ▶ Nmap
  CMD  ▶ nmap --version
  [Tool output here]
  
  Press Enter to return to menu...
```

## Configuration

### YAML Structure

The menu is driven by `/opt/sagco/spm.yml`:

```yaml
tools:
  order: ["core-tools", "security-tools", "ops-tools"]  # Category display order
  
  core-tools:
    icon: "🛠️"  # Category icon (emoji/ASCII)
    description: "Core System Utilities"
    items:
      - name: "Git"
        icon: "📂"  # Item icon
        command: "git --version"
        description: "Version control system"
      - name: "Docker"
        icon: "🐳"
        command: "docker --version"
        description: "Container platform"
  
  security-tools:
    icon: "🔒"
    description: "Security & Penetration Testing"
    items:
      - name: "Nmap"
        icon: "🔍"
        command: "nmap --version"
        description: "Network scanner"
```

### Adding New Categories

1. Add category key to `tools.order` array
2. Define category with `icon`, `description`, and `items`
3. Each item needs: `name`, `icon`, `command`, `description`

### Adding New Tools

Simply add to the `items` array under any category:

```yaml
- name: "MyTool"
  icon: "🔨"
  command: "mytool --help"
  description: "My custom tool"
```

## Architecture

### Components

1. **sagco-menu.py** - Python backend
   - Parses YAML configuration
   - Manages recently used state (JSON)
   - Provides fuzzy search via difflib
   - Handles per-user state tracking

2. **sagco-menu.sh** - Bash frontend
   - Whiptail-based interactive UI
   - Category and tool selection
   - Search prompt integration
   - Command execution

3. **sagco-menu.sh** (profile.d) - Auto-launcher
   - Detects interactive TTY sessions
   - Prevents recursion
   - Launches menu on login

4. **spm.yml** - Configuration
   - YAML source of truth
   - Defines categories and tools
   - Controls ordering and icons

### State Management

Recently used tools are stored per-user in `/var/lib/sagco/menu_state.json`:

```json
{
  "username": {
    "recent": [
      "security-tools:Nmap",
      "core-tools:Git",
      "network-tools:Curl"
    ]
  },
  "global": {
    "recent": []
  }
}
```

## Search Features

### Cross-Tool Fuzzy Search
- Searches across ALL categories when search term provided
- Uses Python's `difflib.get_close_matches()` for fuzzy matching
- Cutoff threshold: 0.6 (60% similarity)
- Searches in: tool name, description, and command

### Search Examples
- Type "nmap" → Finds "Nmap" in security-tools
- Type "docker" → Finds "Docker" in core-tools
- Type "network" → Finds tools with "network" in description
- Type "version" → Finds tools with "--version" in command

## Integration

### Disable Auto-Launch
Comment out or remove `/etc/profile.d/sagco-menu.sh`:
```bash
sudo mv /etc/profile.d/sagco-menu.sh /etc/profile.d/sagco-menu.sh.disabled
```

### Custom Launch Conditions
Edit `/etc/profile.d/sagco-menu.sh` to add conditions:
```bash
# Only launch for specific users
if [[ "$USER" == "pentester" ]]; then
  /opt/sagco/bin/sagco-menu.sh
fi
```

## Development

### Testing Menu Without Auto-Launch
```bash
# Run directly
/opt/sagco/bin/sagco-menu.sh

# Test Python backend
/opt/sagco/bin/sagco-menu.py categories
/opt/sagco/bin/sagco-menu.py items core-tools
/opt/sagco/bin/sagco-menu.py recent
```

### Debugging
```bash
# Check YAML syntax
python3 -c "import yaml; print(yaml.safe_load(open('/opt/sagco/spm.yml')))"

# View recent state
cat /var/lib/sagco/menu_state.json

# Check profile.d integration
ls -la /etc/profile.d/sagco-menu.sh
```

## Requirements

- **Python 3.6+** with PyYAML
- **Bash 4.0+**
- **whiptail** (dialog utility)
- **Interactive TTY** for auto-launch

## Compatibility

Tested on:
- Kali Linux 2023+
- Parrot Security OS
- Ubuntu 20.04+
- Debian 11+

## License

Proprietary - Strategickhaos DAO LLC

## Credits

**Owner**: Strategickhaos DAO LLC  
**Developer**: Dom (Me10101)  
**Version**: 1.2  
**Architecture**: YAML-driven deterministic menu system

---

## Capstone Sentence

> "SAGCO provides a YAML-defined tool catalog (SPM) that drives a post-login terminal UI. On interactive login, a menu reads spm.yml and presents Kali-like tool categories (ordered with icons), launching selected tools deterministically without hardcoding the menu structure."

**v1.2 Complete.** 🔥💜 Cross-tool fuzzy search, ordered/icon'd categories, recent list (JSON-stored).
