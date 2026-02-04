# SAGCO SPM Quick Start Guide

## What is SAGCO SPM?

SAGCO SPM (SAGCO Provisioning Manifest) is a declarative provisioning system for building SAGCO OS - a customized security-focused operating system based on Kali Linux with the "Ratio Ex Nihilo" (Creation from Nothing) identity.

## Quick Installation

```bash
# 1. Ensure you're on Kali Linux or Debian-based system
# 2. Clone/download the SAGCO SPM files
# 3. Add your emblem image (optional):
#    Place ratio_ex_nihilo.png in assets/ directory

# 4. Run the provisioner (requires root)
sudo python3 sagco-spm.py spm.yml

# 5. Reboot to see the full boot experience
sudo reboot
```

## What Gets Installed

- **Core Tools**: git, curl, wget, python3, build-essential, tmux, zsh
- **Security Tools**: nmap, wireshark, metasploit-framework, sqlmap, gobuster
- **Operations**: docker, podman, qemu
- **Boot Identity**: Plymouth splash, custom MOTD, login banner
- **Services**: sagco-banner (boot banner), sagco-runtime (placeholder)

## Files Created

```
sagco-spm.py              # Main provisioner script
spm.yml                   # Configuration manifest
assets/
  banner.ascii            # ASCII art for terminal
  README.md              # Instructions for emblem image
services/
  sagco-banner.service   # Systemd boot banner
  sagco-runtime.service  # Systemd runtime service
ui/
  motd                   # Message of the day
  issue                  # Login screen text
  plymouth/sagco/        # Boot splash theme
test_sagco_spm.py        # Validation test script
```

## Testing

```bash
# Run validation tests
python3 test_sagco_spm.py

# Test in dry-run mode (view what would be installed)
python3 sagco-spm.py spm.yml --help

# Check services after installation
systemctl status sagco-banner.service
systemctl status sagco-runtime.service
```

## Customization

Edit `spm.yml` to:
- Add/remove packages
- Customize boot messages
- Add custom files
- Configure services
- Define post-install commands

## Full Documentation

See `SAGCO_SPM_README.md` for complete documentation.

## Identity

```
___________
  /           \
 /  RATIO EX   \
|   NIHILO     |
|    * * *     |
|   / \ / \    |
|  *   *   *   |
|   \ / \ /    |
|    * * *     |
 \             /
  \___________/
  
  SAGCO OS - Creation from Nothing
```

**Name**: SAGCO OS  
**Codename**: Ratio Ex Nihilo  
**Version**: 1.0.0  
**Motto**: Ratio Ex Nihilo (Creation from Nothing)  
**Build ID**: INV-099

## Support

- Review logs: `/var/log/sagco/`
- Check verification: `/var/lib/sagco/spm_installed.json`
- Service logs: `journalctl -u sagco-banner.service`

---

*SAGCO SPM v1.0 - Minimal, deterministic, auditable provisioning for SAGCO OS*
