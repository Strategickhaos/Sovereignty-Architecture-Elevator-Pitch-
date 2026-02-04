# SAGCO OS - Provisioning Manifest Runner

## Overview

The SAGCO Provisioning Manifest (SPM) system is a declarative provisioning tool for building customized SAGCO OS instances based on Kali Linux. It uses YAML manifests to define the complete system configuration including packages, services, UI customization, and boot identity.

## Quick Start

### Prerequisites
- Kali Linux (rolling) or Debian-based system
- Root access (sudo)
- Python 3.x with pip

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Sovereignty-Architecture-Elevator-Pitch-
```

2. **Ensure you have the emblem image:**
   - Place your `ratio_ex_nihilo.png` emblem in the `assets/` directory
   - See `assets/README.md` for specifications

3. **Run the provisioner:**
```bash
sudo python3 sagco-spm.py spm.yml
```

The script will automatically:
- Install missing Python dependencies (rich, pyyaml)
- Update APT repositories
- Install all specified packages
- Copy configuration files
- Setup systemd services
- Configure Plymouth boot splash
- Verify installation

4. **Reboot to see the full boot identity:**
```bash
sudo reboot
```

## What Gets Installed

### Core Packages
- Development tools: git, curl, wget, build-essential
- Python environment: python3, python3-venv, python3-pip
- Utilities: jq, tmux, zsh
- Boot system: plymouth, plymouth-themes

### Security Tools (Kali Packages)
- nmap - Network scanner
- wireshark - Packet analyzer
- metasploit-framework - Exploitation framework
- sqlmap - SQL injection tool
- gobuster - Directory/file brute-forcer

### Operations Tools
- docker.io - Container runtime
- docker-compose - Container orchestration
- podman - Alternative container runtime
- qemu-system-x86 - CPU emulation

### Python Packages (via pip)
- rich - Terminal formatting
- typer - CLI framework
- pyyaml - YAML parsing
- requests - HTTP library

## Boot Identity Features

### Plymouth Splash Screen
- Custom "Ratio Ex Nihilo" emblem displayed during boot
- Configured automatically by the provisioner
- Theme location: `/usr/share/plymouth/themes/sagco/`

### Login Screen
- Custom issue banner showing SAGCO OS branding
- Location: `/etc/issue`

### Message of the Day (MOTD)
- Post-login welcome message
- Location: `/etc/motd`

### Systemd Services

**sagco-banner.service**
- Displays ASCII art banner and system information
- Runs at boot after network is available

**sagco-runtime.service**
- Placeholder for SAGCO runtime/tools
- Configured for always-restart
- Customize `/opt/sagco/venv/bin/python /opt/sagco/runtime.py` for your needs

## Customization

### Modifying the Manifest

Edit `spm.yml` to customize your installation:

```yaml
# Add more packages
packages:
  apt:
    core:
      - your-package-here
      
# Add custom files
files:
  copy:
    - src: "your/source/file"
      dst: "/destination/path"
      mode: "0644"
      
# Add post-install commands
commands:
  post_install:
    - "your-custom-command"
```

### Custom Services

Add your own systemd services:

1. Create service file in `services/your-service.service`
2. Add to `spm.yml`:
```yaml
services:
  systemd:
    files:
      your-service.service: "services/your-service.service"
```

### Branding Customization

- **ASCII Banner**: Edit `assets/banner.ascii`
- **Emblem Image**: Replace `assets/ratio_ex_nihilo.png`
- **Plymouth Theme**: Modify `ui/plymouth/sagco/script.script`

## Architecture

### Directory Structure
```
.
├── sagco-spm.py           # Main provisioner script
├── spm.yml                # Provisioning manifest
├── assets/                # Branding assets
│   ├── banner.ascii       # ASCII art banner
│   └── ratio_ex_nihilo.png # Emblem image
├── services/              # Systemd service definitions
│   ├── sagco-banner.service
│   └── sagco-runtime.service
└── ui/                    # UI customization files
    ├── motd               # Message of the day
    ├── issue              # Login screen text
    └── plymouth/sagco/    # Plymouth boot theme
        ├── sagco.plymouth
        └── script.script
```

### Installation Paths
- System assets: `/opt/sagco/assets/`
- Virtual environment: `/opt/sagco/venv/`
- Logs: `/var/log/sagco/`
- State: `/var/lib/sagco/`
- Verification manifest: `/var/lib/sagco/spm_installed.json`

## Testing

### Test on a VM First
Always test on a virtual machine before deploying to production:

```bash
# Start a Kali VM
# Mount/copy the SAGCO SPM files
# Run the provisioner
sudo python3 sagco-spm.py spm.yml

# Verify services
systemctl status sagco-banner.service
systemctl status sagco-runtime.service

# Check logs
journalctl -u sagco-banner.service
journalctl -u sagco-runtime.service

# View verification manifest
cat /var/lib/sagco/spm_installed.json
```

## Verification

After provisioning, the system creates a verification manifest at `/var/lib/sagco/spm_installed.json` containing:
- Python version check
- Package installation status
- Service enablement status
- Plymouth theme configuration

## Creating a Custom ISO (v2 Feature)

For creating a bootable ISO with SAGCO OS pre-installed, use Kali's live-build:

```bash
# Install live-build tools
sudo apt install live-build

# Run SAGCO provisioner in chroot during build
# (Detailed instructions in v2 documentation)
```

## Troubleshooting

### Script Requires Root
```bash
# Always run with sudo
sudo python3 sagco-spm.py spm.yml
```

### Missing Dependencies
The script auto-installs `rich` and `pyyaml` if missing. If you encounter issues:
```bash
pip3 install rich pyyaml
```

### Plymouth Theme Not Working
```bash
# Manually rebuild initramfs
sudo plymouth-set-default-theme sagco
sudo update-initramfs -u
```

### Service Not Starting
```bash
# Check service status
systemctl status sagco-banner.service

# View logs
journalctl -xe -u sagco-banner.service

# Reload systemd
sudo systemctl daemon-reload
```

## Version History

### v1.0 - Initial Release
- Python-based SPM runner
- Kali Linux base support
- Package installation (APT + pip)
- Systemd service management
- Plymouth boot splash integration
- ASCII banner and MOTD customization
- Verification and manifest generation

## Future Roadmap

### v1.1
- CPU emulator/VM layer service integration
- Enhanced runtime.py with SAGCO tools menu
- Additional security tool integrations

### v2.0
- Full ISO builder integration with live-build
- Automated ISO creation from SPM
- Pre-seeded configurations
- Network installation support

## Contributing

Contributions welcome! Please submit PRs for:
- Additional package sets
- Service templates
- Plymouth themes
- Documentation improvements

## License

See LICENSE file in repository root.

## Support

For issues or questions:
1. Check verification manifest: `/var/lib/sagco/spm_installed.json`
2. Review logs: `/var/log/sagco/`
3. Check service status: `systemctl status sagco-*`

---

**SAGCO OS - Ratio Ex Nihilo**
*Creation from Nothing*
