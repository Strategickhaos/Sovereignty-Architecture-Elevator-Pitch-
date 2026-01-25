# Phase 2: Memory Virtualization & Paging

## Overview

This phase implements memory virtualization through paging mechanisms, including Extended Page Tables (EPT) for hardware-assisted virtualization. Mirrors ACRN and Xen paging architectures.

## Components

- **hyper_paging.flm**: FlameLang implementation of paging system
- **manifest.json**: Module metadata and dependencies
- **test.json**: Comprehensive test suite
- **README.md**: This documentation

## Architecture

### Paging Hierarchy

```
Virtual Address (32-bit)
┌─────────┬─────────┬──────────┐
│ Index   │ Unused  │  Offset  │
│ [21-12] │ [31-22] │  [11-0]  │
└─────────┴─────────┴──────────┘
     |                    |
     v                    v
  PT Index           Page Offset
  (10 bits)          (12 bits = 4KB)
```

### Page Table Entry (PTE) Format

```
31                    12  11       3   2   1   0
┌──────────────────────┬──────────┬───┬───┬───┐
│  Physical Address    │ Reserved │ X │ W │ R │
└──────────────────────┴──────────┴───┴───┴───┘
                                    |   |   |
                                    |   |   +-- Read
                                    |   +------ Write
                                    +---------- Execute
```

### Extended Page Tables (EPT)

EPT provides second-level address translation for VM isolation:

1. **Guest Virtual → Guest Physical**: Handled by guest OS
2. **Guest Physical → Host Physical**: Handled by EPT (hypervisor)

```
Guest VA ─[Guest PT]→ Guest PA ─[EPT]→ Host PA
```

## Key Functions

### paging_setup()
Initializes identity-mapped page tables (1:1 mapping)
- Maps 4MB of memory (1024 × 4KB pages)
- Sets all pages as present, readable, writable

### map_page(pt, virt, phys, flags)
Maps a virtual page to a physical page
- Extracts index from virtual address
- Sets PTE with physical address and flags

### translate_address(pt, virt)
Performs page walk to translate virtual to physical
- Extracts PT index and offset
- Checks present bit
- Returns physical address or -1 (page fault)

### setup_ept()
Creates Extended Page Tables for VM memory isolation
- Maps guest physical to host physical with offset
- Enables VM memory protection

## Memory Layout

```
0x00000000 - 0x000FFFFF : Identity-mapped (1MB)
0x00100000 - 0x004FFFFF : Guest VM memory (4MB)
0x00001000 - 0x00001FFF : Primary page table
0x00002000 - 0x00002FFF : EPT
0x00003000 - 0x00003FFF : PML4 (multi-level)
```

## Proofs

### Safety Guarantees

1. **Bounded Indices**: Page table indices masked to 10 bits (< 1024)
2. **No Buffer Overflow**: All array accesses proven within bounds
3. **Deterministic**: Paging operations are fully deterministic
4. **Valid Mappings**: All PTEs properly aligned and flagged

### Verification

- Formal proof of index calculation correctness
- Loop bounds analysis ensures no overflow
- Memory access patterns verified safe
- TLB coherency maintained

## Integration with SAGCO-OS

### Uncertainty Model

Paging uncertainty comes from:
- TLB miss rates (p_miss ~ 0.05)
- Page fault handling latency (Gaussian variance)
- EPT violation handling

### Guardian Mapping

Maps paging metrics to geometry:
- **Frequency**: TLB hit rate
- **Amplitude**: Page walk depth
- **Phase**: Memory access pattern coherency

## Usage

```bash
# Compile Phase 2
flamelang compile hyper_paging.flm --output phase2.bin --verify

# Run tests with various page counts
flamebench test test.json --input page_count=1024

# Deploy with dependencies
sagco-deploy phase2.bin --require phase1-boot
```

## Performance Characteristics

- **Page Table Setup**: O(n) where n = number of pages
- **Page Mapping**: O(1) for single-level, O(k) for k-level
- **Translation**: O(k) for k-level page tables
- **TLB Miss Penalty**: ~100 cycles typical

## References

- **Intel VT-x**: Extended Page Tables specification
- **AMD-V**: Nested Page Tables (NPT)
- **ACRN**: Memory virtualization architecture
- **Xen**: Shadow page tables vs. EPT
