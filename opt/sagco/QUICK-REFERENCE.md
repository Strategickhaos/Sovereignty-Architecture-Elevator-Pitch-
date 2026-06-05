# SAGCO-MENU v1.1 Quick Reference

## File Locations

```
/opt/sagco/
├── spm.yml                      # Tool catalog (YAML source of truth)
├── README.md                    # Complete documentation
├── deploy.sh                    # Deployment script
└── bin/
    ├── sagco-menu.py           # Python backend
    └── sagco-menu.sh           # Bash wrapper (whiptail UI)

/etc/profile.d/
└── sagco-menu.sh               # Login integration

/var/lib/sagco/
└── menu_state.json             # Recently used state (auto-created)
```

## Command Reference

### Python Backend (sagco-menu.py)

```bash
# List all categories with icons
/opt/sagco/bin/sagco-menu.py categories

# List tools in a category
/opt/sagco/bin/sagco-menu.py items <category>

# Search tools in a category
/opt/sagco/bin/sagco-menu.py items <category> <search-term>

# Show recently used tools
/opt/sagco/bin/sagco-menu.py recent

# Add tool to recent (internal use)
/opt/sagco/bin/sagco-menu.py add_recent <category> <tool-name>
```

### Bash Wrapper (sagco-menu.sh)

```bash
# Launch interactive menu
/opt/sagco/bin/sagco-menu.sh
```

## YAML Structure

```yaml
tools:
  order: ["category1", "category2", ...]  # Display order
  
  category-name:
    icon: "emoji"                # Category icon
    description: "text"          # Category description
    items:
      - name: "Tool Name"        # Tool name (display)
        icon: "emoji"            # Tool icon
        command: "cmd"           # Command to execute
        description: "text"      # Tool description
```

## Common Tasks

### Add New Tool

Edit `/opt/sagco/spm.yml`:

```yaml
items:
  - name: "MyTool"
    icon: "🔧"
    command: "mytool --help"
    description: "My custom tool"
```

### Add New Category

Edit `/opt/sagco/spm.yml`:

```yaml
tools:
  order: ["core-tools", "security-tools", "ops-tools", "custom"]
  
  custom:
    icon: "⭐"
    description: "Custom Tools"
    items:
      - name: "Tool1"
        icon: "🎯"
        command: "tool1"
        description: "First tool"
```

### Change Category Order

Edit `/opt/sagco/spm.yml`:

```yaml
tools:
  order: ["security-tools", "ops-tools", "core-tools"]  # New order
```

### Disable Auto-Launch

```bash
sudo rm /etc/profile.d/sagco-menu.sh
# OR
sudo mv /etc/profile.d/sagco-menu.sh /etc/profile.d/sagco-menu.sh.disabled
```

### Clear Recent History

```bash
sudo rm /var/lib/sagco/menu_state.json
```

### Test Configuration

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('/opt/sagco/spm.yml'))"

# Test categories
/opt/sagco/bin/sagco-menu.py categories

# Test search
/opt/sagco/bin/sagco-menu.py items security-tools network
```

## Troubleshooting

### Menu doesn't appear on login
- Check: `/etc/profile.d/sagco-menu.sh` exists and is executable
- Check: Running in interactive TTY (`tty` command)
- Check: Shell is interactive (`echo $-` contains 'i')

### Python script errors
- Install PyYAML: `pip3 install pyyaml`
- Check Python version: `python3 --version` (3.6+)
- Verify file paths exist

### Whiptail not found
- Debian/Ubuntu: `apt-get install whiptail`
- RHEL/CentOS: `yum install newt`

### Permission errors
- State directory: `sudo chmod 755 /var/lib/sagco`
- Scripts: `sudo chmod +x /opt/sagco/bin/*`

## Environment Variables (Testing)

```bash
# Override paths for testing
export SPM_PATH="/path/to/spm.yml"
export STATE_PATH="/path/to/menu_state.json"
export PY="/path/to/sagco-menu.py"
export SPM="/path/to/spm.yml"
```

## Version

**SAGCO-MENU v1.1** - YAML-driven, search/filter, icons, ordering, recently used

---

🔥💜 Built for Kali/Parrot-style terminal control planes
