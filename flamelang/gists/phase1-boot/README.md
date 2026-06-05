# Phase 1: Hypervisor Boot/GDT

## Overview

This phase implements the boot sequence and Global Descriptor Table (GDT) initialization for a Type-1 hypervisor, mirroring architectures from ACRN, Xen, and Gunyah.

## Components

- **hyper_boot.flm**: FlameLang implementation of boot sequence
- **manifest.json**: Module metadata and dependencies
- **test.json**: Test suite for validation
- **README.md**: This documentation

## Architecture

### Boot Sequence

1. **Entry Point**: Hypervisor receives control from UEFI/GRUB bootloader
2. **GDT Initialization**: Set up Global Descriptor Table with:
   - Null descriptor (required by x86 architecture)
   - Code segment (64-bit, ring 0, executable)
3. **Protected Mode**: Enable CR0.PE bit to enter protected mode
4. **State Initialization**: Set up initial hypervisor data structures

### GDT Structure

The GDT contains segment descriptors for memory protection:

```
+-------+-------+-------+
| Index | Base  | Flags |
+-------+-------+-------+
|   0   | 0x00  | NULL  | <- Required null descriptor
|   1   | 0xFF  | 0xAF9B| <- Code segment (64-bit, ring 0)
+-------+-------+-------+
```

### Flags Breakdown (0xAF9B)

- **Present** (P=1): Segment is valid
- **DPL=0**: Ring 0 (hypervisor privilege)
- **Type=1011**: Code segment, executable, readable
- **64-bit**: Long mode enabled

## Proofs

### Safety Guarantees

1. **No Buffer Overflow**: GDT array is bounded (3 entries)
2. **Deterministic**: Boot sequence is fully deterministic (p=1.0)
3. **No Memory Violations**: All accesses within valid ranges

### Verification

- Formal proof that GDT indices never exceed bounds
- State machine proof of boot sequence correctness
- No undefined behavior in any execution path

## Integration with SAGCO-OS

This phase is the foundation for the SAGCO hypervisor stack:

- **Compiler**: FlameLang compiler parses .flm → IR → x86/ARM
- **Proofs**: Safety proofs verified before code generation
- **VI Integration**: Uncertainty model for boot timing variability
- **Guardian**: Maps boot state to geometric stability metrics

## Usage

```bash
# Compile Phase 1
flamelang compile hyper_boot.flm --output phase1.bin --verify

# Run tests
flamebench test test.json

# Deploy to hypervisor
sagco-deploy phase1.bin --target hypervisor-core
```

## References

- **ACRN**: Intel ACRN hypervisor boot flow
- **Xen**: Xen Project hypervisor initialization
- **Gunyah**: Qualcomm Gunyah boot sequence
- **x86-64 ABI**: System V AMD64 ABI specification
