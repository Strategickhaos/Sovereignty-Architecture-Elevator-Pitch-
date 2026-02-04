# SAGCO Runtime Components

This directory contains the SAGCO runtime, compiler, and CPU VM executables.

## Components

### runtime.sh
The SAGCO runtime initialization script that sets up the environment and loads core libraries.
- Configures environment variables
- Creates required directories
- Monitors runtime state

### flamelang-compiler
The FlameLang compiler daemon that compiles FlameLang source to SAGCO bytecode.
- Watches for source files
- Compiles to bytecode
- Outputs to artifacts directory

### sagco-cpu-vm
The SAGCO-CPU bytecode interpreter/VM (Option 2: Userspace VM).
- Executes SAGCO bytecode
- Provides virtual CPU with registers and stack
- Runs in Ring 3 (userspace)

## Directory Structure

```
/opt/sagco/
├── runtime.sh              # Runtime initialization
├── flamelang-compiler      # FlameLang compiler
├── sagco-cpu-vm           # Bytecode VM
├── artifacts/             # Compiled bytecode artifacts
├── assets/                # Static assets (emblems, etc.)
└── src/                   # FlameLang source files (optional)
```

## Installation

1. Create the SAGCO directory:
   ```bash
   sudo mkdir -p /opt/sagco/{artifacts,assets,src}
   ```

2. Copy executables:
   ```bash
   sudo cp runtime.sh flamelang-compiler sagco-cpu-vm /opt/sagco/
   sudo chmod +x /opt/sagco/runtime.sh
   sudo chmod +x /opt/sagco/flamelang-compiler
   sudo chmod +x /opt/sagco/sagco-cpu-vm
   ```

3. The systemd services will start these automatically

## Manual Testing

Test each component individually:

```bash
# Test runtime
/opt/sagco/runtime.sh

# Test compiler (in another terminal)
/opt/sagco/flamelang-compiler --daemon

# Test VM (in another terminal)
/opt/sagco/sagco-cpu-vm --load-bytecode /opt/sagco/artifacts/
```

## Notes

- These are placeholder implementations
- In production, replace with actual FlameLang compiler and SAGCO-CPU VM
- The VM runs in userspace (Ring 3), not as a kernel module
- All components log to stdout/stderr, captured by systemd journal
