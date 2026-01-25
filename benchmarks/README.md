# SAGCO-HYDRA Benchmark Suites

This directory contains comprehensive benchmark and test suites for all layers of the SAGCO-HYDRA architecture.

## Test Suites

### Oracle Tests (ORC-001 → ORC-010)
Guardian Layer (ORB1) validation tests.

**Location:** `oracle-tests/test_oracle_benchmarks.py`

**Tests:**
- ORC-001: Signature detection accuracy (>= 95%)
- ORC-002: False positive rate (<= 5%)
- ORC-003: Network anomaly detection
- ORC-004: Protocol analysis accuracy
- ORC-005: Password strength scoring
- ORC-006: Shannon entropy calculation
- ORC-007: Search space estimation
- ORC-008: Pattern recognition performance
- ORC-009: Ensemble voting consensus
- ORC-010: Guardian response time (<= 100ms)

**Run:**
```bash
cd oracle-tests
python3 test_oracle_benchmarks.py
```

### FlameLang Tests (FLC-001 → FLC-008)
FlameLang Compiler (FLM2) validation tests.

**Location:** `flamelang-specs/test_flamelang_benchmarks.py`

**Tests:**
- FLC-001: Lexer throughput (>= 100KB/s)
- FLC-002: Parser produces valid AST
- FLC-003: Type checker accuracy (100%)
- FLC-004: Quadrilateral IR generation
- FLC-005: Optimization improves performance (>= 2x)
- FLC-006: x86-64 code generation
- FLC-007: ARM64 code generation
- FLC-008: End-to-end compilation time (<= 1s)

**Plus 5-Layer Transformation Tests:**
- Layer 1: English → Hebrew Gematria
- Layer 2: Hebrew → Unicode
- Layer 3: Unicode → Wave (432Hz)
- Layer 4: Wave → DNA
- Layer 5: DNA → LLVM IR

**Run:**
```bash
cd flamelang-specs
python3 test_flamelang_benchmarks.py
```

### Hypervisor Tests (HYP-001 → HYP-006)
SAGCO-HYDRA Hypervisor (Layer 0) validation tests.

**Location:** `hypervisor-tests/test_hypervisor_benchmarks.py`

**Tests:**
- HYP-001: Boot sequence completes successfully
- HYP-002: VMX/SVM hardware support detection
- HYP-003: Extended/Nested page table support
- HYP-004: Virtual CPU creation and management
- HYP-005: Memory isolation between VMs
- HYP-006: VirtIO device performance

**Additional Test Categories:**
- **KVM Tests:** Module loading, FFI bindings, VM creation
- **Neural Tick Tests:** Scheduling latency, fairness, priorities
- **Boot Tests:** GRUB, kernel, init, shell, boot time

**Run:**
```bash
cd hypervisor-tests
python3 test_hypervisor_benchmarks.py
```

### Enterprise Framework Tests
Legacy test suite for LLM and security analytics.

**Location:** Root benchmark files
- `test_comprehensive.py`
- `test_data_ingestion.py`
- `test_llm_safety.py`
- `test_security_analytics.py`

**Run:**
```bash
python3 run_all_tests.py --mode smoke  # Quick validation
python3 run_all_tests.py --mode full   # Complete regression
```

## Multi-Language Efficiency Test

The `sagco-benchmark.py` tool (in `../tools/`) provides cross-language performance comparison.

**Run:**
```bash
cd ../tools
./sagco-benchmark.py
```

**Languages Tested:**
- Python (baseline)
- Rust (optimal performance)
- C# (JIT compiled)
- Bash (shell scripting)
- FlameLang (when available)

## DNA Mutation Testing

After benchmark runs, the system suggests DNA strand mutations:

**Example:**
```
Current: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1
Suggest: SAGCO-ATG-FLM2.1-MSMC2-P16-CMD27-ISO103-MESH5-ORB1
```

Mutations indicate:
- Performance improvements
- New features added
- Bug fixes completed
- Architectural changes

## CI/CD Integration

These tests can be integrated into continuous integration:

```yaml
# Example GitHub Actions workflow
- name: Run Oracle Tests
  run: python3 benchmarks/oracle-tests/test_oracle_benchmarks.py

- name: Run FlameLang Tests
  run: python3 benchmarks/flamelang-specs/test_flamelang_benchmarks.py

- name: Run Hypervisor Tests
  run: python3 benchmarks/hypervisor-tests/test_hypervisor_benchmarks.py

- name: Run Multi-Language Benchmark
  run: python3 tools/sagco-benchmark.py
```

## Requirements

**Python Packages:**
```bash
pip3 install pyyaml
# All other dependencies are Python standard library
```

**System Requirements:**
- Python 3.7+
- Rust toolchain (for Rust benchmarks)
- .NET SDK (for C# benchmarks)
- Bash shell

## Reporting

All tests output standard unittest results:
- Pass/Fail status
- Execution time
- Detailed failure messages
- Summary statistics

For enterprise reporting, use the master runner:
```bash
python3 run_all_tests.py --mode full --output reports/
```

Reports are saved to:
- `reports/detailed_results_TIMESTAMP.json`
- `reports/executive_summary_TIMESTAMP.json`
- `reports/latest_results.json`
- `reports/latest_summary.json`

## Architecture Validation

These benchmarks validate the entire SAGCO-HYDRA stack:

```
Layer 4 (Guardian) ← Oracle Tests (ORC-001 → ORC-010)
Layer 3 (Mesh)     ← Mesh connectivity (via sagco-mesh)
Layer 2 (Kernel)   ← Enterprise framework tests
Layer 1 (Compiler) ← FlameLang tests (FLC-001 → FLC-008)
Layer 0 (Hypervisor) ← Hypervisor tests (HYP-001 → HYP-006)
```

## License

Part of the SAGCO-HYDRA project.  
Copyright © 2025 Strategickhaos DAO LLC  
Wyoming Entity: 2025-001708194

---

*"Seder Mitokh Kaos - Order from Chaos"*
