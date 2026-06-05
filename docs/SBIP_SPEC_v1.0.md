# SAGCO Boot Identity Pipeline (SBIP) — v1.0

**ID:** INV-100  
**Classification:** NOVEL (system architecture)  
**Date:** 2026-02-04  
**Status:** IMPLEMENTED (v1.0)  

**Overview:**  
SBIP is a deterministic boot sequence that integrates identity display, artifact verification, and toolchain autostart into the boot process. It asserts SAGCO provenance (trademark emblem, entity metadata) during early boot, verifies core artifacts, mounts the root filesystem, and starts runtime + compiler services.

**Killer Sentence (Capstone/Lawyer-Safe):**  
> "SAGCO bootstraps its toolchain as part of the init sequence: the system boots into a SAGCO initramfs, displays the system identity screen, verifies core artifacts (hash/signature), mounts the root filesystem, and starts the SAGCO runtime and compiler services automatically."

**CPU Layer (v1):**  
SAGCO targets standard hardware ISAs (e.g., x86_64) via an LLVM backend. The 'CPU layer' refers to the compilation target architecture and its execution environment. FlameLang compiles to native binaries executed directly on the host CPU.

**Optional Future (v1.1+):**  
A SAGCO-CPU VM bytecode interpreter (userspace) for sandboxed execution, started as an optional systemd service.

**Boot Stages Mapped:**  

| Stage | What Happens | Files/Commands |
|-------|--------------|------------|
| **0: Bootloader (GRUB)** | Loads kernel + initramfs with cmdline flag (`sagco=1`). Optional theme for pre-kernel visuals. | /etc/default/grub: `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash sagco=1"`; `update-grub`. |
| **1: Kernel Start** | Initializes framebuffer. Custom config for banner strings ("SAGCO OS - Ratio Ex Nihilo"). | Kernel source patch (optional); default Kali kernel. |
| **2: initramfs / Early Userspace** | Displays splash (Plymouth with emblem), verifies artifacts (hash checks). Mounts root. | /etc/initramfs-tools/scripts/init-premount/sagco-verify (hook script below). `update-initramfs -u`. |
| **3: systemd Init** | Starts services: Runtime (toolchain init), Compiler (FlameLang daemon). | /etc/systemd/system/sagco-runtime.service, /etc/systemd/system/sagco-compiler.service (below). `systemctl enable`. |

**Prior Art Gap (Capstone-Safe):**  
- Plymouth splashes exist (but not provenance-fused).  
- Boot verification exists (but not identity-integrated).  
- Toolchain autostart exists (but not deterministic pipeline).  
- NONE: Unified sequence of identity display + verification + runtime bootstrap.

**Known Limitations:**  
- Relies on Plymouth (fallback to text if no GPU).  
- Verification assumes pre-baked hashes (mitigate with signing).  
- Userspace-only (Ring 3); future kernel module for Ring 0 primitives.  

**Artifacts Integration (From Your Images):**  
- Emblem PNG: "ratio_ex_nihilo.png" (circular sigil with lightning; Plymouth splash).  
- Math Eye Sketch: ASCII banner rep (post-login).  
- Historical Sigil: Theme inspiration.

**Deployment:**  
- Install Plymouth: `apt install plymouth plymouth-themes`.  
- Copy emblem to Plymouth dir: `/usr/share/plymouth/themes/sagco/`.  
- Set theme: `plymouth-set-default-theme -R sagco`.  
- Reboot: See splash, verify logs in journal (`journalctl -u initramfs`), services running (`systemctl status sagco-*`).
