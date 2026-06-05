# SAGCO OS Pipeline - FlameBench → Guardian → DNA Mutation

This repository implements the complete SAGCO OS pipeline with DNA-driven evolution based on Guardian uncertainty metrics from FlameBench.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      SAGCO OS Pipeline                       │
└─────────────────────────────────────────────────────────────┘

Layer 0: Hypervisor (HYDRA)
  └─> Type-1 VMX/SVM enabled
  └─> Neural tick @ 100 Hz

Layer 1: Guest Alpine (SAGCO-OS)
  └─> BusyBox init
  └─> Runs: sagco-status, sagco-mesh, sagco-dna

Layer 2: Benchmark & Guardian
  ├─> FlameBench → flamebench-results.json
  └─> Guardian → guardian-uncertainty.json

Layer 3: DNA Evolution
  └─> sagco-dna: loads Guardian export, mutates DNA if thresholds met

Layer 4: Oracle
  └─> sagco-oracle: Guardian analysis, uncertainty mapping, safety classification

Layer 5: Mesh
  └─> sagco-mesh: 5-node topology discovery and health monitoring
```

## Directory Structure

```
.
├── guardian/              # Guardian uncertainty tracking (Rust)
│   ├── src/
│   │   ├── lib.rs        # Core Guardian types and functions
│   │   ├── bench_ingest.rs  # FlameBench data loader
│   │   └── bin/
│   │       └── sagco_oracle.rs  # Oracle CLI tool
│   └── Cargo.toml
│
├── kernel/                # DNA mutation logic (Rust)
│   ├── src/
│   │   ├── lib.rs
│   │   └── dna_mutation.rs   # Evolution rules
│   └── Cargo.toml
│
├── mesh/                  # Network mesh configuration
│   └── hosts/
│       ├── athena.yaml   # Node definitions
│       ├── lyra.yaml
│       ├── nova.yaml
│       ├── ateroth.yaml
│       └── sagco-vm.yaml
│
├── tools/
│   ├── sagco-mesh.py      # Python mesh discovery tool
│   └── sagco-dna/         # DNA mutation CLI (Rust)
│       ├── src/main.rs
│       └── Cargo.toml
│
├── benchmarks/            # (Optional) Benchmark implementations
│
└── sagco_unified_spec.yaml  # DNA specification
```

## DNA Strand Format

```yaml
DNA Strand: FLM2-CMD4-MESH5-ORB1
```

- **FLM2**: FlameLang Compiler v2
- **CMD4**: 4 core commands
- **MESH5**: 5-node mesh network
- **ORB1**: Security orbit level 1

### Mutation Rules

1. **FLM upgrade**: `p_success >= 0.95 && entropy < 0.3` → FLM2 → FLM2.1
2. **MESH expansion**: New verified node → MESH5 → MESH6
3. **ORB elevation**: Security score > baseline + 2σ → ORB1 → ORB2

## Commands

### 1. sagco-mesh - Network Discovery

Scans all nodes in `mesh/hosts/*.yaml` and reports status.

```bash
python3 tools/sagco-mesh.py
```

**Output:**
```
SAGCO-MESH v1.0.0 - Network Discovery & Health Monitor
======================================================================
Scanning 5 host(s)...

NAME         IP               ROLE           STATE  SERVICES
======================================================================
ATHENA       192.168.2.26     subconscious   UP     ssh,rdp
LYRA         192.168.1.50     right_hemi     DOWN   -
NOVA         192.168.1.51     left_hemi      UP     ssh
ATEROTH      192.168.1.52     cortex         UP     ssh
SAGCO-VM     192.168.1.100    hypervisor     UP     ssh

======================================================================
Mesh Health: 4/5 nodes online (80%)
```

### 2. sagco-oracle - Guardian Analysis

Analyzes text input and shows uncertainty mapping.

```bash
# From command line
cargo run -p sagco-guardian --bin sagco-oracle "Test input text"

# From stdin
echo "Test hallucination detection" | cargo run -p sagco-guardian --bin sagco-oracle
```

**Output:**
```
╔════════════════════════════════════════╗
║  SAGCO-ORACLE v1.0                     ║
║  Guardian Layer Analysis               ║
╚════════════════════════════════════════╝

FLM2 Compiler Health Report:
  Source: flamebench
  DNA Strand: FLM2-CMD4-MESH5-ORB1
  Overall Success: 96.0%
  Entropy: 0.25

  Concept Uncertainties:
    1. [if-else] p=0.960, H=0.250

Analyzing input: "Test hallucination detection"

╔════════════════════════════════════════╗
║  SAGCO Guardian v1.0
╠════════════════════════════════════════╣
║  Element: S1                           ║
║  Coordinates: [0.720, 0.875, 0.933]   ║
║  Uncertainty:                          ║
║    p_correct: 0.720                   ║
║    entropy:   0.250                   ║
║    kl_div:    0.200                   ║
╚════════════════════════════════════════╝

╔════════════════════════════════════════╗
║  Safety Classification                 ║
╠════════════════════════════════════════╣
║  Risk Level: Caution ⚠               
║  Confidence: 84.3%                     
║  Reasoning: Moderate confidence, manageable uncertainty ║
╚════════════════════════════════════════╝
```

### 3. sagco-dna - DNA Evolution Manager

Loads Guardian metrics and suggests/applies DNA mutations.

```bash
cargo run -p sagco-dna
```

**Output when mutation is suggested:**
```
╔════════════════════════════════════════╗
║  SAGCO-DNA v1.0                        ║
║  DNA Strand Evolution Manager          ║
╚════════════════════════════════════════╝

Loading Guardian metrics from: guardian-uncertainty.json

Current DNA Strand: FLM2-CMD4-MESH5-ORB1
FLM2 Compiler Health:
  p_success = 0.960
  entropy   = 0.250

✓ Mutation suggested: FLM2-CMD4-MESH5-ORB1 → FLM2.1-CMD4-MESH5-ORB1
  Reason: p_success >= 0.95 and entropy < 0.3

Updating sagco_unified_spec.yaml...
✓ DNA strand updated successfully!
```

## Pipeline Workflow

### Complete Flow

1. **Run FlameBench** (produces guardian-uncertainty.json)
   ```bash
   cd /path/to/flamebench
   python flamebench.py
   ```

2. **Check mesh health**
   ```bash
   python3 tools/sagco-mesh.py
   ```

3. **Analyze with Oracle** (optional)
   ```bash
   cargo run -p sagco-guardian --bin sagco-oracle "Sample text"
   ```

4. **Run DNA evolution**
   ```bash
   cargo run -p sagco-dna
   ```

### Expected File Locations

**Windows:**
- Guardian export: `E:\FlameBench\guardian-uncertainty.json`
- DNA spec: `E:\Strategickhaos\sagco-os\sagco_unified_spec.yaml`

**Linux/Alpine:**
- Guardian export: `/opt/flamebench/guardian-uncertainty.json`
- DNA spec: `/opt/sagco-os/sagco_unified_spec.yaml`

## Guardian Export Format

The Guardian uncertainty export (`guardian-uncertainty.json`) should have this structure:

```json
{
  "source": "flamebench",
  "dna_strand": "FLM2-CMD4-MESH5-ORB1",
  "uncertainties": [
    {
      "tag": "if-else",
      "p_correct": 0.96,
      "entropy": 0.25,
      "alpha": 48.0,
      "beta": 2.0,
      "sample_size": 50
    },
    {
      "tag": "loop",
      "p_correct": 0.94,
      "entropy": 0.28,
      "alpha": 47.0,
      "beta": 3.0,
      "sample_size": 50
    }
  ],
  "overall": {
    "p_success": 0.95,
    "entropy": 0.30
  }
}
```

## Building

### Build all components
```bash
# Build Guardian (includes sagco-oracle)
cargo build -p sagco-guardian --release

# Build Kernel
cargo build -p sagco-kernel --release

# Build sagco-dna
cargo build -p sagco-dna --release
```

### Run tests
```bash
cargo test -p sagco-guardian
cargo test -p sagco-kernel
```

## Integration with Hypervisor

The SAGCO OS pipeline integrates with the Type-1 hypervisor (HYDRA):

1. **Boot sequence**: Bootloader → Long mode → HYDRA init
2. **Guest startup**: Alpine boots → sagco-init mounts overlays
3. **Automatic checks**: sagco-init runs sagco-status, sagco-mesh, sagco-dna
4. **Neural tick**: 100 Hz timer interrupt for neural processing
5. **Mesh monitoring**: Continuous health checks via sagco-mesh

## Dependencies

### Rust crates
- `serde`, `serde_json`, `serde_yaml` - Serialization
- `anyhow` - Error handling
- `regex` - DNA parsing

### Python packages
- `pyyaml` - YAML parsing for mesh hosts

Install with:
```bash
pip install pyyaml
```

## Development

### Adding a new mesh node

1. Create `mesh/hosts/newnode.yaml`:
```yaml
name: NEWNODE
role: worker
ip: 192.168.1.53
os: "Ubuntu 22.04"
cpu: "Intel i5"
ram_gb: 16
tags: ["mesh", "worker"]
```

2. Run sagco-mesh to verify:
```bash
python3 tools/sagco-mesh.py
```

3. If verified, suggest MESH mutation:
```rust
suggest_mesh_mutation("FLM2-CMD4-MESH5-ORB1", true)
// Returns: "FLM2-CMD4-MESH6-ORB1"
```

## License

See LICENSE file in repository root.

## Authors

StrategicKhaos - SAGCO OS Architecture

---

**Production-Hypervisor-Ready** ✓  
**Dom0 Micromanaged Mode** ✓  
**Not Vibes** ✓
