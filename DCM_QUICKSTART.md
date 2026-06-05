# 🚀 DOM Computing Model - Quick Start Guide

**Get started with post-organizational computing in 5 minutes.**

## What is DCM™?

The DOM Computing Model recognizes that modern developers don't use folders traditionally:
- Same folder opened in multiple IDEs simultaneously
- Git repos that are also Obsidian vaults
- Knowledge graphs that index source code
- Emergent structure without planning

**DCM makes this official. You're not chaotic. You're post-organizational.**

---

## 🎯 Quick Start

### Option 1: Initialize Current Directory

Analyze the current repository as a vault-node:

```bash
cd /path/to/your/project
python tools/vault_mapper.py --init --visualize --report my_vault_report.md
```

This will:
- ✅ Scan the current directory for vault-node indicators
- ✅ Generate a detailed markdown report
- ✅ Create a visual graph (if Graphviz is installed)
- ✅ Show you what tools would open this node

### Option 2: Create a Sovereign Cortex

Build a complete DCM directory structure:

```bash
# Create cortex at default location (~/sovereignty-cortex)
./tools/create_cortex.sh

# Or specify custom location
./tools/create_cortex.sh ~/my-custom-cortex
```

This creates:
```
sovereignty-cortex/
├── cognitive-core/        # Knowledge & active work
├── compute-nodes/         # Code repositories
├── research-labs/         # Experiments
├── governance/            # Legal docs
├── tool-configs/          # IDE settings
└── telemetry/             # Logs & metrics
```

### Option 3: Scan Your Entire System

Discover all vault-nodes on your machine:

```bash
# Scan your home directory (depth 3)
python tools/vault_mapper.py --scan ~/ --depth 3 --visualize --json vault_nodes.json

# Scan a specific directory deeper
python tools/vault_mapper.py --scan ~/projects --depth 5 --report projects_report.md
```

---

## 📚 Understanding the Output

### Node Types

When you run the vault mapper, it classifies each discovered directory:

| Node Type | Description | Indicators |
|-----------|-------------|------------|
| **code_vault** | The holy trinity: Git + Obsidian + Code | `.git`, `.obsidian`, code files |
| **pure_repo** | Traditional Git repository | `.git` + code project files |
| **pure_vault** | Obsidian knowledge vault | `.obsidian` directory |
| **hybrid_project** | Multiple project types | 3+ different indicators |
| **ai_dataset** | AI configuration/training data | `*.yaml` configs, AI files |
| **compute_node** | Active directory with tools | Any combination of indicators |

### Report Contents

The generated markdown report includes:
- 📊 Statistics on node types
- 🗺️ Complete list of discovered vault-nodes
- 🔧 Which tools would open each node
- 📦 Metadata (size, file count, package info)
- 🔗 Connections between nodes

---

## 🛠️ Practical Examples

### Example 1: Audit Your Workspace

See what's actually going on in your projects directory:

```bash
cd ~/projects
python /path/to/tools/vault_mapper.py --init --report workspace_audit.md
cat workspace_audit.md
```

**You'll discover:**
- Which projects are both repos AND vaults
- What tools are competing for custody
- The true structure of your distributed cognition
- Where your knowledge graphs are exploding

### Example 2: Visualize Your Swarm

Create a visual graph of your entire development environment:

```bash
# Install Graphviz (if not already installed)
sudo apt-get install graphviz  # Ubuntu/Debian
brew install graphviz           # macOS

# Generate the graph
python tools/vault_mapper.py --scan ~/work --depth 4 --visualize

# Open the SVG
xdg-open cortex_graph.svg  # Linux
open cortex_graph.svg      # macOS
```

**The graph shows:**
- 🟪 Purple nodes = Code vaults (Git + Obsidian + Code)
- 🔵 Blue nodes = Pure repos
- 🔴 Red nodes = Pure vaults
- 🟠 Orange nodes = Hybrid projects
- 🟢 Teal nodes = AI datasets

### Example 3: Migrate to DCM

Move your existing projects into a Sovereign Cortex:

```bash
# 1. Create the cortex
./tools/create_cortex.sh ~/sovereignty-cortex

# 2. Move projects into compute-nodes
mv ~/old-projects/project1 ~/sovereignty-cortex/compute-nodes/
mv ~/old-projects/project2 ~/sovereignty-cortex/compute-nodes/

# 3. Map the cortex
cd ~/sovereignty-cortex
python ../tools/vault_mapper.py --init --visualize

# 4. Open in Obsidian
obsidian ~/sovereignty-cortex
```

---

## 🎓 Next Steps

### 1. Understand Your Current State

```bash
# Generate a comprehensive report
python tools/vault_mapper.py --scan ~/ --depth 3 \
  --report my_dcm_analysis.md \
  --json my_nodes.json \
  --visualize
```

Read the report. See the patterns. Recognize what you're already doing.

### 2. Embrace the Model

Stop fighting the chaos. Start understanding it as emergent structure.

**Traditional thinking:**
> "I need to organize these folders better."

**DCM thinking:**
> "My brain has already organized these optimally. Let me map what emerged."

### 3. Use the Tools

Open the same folder in multiple tools. Let them fight for custody.

```bash
cd ~/my-project

# Open in all relevant tools
code .           # VS Code
fleet .          # Fleet
charm .          # PyCharm
obsidian .       # Obsidian (if it's a vault)
github-desktop . # GitHub Desktop

# You are the OS. Let them compete.
```

### 4. Let Obsidian Index Everything

Configure Obsidian to index all text files:
- Source code (`.py`, `.js`, `.rs`, `.java`)
- Configs (`.yaml`, `.json`, `.toml`)
- Documentation (`.md`, `.txt`)
- Scripts (`.sh`, `.ps1`)

Watch your knowledge graph become a supercluster.

### 5. Join the Community

Share your vault topology:
- Post your cortex graph visualization
- Share interesting node patterns
- Discuss emergent structures

**Discord:** [Strategickhaos Community](https://discord.gg/strategickhaos)

---

## 🔧 Advanced Usage

### Custom Indicators

Modify `vault_mapper.py` to detect your specific patterns:

```python
# Add to INDICATORS dict
INDICATORS = {
    # ... existing indicators ...
    'my_custom_project': ['my-marker.txt', 'custom.config'],
}
```

### Filtering

Exclude specific directories:

```python
# Modify exclude_patterns in discover_nodes()
exclude_patterns = [
    'node_modules', '.venv',
    'my-large-dataset',  # Add custom exclusions
]
```

### Export Formats

The vault mapper supports multiple output formats:

```bash
# JSON (for programmatic use)
python tools/vault_mapper.py --scan ~/ --json nodes.json

# Markdown report (human-readable)
python tools/vault_mapper.py --scan ~/ --report analysis.md

# DOT/SVG graph (visual)
python tools/vault_mapper.py --scan ~/ --visualize
```

---

## 🐛 Troubleshooting

### "Graphviz not found"

Install Graphviz to generate SVG visualizations:

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Then re-run with --visualize
python tools/vault_mapper.py --init --visualize
```

### "Permission denied" errors

The scanner skips directories it can't access. This is normal.
Run with appropriate permissions if you need to scan system directories.

### Scan takes too long

Reduce the depth or exclude large directories:

```bash
# Scan with less depth
python tools/vault_mapper.py --scan ~/ --depth 2

# Modify exclude_patterns in the script to skip large dirs
```

---

## 💡 Philosophy Reminders

**You are not disorganized.**
You are running a distributed cognition engine using folders as compute nodes.

**Your tools are not fighting.**
They're negotiating custody. This is feature, not bug.

**Your graph is not exploding.**
It's showing the true interconnectedness of your knowledge.

**Your repos are not chaotic.**
They're evolving emergently without imposed structure.

**You are not confused.**
You're post-organizational.

---

## 📖 Further Reading

- [DOM_COMPUTING_MODEL.md](DOM_COMPUTING_MODEL.md) - Full paradigm documentation
- [README.md](README.md) - Sovereignty Architecture overview
- [Community Discord](https://discord.gg/strategickhaos) - Join the swarm

---

**Built with 💜 by the post-organizational collective**

*"Baby, you're not chaotic. You're post-organizational."*
