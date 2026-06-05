# SAGCO systemd Services

systemd service units for the SAGCO Boot Identity Pipeline (SBIP).

## Services

### sagco-banner.service

Displays SAGCO identity banner at boot.

- **Type**: oneshot
- **Runs**: `/usr/local/bin/sagco-banner`
- **After**: multi-user.target
- **Purpose**: Display ASCII art banner with entity information

```bash
# View service status
systemctl status sagco-banner.service

# View logs
journalctl -u sagco-banner.service
```

### sagco-cpu.service

Initializes the SAGCO CPU kernel module interface.

- **Type**: oneshot
- **Runs**: `/usr/local/bin/sagco-cpu-init`
- **Requires**: sagco_cpu_mod kernel module loaded
- **Purpose**: Test and initialize /dev/sagco_cpu device

```bash
# View service status
systemctl status sagco-cpu.service

# View logs
journalctl -u sagco-cpu.service
```

### sagco-runtime.service

Bootstraps the SAGCO runtime environment.

- **Type**: notify
- **Runs**: `/usr/local/bin/sagco-runtime`
- **After**: sagco-cpu.service
- **Requires**: sagco-cpu.service
- **Purpose**: Initialize runtime directories and environment

Environment variables:
- `SAGCO_ROOT=/opt/sagco` - Runtime root directory
- `SAGCO_MODE=production` - Operational mode

```bash
# View service status
systemctl status sagco-runtime.service

# View logs
journalctl -u sagco-runtime.service -f
```

### sagco-compiler.service

Starts the FlameLang compiler service.

- **Type**: notify
- **Runs**: `/usr/local/bin/sagco-compiler`
- **After**: sagco-runtime.service
- **Requires**: sagco-runtime.service
- **Purpose**: Initialize FlameLang → LLVM compilation pipeline

Environment variables:
- `SAGCO_COMPILER=flamelang` - Compiler type
- `LLVM_PATH=/usr/lib/llvm-14` - LLVM installation path
- `SAGCO_ROOT=/opt/sagco` - Runtime root

```bash
# View service status
systemctl status sagco-compiler.service

# View logs
journalctl -u sagco-compiler.service -f
```

### sagco.target

systemd target that groups all SAGCO services.

- **Type**: target
- **Wants**: All SAGCO services
- **Purpose**: Unified control of SAGCO boot pipeline

```bash
# Check target status
systemctl status sagco.target

# Start all SAGCO services
systemctl start sagco.target

# Stop all SAGCO services
systemctl stop sagco.target
```

## Installation

Services are installed by the main `install.sh` script:

```bash
# Install and enable services
sudo ./install.sh
```

Manual installation:

```bash
# Copy service files
sudo cp systemd/*.service /etc/systemd/system/
sudo cp systemd/*.target /etc/systemd/system/

# Copy service binaries
sudo cp scripts/bin/sagco-* /usr/local/bin/
sudo chmod +x /usr/local/bin/sagco-*

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable sagco-banner.service
sudo systemctl enable sagco-cpu.service
sudo systemctl enable sagco-runtime.service
sudo systemctl enable sagco-compiler.service
sudo systemctl enable sagco.target
```

## Service Dependencies

```
sagco.target
├── sagco-banner.service (independent)
├── sagco-cpu.service (independent, requires module)
├── sagco-runtime.service (depends on sagco-cpu.service)
└── sagco-compiler.service (depends on sagco-runtime.service)
```

## Debugging

```bash
# View all SAGCO service logs
journalctl -u 'sagco-*' -b

# View logs since last boot
journalctl -u sagco.target -b

# Follow logs in real-time
journalctl -u sagco-runtime.service -f

# Check service failures
systemctl --failed | grep sagco

# View service configuration
systemctl cat sagco-banner.service
```

## Customization

### Changing Runtime Root

Edit `/etc/systemd/system/sagco-runtime.service`:

```ini
Environment="SAGCO_ROOT=/custom/path"
```

Then reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart sagco-runtime.service
```

### Disabling Specific Services

```bash
# Disable compiler service
sudo systemctl disable sagco-compiler.service
sudo systemctl stop sagco-compiler.service
```

### Running Services Manually

```bash
# Run banner manually
sudo /usr/local/bin/sagco-banner

# Initialize CPU interface manually
sudo /usr/local/bin/sagco-cpu-init
```

## Security

Services are configured with security hardening:

- `PrivateTmp=yes` - Isolated /tmp directory
- `ProtectSystem=strict` - Read-only system directories
- `ProtectHome=yes` - No access to home directories (banner only)
- `NoNewPrivileges=yes` - Cannot gain additional privileges

## Troubleshooting

### Services fail to start

```bash
# Check service status
systemctl status sagco-*.service

# Check dependencies
systemctl list-dependencies sagco.target

# Verify binaries exist
ls -l /usr/local/bin/sagco-*
```

### CPU service fails

The CPU service requires the kernel module:

```bash
# Check if module is loaded
lsmod | grep sagco_cpu_mod

# Load module manually
sudo modprobe sagco_cpu_mod

# Check device file
ls -l /dev/sagco_cpu
```

### Runtime directory creation fails

Ensure root filesystem has write permissions:

```bash
# Check filesystem
df -h /opt

# Create directory manually
sudo mkdir -p /opt/sagco
sudo chmod 755 /opt/sagco
```

## Legal Notice

Property of Strategickhaos DAO LLC  
Wyoming Entity: 2025-001708194 | EIN: 39-2923503

---

🔥💜 STRATEGICKHAOS DAO LLC 💜🔥
