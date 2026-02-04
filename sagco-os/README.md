# SAGCO OS - Strategic Academic Governance & Cognitive Operations System

**Version:** 1.0.0  
**Codename:** Ratio Ex Nihilo  
**Build ID:** INV-099  
**Owner:** Strategickhaos DAO LLC

## Overview

SAGCO OS is a cognitive operating system designed for academic and engineering workflows, featuring a Kali/Parrot-style post-login TUI menu system.

## Features

### Post-Login TUI Menu System
- **Kali-Style Categories**: Tool groups organized like Kali/Parrot Linux
- **Interactive Launcher**: whiptail-based TUI for easy navigation
- **YAML-Driven**: All tools configured in `spm.yml`
- **Auto-Start**: Displays banner and menu on login via systemd

### Tool Categories

1. **Core Tools**: Git, TMUX, and essential utilities
2. **Security Tools**: Nmap, Metasploit, and penetration testing tools
3. **Operations Tools**: Docker, QEMU, and infrastructure management

## Directory Structure

```
sagco-os/
├── spm.yml                    # Main configuration file
├── install.sh                 # Installation script (recommended)
├── demo.sh                    # Demo script (shows features)
├── README.md                  # This file
├── scripts/
│   ├── sagco-spm.py          # SPM runner/installer
│   └── sagco-menu.sh         # TUI menu launcher
├── services/
│   ├── sagco-banner.service  # Banner + menu service
│   └── sagco-runtime.service # Runtime service
├── assets/
│   └── banner.ascii          # ASCII banner art
└── ui/
    ├── motd                  # Message of the day
    └── issue                 # Login issue file
```

## Quick Start

### Demo (No Installation Required)

See what SAGCO OS looks like without installing:

```bash
cd sagco-os
./demo.sh
```

### Installation

**Automated Installation (Recommended):**

```bash
cd sagco-os
sudo ./install.sh
```

This will:
- Install required packages (whiptail, jq, python3-yaml)
- Copy files to `/opt/sagco/`
- Install systemd services
- Configure the TUI menu system

**Manual Installation:**

```bash
cd sagco-os
sudo python3 scripts/sagco-spm.py spm.yml
```

### Post-Installation

Enable and start services:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sagco-banner.service
sudo systemctl enable sagco-runtime.service
```

### Test the Menu

You can test the menu without rebooting:

```bash
sudo /opt/sagco/scripts/sagco-menu.sh
```

## Usage

After installation and reboot:

1. **Login** to the system
2. **Banner displays** automatically showing SAGCO OS branding
3. **TUI Menu launches** with tool categories
4. **Navigate** using arrow keys
5. **Select** a category to see available tools
6. **Launch** tools with Enter key
7. **Exit** returns you to shell

### Manual Launch

You can always launch the menu manually:

```bash
sagco-menu
```

Or directly:

```bash
/opt/sagco/scripts/sagco-menu.sh
```

## Configuration

### Adding New Tools

Edit `spm.yml` and add tools to the appropriate category:

```yaml
tools:
  your-category:
    description: "Your Category Description"
    items:
      - name: "Tool Name"
        command: "command-to-run"
        description: "Tool description"
```

### Adding New Categories

Add a new top-level entry under `tools:`:

```yaml
tools:
  new-category:
    description: "New Category"
    items:
      - name: "Example Tool"
        command: "echo 'Hello'"
        description: "Example"
```

## Components

### sagco-spm.py
Python-based package manager that:
- Reads `spm.yml` configuration
- Installs packages (apt, pip)
- Copies files to system locations
- Configures systemd services
- Creates verification manifests

### sagco-menu.sh
Bash + whiptail TUI launcher that:
- Reads tool definitions from `/opt/sagco/spm.yml`
- Presents categories in a menu
- Launches selected tools
- Loops back to menu after execution

### sagco-banner.service
Systemd service that:
- Displays ASCII banner on login
- Launches sagco-menu.sh
- Provides Kali/Parrot-style experience

## Requirements

- Debian-based Linux (Kali Rolling recommended)
- Python 3.10+
- whiptail (for TUI)
- jq (for JSON processing)
- python3-yaml (for YAML parsing)

## Testing

### Test Menu Locally

```bash
# Set up test environment
export SPM=/path/to/sagco-os/spm.yml
mkdir -p /opt/sagco
cp spm.yml /opt/sagco/spm.yml

# Run menu
./scripts/sagco-menu.sh
```

### Test Banner

```bash
cat assets/banner.ascii
```

### Test SPM Runner

```bash
python3 scripts/sagco-spm.py spm.yml
```

## Boot Logs

- **Boot logs**: Check with `dmesg` and initramfs script output
- **System services**: Monitor with `journalctl -u sagco-runtime -u sagco-banner`

## Architecture

### spm.yml Structure

```yaml
spm_version: "1.0"
identity:          # OS identity and branding
targets:           # Target distro/arch
repos:             # APT repositories
packages:          # Packages to install (apt, pip)
groups:            # Meta-package groups
tools:             # TUI-launchable tool categories ⭐ NEW
services:          # Systemd services
ui:                # UI configuration
files:             # Files to copy
commands:          # Post-install commands
verification:      # Verification steps
artifacts:         # Log/state directories
```

### Post-Login Flow

```
Login → sagco-banner.service starts
    ↓
Banner displays (banner.ascii)
    ↓
sagco-menu.sh launches
    ↓
Reads /opt/sagco/spm.yml
    ↓
Shows whiptail TUI with categories
    ↓
User selects category
    ↓
Shows tools in category
    ↓
User selects tool
    ↓
Executes tool command
    ↓
Returns to menu
```

## Customization

### Change Banner

Edit `assets/banner.ascii` with your custom ASCII art.

### Change Service Behavior

Edit `services/sagco-banner.service`:

```ini
[Service]
ExecStart=/bin/bash -c 'clear && cat /opt/sagco/assets/banner.ascii && /opt/sagco/scripts/sagco-menu.sh'
```

### Skip Menu on Login

Disable the service:

```bash
sudo systemctl disable sagco-banner.service
```

## Verification

Check installation status:

```bash
# Check if SPM ran successfully
cat /var/lib/sagco/spm_installed.json

# Check logs
tail -f /var/log/sagco/spm_verify.log

# Test services
systemctl status sagco-banner.service
systemctl status sagco-runtime.service
```

## Troubleshooting

### Menu doesn't appear on login
- Check service status: `systemctl status sagco-banner.service`
- Check logs: `journalctl -u sagco-banner.service`
- Verify files exist: `ls /opt/sagco/`

### Tools don't launch
- Verify tool is installed: `which <tool>`
- Check command in spm.yml is correct
- Run menu manually to see errors: `/opt/sagco/scripts/sagco-menu.sh`

### Python errors
- Install dependencies: `pip3 install pyyaml`
- Check Python version: `python3 --version` (needs 3.10+)

## License

Proprietary - Strategickhaos DAO LLC. All rights reserved.

---

**"Ratio Ex Nihilo"** - Reason from Nothing 🔥💜
