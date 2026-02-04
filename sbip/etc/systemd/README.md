# Systemd Services

This directory contains systemd service files for SAGCO Boot Identity Pipeline (SBIP).

## Services

### sagco-banner.service
Displays the SAGCO boot banner (ASCII art with "Ratio Ex Nihilo" theme).
- Type: Oneshot
- Runs: At multi-user target

### sagco-runtime.service
Initializes the SAGCO runtime and toolchain.
- Type: Simple (daemon)
- Runs: After banner display
- Dependencies: Requires `/opt/sagco/runtime.sh`

### sagco-compiler.service
Starts the FlameLang compiler daemon.
- Type: Simple (daemon)
- Runs: After runtime initialization
- Dependencies: Requires `/opt/sagco/flamelang-compiler`

### sagco-cpu.service
Starts the SAGCO CPU bytecode interpreter/VM (Option 2).
- Type: Simple (daemon)
- Runs: After compiler is ready
- Dependencies: Requires `/opt/sagco/sagco-cpu-vm`

## Installation

1. Copy service files:
   ```bash
   sudo cp *.service /etc/systemd/system/
   ```

2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Enable services:
   ```bash
   sudo systemctl enable sagco-banner.service
   sudo systemctl enable sagco-runtime.service
   sudo systemctl enable sagco-compiler.service
   sudo systemctl enable sagco-cpu.service
   ```

4. Start services:
   ```bash
   sudo systemctl start sagco-banner.service
   sudo systemctl start sagco-runtime.service
   sudo systemctl start sagco-compiler.service
   sudo systemctl start sagco-cpu.service
   ```

## Check Status

View status of all SAGCO services:
```bash
sudo systemctl status sagco-*
```

View logs:
```bash
sudo journalctl -u sagco-* -f
```

## Boot Order

Services start in this order:
1. `sagco-banner.service` - Display boot identity
2. `sagco-runtime.service` - Initialize runtime
3. `sagco-compiler.service` - Start compiler
4. `sagco-cpu.service` - Start CPU VM

## Notes

- All services include security hardening with `NoNewPrivileges`, `PrivateTmp`, and `ProtectSystem`
- Services restart automatically on failure (except banner)
- Logs are sent to systemd journal
