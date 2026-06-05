# SynapseBus-Core Genesis System

## Overview

This repository implements the **Genesis Architecture** for SynapseBus-Core, solving the "Workflow Bottleneck" by creating a Self-Hydrating Repository System.

Instead of manually creating files, we deploy a Swarm of Agents (Dockerized Python scripts) that:
1. Read chat dumps
2. Parse the architecture
3. "Print" the directory tree into reality
4. Auto-generate code from knowledge bases

## Three AI Engineering Bottleneck Inventions

### Invention I: The "Chat-to-Spec" Ingestion Valve

**The Bottleneck**: Pasting massive chats loses structure in text.

**The Invention**: A specialized parser agent (`scripts/ingest_chat.py`) that:
- Regex-matches code blocks and directory trees
- Parses "Mad Scientist" commands
- Converts unstructured text into rigorous `blueprint.yaml`
- Cross-references Board Meeting 003 notes
- Maps modules to valid Ripley Gates

**Usage**:
```bash
python3 scripts/ingest_chat.py chat_dump.txt
```

### Invention II: The "Holographic" Docker Hub Methodology

**The Bottleneck**: Building Docker images for multiple tools manually is slow.

**The Invention**: A recursive docker-compose strategy where:
- Repository is the build server
- Each subdirectory contains `.flame` files
- "Inline LLM" compiles to Dockerfile on the fly
- Pushes to Docker Hub only if GSCH Entropy is low
- Applies GSCH Framework: "Buffer" (absorb build spikes) and "Dissolve" (delete failed artifacts)

**Workflow**: `.github/workflows/thermodynamics.yaml`

### Invention III: The "Synaptic" Knowledge Linker

**The Bottleneck**: Empty source files.

**The Invention**: An "Inline Coding LLM" (`scripts/hydrate_file.py`) that:
- Runs inside the directory
- Sees `src/claims/gsch_claim8.rs`
- Reads the filename and context reference
- Queries uploaded PDFs for "Claim 8"
- Auto-generates Rust struct based on patent definition

**Usage**:
```bash
cd synapse-bus-core
TARGET_DIR=. python3 ../scripts/hydrate_file.py
```

## The Master Generator: genesis.py

This is the Python script that acts as the repository source code tree generator.

**Usage**:
```bash
python3 genesis.py
```

This creates the entire ecosystem:
- Directory structure from YAML blueprint
- Seed files with references
- Docker Compose orchestration
- Supporting files (.gitignore, README)

## Quick Start

### 1. Generate the Repository Structure

```bash
python3 genesis.py
```

This creates the `synapse-bus-core/` directory with the full structure.

### 2. Hydrate with Code

```bash
cd synapse-bus-core
TARGET_DIR=. python3 ../scripts/hydrate_file.py
```

This populates seed files with actual code based on the knowledge base.

### 3. Run Agent Swarm (Optional)

```bash
cd synapse-bus-core
docker-compose up architect  # Parse chat dumps
docker-compose up mason      # Hydrate source files
docker-compose up builder    # Build containers
```

## GitHub Workflows

### Thermodynamics Workflow

File: `.github/workflows/thermodynamics.yaml`

This workflow is the "Gatekeeper" that prevents high-complexity code from entering Docker Hub:

- **Calculates entropy** based on cyclomatic complexity and maintainability
- **Validates threshold**: Entropy must be < 0.8
- **Blocks builds** if entropy exceeds threshold
- **Generates reports** with thermodynamic analysis

**Principles**:
- **Buffer**: Absorb complexity spikes through modular design
- **Dissolve**: Remove failed artifacts to return energy
- **Clamp**: Limit entropy growth through validation gates

### Ripley Gates Workflow

File: `.github/workflows/ripley-gates.yaml`

All code must pass through the 12 Ripley Gates (alchemical transformation stages):

1. **Calcination** - Initial compilation check
2. **Solution** - Integration testing (Buffer primitive)
3. **Separation** - Module isolation (Clamp primitive)
4. **Conjunction** - Component merging
5. **Putrefaction** - Security and entropy validation
6. **Congelation** - Freeze/stabilization
7. **Cibation** - Nourishment/enhancement
8. **Sublimation** - Purification
9. **Fermentation** - Active processing
10. **Exaltation** - Elevation/optimization
11. **Multiplication** - Scaling
12. **Projection** - Deployment

Currently implemented gates: 1, 2, 3, 5

## Directory Structure

```
synapse-bus-core/
├── .github/workflows/       # CI/CD workflows
│   ├── thermodynamics.yaml  # Entropy gatekeeper
│   └── ripley-gates.yaml    # Validation gates
├── src/                     # Source code
│   ├── claims/              # Patent claim implementations
│   ├── primitives/          # GSCH primitives (buffer, clamp)
│   ├── nervous_system/      # Neural processing
│   └── organs/              # Tool implementations
├── infra/                   # Infrastructure definitions
│   └── k8s/                 # Kubernetes configs
├── scripts/                 # Agent scripts
│   ├── ingest_chat.py       # Chat-to-Spec parser
│   └── hydrate_file.py      # Mason agent
├── knowledge/               # Knowledge base
│   └── bibliography/        # References (PDFs, notes)
├── docker-compose.yml       # Agent orchestration
└── README.md
```

## Generated Files

The genesis system generates:

1. **Seed files** - Placeholder files with context references
2. **Rust structs** - Based on patent claims (e.g., GSCH Claim 8)
3. **FlameLang modules** - Primitives with thermodynamic properties
4. **Kubernetes configs** - Infrastructure definitions
5. **Docker Compose** - Agent orchestration

## Knowledge Base

The Mason agent queries the knowledge base at `knowledge/bibliography/` for:

- Patent claims (INV-076, etc.)
- Board Meeting notes
- Ripley Gate definitions
- GSCH Framework principles
- Algorithm references

## GSCH Framework

The Gravitational Stress Channel Handling (GSCH) framework provides:

- **Buffer Primitive**: Absorb stress spikes
- **Clamp Primitive**: Limit stress range
- **Dissolve Pattern**: Remove failed components
- **Stress Routing**: Channel stress through proper primitives

## 880x Cost Reduction

The system implements "Local-First" patterns for massive cost reduction:

- Local LLM inference (Ollama/Qwen2.5)
- No external API calls during build
- Bibliography-driven code generation
- Cached knowledge base

## Contributing

1. Add chat dumps to parse
2. Update knowledge base in `knowledge/bibliography/`
3. Run genesis to regenerate structure
4. Run mason to hydrate files
5. Validate through Ripley Gates
6. Check thermodynamics before publishing

## License

Strategickhaos Sovereignty Architecture
