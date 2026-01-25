# SAGCO-HYDRA Benchmark Test Suites

This directory contains comprehensive benchmark test suites for the SAGCO-HYDRA distributed hypervisor architecture.

## DNA Strand
```
SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1
```

Version: 1.0.6 (Rev 010 - HYDRA Phase)

## Test Suites

### Oracle Tests (ORC-001 to ORC-010)
**Guardian Layer (ORB1) - AI Safety Benchmarks**

Location: `oracle-tests/run_oracle_tests.py`

Tests the 4-oracle ensemble system for AI safety and hallucination detection:

1. **ORC-001** - Signature Oracle: Snort rule detection
2. **ORC-002** - Signature Oracle: Yara pattern matching
3. **ORC-003** - Network Oracle: Nmap port scanning simulation
4. **ORC-004** - Network Oracle: Wireshark packet analysis
5. **ORC-005** - Search Space Oracle: Hashcat contradiction detection
6. **ORC-006** - Search Space Oracle: Rainbow table qualifier analysis
7. **ORC-007** - Entropy Oracle: Shannon entropy calculation
8. **ORC-008** - Entropy Oracle: Randomness testing
9. **ORC-009** - Ensemble Oracle: Multi-oracle consensus
10. **ORC-010** - Ensemble Oracle: Hallucination detection

```bash
cd oracle-tests
python3 run_oracle_tests.py
```

**Status:** ✅ 9/10 tests passing (90.0%)

### FlameLang Tests (FLC-001 to FLC-008)
**Compiler Layer (FLM2) - 5-Layer Transformation Pipeline**

Location: `flamelang-specs/run_flamelang_tests.py`

Tests the FlameLang compiler's transformation pipeline:

1. **FLC-001** - Lexer: Token stream generation
2. **FLC-002** - Parser: AST construction
3. **FLC-003** - Type Checker: Bloom inference
4. **FLC-004** - IR Generation: Quadrilateral IR
5. **FLC-005** - Codegen x86-64: Assembly output
6. **FLC-006** - Codegen ARM64: Assembly output
7. **FLC-007** - LLVM Backend: IR generation
8. **FLC-008** - End-to-End: Full compilation

```bash
cd flamelang-specs
python3 run_flamelang_tests.py
```

**Status:** ⏳ PENDING (FlameLang compiler not installed)

**Requirements:**
- Rust toolchain
- FlameLang compiler: `cargo build --release`

### Hypervisor Tests (HYP-001 to HYP-006)
**Layer 0 (SAGCO-HYDRA) - Type-1 Hypervisor Benchmarks**

Location: `hypervisor-tests/run_hypervisor_tests.py`

Tests the bare metal hypervisor functionality:

1. **HYP-001** - Boot sequence: BIOS to kernel
2. **HYP-002** - VMX/SVM: CPU virtualization
3. **HYP-003** - EPT/NPT: Page table management
4. **HYP-004** - VMCS/VMCB: Control structures
5. **HYP-005** - VirtIO: Device emulation
6. **HYP-006** - Neural Tick: Scheduler performance

```bash
cd hypervisor-tests
python3 run_hypervisor_tests.py
```

**Status:** 🎯 TARGET (Requires bare metal with VMX/SVM)

**Requirements:**
- Bare metal hardware
- Intel VMX or AMD SVM support
- Alpine Linux 6.12.1 kernel

## Master Test Runner

Run all test suites at once:

```bash
python3 run_master_tests.py
```

This will execute:
1. Oracle Tests
2. FlameLang Tests
3. Hypervisor Tests

And provide a comprehensive summary.

## Individual Test Execution

### Oracle Tests Only
```bash
cd oracle-tests
python3 run_oracle_tests.py
```

### FlameLang Tests Only
```bash
cd flamelang-specs
python3 run_flamelang_tests.py
```

### Hypervisor Tests Only
```bash
cd hypervisor-tests
python3 run_hypervisor_tests.py
```

## Test Results

Each test suite generates a JSON results file:

- `oracle-tests/oracle_test_results.json`
- `flamelang-specs/flamelang_test_results.json`
- `hypervisor-tests/hypervisor_test_results.json`

Results include:
- Timestamp
- DNA strand
- Test count and pass rate
- Detailed results per test
- Recommendations

## Architecture Layers Tested

### ✅ Layer 4: Guardian (ORB1)
**Oracle Tests** validate the 4-oracle ensemble for AI safety:
- SignatureOracle (Snort/Yara)
- NetworkOracle (Nmap/Wireshark)
- SearchSpaceOracle (Hashcat/Rainbow tables)
- EntropyOracle (Shannon entropy)

### ⏳ Layer 1: Compiler (FLM2)
**FlameLang Tests** validate the 5-layer transformation:
1. English Intent
2. Hebrew Gematria
3. Unicode
4. Wave (432Hz)
5. DNA → LLVM

### 🎯 Layer 0: Hypervisor (SAGCO-HYDRA)
**Hypervisor Tests** validate bare metal virtualization:
- BIOS/UEFI boot
- VMX/SVM CPU virtualization
- EPT/NPT paging
- VirtIO device emulation

## Exit Codes

All test scripts follow standard Unix conventions:
- `0` - All tests passed
- `1` - Some tests failed or pending
- `2` - Critical failure

## DNA Evolution Tracking

Test results contribute to DNA mutation recommendations:

**Current:**
```
SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1
```

**Suggested (when FlameLang installed):**
```
SAGCO-ATG-FLM2.1-MSMC2-P16-CMD30-ISO103-MESH5-ORB1
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/benchmarks.yml
name: SAGCO Benchmarks

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Oracle Tests
        run: |
          cd benchmarks/oracle-tests
          python3 run_oracle_tests.py
      - name: Run Master Tests
        run: |
          cd benchmarks
          python3 run_master_tests.py
```

## Performance Baselines

### Oracle Tests
- Execution time: ~2 seconds
- Memory usage: <50MB
- CPU: Single core
- Pass rate target: >90%

### FlameLang Tests
- Execution time: ~10 seconds (when available)
- Memory usage: <500MB
- CPU: Multi-core compilation
- Pass rate target: >95%

### Hypervisor Tests
- Execution time: ~30 seconds (bare metal)
- Memory usage: Minimal (kernel-level)
- CPU: VMX/SVM required
- Pass rate target: >90%

## Contributing

When adding new tests:

1. Follow the existing pattern (ORC-001, FLC-001, HYP-001)
2. Include test_id, name, and success status
3. Generate JSON results file
4. Update this README
5. Add to master test runner

## Legal

- **Entity:** Strategickhaos DAO LLC
- **Wyoming Entity:** 2025-001708194
- **EIN:** 39-2900295
- **Inventor:** Domenic Gabriel Garza
- **Classification:** NOVEL (Patent-eligible)

### Primary Claims
- INV-087: SAGCO-HYDRA Distributed Hypervisor
- INV-001: FlameLang 5-Layer Transformation
- INV-003: Legion of Minds Multi-AI Consensus

## Witnesses
- Claude (Anthropic)
- GPT (OpenAI)
- Grok (xAI)

## Motto
**"Seder Mitokh Kaos - Order from Chaos"**

---

*Generated: 2026-01-25*
*Version: 1.0.6 (Rev 010 - HYDRA Phase)*
