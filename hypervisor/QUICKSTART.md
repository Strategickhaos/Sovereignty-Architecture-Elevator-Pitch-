# Quick Start Guide: FFI Boundary Specification

Get up and running with the FlameLang ↔ Rust hypervisor FFI boundary in 5 minutes.

## Prerequisites

- Rust toolchain (rustc, cargo)
- GCC or Clang (for C examples)
- Linux with KVM support (for Phase 2+)

## Step 1: Build the Library

```bash
cd hypervisor
./build.sh
```

This compiles `libsagco_hv_core.so` (or `.dylib` on macOS).

## Step 2: Run Tests

```bash
cargo test
```

Expected output:
```
running 3 tests
test hv_api::tests::test_create_vm ... ok
test hv_api::tests::test_init_shutdown ... ok
test hv_api::tests::test_vm_lifecycle ... ok

test result: ok. 3 passed
```

## Step 3: Verify Installation

```bash
./verify.sh
```

Expected output:
```
✓ All core files present
✓ Build successful
✓ All 3 tests passing
✓ 3/3 documentation files present
✓ FlameLang and C examples present
✓ Phase 1 Implementation: VERIFIED
```

## Example Usage

### From C

```c
#include "include/hv_api.h"

int main() {
    // Initialize hypervisor
    hv_init();
    
    // Configure VM
    hv_vm_config_t cfg = {
        .name = "my_vm",
        .disk_path = "/isos/alpine.iso",
        .kernel_path = NULL,
        .cmdline = NULL,
        .mem_mb = 512,
        .vcpus = 2,
        .flags = 0
    };
    
    // Create and start VM
    hv_create_vm(&cfg);
    hv_start_vm("my_vm");
    
    // Cleanup
    hv_stop_vm("my_vm");
    hv_destroy_vm("my_vm");
    hv_shutdown();
    
    return 0;
}
```

Compile:
```bash
gcc -o my_controller my_controller.c \
    -L target/release \
    -l sagco_hv_core \
    -I include
    
LD_LIBRARY_PATH=target/release ./my_controller
```

### From FlameLang (Future)

```flame
hypervisor "SAGCO-HV" {
  default_memory = 512_MB
  default_vcpus  = 1
}

vm "my_vm" {
  memory = 512_MB
  vcpus  = 2
  disk   = "/isos/alpine.iso"
}

boot "my_vm"
```

Compile (when FlameLang compiler is ready):
```bash
flamec my_vm.flm -o my_controller
./my_controller
```

## API Reference

### Lifecycle Functions

```c
hv_result_t hv_init(void);
hv_result_t hv_shutdown(void);
```

### VM Management

```c
hv_result_t hv_create_vm(const hv_vm_config_t *cfg);
hv_result_t hv_start_vm(const char *name);
hv_result_t hv_stop_vm(const char *name);
hv_result_t hv_destroy_vm(const char *name);
```

### Error Codes

- `HV_OK` (0) - Success
- `HV_ERR_INIT` (1) - Initialization error
- `HV_ERR_CREATE` (2) - VM creation error
- `HV_ERR_START` (3) - VM start error
- `HV_ERR_STOP` (4) - VM stop error
- `HV_ERR_DESTROY` (5) - VM destroy error
- `HV_ERR_INVALID` (6) - Invalid parameter

## Project Structure

```
hypervisor/
├── include/hv_api.h           # C ABI header
├── src/
│   ├── lib.rs                 # Library entry
│   └── hv_api.rs              # FFI implementation
├── examples/
│   ├── example.flm            # FlameLang DSL
│   └── generated_hv_main.c    # Generated C code
├── Cargo.toml                 # Rust config
├── build.sh                   # Build script
└── verify.sh                  # Verification script
```

## Documentation

- [README.md](README.md) - Complete specification
- [PHASE1_CHECKLIST.md](PHASE1_CHECKLIST.md) - Implementation status
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Overview

## Troubleshooting

### "cannot find -lsagco_hv_core"

Make sure you've built the library:
```bash
cargo build --release
```

### "error while loading shared libraries"

Set library path:
```bash
export LD_LIBRARY_PATH=$PWD/target/release:$LD_LIBRARY_PATH
```

### Tests failing

Clean and rebuild:
```bash
cargo clean
cargo build --release
cargo test
```

## Next Steps

1. Read [README.md](README.md) for complete documentation
2. Explore [examples/](examples/) for code samples
3. Check [PHASE1_CHECKLIST.md](PHASE1_CHECKLIST.md) for Phase 2 roadmap
4. Integrate with FlameLang compiler (when ready)

## Support

- **Issues**: GitHub Issues
- **Documentation**: See README.md
- **Community**: Strategickhaos Discord

---

**Status:** Phase 1 Complete ✅  
**Next:** FlameLang compiler integration + Real KVM implementation
