# FFI Boundary Specification: FlameLang ↔ Rust Hypervisor Core

**Status:** Phase 1 Implementation Complete  
**Version:** 0.1.0  
**Author:** Strategickhaos DAO LLC  
**Date:** 2025-01-24

---

## Overview

This document defines the Foreign Function Interface (FFI) boundary between **FlameLang** (the high-level control language) and the **Rust KVM Hypervisor Core** (the low-level execution engine).

### The Contract

```
FlameLang Source Code
        ↓
FlameLang Compiler (AST → IR → Codegen)
        ↓
Generated C/LLVM Code (calls hv_* functions)
        ↓
libsagco_hv_core.so (Rust FFI layer)
        ↓
KVM /dev/kvm ioctls (kernel interface)
```

**Key Principle:** FlameLang never touches `/dev/kvm` directly. All hypervisor operations go through the C ABI defined in `hv_api.h`.

---

## 1. C ABI: The Contract

### Header File: `include/hv_api.h`

The C header defines:
- **Error codes** (`hv_result_t`)
- **VM configuration** (`hv_vm_config_t`)
- **Lifecycle functions** (init/shutdown)
- **VM management functions** (create/start/stop/destroy)

### Example Usage from C:

```c
#include "hv_api.h"

int main() {
    hv_init();
    
    hv_vm_config_t cfg = {
        .name = "my_vm",
        .disk_path = "/isos/alpine.iso",
        .mem_mb = 512,
        .vcpus = 2
    };
    
    hv_create_vm(&cfg);
    hv_start_vm("my_vm");
    
    // ... VM runs ...
    
    hv_stop_vm("my_vm");
    hv_destroy_vm("my_vm");
    hv_shutdown();
    
    return 0;
}
```

---

## 2. Rust Implementation: `src/hv_api.rs`

The Rust side implements the C ABI with:
- `#[no_mangle]` for stable symbol names
- `extern "C"` for C calling convention
- `#[repr(C)]` for C-compatible memory layout

### Current Implementation (Phase 1)

Phase 1 is a **stub implementation** that:
- ✅ Validates parameters
- ✅ Manages VM registry in memory
- ✅ Provides comprehensive logging
- ✅ Tests the FFI boundary
- ❌ Does NOT actually use KVM yet

### Future Implementation (Phase 2+)

Phase 2+ will add actual KVM integration:
- Open `/dev/kvm`
- Create VM with `KVM_CREATE_VM`
- Allocate guest memory
- Load kernel/disk images
- Create and run vCPUs
- Handle VM exits (MMIO, IO, etc.)

---

## 3. FlameLang DSL Syntax

### Hypervisor Block

```flame
hypervisor "SAGCO-HV" {
  default_memory = 512_MB
  default_vcpus  = 1
}
```

Lowers to: `hv_init()`

### VM Definition Block

```flame
vm "sagco_live_1" {
  memory  = 1024_MB
  vcpus   = 2
  disk    = "/isos/sagco-live.iso"
  kernel  = "/boot/vmlinuz-sagco"
  cmdline = "root=/dev/vda console=ttyS0"
}
```

Lowers to:
```c
hv_vm_config_t cfg = {
    .name = "sagco_live_1",
    .disk_path = "/isos/sagco-live.iso",
    .kernel_path = "/boot/vmlinuz-sagco",
    .cmdline = "root=/dev/vda console=ttyS0",
    .mem_mb = 1024,
    .vcpus = 2,
    .flags = 0
};
hv_create_vm(&cfg);
```

### Boot Command

```flame
boot "sagco_live_1"
```

Lowers to:
```c
hv_start_vm("sagco_live_1");
```

---

## 4. Compiler Integration

### FlameLang Compiler Pipeline

1. **Parse** FlameLang source into AST
2. **Lower** hypervisor constructs to IR nodes
3. **Codegen** IR to C/LLVM calls to `hv_*` functions
4. **Link** with `libsagco_hv_core.so`
5. **Output** executable binary

### Grammar Extensions

```ebnf
program ::= statement*

statement ::= hypervisor_decl
            | vm_decl
            | boot_cmd
            | stop_cmd
            | destroy_cmd

hypervisor_decl ::= "hypervisor" STRING "{" hv_config* "}"

hv_config ::= "default_memory" "=" memory_size
            | "default_vcpus" "=" NUMBER

vm_decl ::= "vm" STRING "{" vm_config* "}"

vm_config ::= "memory" "=" memory_size
            | "vcpus" "=" NUMBER
            | "disk" "=" STRING
            | "kernel" "=" STRING
            | "cmdline" "=" STRING

boot_cmd ::= "boot" STRING

memory_size ::= NUMBER ("_MB" | "_GB")
```

---

## 5. Building the Hypervisor Core

### Build Rust Library

```bash
cd hypervisor
cargo build --release
```

This produces:
- `target/release/libsagco_hv_core.so` (Linux)
- `target/release/libsagco_hv_core.dylib` (macOS)
- `target/release/sagco_hv_core.dll` (Windows)

### Run Tests

```bash
cargo test
```

### Link from C

```bash
gcc -o hv_controller \
    examples/generated_hv_main.c \
    -L target/release \
    -l sagco_hv_core \
    -I include
    
LD_LIBRARY_PATH=target/release ./hv_controller
```

---

## 6. Phase 1 Goal: First Boot

### Success Criteria

✅ Write FlameLang file that boots one VM via KVM

```flame
hypervisor "SAGCO-HV" {
  default_memory = 256_MB
  default_vcpus  = 1
}

vm "test" {
  memory = 256_MB
  vcpus  = 1
  disk   = "/isos/sagco-live.iso"
}

boot "test"
```

✅ Compiler generates C code calling `hv_*` functions  
✅ Links with `libsagco_hv_core.so`  
✅ (Phase 2) See guest boot in console

### Current Status

- [x] C ABI header defined
- [x] Rust FFI layer implemented (stub mode)
- [x] Tests passing
- [x] Example FlameLang DSL documented
- [x] Example generated C code provided
- [ ] FlameLang compiler integration (future)
- [ ] Real KVM implementation (Phase 2)

---

## 7. API Reference

### Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | `HV_OK` | Operation succeeded |
| 1 | `HV_ERR_INIT` | Initialization failed |
| 2 | `HV_ERR_CREATE` | VM creation failed |
| 3 | `HV_ERR_START` | VM start failed |
| 4 | `HV_ERR_STOP` | VM stop failed |
| 5 | `HV_ERR_DESTROY` | VM destruction failed |
| 6 | `HV_ERR_INVALID` | Invalid parameter |

### Functions

#### `hv_init()`
Initialize the hypervisor subsystem.
- Opens `/dev/kvm` (Phase 2+)
- Checks KVM API version
- Sets up global state

#### `hv_shutdown()`
Clean up and shut down hypervisor.
- Closes all VMs
- Releases resources

#### `hv_create_vm(cfg)`
Create a new virtual machine.
- Allocates VM resources
- Sets up memory regions
- Prepares vCPUs

#### `hv_start_vm(name)`
Start a stopped VM.
- Launches vCPU threads
- Enters KVM_RUN loop

#### `hv_stop_vm(name)`
Stop a running VM.
- Exits KVM_RUN loop
- Terminates vCPU threads

#### `hv_destroy_vm(name)`
Destroy a VM and free resources.
- Must be stopped first
- Releases memory
- Closes file descriptors

---

## 8. Next Steps

### For FlameLang Compiler Team

1. Implement parser for hypervisor/vm/boot constructs
2. Add IR nodes for hypervisor operations
3. Implement codegen to C or LLVM
4. Set up linking with libsagco_hv_core.so
5. Test end-to-end compilation

### For Hypervisor Core Team

1. Add KVM dependencies (kvm-ioctls, kvm-bindings)
2. Implement `/dev/kvm` open and API version check
3. Add memory allocation and region setup
4. Implement vCPU creation and initial state
5. Add KVM_RUN loop with exit handling
6. Test with minimal Linux kernel boot

### For Integration

1. Create example SAGCO-OS system
2. Add hypervisor controller binary to /usr/bin
3. Test FlameLang → compiled binary → VM boot
4. Document deployment process
5. Add networking, PCI, multiple guests (later phases)

---

## 9. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FlameLang Source                       │
│  hypervisor "SAGCO-HV" { ... }                             │
│  vm "test" { memory = 256_MB ... }                         │
│  boot "test"                                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  FlameLang Compiler                         │
│  Parser → AST → IR → Codegen                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Generated C Code                           │
│  hv_init();                                                │
│  hv_create_vm(&cfg);                                       │
│  hv_start_vm("test");                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 C ABI (hv_api.h)                           │
│  FFI Boundary - Stable Contract                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Rust Implementation (hv_api.rs)                  │
│  libsagco_hv_core.so                                       │
│  - Parameter validation                                    │
│  - VM registry management                                  │
│  - KVM ioctl wrappers                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Linux KVM (/dev/kvm)                       │
│  - KVM_CREATE_VM                                           │
│  - KVM_SET_USER_MEMORY_REGION                             │
│  - KVM_CREATE_VCPU                                         │
│  - KVM_RUN                                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Security Considerations

### Privilege Separation

- FlameLang code runs with user privileges
- FFI boundary enforces parameter validation
- KVM operations require appropriate permissions

### Memory Safety

- Rust guarantees memory safety in hypervisor core
- FFI boundary carefully validates C pointers
- No buffer overflows or use-after-free

### Resource Limits

- VM memory limits enforced
- vCPU count validated
- Future: cgroups integration for resource control

---

## License

MIT License - See LICENSE file for details

---

## Contact

- **Organization:** Strategickhaos DAO LLC
- **Project:** SAGCO OS
- **Repository:** https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
