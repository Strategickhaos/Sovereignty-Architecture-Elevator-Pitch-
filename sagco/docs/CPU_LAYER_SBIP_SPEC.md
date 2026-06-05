# SAGCO CPU Layer - SBIP Specification

## Overview

The SAGCO CPU layer targets hardware architectures like x86_64 through LLVM-compiled native binaries. FlameLang outputs are executed directly on the host CPU after compilation, with SBIP ensuring deterministic bootstrapping of the runtime environment.

## CPU Layer Architecture

### Native Execution (Primary)

The SAGCO CPU layer provides direct hardware execution through the LLVM compilation pipeline:

```
┌──────────────────────────────────────────────────────────────┐
│                    FlameLang Source Code                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              FlameLang Compiler (AST Generation)             │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    LLVM IR Generation                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│            LLVM Optimization & Code Generation               │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Native x86_64 Binary Execution                  │
│              (Direct CPU, No Interpretation)                 │
└──────────────────────────────────────────────────────────────┘
```

### VM Execution (Optional)

An optional future SAGCO-CPU VM service can interpret bytecode for enhanced portability:

```
┌──────────────────────────────────────────────────────────────┐
│                    FlameLang Source Code                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│           FlameLang Compiler (Bytecode Backend)              │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   SAGCO Bytecode (.bc)                       │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│      SAGCO-CPU VM (Stack-Based Interpreter, Sandboxed)       │
│           Started via systemd after identity verify          │
└──────────────────────────────────────────────────────────────┘
```

## SBIP Integration

SAGCO CPU layer integrates with the Sovereignty Bootstrap Integration Protocol across three stages:

### Stage 1: Initramfs - Identity Verification

**Location**: initramfs early boot  
**Purpose**: Verify system identity and kernel integrity

- Display sovereignty splash screen
- Verify boot chain signatures
- Load trusted kernel modules (if any)
- Transition to Stage 2

### Stage 2: Initramfs - Artifact Verification

**Location**: initramfs late boot  
**Script**: `/init.d/sagco-init` or custom init hook  
**Purpose**: Verify and prepare SAGCO artifacts

**Actions performed by sagco-init:**
```bash
# 1. Display SAGCO banner
echo "SAGCO OS - Ratio Ex Nihilo - Bootstrapping Toolchain"

# 2. Verify artifact directory
if [ -d /opt/sagco/artifacts ]; then
    # 3. Verify bytecode files (hash checking)
    for bc in /opt/sagco/artifacts/*.bc; do
        sha256sum --check "$bc.sha256" || fail_boot "Artifact verification failed"
    done
    
    # 4. Optional: Execute critical bootstrap bytecode
    if [ -f /opt/sagco/artifacts/bootstrap.bc ]; then
        /opt/sagco/vm/sagco_cpu_vm.py /opt/sagco/artifacts/bootstrap.bc \
            || log_failure_msg "VM exec failed"
    fi
fi
```

### Stage 3: Systemd - Runtime Services

**Location**: Userspace, systemd-managed  
**Service**: `sagco-cpu.service`  
**Purpose**: Run VM daemon for ongoing bytecode execution

**Service activation:**
```bash
# Enable at boot
systemctl enable sagco-cpu.service

# Service starts VM daemon
ExecStart=/usr/bin/python3 /opt/sagco/vm/sagco_cpu_vm.py \
    --daemon --load-dir /opt/sagco/artifacts
```

**Service characteristics:**
- **User isolation**: Runs as dedicated `sagco` user
- **Sandboxed**: SystemD security features (ProtectSystem, NoNewPrivileges)
- **Resource limited**: Memory and CPU constraints
- **Auto-restart**: Restart on failure with backoff

## Deterministic Bootstrap

SBIP ensures deterministic bootstrapping through:

1. **Cryptographic Verification**: All artifacts verified against trusted hashes
2. **Ordered Execution**: Stage 1 → Stage 2 → Stage 3 (strictly sequential)
3. **Identity Binding**: Boot artifacts tied to system identity
4. **Fail-Safe**: Boot halts if verification fails

## Native Binary Deployment

For production workloads, native binaries provide optimal performance:

```bash
# Compile FlameLang to native
cd /opt/sagco/compiler
python3 flamelang_compiler.py native app.flame

# Link to executable
clang /opt/sagco/artifacts/app.o -o /opt/sagco/artifacts/app

# Hash for verification
sha256sum /opt/sagco/artifacts/app > /opt/sagco/artifacts/app.sha256

# Execute directly (no VM)
/opt/sagco/artifacts/app
```

**Integration with SBIP:**
- Stage 2 verifies binary hash
- Stage 3 can launch as systemd service (separate .service file)
- No interpreter overhead

## VM Service Deployment

For portable or sandboxed workloads, use VM mode:

```bash
# Compile FlameLang to bytecode
cd /opt/sagco/compiler
python3 flamelang_compiler.py vm app.flame

# Hash for verification
sha256sum /opt/sagco/artifacts/app.bc > /opt/sagco/artifacts/app.bc.sha256

# VM daemon automatically picks up .bc files
systemctl start sagco-cpu.service
journalctl -u sagco-cpu.service -f  # Watch execution
```

## Directory Structure

```
/opt/sagco/
├── compiler/
│   └── flamelang_compiler.py      # Compiler (LLVM & bytecode backends)
├── vm/
│   └── sagco_cpu_vm.py            # VM interpreter (optional)
├── artifacts/
│   ├── *.ll                       # LLVM IR (intermediate)
│   ├── *.o                        # Object files
│   ├── *.bc                       # Bytecode files
│   ├── *.sha256                   # Hash manifests
│   └── executables                # Native binaries
└── sbip/
    ├── sagco-init                 # Stage 2 boot script
    └── sagco-cpu.service          # Stage 3 systemd service
```

## Security Model

### Native Mode
- **Threat**: Malicious native code
- **Mitigation**: Cryptographic verification in Stage 2, signed binaries
- **Execution**: Direct CPU (no sandbox, but verified)

### VM Mode
- **Threat**: Malicious bytecode
- **Mitigation**: Bytecode verification, VM sandboxing, systemd isolation
- **Execution**: Interpreter (limited syscalls, resource-constrained)

## Performance Expectations

| Mode   | Compilation | Startup  | Runtime  | Portability | Sandboxing |
|--------|-------------|----------|----------|-------------|------------|
| Native | Slow        | Fast     | Fast     | Low         | No         |
| VM     | Fast        | Fast     | Moderate | High        | Yes        |

## Future Extensions

1. **JIT Compilation**: Compile hot bytecode paths to native code at runtime
2. **Kernel Module**: Optional kernel-space VM primitives for performance
3. **Hardware Acceleration**: Use CPU extensions (AVX, SIMD) in bytecode
4. **Distributed Execution**: Execute bytecode across swarm nodes

---

*SBIP Stage Integration: Stage 2 (sagco-init) verifies artifacts, Stage 3 (systemd) runs VM daemon.*
