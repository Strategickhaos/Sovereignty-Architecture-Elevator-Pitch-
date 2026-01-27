# 🔧 DOM Computing Model - Tools

This directory contains the tools for implementing and working with the DOM Computing Model (DCM™).

## Available Tools

### 1. `vault_mapper.py` - Vault-Node Discovery & Mapping

The primary tool for discovering and analyzing your distributed cognition network.

**Features:**
- Recursively scans directories to find vault-nodes
- Classifies nodes by type (code_vault, pure_repo, pure_vault, etc.)
- Generates comprehensive markdown reports
- Exports to JSON for programmatic use
- Creates visual graphs (with Graphviz)

**Usage:**

```bash
# Scan current directory
python vault_mapper.py --init --report my_report.md

# Scan a specific directory with visualization
python vault_mapper.py --scan ~/projects --depth 4 --visualize

# Full analysis with all outputs
python vault_mapper.py --scan ~/ --depth 3 \
  --report vault_analysis.md \
  --json vault_data.json \
  --visualize
```

**Options:**
- `--scan PATH`: Root directory to scan (e.g., `~/` or `~/projects`)
- `--depth N`: Maximum recursion depth (default: 3)
- `--init`: Scan current directory
- `--visualize`: Generate visual graph (requires Graphviz)
- `--report FILE`: Output markdown report (default: `vault_map_report.md`)
- `--json FILE`: Export nodes to JSON

**Output Types:**

1. **Markdown Report** (`vault_map_report.md`)
   - Statistics on node types
   - Complete list of discovered nodes
   - Tool associations and metadata

2. **JSON Export** (`vault_nodes.json`)
   - Structured data for programmatic use
   - Complete node information
   - Scan metadata

3. **Visual Graph** (`cortex_graph.svg`)
   - Node type color coding
   - Relationship visualization
   - Requires Graphviz: `apt-get install graphviz`

### 2. `create_cortex.sh` - Sovereign Cortex Creator

Creates a complete Sovereign Cortex Tree structure.

**Features:**
- Builds recommended DCM directory structure
- Creates README files for each section
- Initializes as Git repository
- Sets up .gitignore

**Usage:**

```bash
# Create at default location (~/sovereignty-cortex)
./create_cortex.sh

# Create at custom location
./create_cortex.sh ~/my-custom-cortex

# Then navigate and explore
cd ~/sovereignty-cortex
code . && obsidian .
```

**Structure Created:**
```
sovereignty-cortex/
├── cognitive-core/        # Primary knowledge nodes
│   ├── active-projects/
│   ├── knowledge-base/
│   └── ai-context/
├── compute-nodes/         # Active repositories
├── research-labs/         # Experimental spaces
│   ├── language-models/
│   ├── neural-architectures/
│   └── proof-of-concepts/
├── governance/            # Legal & organizational
│   ├── dao-documents/
│   ├── legal-proofs/
│   └── credentials/
├── tool-configs/          # IDE configurations
│   ├── obsidian-vaults/
│   ├── ide-workspaces/
│   └── ai-configs/
└── telemetry/             # System intelligence
    ├── logs/
    ├── metrics/
    └── swarm-data/
```

## Node Types

The vault mapper classifies directories into these types:

| Type | Description | Indicators |
|------|-------------|------------|
| **code_vault** | Git + Obsidian + Code (holy trinity) | `.git`, `.obsidian`, code files |
| **pure_repo** | Traditional Git repository | `.git` + project files |
| **pure_vault** | Obsidian knowledge vault | `.obsidian` directory |
| **hybrid_project** | Multiple project types | 3+ indicators |
| **ai_dataset** | AI configuration/training data | `*.yaml` AI configs |
| **compute_node** | Active compute node | Any combination |

## Installation

These tools require Python 3.6+ (already available on most systems).

**Optional: Install Graphviz for visualizations**

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Fedora/RHEL
sudo dnf install graphviz
```

## Examples

### Example 1: Analyze Your Workspace

```bash
cd ~/projects
python /path/to/tools/vault_mapper.py --init --report workspace_analysis.md
cat workspace_analysis.md
```

### Example 2: Map Your Entire System

```bash
python tools/vault_mapper.py --scan ~/ --depth 3 \
  --report my_dcm_map.md \
  --json my_nodes.json \
  --visualize

# View the graph
xdg-open cortex_graph.svg  # Linux
open cortex_graph.svg      # macOS
```

### Example 3: Create and Populate Cortex

```bash
# Create cortex structure
./tools/create_cortex.sh ~/sovereignty-cortex

# Move projects into it
mv ~/old-projects/project1 ~/sovereignty-cortex/compute-nodes/

# Map the cortex
cd ~/sovereignty-cortex
python ../tools/vault_mapper.py --init --visualize

# Open in tools
code .
obsidian .
```

## Extending the Tools

### Add Custom Indicators

Edit `vault_mapper.py` to detect your specific patterns:

```python
INDICATORS = {
    # ... existing indicators ...
    'my_framework': ['my-config.yaml', 'my-marker.txt'],
}

TOOL_MAP = {
    # ... existing tools ...
    'my_framework': ['MyIDE', 'MyTool'],
}
```

### Custom Exclusions

Modify the `exclude_patterns` in `vault_mapper.py`:

```python
exclude_patterns = [
    'node_modules', '.venv',
    'my-large-dataset',  # Add your exclusions
    'archived-projects',
]
```

## Troubleshooting

### "Permission denied" Errors

The scanner skips directories it can't access. This is normal.
Run with sudo if you need to scan system directories (not recommended).

### Scan Takes Too Long

1. Reduce depth: `--depth 2`
2. Exclude large directories in the script
3. Scan specific directories instead of root

### Graphviz Not Found

Install Graphviz or use the DOT file directly:
```bash
# Install Graphviz
sudo apt-get install graphviz

# Or use online DOT viewer
# Copy cortex_graph.dot to: http://www.webgraphviz.com/
```

## Integration with Other Tools

### Use with Obsidian

1. Create cortex: `./create_cortex.sh`
2. Open in Obsidian: `obsidian ~/sovereignty-cortex`
3. Enable all file types in Obsidian settings
4. Watch your graph explode (this is good!)

### Use with VS Code

```bash
# Open cortex in VS Code
code ~/sovereignty-cortex

# Install recommended extensions:
# - Obsidian for VS Code
# - Git Graph
# - GitLens
```

### Export to CI/CD

```bash
# Generate JSON for CI analysis
python tools/vault_mapper.py --init --json vault_nodes.json

# Use in scripts
cat vault_nodes.json | jq '.nodes[] | select(.node_type == "code_vault")'
```

## Philosophy

These tools don't impose organization. They **discover** the organization that already exists in your distributed cognition network.

**Traditional tools say:**
> "Organize your files this way."

**DCM tools say:**
> "Here's what you're already doing. Let me map it."

---

## Further Reading

- [DOM Computing Model Documentation](../DOM_COMPUTING_MODEL.md)
- [Quick Start Guide](../DCM_QUICKSTART.md)
- [Main README](../README.md)

---

**Built with 💜 by the post-organizational collective**
