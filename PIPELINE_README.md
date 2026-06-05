# SAGCO Pipeline and Commands

This implementation provides the flamebench → Guardian → DNA mutation pipeline along with the `sagco-mesh` and `sagco-oracle` commands.

## Architecture Overview

```
flamebench → guardian-uncertainty.json → sagco-dna → DNA mutation
                    ↓
                sagco-oracle (analysis)
```

## Components

### 1. Guardian Crate (`guardian/`)

The Guardian crate provides uncertainty quantification and safety classification for AI outputs.

**Key Features:**
- Uncertainty measurement (p_correct, entropy, KL divergence)
- Geometric manifold mapping
- Safety classification (Safe, Caution, Warning, Critical)
- Benchmark ingestion from flamebench results

**Modules:**
- `lib.rs`: Core Guardian types and mapping logic
- `bench_ingest.rs`: Loads guardian-uncertainty.json files
- `bin/sagco_oracle.rs`: CLI tool for text analysis

### 2. Kernel Crate (`kernel/`)

The kernel crate implements DNA strand evolution based on performance metrics.

**Key Features:**
- DNA mutation logic for FLM, CMD, MESH, and ORB codons
- Threshold-based evolution rules
- YAML spec manipulation

**Modules:**
- `lib.rs`: Core kernel library
- `dna_mutation.rs`: Mutation algorithms
- `bin/sagco_dna.rs`: DNA evolution CLI tool

### 3. SAGCO Mesh (`mesh/`)

Network topology management and discovery.

**Structure:**
- `mesh/hosts/*.yaml`: Host definition files (athena, lyra, nova, ateroth, sagco-vm)
- Each host has: name, role, IP, OS, CPU, RAM, GPU, tags

### 4. Tools (`tools/`)

**sagco-mesh.py:**
- Scans all mesh nodes
- Checks connectivity (ping)
- Scans ports (SSH port 22, RDP port 3389)
- Displays topology table

## Usage

### Build

```bash
cargo build --release
```

Binaries will be in `target/release/`:
- `sagco-oracle`
- `sagco-dna`

### sagco-oracle

Analyze text inputs using Guardian uncertainty mapping:

```bash
# Via argument
./target/release/sagco-oracle "Test text to analyze"

# Via stdin
echo "AI generated content" | ./target/release/sagco-oracle

# With compiler health (requires guardian-uncertainty.json)
./target/release/sagco-oracle "Text to analyze"
```

**Output:**
- Uncertainty metrics (p_correct, entropy, KL divergence)
- Geometry point analysis (S, U, O values)
- Safety classification with recommendations
- Optional FLM2 compiler health (if guardian-uncertainty.json exists)

### sagco-dna

Evolve DNA strand based on compiler performance:

```bash
./target/release/sagco-dna
```

**Requirements:**
- `guardian-uncertainty.json` (from flamebench)
- `sagco_unified_spec.yaml` (DNA specification)

**Behavior:**
- Loads benchmark results
- Displays compiler health metrics
- Checks evolution thresholds
- Mutates DNA strand if thresholds met
- Updates sagco_unified_spec.yaml

**Evolution Rules:**
- FLM2 → FLM2.1: when p_success ≥ 0.95
- CMD1 → CMD2: when command_count ≥ 10
- MESH5 → MESH6: when node_count > 5
- ORB1 → ORB2: when safety_score ≥ 0.90

### sagco-mesh

Discover and monitor mesh topology:

```bash
python3 tools/sagco-mesh.py
```

**Output:**
- Scans all hosts in `mesh/hosts/*.yaml`
- Shows UP/DOWN status
- Lists available services (ssh, rdp)
- Summary statistics

## DNA Specification

The `sagco_unified_spec.yaml` file defines the DNA strand:

```yaml
DNA_Strand: FLM2-CMD1-MESH5-ORB1

codons:
  FLM2:
    name: "FlameLang Compiler v2"
    threshold_p_success: 0.95
  CMD1:
    name: "Command System v1"
  MESH5:
    name: "5-Node Mesh Topology"
  ORB1:
    name: "Oracle v1"
```

## Pipeline Flow

1. **FlameBench** runs compiler benchmarks
   - Outputs: `flamebench-results.json`
   
2. **Guardian** processes benchmarks
   - Creates: `guardian-uncertainty.json`
   - Contains concept uncertainties and overall stats
   
3. **sagco-dna** reads uncertainty data
   - Analyzes compiler health
   - Determines if mutation thresholds met
   - Updates DNA strand in `sagco_unified_spec.yaml`
   
4. **sagco-oracle** provides real-time analysis
   - Maps inputs to geometric manifold
   - Classifies safety level
   - Optionally shows compiler health

## Testing

Run tests:

```bash
cargo test
```

**Test Coverage:**
- Guardian uncertainty creation
- Safety classification
- Benchmark file loading
- DNA mutation logic (FLM, CMD, MESH, ORB)
- Threshold validation

## Example Workflow

```bash
# 1. Run flamebench (creates guardian-uncertainty.json)
# cd /path/to/flamebench
# python flamebench.py

# 2. Check compiler health and evolve DNA
cd /path/to/sagco-os
./target/release/sagco-dna

# 3. Analyze text with oracle
echo "AI output text" | ./target/release/sagco-oracle

# 4. Check mesh topology
python3 tools/sagco-mesh.py
```

## File Locations

**Default paths searched:**
- Guardian uncertainty: `guardian-uncertainty.json`, `flamebench/guardian-uncertainty.json`, `/tmp/guardian-uncertainty.json`
- DNA spec: `sagco_unified_spec.yaml`, `../sagco_unified_spec.yaml`, `/opt/sagco-os/sagco_unified_spec.yaml`
- Mesh hosts: `mesh/hosts/*.yaml`

## Dependencies

**Rust:**
- serde (serialization)
- serde_json (JSON parsing)
- serde_yaml (YAML parsing)
- anyhow (error handling)

**Python:**
- PyYAML (YAML parsing)
- Standard library (socket, subprocess, pathlib)

## Future Enhancements

From the problem statement, planned additions:
1. Hypervisor layer (HYDRA) for Type-1 virtualization
2. Alpine guest OS integration
3. Neural tick scheduling
4. Expanded mutation rules based on mesh health
5. Integration with MCP protocol
6. NFT receipts for evolution milestones
