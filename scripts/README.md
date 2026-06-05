# SAGCO Scripts Directory

This directory contains various scripts for the SAGCO Boot Identity Pipeline (SBIP) and related tools.

## Directory Structure

```
scripts/
├── bin/                    # Service binaries
│   ├── sagco-banner        # Identity banner display
│   ├── sagco-runtime       # Runtime bootstrap
│   ├── sagco-compiler      # Compiler service
│   └── sagco-cpu-init      # CPU interface init
└── initramfs/              # initramfs integration
    ├── sagco-verify        # Artifact verification
    ├── sagco-hook          # Hook for update-initramfs
    └── README.md           # Documentation
```

## Service Binaries (bin/)

### sagco-banner

Displays the SAGCO identity banner with ASCII art and entity information.

- Called by: `sagco-banner.service`
- Logs to: systemd journal
- Purpose: Visual identity display at boot

### sagco-runtime

Initializes the SAGCO runtime environment.

- Called by: `sagco-runtime.service`
- Creates: `/opt/sagco/` directory structure
- Exports: Environment variables for toolchain
- Purpose: Bootstrap SAGCO runtime environment

### sagco-compiler

Starts the FlameLang compiler service.

- Called by: `sagco-compiler.service`
- Checks: LLVM installation
- Creates: Compiler configuration
- Purpose: Initialize FlameLang → LLVM pipeline

### sagco-cpu-init

Initializes interaction with the sagco_cpu_mod kernel module.

- Called by: `sagco-cpu.service`
- Requires: `/dev/sagco_cpu` device
- Tests: CPU state operations
- Purpose: Verify kernel module interface

## initramfs Scripts

See `initramfs/README.md` for detailed documentation on initramfs integration.

## Installation

Service binaries are installed to `/usr/local/bin/` by the main installer:

```bash
sudo ./install.sh
```

Manual installation:

```bash
# Install service binaries
sudo cp scripts/bin/sagco-* /usr/local/bin/
sudo chmod +x /usr/local/bin/sagco-*

# Install initramfs scripts
sudo mkdir -p /usr/local/share/sagco/scripts
sudo cp scripts/initramfs/sagco-verify /usr/local/share/sagco/scripts/
sudo cp scripts/initramfs/sagco-hook /etc/initramfs-tools/hooks/sagco
sudo chmod +x /usr/local/share/sagco/scripts/sagco-verify
sudo chmod +x /etc/initramfs-tools/hooks/sagco

# Update initramfs
sudo update-initramfs -u
```

## Usage

Service binaries are typically run by systemd services, but can be executed manually:

```bash
# Display banner
sudo /usr/local/bin/sagco-banner

# Initialize runtime (starts background service)
sudo /usr/local/bin/sagco-runtime

# Initialize CPU interface
sudo /usr/local/bin/sagco-cpu-init
```

## Development

When modifying service binaries:

1. Edit the script in `scripts/bin/`
2. Reinstall: `sudo cp scripts/bin/sagco-* /usr/local/bin/`
3. Restart service: `sudo systemctl restart sagco-*.service`
4. View logs: `journalctl -u sagco-*.service -f`

## Logging

All scripts log to the systemd journal using `logger`:

```bash
# View all SAGCO logs
journalctl -t sagco-banner -t sagco-runtime -t sagco-compiler -t sagco-cpu-init

# Follow logs in real-time
journalctl -t sagco-runtime -f
```

## Legal Notice

Property of Strategickhaos DAO LLC  
Wyoming Entity: 2025-001708194 | EIN: 39-2923503

---

🔥💜 STRATEGICKHAOS DAO LLC 💜🔥
