# SAGCO-MENU v1.2 - Quick Start Guide

## 🚀 Installation (3 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/sagco

# 2. Run installer (requires sudo)
sudo ./install.sh

# 3. Test immediately (or login to new shell)
/opt/sagco/bin/sagco-menu.sh
```

## 🎯 Key Features

### Cross-Tool Fuzzy Search
- Search across ALL categories simultaneously
- Fuzzy matching finds similar terms (60% threshold)
- Searches in: tool name, description, and command

### Example Searches
```
Search: "nmap"     → Finds "Nmap" in security tools
Search: "docker"   → Finds "Docker" in core tools
Search: "network"  → Finds all network-related tools
Search: "version"  → Finds tools with "--version" in command
```

### Recently Used Tracking
- Last 5 tools tracked per-user
- Stored in `/var/lib/sagco/menu_state.json`
- Appears as first menu option for quick access

### Category Ordering & Icons
- Categories display in YAML-defined order
- Each category has an icon (emoji/ASCII)
- Each tool has an icon for visual identification

## 📋 Menu Navigation

```
1. Main Menu
   ┌─────────────────────────────────────┐
   │ SAGCO Tools Menu                    │
   ├─────────────────────────────────────┤
   │ 🕒 Recently Used                    │
   │ 🛠️  Core System Utilities           │
   │ 🔒 Security & Penetration Testing   │
   │ ⚙️  DevOps & Operations             │
   │ 🌐 Network Utilities                │
   └─────────────────────────────────────┘

2. Search Prompt (Optional)
   ┌─────────────────────────────────────┐
   │ Enter search term:                  │
   │ [nmap]                              │
   └─────────────────────────────────────┘

3. Tool Selection
   ┌─────────────────────────────────────┐
   │ 🔍 Nmap - Network scanner           │
   │ 💉 SQLMap - SQL injection tool      │
   │ 🎯 Metasploit - Exploitation...     │
   └─────────────────────────────────────┘

4. Tool Execution
   SAGCO ▶ Nmap
   CMD  ▶ nmap --version
   
   Nmap version 7.94 ( https://nmap.org )
   
   Press Enter to return to menu...
```

## 🔧 Customization

### Add New Category

Edit `/opt/sagco/spm.yml`:

```yaml
tools:
  order: ["core-tools", "security-tools", "ops-tools", "network-tools", "custom-tools"]
  
  custom-tools:
    icon: "🎨"
    description: "My Custom Tools"
    items:
      - name: "MyTool"
        icon: "⭐"
        command: "mytool --version"
        description: "Custom tool description"
```

### Add New Tool

Add to any category's `items` array:

```yaml
- name: "Nessus"
  icon: "🔬"
  command: "nessus --version"
  description: "Vulnerability scanner"
```

## 🛠️ Troubleshooting

### Menu doesn't launch on login
```bash
# Check if profile.d script exists
ls -la /etc/profile.d/sagco-menu.sh

# Test manually
/opt/sagco/bin/sagco-menu.sh
```

### "whiptail not found"
```bash
sudo apt-get install whiptail
```

### "yaml module not found"
```bash
pip3 install pyyaml
```

### Disable auto-launch
```bash
sudo mv /etc/profile.d/sagco-menu.sh /etc/profile.d/sagco-menu.sh.disabled
```

## 📊 State Management

View your recently used tools:
```bash
cat /var/lib/sagco/menu_state.json
```

Reset your recent list:
```bash
sudo rm /var/lib/sagco/menu_state.json
```

## 🎓 Advanced Usage

### Test Python Backend
```bash
# List categories
/opt/sagco/bin/sagco-menu.py categories

# List tools in category
/opt/sagco/bin/sagco-menu.py items security-tools

# Search across all tools
/opt/sagco/bin/sagco-menu.py items all nmap

# View recent
/opt/sagco/bin/sagco-menu.py recent
```

### Validate YAML
```bash
python3 -c "import yaml; print(yaml.safe_load(open('/opt/sagco/spm.yml')))"
```

## 🔥 What's New in v1.2

- ✨ **Cross-tool search** - Search ALL categories at once
- 🔍 **Fuzzy matching** - Intelligent search using difflib
- 🎨 **Icons** - Category and tool icons for visual identification
- 🕒 **Recently used** - Last 5 tools tracked per-user
- 📑 **Ordered categories** - YAML-defined display order
- 👤 **Per-user state** - Each user has independent recent list

## 💜 Credits

**Owner**: Strategickhaos DAO LLC  
**Developer**: Dom (Me10101)  
**Version**: 1.2  
**Architecture**: YAML-driven deterministic menu system

DOM. 😭🔥💜
