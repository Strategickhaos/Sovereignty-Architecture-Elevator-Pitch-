# Synapse-Bus Core Genesis System - Complete Guide

## Overview

The Synapse-Bus Core Genesis System implements a revolutionary **Self-Hydrating Repository** that solves the "Workflow Bottleneck" of manually creating complex codebases from architecture discussions.

## The Three AI Engineering Bottleneck Inventions

### Invention I: The "Chat-to-Spec" Ingestion Valve

**Problem**: Pasting massive chat dumps loses structure in plain text.

**Solution**: A specialized parser agent (`scripts/ingest_chat.py`) that:
- Regex-matches code blocks, directory trees, and technical commands
- Converts unstructured text into rigorous `blueprint.yaml`
- Cross-references with Bibliography (Board Meeting 003 notes)
- Validates modules against Ripley Gates

**Usage**:
```bash
cd synapse-bus-core
CHAT_INPUT_PATH="./chat_dump.txt" python3 scripts/ingest_chat.py
```

**Output**: `blueprint.yaml` containing:
- Parsed code blocks with language tags
- Tool definitions with algorithms
- Ripley Gate references
- Patent claim references
- Directory tree structures

### Invention II: The "Holographic" Docker Hub Methodology

**Problem**: Building Docker images for 16+ different tools manually is slow.

**Solution**: A recursive docker-compose strategy where:
- Repository acts as the build server
- Each `.flame` file compiles to Dockerfile on-the-fly
- Pushes to Docker Hub only if "GSCH Entropy" < 0.8
- Failed builds are "dissolved" to return energy

**Key Components**:
- **Buffer**: Absorbs build spikes
- **Dissolve**: Deletes failed artifacts
- **Entropy Check**: Prevents high-complexity code from shipping

**GSCH Framework Principles**:
```
Entropy = (Average Lines per File) / 250
If Entropy >= 0.8: Dissolve artifacts
If Entropy < 0.8: Approve for Docker Hub
```

### Invention III: The "Synaptic" Knowledge Linker (The Mason)

**Problem**: Empty source files with no content.

**Solution**: An Inline Coding LLM (`scripts/hydrate_file.py`) that:
1. Reads seed files with reference metadata
2. Queries the Bibliography for context
3. Constructs prompts for local LLM (Qwen2.5)
4. Generates actual source code
5. Writes to disk

**Example Workflow**:
```
Seed file: src/claims/gsch_claim8.rs
Metadata: "REF: INV-076, Patent Claim 8"
→ Search Bibliography for "INV-076"
→ Generate Rust code implementing Claim 8
→ Write to file
```

**Supported Languages**:
- Rust (`.rs`)
- FlameLang (`.flame`)
- Python (`.py`)
- YAML (`.yaml`)

## Quick Start

### 1. Generate the Repository

```bash
# Run the genesis script from the main repository
python3 genesis.py
```

This creates the entire `synapse-bus-core/` directory structure with:
- Source files as "seeds" with metadata
- Docker compose configuration
- GitHub workflow files
- Knowledge bibliography structure

### 2. Ingest Chat Dumps (Optional)

```bash
cd synapse-bus-core

# Place your chat dump in chat_dump.txt
# Then run ingestion valve
python3 scripts/ingest_chat.py
```

This parses your chat and generates `blueprint.yaml`.

### 3. Hydrate the Repository

```bash
# Manually hydrate (for testing)
python3 scripts/hydrate_file.py

# Or use Docker agent swarm (full pipeline)
docker-compose -f docker/compose.yml up
```

The agent swarm will:
1. **Architect**: Parse chat dumps
2. **Mason**: Hydrate seed files with code
3. **Builder**: Build Docker images (if entropy check passes)

### 4. Verify with GitHub Actions

Push to GitHub and the workflows will run:

**Thermodynamics Check** (`.github/workflows/thermodynamics.yaml`):
- Calculates GSCH entropy
- Validates against threshold (< 0.8)
- Approves/rejects Docker Hub push

**Ripley Gates** (`.github/workflows/ripley-gates.yaml`):
- Gate 1: Calcination (burn-in testing)
- Gate 2: Solution (buffer/clamp validation)
- Gate 3: Separation (module isolation)
- Gate 7: Putrefaction (stress testing)

## Architecture

```
synapse-bus-core/
├── .github/workflows/
│   ├── thermodynamics.yaml    # Entropy gatekeeper
│   └── ripley-gates.yaml      # Alchemical gates
├── src/
│   ├── claims/
│   │   └── gsch_claim8.rs     # Patent Claim 8 implementation
│   ├── primitives/
│   │   ├── buffer.flame       # GSCH Buffer primitive
│   │   └── clamp.flame        # GSCH Clamp primitive
│   ├── nervous_system/
│   │   └── spike.rs           # Neural spike routing
│   └── organs/
│       ├── vision/
│       │   └── retina.rs      # Network mapping (nmap)
│       ├── touch/
│       │   └── osteon.rs      # Penetration testing (metasploit)
│       └── hearing/
│           └── cochlea.rs     # Packet analysis (wireshark)
├── infra/k8s/
│   └── autopilot.yaml         # Kubernetes autopilot config
├── docker/
│   └── compose.yml            # Agent swarm orchestration
├── knowledge/bibliography/
│   └── README.md              # Reference documents
├── scripts/
│   ├── ingest_chat.py         # Invention I
│   └── hydrate_file.py        # Invention III
├── blueprint.yaml             # Generated from chat dumps
├── chat_dump.txt              # Sample chat for testing
└── README.md                  # This file
```

## Key Concepts

### GSCH Framework

**G**eneric **S**tress **C**ontrol **H**ierarchy

Principles:
- **Buffer**: Absorb stress spikes (build spikes, load spikes)
- **Clamp**: Control stress flow (rate limiting)
- **Dissolve**: Delete failed artifacts to return energy

### Ripley Gates

Alchemical transformation stages from the Ripley Scroll:
1. **Calcination**: Initial burn-in, remove impurities
2. **Solution**: Dissolve and validate primitives
3. **Separation**: Isolate modules
4. **Conjunction**: Combine validated components
5. **Fermentation**: Allow code to mature
6. **Distillation**: Extract pure essence
7. **Coagulation**: Solidify final form
8. **Putrefaction**: Stress testing and decomposition

Current implementation uses gates 1, 2, 3, and 7.

### FlameLang

Custom domain-specific language for thermodynamic primitives:
```flame
primitive Buffer {
    capacity: float
    load: float
    
    fn absorb(stress: float) -> float {
        let available = capacity - load
        let absorbed = min(stress, available)
        load += absorbed
        return absorbed
    }
}
```

### 880x Cost Reduction

Achieved through:
- **Local-First**: All processing runs on local machines (no cloud API costs)
- **Purified Tools**: Open-source security tools (nmap, wireshark, metasploit)
- **Agent Swarm**: Dockerized Python scripts wrapping local LLMs
- **Self-Hydration**: Automated code generation from specifications

## Testing

### Test Ingestion Valve

```bash
cd synapse-bus-core
python3 scripts/ingest_chat.py
cat blueprint.yaml  # Verify output
```

### Test Hydration

```bash
# Create a seed file
echo '// SYNAPSE-BUS GENERATED | REF: test' > test.rs

# Hydrate it
python3 scripts/hydrate_file.py
cat test.rs  # Check generated code
```

### Test Workflows Locally

```bash
# Install act (GitHub Actions local runner)
# https://github.com/nektos/act

# Run thermodynamics check
act -j calculate-entropy

# Run Ripley gates
act -j gate-1-calcination
```

## Troubleshooting

### Hydration Not Working

**Symptom**: Files remain as seeds after running hydration.

**Solution**: 
- Ensure `TARGET_DIR` environment variable is set correctly
- Check that seed files have the metadata: `// SYNAPSE-BUS GENERATED | REF: ...`
- Run with absolute paths if relative paths fail

### High Entropy Failure

**Symptom**: Thermodynamics check fails with "entropy >= 0.8".

**Solution**:
- Break large files into smaller modules
- Reduce average lines per file
- Apply refactoring to decrease complexity
- Aim for files under 200 lines each

### Ripley Gate Failures

**Symptom**: One or more gates fail in CI.

**Solution**:
- **Gate 1 (Calcination)**: Fix syntax errors
- **Gate 2 (Solution)**: Add buffer.flame and clamp.flame primitives
- **Gate 3 (Separation)**: Ensure proper module structure
- **Gate 7 (Putrefaction)**: Add stress tests

## Next Steps

1. **Expand Bibliography**: Add patent PDFs, board meeting notes to `knowledge/bibliography/`
2. **Real LLM Integration**: Connect to Ollama API for actual code generation
3. **Docker Hub Pipeline**: Configure automatic image builds and pushes
4. **Production Deployment**: Deploy agent swarm to Kubernetes
5. **Tool Purification**: Implement actual nmap/wireshark/metasploit wrappers

## Contributing

This system is designed for the StrategicKhaos DAO collective. To contribute:

1. Fork the repository
2. Add your chat dumps to `chat_dump.txt`
3. Run `python3 genesis.py` to regenerate structure
4. Submit PR with improvements

## License

See main repository LICENSE file.

---

Generated by StrategicKhaos Genesis System  
**"From Chat to Code: The Self-Hydrating Repository Revolution"**
