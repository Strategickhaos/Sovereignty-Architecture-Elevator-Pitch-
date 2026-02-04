# SAGCO Boot Identity Pipeline (SBIP) Specification v1.0

**ID:** INV-100  
**Classification:** NOVEL (system architecture)  
**Date:** 2026-02-04  
**Status:** IMPLEMENTED (v1.0)  
**Repository:** https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

## Overview

SBIP is a deterministic boot sequence that asserts SAGCO identity (trademark emblem), verifies artifacts, and bootstraps the toolchain (runtime + compiler + CPU VM). It integrates with Kali Linux base for v1.

## Killer Sentence (Capstone/Lawyer-Safe)

> "SAGCO bootstraps its toolchain as part of the init sequence: the kernel boots into a SAGCO initramfs, which displays the system identity screen, verifies core artifacts, mounts the root filesystem, and starts the SAGCO runtime + compiler services automatically."

## CPU Architecture Decision

Based on the TRIG6 periodic table and DNA→LLVM pipeline, **Option 2** is implemented:

> **"Our CPU is Option 2 — a SAGCO-CPU bytecode interpreter/VM layer that executes FlameLang-compiled artifacts. It starts as a systemd service (sagco-cpu.service) after the SAGCO runtime initializes."**

This is a userspace VM like LuaJIT or WebAssembly runtime, but SAGCO-branded. It's not raw hardware (Option 1) or kernel module (Option 3).

## Boot Stages

| Stage | What Happens | Code/Files |
|-------|--------------|------------|
| **0: Bootloader (GRUB)** | Loads kernel + initramfs with SAGCO theme/logo. Cmdline flag: `sagco=1`. | `sbip/boot/grub/` - GRUB config + theme. Emblem: ratio_ex_nihilo.png |
| **1: Kernel Start** | Initializes framebuffer for splash. Banner: "SAGCO OS - Ratio Ex Nihilo". | Kernel config (use Kali default kernel) |
| **2: initramfs / Early Userspace** | Displays splash (Plymouth with emblem), verifies artifacts (hash checks). Mounts root. | `sbip/etc/initramfs-tools/scripts/init-top/sagco-init` |
| **3: systemd Init** | Starts services: Banner (ASCII art), Runtime (toolchain), Compiler (FlameLang), CPU VM (bytecode exec). | `sbip/etc/systemd/system/sagco-*.service` |

## Prior Art Gap (Capstone-Safe)

- Plymouth splashes exist (but not legally-bound to trademarks)
- Boot verification exists (but not fused with identity)
- Trademark display exists (but not at kernel level)
- **NONE**: Unified pipeline of legal identity + boot + runtime/VM

## Known Limitations

- Relies on Plymouth (Kali-compatible; fallback to text if no GPU)
- Verification assumes artifact hashes pre-baked (mitigate with signing)
- CPU VM is userspace (Ring 3); future kernel module for Ring 0 if needed

## Artifacts

- **Emblem PNG**: "ratio_ex_nihilo.png" (circular sigil with lightning)
- **Math Eye Sketch**: Used for ASCII banner inspiration
- **Historical Sigil**: Inspiration for theme

## Directory Structure

```
sbip/
├── boot/grub/                          # Stage 0: Bootloader
│   ├── themes/sagco/
│   │   └── theme.txt
│   ├── grub_config_snippet.txt
│   └── README.md
├── usr/share/plymouth/                 # Stage 1-2: Splash
│   ├── themes/sagco/
│   │   ├── sagco.plymouth
│   │   └── sagco.script
│   └── README.md
├── etc/initramfs-tools/                # Stage 2: Verification
│   ├── scripts/init-top/
│   │   └── sagco-init
│   └── README.md
├── etc/systemd/system/                 # Stage 3: Services
│   ├── sagco-banner.service
│   ├── sagco-runtime.service
│   ├── sagco-compiler.service
│   ├── sagco-cpu.service
│   └── README.md
├── opt/sagco/                          # Runtime Components
│   ├── runtime.sh
│   ├── flamelang-compiler
│   ├── sagco-cpu-vm
│   ├── artifacts/                      # Bytecode output
│   ├── assets/                         # Static assets
│   └── README.md
├── EMBLEM_README.md                    # Emblem image guide
├── INSTALL.md                          # Installation guide
└── SPECIFICATION.md                    # This file
```

## Installation

See `INSTALL.md` for complete installation instructions.

Quick setup:
```bash
# 1. Install bootloader theme
sudo cp -r sbip/boot/grub/themes/sagco /boot/grub/themes/
# Edit /etc/default/grub and add GRUB config snippet
sudo update-grub

# 2. Install Plymouth theme
sudo cp -r sbip/usr/share/plymouth/themes/sagco /usr/share/plymouth/themes/
sudo plymouth-set-default-theme sagco
sudo update-initramfs -u

# 3. Install initramfs hook
sudo cp sbip/etc/initramfs-tools/scripts/init-top/sagco-init /etc/initramfs-tools/scripts/init-top/
sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-init
sudo update-initramfs -u

# 4. Install systemd services
sudo cp sbip/etc/systemd/system/sagco-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagco-banner sagco-runtime sagco-compiler sagco-cpu

# 5. Install runtime components
sudo mkdir -p /opt/sagco/{artifacts,assets}
sudo cp sbip/opt/sagco/{runtime.sh,flamelang-compiler,sagco-cpu-vm} /opt/sagco/
sudo chmod +x /opt/sagco/{runtime.sh,flamelang-compiler,sagco-cpu-vm}
```

## Testing

1. **Test Plymouth theme** (without reboot):
   ```bash
   sudo plymouthd
   sudo plymouth --show-splash
   # Wait 5 seconds
   sudo plymouth quit
   ```

2. **Test systemd services**:
   ```bash
   sudo systemctl start sagco-banner
   sudo systemctl status sagco-*
   sudo journalctl -u sagco-* -f
   ```

3. **Full boot test**: Reboot the system
   ```bash
   sudo reboot
   ```

## Verification

After boot, verify SBIP is active:

```bash
# Check kernel parameters
cat /proc/cmdline | grep sagco=1

# Check systemd services
systemctl status sagco-*

# View boot logs
journalctl -b | grep SAGCO

# Check runtime status
sudo journalctl -u sagco-runtime -n 50
sudo journalctl -u sagco-cpu -n 50
```

## Integration with SPM

For integration with SAGCO Package Manager (SPM), add the service units to `spm.yml` under services/files/commands. The SPM runner will copy and enable them automatically.

## Future Enhancements (v1.1)

- Full ISO with pre-configured SBIP
- Custom kernel with built-in SAGCO banner
- Kernel module version of CPU VM (Ring 0)
- Cryptographic signing of artifacts
- Secure Boot integration
- TPM-based attestation

## References

- FLAMELANG_SPECIFICATION.md - FlameLang language specification
- BOOT_RECON.md - Boot reconnaissance documentation
- [Plymouth Documentation](https://www.freedesktop.org/wiki/Software/Plymouth/)
- [systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

## License

See LICENSE file in repository root.

## Authors

Strategic Khaos DAO LLC / SAGCO Project

---

*"From Nothing, Through Reason" - Ratio Ex Nihilo*
