# SAGCO Boot Identity Pipeline (SBIP)

**Version:** 1.0  
**Status:** Implemented  
**Classification:** NOVEL (system architecture)  
**Invention ID:** INV-100

![SAGCO OS - Ratio Ex Nihilo](https://img.shields.io/badge/SAGCO%20OS-v1.0-purple)
![Boot Pipeline](https://img.shields.io/badge/Boot-Identity%20Pipeline-blue)
![License](https://img.shields.io/badge/License-See%20LICENSE-green)

## Overview

SBIP (SAGCO Boot Identity Pipeline) is a deterministic boot sequence that:
- **Asserts SAGCO identity** with trademark emblem during boot
- **Verifies artifacts** using cryptographic hashes
- **Bootstraps the toolchain** (runtime + compiler + CPU VM)
- **Integrates with Linux** (tested on Kali/Debian)

**The killer feature:** A unified pipeline of legal identity assertion + boot verification + runtime initialization.

## What Makes This Novel?

While individual components exist (Plymouth, boot verification, systemd), **NONE** combine:
1. Legally-bound trademark display at kernel level
2. Boot-time artifact verification fused with identity
3. Automatic toolchain bootstrap as part of init sequence
4. Custom CPU VM (Option 2: userspace bytecode interpreter)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Stage 0: Bootloader (GRUB)                              │
│ - Displays SAGCO theme with emblem                      │
│ - Loads kernel with sagco=1 parameter                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Kernel Start                                   │
│ - Initializes framebuffer                               │
│ - Banner: "SAGCO OS - Ratio Ex Nihilo"                  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 2: initramfs / Early Userspace                    │
│ - Plymouth displays splash with emblem                  │
│ - sagco-init hook verifies artifacts                    │
│ - Mounts root filesystem                                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 3: systemd Init                                   │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ sagco-banner.service    → ASCII banner display      │ │
│ │ sagco-runtime.service   → Toolchain initialization  │ │
│ │ sagco-compiler.service  → FlameLang compiler daemon │ │
│ │ sagco-cpu.service       → SAGCO-CPU bytecode VM     │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## CPU Architecture: Option 2

The SAGCO-CPU is a **bytecode interpreter/VM layer** (not hardware, not kernel module):
- Executes FlameLang-compiled artifacts
- Userspace VM (Ring 3) like LuaJIT or WebAssembly
- Runs as systemd service (`sagco-cpu.service`)
- Starts after compiler is ready

## Quick Start

### Installation

See [INSTALL.md](INSTALL.md) for complete instructions.

Quick install (requires root):
```bash
cd sbip
sudo ./install.sh  # TODO: Create automated install script
```

Manual install:
```bash
# 1. Install bootloader theme
sudo cp -r boot/grub/themes/sagco /boot/grub/themes/
# Edit /etc/default/grub - see INSTALL.md
sudo update-grub

# 2. Install Plymouth theme
sudo cp -r usr/share/plymouth/themes/sagco /usr/share/plymouth/themes/
sudo plymouth-set-default-theme sagco
sudo update-initramfs -u

# 3. Install initramfs hook
sudo cp etc/initramfs-tools/scripts/init-top/sagco-init /etc/initramfs-tools/scripts/init-top/
sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-init
sudo update-initramfs -u

# 4. Install systemd services
sudo cp etc/systemd/system/sagco-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagco-{banner,runtime,compiler,cpu}

# 5. Install runtime
sudo mkdir -p /opt/sagco/{artifacts,assets}
sudo cp opt/sagco/{runtime.sh,flamelang-compiler,sagco-cpu-vm} /opt/sagco/
sudo chmod +x /opt/sagco/{runtime.sh,flamelang-compiler,sagco-cpu-vm}
```

### Testing

Test without rebooting:
```bash
# Test Plymouth theme
sudo plymouthd && sudo plymouth --show-splash
sleep 5
sudo plymouth quit

# Test services
sudo systemctl start sagco-banner
sudo systemctl status sagco-*
sudo journalctl -u sagco-* -f
```

Full boot test:
```bash
sudo reboot
```

## Files Structure

```
sbip/
├── boot/grub/                          # GRUB bootloader theme
│   ├── themes/sagco/theme.txt
│   └── grub_config_snippet.txt
├── usr/share/plymouth/                 # Plymouth splash screen
│   └── themes/sagco/
│       ├── sagco.plymouth
│       └── sagco.script
├── etc/initramfs-tools/                # Early boot hook
│   └── scripts/init-top/sagco-init
├── etc/systemd/system/                 # System services
│   ├── sagco-banner.service
│   ├── sagco-runtime.service
│   ├── sagco-compiler.service
│   └── sagco-cpu.service
├── opt/sagco/                          # Runtime components
│   ├── runtime.sh
│   ├── flamelang-compiler
│   ├── sagco-cpu-vm
│   ├── artifacts/                      # Bytecode output
│   └── assets/                         # Static assets
├── SPECIFICATION.md                    # Complete specification
├── INSTALL.md                          # Installation guide
├── EMBLEM_README.md                    # Emblem image guide
└── README.md                           # This file
```

## Documentation

- [SPECIFICATION.md](SPECIFICATION.md) - Complete SBIP specification
- [INSTALL.md](INSTALL.md) - Step-by-step installation guide
- [EMBLEM_README.md](EMBLEM_README.md) - Emblem image requirements
- Individual README.md files in each subdirectory

## Requirements

- Linux system (Kali, Debian, or compatible)
- GRUB bootloader
- Plymouth boot splash
- systemd init system
- Root access

## Status

✅ **Implemented:**
- GRUB theme with SAGCO branding
- Plymouth splash screen theme
- initramfs verification hook
- systemd service units (banner, runtime, compiler, CPU VM)
- Placeholder runtime components

🚧 **TODO:**
- Replace placeholder emblem with official SAGCO trademark image
- Implement actual FlameLang compiler
- Implement actual SAGCO-CPU VM
- Add cryptographic signing
- Create automated install script
- Build full ISO with SBIP pre-configured

## Integration

### SPM Integration

For SAGCO Package Manager (SPM) integration, add service units to `spm.yml`:

```yaml
services:
  sagco-banner:
    file: /etc/systemd/system/sagco-banner.service
  sagco-runtime:
    file: /etc/systemd/system/sagco-runtime.service
  sagco-compiler:
    file: /etc/systemd/system/sagco-compiler.service
  sagco-cpu:
    file: /etc/systemd/system/sagco-cpu.service
```

## Development

### Testing Changes

After modifying any component:

1. **GRUB changes**: `sudo update-grub && sudo reboot`
2. **Plymouth changes**: `sudo update-initramfs -u && sudo reboot`
3. **initramfs hook**: `sudo update-initramfs -u && sudo reboot`
4. **systemd services**: `sudo systemctl daemon-reload && sudo systemctl restart sagco-*`
5. **Runtime components**: `sudo systemctl restart sagco-runtime sagco-compiler sagco-cpu`

### Debugging

```bash
# View boot logs
sudo journalctl -b | grep -i sagco

# Check service status
sudo systemctl status sagco-*

# View service logs
sudo journalctl -u sagco-banner -u sagco-runtime -u sagco-compiler -u sagco-cpu -f

# Test Plymouth
sudo plymouth --show-splash && sleep 5 && sudo plymouth quit

# Check initramfs contents
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco
```

## Known Limitations

1. **Plymouth dependency**: Requires functional framebuffer (may not work in all VM environments)
2. **Artifact verification**: Currently basic SHA256, needs signing for production
3. **Ring 3 only**: CPU VM runs in userspace; Ring 0 kernel module planned for v1.1
4. **Placeholder components**: Compiler and VM are placeholders; need implementation

## Future Enhancements (v1.1+)

- [ ] Full bootable ISO with SBIP pre-configured
- [ ] Custom kernel with built-in SAGCO banner
- [ ] SAGCO-CPU kernel module (Ring 0)
- [ ] Cryptographic signing with GPG/OpenSSL
- [ ] Secure Boot integration
- [ ] TPM-based attestation
- [ ] Web-based boot status dashboard
- [ ] Multi-architecture support (ARM, RISC-V)

## License

See [LICENSE](../LICENSE) file in repository root.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) in repository root.

## Authors

**Strategic Khaos DAO LLC** / **SAGCO Project**

## References

- [FLAMELANG_SPECIFICATION.md](../FLAMELANG_SPECIFICATION.md) - FlameLang language spec
- [BOOT_RECON.md](../BOOT_RECON.md) - Boot reconnaissance
- [Plymouth Documentation](https://www.freedesktop.org/wiki/Software/Plymouth/)
- [systemd Documentation](https://www.freedesktop.org/software/systemd/)

---

**SAGCO OS v1.0**  
*"From Nothing, Through Reason" - Ratio Ex Nihilo* 🔥💜
