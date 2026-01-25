# SAGCO-HYDRA Tools

This directory contains the command arsenal (CMD27) for the SAGCO-HYDRA system.

## Commands

### sagco-one
Unified control command for SAGCO-HYDRA operations.

**Usage:**
```bash
# Display DNA strand
./sagco-one dna

# Check toolchain status
./sagco-one status

# Show evolution timeline
./sagco-one evolution

# Deploy SAGCO-VM
./sagco-one deploy

# Full status report
./sagco-one full
```

### sagco-mesh
Neural mesh node discovery and status monitoring.

**Usage:**
```bash
# Discover all 5 mesh nodes
./sagco-mesh

# Shows topology and connectivity status for:
# - ATHENA (Subconscious)
# - LYRA (Right Hemisphere)
# - NOVA (Left Hemisphere)
# - ATEROTH (Archive)
# - SAGCO-VM (Soul)
```

### sagco-oracle
Guardian Layer analysis for hallucination detection.

**Usage:**
```bash
# Analyze text from command line
./sagco-oracle "Text to analyze"

# Analyze text from stdin
echo "Text to analyze" | ./sagco-oracle

# Analyze from file
cat document.txt | ./sagco-oracle
```

**Oracle Ensemble:**
- **SignatureOracle** - Pattern matching (Snort/Yara style)
- **NetworkOracle** - Information flow analysis
- **SearchSpaceOracle** - Entropy and cryptographic strength
- **EntropyOracle** - Shannon information theory

### sagco-benchmark.py
Multi-language efficiency benchmark test.

**Usage:**
```bash
# Run full benchmark suite
./sagco-benchmark.py

# Tests performance of:
# - Python (interpreted)
# - Rust (compiled, optimized)
# - C# (JIT compiled)
# - Bash (shell script)
# - FlameLang (if available)
```

**Output:**
- Execution time per language
- Operations per second
- Relative efficiency (Rust = 100%)
- Evolution recommendations
- Suggested DNA mutations

### sagco-deploy.py
Universal file deployer for SAGCO artifacts.

**Usage:**
```bash
# Interactive wizard mode
./sagco-deploy.py --interactive

# Deploy latest file to current directory
./sagco-deploy.py latest .

# Deploy specific file
./sagco-deploy.py sagco-os-v1.0.3.iso /mnt/iso

# Verbose output
./sagco-deploy.py -v file.iso /destination
```

## Installation

All tools are Python 3 scripts with minimal dependencies:

```bash
# Make executable
chmod +x sagco-*

# Add to PATH (optional)
export PATH=$PATH:$(pwd)

# Install Python dependencies (if needed)
pip3 install pyyaml
```

## Requirements

- Python 3.7+
- PyYAML (for spec parsing)
- Standard Unix utilities (ping, etc.)

## Testing

All tools have been tested and validated:

```bash
# Test each tool
./sagco-one dna
./sagco-mesh
echo "test" | ./sagco-oracle
./sagco-benchmark.py
```

## Architecture Integration

These tools integrate with the SAGCO-HYDRA 5-layer architecture:

- **Layer 0 (Hypervisor):** sagco-deploy for ISO deployment
- **Layer 1 (Compiler):** sagco-benchmark for FlameLang testing
- **Layer 2 (Kernel):** sagco-one for system control
- **Layer 3 (Mesh):** sagco-mesh for node discovery
- **Layer 4 (Guardian):** sagco-oracle for validation

## DNA Strand

Current DNA: `SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1`

See `../docs/DNA_STRAND.md` for complete specification.

## License

Part of the SAGCO-HYDRA project.  
Copyright © 2025 Strategickhaos DAO LLC  
Wyoming Entity: 2025-001708194

---

*"Seder Mitokh Kaos - Order from Chaos"*
