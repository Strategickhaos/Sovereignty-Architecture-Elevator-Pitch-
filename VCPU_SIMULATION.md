# SAGCO vCPU Hypervisor Simulation

## Overview

This implementation provides a QEMU-inspired virtual CPU (vCPU) simulation integrated with the Sovereignty Architecture Geometric Computing and Ontology (SAGCO) framework. The simulation demonstrates how SAGCO's proof systems, Variational Inference (VI), and geometric guardian mapping can be applied to hypervisor-level vCPU management.

## Architecture

### Components

1. **vCPU Simulation** (`src/bin/sagco_vcpu_sim.rs`)
   - Multi-threaded vCPU execution (mirrors QEMU's thread-per-vCPU model)
   - TCG-style fetch/decode/execute loop
   - 16 general-purpose registers
   - 4KB memory space
   - Interrupt queue and handling
   - Cycle timing with jitter simulation

2. **Trigonometric Tables** (`src/sagco_tables.rs`)
   - O(1) sine/cosine lookups
   - Used for cycle timing jitter simulation
   - Precomputed 360-degree tables

3. **Probability Module** (`src/probability.rs`)
   - Gaussian distributions for Variational Inference
   - KL divergence calculation
   - Entropy measurement
   - Uncertainty quantification

4. **Guardian Safety System** (`src/sagco_guardian.rs`)
   - Maps uncertainty to geometric points
   - 4-quadrant classification (Q1-Q4)
   - 60-minute DNA clock
   - Safety gate enforcement

## Instruction Set

The simulated vCPU supports the following opcodes:

| Opcode | Instruction | Description |
|--------|-------------|-------------|
| `0x01` | ADD a, b    | Add register b to register a |
| `0x02` | SUB a, b    | Subtract register b from register a |
| `0x10` | LOAD r, addr | Load from memory address into register |
| `0x11` | STORE r, addr | Store register value to memory address |
| `0x20` | JMP addr    | Jump to address |
| `0x30` | INT code    | Queue interrupt |
| `0xFF` | HALT        | Halt execution |

## SAGCO Integration

### Variational Inference (VI)

The simulator tracks cycle execution times as a Gaussian distribution:
- **Mean**: Average cycle time
- **Variance**: Timing jitter
- **KL Divergence**: Measure of deviation from expected timing
- **Entropy**: Bits of uncertainty in timing

### Guardian Safety Gates

The guardian maps uncertainty to geometric points:
- **Q1 Linguistic** (Minutes 0-14): Container/Error detection
- **Q2 Numeric** (Minutes 15-29): Timeout/Latency gates
- **Q3 Wave** (Minutes 30-44): Runtime proof verification
- **Q4 DNA** (Minutes 45-59): System race detection

Safety rules:
- Reject if minute 0 with Container element
- Reject if minute 15 with Numeric element
- Reject if minutes 45-50 with DNA element
- Accept all other configurations

### Proof-Bounded Operations

All memory operations are bounded:
- Array indices checked against MEM_SIZE
- Program loading with bounds verification
- No buffer overflows possible

## Building and Running

### Build

```bash
cargo build --release
```

### Run Tests

```bash
cargo test
```

Expected output:
```
running 10 tests
test probability::tests::test_gaussian_kl ... ok
test probability::tests::test_entropy ... ok
test probability::tests::test_uncertainty_acceptable ... ok
test sagco_guardian::tests::test_map_to_geometry ... ok
test sagco_guardian::tests::test_safety_classification ... ok
test sagco_tables::tests::test_sin_lookup ... ok
test sagco_tables::tests::test_cos_lookup ... ok
test tests::test_vcpu_exec ... ok
test tests::test_vcpu_halt ... ok
test tests::test_vcpu_sim ... ok

test result: ok. 10 passed; 0 failed
```

### Run Simulation

```bash
cargo run --release --bin sagco_vcpu_sim
```

Expected output:
```
═══════════════════════════════════════════════════════════
  SAGCO vCPU HYPERVISOR SIMULATION (QEMU-Inspired)
  Multi-threaded vCPU with VI + Guardian Safety Gates
═══════════════════════════════════════════════════════════

Running vCPU simulation with 2 cores...

✅ Simulation Complete!
   Average KL Divergence: 1.3069
   Threshold: 0.50
   Status: ✗ FAILED (high jitter detected)

🧬 SAGCO Integration:
   ✓ Variational Inference on cycle timing
   ✓ Guardian geometry mapping
   ✓ Safety gates enforced
   ✓ Proof-bounded memory access

═══════════════════════════════════════════════════════════
```

## 16 Proofs Implementation

See [`VCPU_16_PROOFS.md`](VCPU_16_PROOFS.md) for detailed documentation of how the SAGCO compiler solves traditional programming language bottlenecks through:

1. Safe memory access
2. Fast compilation
3. Formal safety verification
4. Race-free concurrency
5. Bounded floating-point uncertainty
6. Scalable parallelism
7. Geometric explainability
8. Efficient domain-specific code
9. Unbiased logical inference
10. Safe edge case handling
11. Low-overhead inference
12. Stable parameters
13. General-purpose code
14. Secure compilation
15. Multi-modal alignment
16. Verified deployment

## QEMU Comparison

This simulation mirrors QEMU's vCPU architecture:

| Feature | QEMU | SAGCO vCPU |
|---------|------|------------|
| Threading | pthread (thread per vCPU) | std::thread (thread per vCPU) |
| Execution | TCG translation blocks | Fetch/decode/execute loop |
| Memory | Guest physical memory | 4KB bounded memory |
| Interrupts | cpu_interrupt() flags | Interrupt queue |
| Synchronization | QemuMutex | Arc<Mutex<_>> |
| State | CPUState struct | vCPU struct |
| Safety | Runtime checks | Compile-time proofs + VI |

### Key Differences

1. **Proofs**: SAGCO adds compile-time proof verification
2. **VI**: Probabilistic tracking of execution uncertainty
3. **Guardian**: Geometric safety classification
4. **Bounded**: All operations formally bounded
5. **Entropy**: Tracks and limits execution entropy

## Example Program

```rust
let program: Vec<u8> = vec![
    0x10, 0, 5,    // LOAD R0, addr=5
    0x10, 1, 3,    // LOAD R1, addr=3
    0x01, 0, 1,    // ADD R0, R1
    0xFF,          // HALT
];
```

This program:
1. Loads value from address 5 into register 0
2. Loads value from address 3 into register 1
3. Adds R1 to R0
4. Halts execution

## Performance Characteristics

- **Thread Overhead**: O(n) where n = number of vCPUs
- **Memory Access**: O(1) with bounds checking
- **Cycle Time**: ~1.0-1.1 units with trig jitter
- **VI Overhead**: O(k) where k = number of cycles tracked
- **Guardian Classification**: O(1) lookup

## Future Enhancements

1. **KVM Acceleration**: Add hardware virtualization support
2. **Extended ISA**: More complex instruction set
3. **MMU Simulation**: Memory management unit
4. **Device Emulation**: Virtual devices (disk, network)
5. **Proof Optimization**: More efficient proof checking
6. **Multi-Guardian**: Hierarchical safety gates

## References

- QEMU Source: https://github.com/qemu/qemu
- SAGCO Architecture: See repository documentation
- FlameLang Specification: See `FLAMELANG_SPECIFICATION.md`
- 16 Proofs: See `VCPU_16_PROOFS.md`

## License

Part of the Sovereignty Architecture project. See LICENSE for details.
