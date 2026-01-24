# FlameLang Hypervisor Integration

This document describes the integration between FlameLang and the SAGCO Hypervisor Core.

## Quick Links

- **Hypervisor Implementation**: [hypervisor/README.md](hypervisor/README.md)
- **Phase 1 Status**: [hypervisor/PHASE1_CHECKLIST.md](hypervisor/PHASE1_CHECKLIST.md)
- **FlameLang Specification**: [FLAMELANG_SPECIFICATION.md](FLAMELANG_SPECIFICATION.md)

## Overview

The FFI (Foreign Function Interface) boundary allows FlameLang to control KVM-based virtual machines through a clean C ABI. This enables sovereign hypervisor control directly from FlameLang code.

```
┌─────────────────────────────────────────────────┐
│           FlameLang Source Code                 │
│  hypervisor "SAGCO-HV" { ... }                 │
│  vm "my_vm" { memory = 1024_MB ... }           │
│  boot "my_vm"                                   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│        FlameLang Compiler (flamec)              │
│   Parser → AST → IR → C/LLVM Codegen           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         Generated Binary                        │
│   Links with libsagco_hv_core.so               │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│      SAGCO Hypervisor Core (Rust)              │
│   FFI Boundary → KVM → /dev/kvm               │
└─────────────────────────────────────────────────┘
```

## Getting Started

### 1. Build the Hypervisor Core

```bash
cd hypervisor
./build.sh

# Or manually:
cargo build --release
cargo test
```

### 2. Example FlameLang Code

Create a file `my_vm.flm`:

```flame
hypervisor "SAGCO-HV" {
  default_memory = 512_MB
  default_vcpus  = 1
}

vm "alpine_test" {
  memory = 256_MB
  vcpus  = 1
  disk   = "/isos/alpine-virt.iso"
}

boot "alpine_test"
```

### 3. Compile with FlameLang (Future)

```bash
flamec my_vm.flm -o alpine_controller
./alpine_controller
```

## Current Status

### ✅ Phase 1: Complete

The FFI boundary is fully implemented and tested:
- C ABI header defines the contract
- Rust implementation provides the functions
- Unit tests validate the interface
- Documentation is comprehensive

### 🚧 Phase 2: In Progress

- [ ] FlameLang compiler integration
- [ ] Real KVM implementation
- [ ] Actual VM boot functionality

### 📋 Phase 3: Future

- [ ] Multiple VM support
- [ ] Networking
- [ ] PCI device passthrough
- [ ] Resource management and scheduling

## API Preview

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

## Architecture Principles

1. **Separation of Concerns**: FlameLang handles logic, Rust handles execution
2. **Type Safety**: Rust ensures memory safety, C ABI provides compatibility
3. **Clean Abstraction**: FlameLang never touches `/dev/kvm` directly
4. **Testability**: Each layer can be tested independently
5. **Scalability**: Design supports multiple VMs and future features

## Integration with SAGCO-OS

When integrated into SAGCO-OS:

```
/usr/bin/
  ├── flamec                    # FlameLang compiler
  └── sagco-hv                  # Compiled hypervisor controller

/usr/lib/
  └── libsagco_hv_core.so       # Hypervisor core library

/etc/sagco/
  └── hypervisor.flm            # System hypervisor configuration

/isos/
  └── sagco-live.iso            # OS images for VMs
```

## Contributing

See the main [README.md](README.md) for contribution guidelines.

For hypervisor-specific development:
1. Read [hypervisor/README.md](hypervisor/README.md)
2. Check [hypervisor/PHASE1_CHECKLIST.md](hypervisor/PHASE1_CHECKLIST.md)
3. Run tests: `cd hypervisor && cargo test`
4. Submit PRs with clear descriptions

## License

MIT License - See [LICENSE](LICENSE) file

## Contact

- **Organization:** Strategickhaos DAO LLC
- **Project:** SAGCO OS / FlameLang
- **Repository:** https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-

---

**"Lock in. This is doable in your stack."** 🔥
