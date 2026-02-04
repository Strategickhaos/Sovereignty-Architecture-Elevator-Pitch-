# SAGCO-MENU v1.1

**Kali/Parrot-grade UX without sacrificing determinism or YAML purity**

A YAML-driven, state-aware TUI menu system for the Sovereignty Architecture, supporting ordered categories, iconography, fuzzy search, and a recency list—without hardcoding menu structure or introducing runtime dependencies.

## ✨ Features

- **YAML = Single Source of Truth**: All menu structure, icons, and commands defined in `tools.yaml`
- **Zero New Dependencies**: Built with Python + whiptail (standard Linux tools)
- **Fuzzy Search**: Search by name or description across all tools
- **Recents Loop**: Reinforces workflow with recently-used tools
- **Login-Safe Integration**: TTY-gated, only runs in interactive terminals
- **Per-User State**: No sudo friction, multi-user friendly
- **Deterministic**: Predictable behavior, no runtime surprises

## 🚀 Quick Start

```bash
# Launch the menu
./sagco-menu.sh
```

## 📋 Menu Structure

The menu is organized into categories defined in `tools.yaml`:

- **Network Analysis** 🌐: Network mapping, traffic monitoring, port scanning
- **Security Analysis** 🔐: Vulnerability scanning, security benchmarks, LLM safety
- **System Operations** ⚙️: Legion orchestration, performance monitoring, antibody deployment
- **Intelligence Gathering** 🕵️: Web crawling, video intelligence, XCOM parsing
- **Deployment & Infrastructure** 🚀: Quick deploy, empire deployment, status checks

## 🔧 Architecture

### Components

1. **tools.yaml**: YAML configuration defining categories, tools, icons, and commands
2. **sagco-menu.py**: Python state manager for recent tools (per-user storage)
3. **sagco-menu.sh**: Bash/whiptail TUI interface

### State Management

- State stored in `/var/lib/sagco/menu_state_<USER>.json`
- Falls back to `~/.sagco_menu_state.json` if `/var/lib/sagco` isn't writable
- Recent tools capped at 5 unique items
- Automatic deduplication

## 🛡️ Micro-Hardening Features

### 1. Per-User State (Multi-User Friendly)
```python
USER = os.getenv("USER") or "global"
STATE_PATH = f"/var/lib/sagco/menu_state_{USER}.json"
```

- No permission issues between users
- Each user maintains their own recents list
- Still deterministic and predictable

### 2. Empty Search Guard (UX Polish)
```bash
if [[ ${#TOOL_ARGS[@]} -eq 0 ]]; then
  whiptail --title "No Results" --msgbox "No tools matched your search." 8 50
  return
fi
```

- Friendly message instead of empty menu
- Prevents confusion when searches return no results

### 3. Capped Recents (Bounded Growth)
```python
# Cap to last 5 items
recent = recent[-5:]
state["recent"] = recent
save_state(state)
```

- Explicit cap at 5 recent tools
- Automatic deduplication
- No unbounded growth

## 📝 Usage

### Main Menu Options

1. **🔍 Search Tools (Fuzzy)**: Search across all tools by name or description
2. **📋 Browse Categories**: Browse tools organized by category
3. **⏱️ Recent Tools**: Quick access to recently-used tools
4. **🗑️ Clear Recents**: Clear the recent tools list
5. **❌ Exit**: Exit the menu

### Adding New Tools

Edit `tools.yaml` to add new categories or tools:

```yaml
categories:
  - name: "Your Category"
    icon: "🎯"
    tools:
      - name: "Your Tool"
        description: "What your tool does"
        command: "your-command-here"
        icon: "⚡"
```

### Command-Line State Management

```bash
# Add a tool to recents
./sagco-menu.py add "Tool Name" "command"

# View recent tools
./sagco-menu.py get

# Clear recent tools
./sagco-menu.py clear
```

## 🔐 Requirements

- Python 3.x
- whiptail (usually pre-installed on Debian/Ubuntu)
- PyYAML (optional, falls back to basic parsing)

Install whiptail if needed:
```bash
sudo apt-get install whiptail
```

Install PyYAML for better YAML parsing (optional):
```bash
pip3 install pyyaml
```

## 🎯 Design Philosophy

> "The post-login TUI is YAML-driven and state-aware, supporting ordered categories, iconography, fuzzy search, and a recency list—without hardcoding menu structure or introducing runtime dependencies."

This menu system embodies the principles of:
- **Simplicity**: No complex dependencies or frameworks
- **Determinism**: Predictable behavior, easy to reason about
- **Maintainability**: YAML-based configuration, easy to extend
- **User Experience**: Kali/Parrot-grade UX with modern features
- **Security**: Per-user state, proper permission handling

## 🚀 Future Enhancements (v1.2 Ideas)

- **A) Search Everywhere**: Global search across all categories in one input
- **B) Tool Metadata Badges**: Add tags like `network`, `exploit`, `vm` and filter by tag
- **C) Menu Telemetry**: Local logging to `/var/log/sagco/menu.log` for demos
- **D) ISO Integration**: Bake menu + SBIP into a Kali live ISO

## 📄 License

Part of the Sovereignty Architecture project.
