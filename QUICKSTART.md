# 🚀 SAGCO-HYDRA Quick Start Guide

**DNA Strand:** `SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1`  
**Version:** 1.1.0

## Installation (2 minutes)

```bash
# 1. Clone repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# 2. Make tools executable
chmod +x tools/sagco-*

# 3. (Optional) Add to PATH
export PATH=$PATH:$(pwd)/tools
```

## Essential Commands (30 seconds each)

### Display DNA Strand
```bash
tools/sagco-one dna
```
Shows the complete DNA codon registry with status indicators.

### Check System Status
```bash
tools/sagco-one status
```
Validates toolchain availability (Python, Rust, C#, Bash, FlameLang).

### Discover Mesh Nodes
```bash
tools/sagco-mesh
```
Displays topology and connectivity of all 5 neural mesh nodes.

### Analyze Text for Hallucinations
```bash
echo "Studies definitely show this is 100% certain" | tools/sagco-oracle
```
Runs Guardian Layer analysis through 4 oracle ensemble.

### Run Performance Benchmark
```bash
tools/sagco-benchmark.py
```
Tests efficiency across Python, Rust, C#, Bash, and FlameLang.

## Test Suites (1 minute each)

### Oracle Tests (ORC-001 → ORC-010)
```bash
cd benchmarks/oracle-tests
python3 test_oracle_benchmarks.py
```

### FlameLang Tests (FLC-001 → FLC-008)
```bash
cd benchmarks/flamelang-specs
python3 test_flamelang_benchmarks.py
```

### Hypervisor Tests (HYP-001 → HYP-006)
```bash
cd benchmarks/hypervisor-tests
python3 test_hypervisor_benchmarks.py
```

## 5-Layer Architecture

```
Layer 4: Guardian (ORB1)      ← Oracle analysis
Layer 3: Mesh (MESH5)         ← 5-node network
Layer 2: Kernel (SAGCO-OS)    ← Cognitive loop
Layer 1: Compiler (FLM2)      ← FlameLang
Layer 0: Hypervisor (HYDRA)   ← Bare metal
```

## Key Files

| File | Purpose |
|------|---------|
| `sagco_unified_spec.yaml` | Complete DNA specification |
| `docs/ARCHITECTURE.md` | System architecture |
| `docs/DNA_STRAND.md` | DNA codon details |
| `docs/SAGCO_HYDRA_README.md` | Overview |
| `tools/README.md` | Command documentation |
| `benchmarks/README.md` | Test suite documentation |

## Neural Mesh Nodes

1. **ATHENA** - Subconscious (i7-9700F, 64GB, RTX)
2. **LYRA** - Right Hemisphere (ASUS Laptop)
3. **NOVA** - Left Hemisphere (Intel Laptop)
4. **ATEROTH** - Archive (Sony VAIO)
5. **SAGCO-VM** - Soul (Alpine VirtualBox)

## Next Steps

1. ✅ Run `tools/sagco-one full` for complete status
2. ✅ Explore `docs/ARCHITECTURE.md` for deep dive
3. ✅ Run benchmark suites to validate system
4. ✅ Check `mesh/hosts/*.yaml` for node configs
5. ✅ Review `sagco_unified_spec.yaml` for full spec

## Requirements

- **Python 3.7+** (required)
- **PyYAML** (recommended)
- **Rust toolchain** (optional, for Rust benchmarks)
- **.NET SDK** (optional, for C# benchmarks)

## Support

- **Documentation:** See `docs/` directory
- **Issues:** GitHub Issues
- **Community:** Discord (see COMMUNITY.md)

---

*"Seder Mitokh Kaos - Order from Chaos"*

**Strategickhaos DAO LLC** | Wyoming Entity: 2025-001708194
