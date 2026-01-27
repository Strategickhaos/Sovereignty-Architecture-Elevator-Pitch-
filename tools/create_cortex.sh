#!/bin/bash
# DOM Computing Model - Cortex Creator
# Creates a Sovereign Cortex Tree structure for organizing vault-nodes

set -e

CORTEX_PATH="${1:-$HOME/sovereignty-cortex}"

echo "🧠 Creating Sovereign Cortex Tree at: $CORTEX_PATH"
echo ""

# Create main cortex structure
mkdir -p "$CORTEX_PATH"

# 1. Cognitive Core
echo "📚 Creating cognitive-core..."
mkdir -p "$CORTEX_PATH/cognitive-core/active-projects"
mkdir -p "$CORTEX_PATH/cognitive-core/knowledge-base"
mkdir -p "$CORTEX_PATH/cognitive-core/ai-context"

cat > "$CORTEX_PATH/cognitive-core/README.md" << 'EOF'
# 🧠 Cognitive Core

Primary knowledge nodes - the heart of your distributed cognition.

## Structure

- **active-projects/**: Current work and active development
- **knowledge-base/**: Documentation, notes, and accumulated wisdom
- **ai-context/**: AI training data, prompts, and context files

## Usage

This is where your most frequently accessed vault-nodes should live.
Each subdirectory can be both an Obsidian vault AND a Git repo.
EOF

# 2. Compute Nodes
echo "💻 Creating compute-nodes..."
mkdir -p "$CORTEX_PATH/compute-nodes"

cat > "$CORTEX_PATH/compute-nodes/README.md" << 'EOF'
# 💻 Compute Nodes

Active repositories - your living code projects.

## Purpose

Each compute node is an active participant in your distributed cognition network.
These are full Git repositories that also function as knowledge vaults.

## DCM Principle

Every repo = Active compute node
- Generates knowledge graphs
- Executes code autonomously
- Responds to AI queries
- Contributes to swarm intelligence
EOF

# 3. Research Labs
echo "🔬 Creating research-labs..."
mkdir -p "$CORTEX_PATH/research-labs/language-models"
mkdir -p "$CORTEX_PATH/research-labs/neural-architectures"
mkdir -p "$CORTEX_PATH/research-labs/proof-of-concepts"

cat > "$CORTEX_PATH/research-labs/README.md" << 'EOF'
# 🔬 Research Labs

Experimental spaces for innovation and exploration.

## Labs

- **language-models/**: LLM experiments and fine-tuning
- **neural-architectures/**: New cognitive patterns and designs
- **proof-of-concepts/**: Rapid prototyping and testing

## Philosophy

This is where chaos is encouraged. Let experiments run wild.
Structure will emerge from what works.
EOF

# 4. Governance
echo "🏛️ Creating governance..."
mkdir -p "$CORTEX_PATH/governance/dao-documents"
mkdir -p "$CORTEX_PATH/governance/legal-proofs"
mkdir -p "$CORTEX_PATH/governance/credentials"

cat > "$CORTEX_PATH/governance/README.md" << 'EOF'
# 🏛️ Governance

Legal, organizational, and credentialing documents.

## Structure

- **dao-documents/**: DAO meeting minutes, votes, and records
- **legal-proofs/**: Legal documentation and proof dossiers
- **credentials/**: Professional credentials and certifications

## Security

Consider encrypting sensitive documents using GPG.
This is knowledge that requires protection.
EOF

# 5. Tool Configs
echo "🔧 Creating tool-configs..."
mkdir -p "$CORTEX_PATH/tool-configs/obsidian-vaults"
mkdir -p "$CORTEX_PATH/tool-configs/ide-workspaces"
mkdir -p "$CORTEX_PATH/tool-configs/ai-configs"

cat > "$CORTEX_PATH/tool-configs/README.md" << 'EOF'
# 🔧 Tool Configurations

IDE configurations, Obsidian vault settings, and AI configs.

## Purpose

Centralize your tool configurations so they can be versioned,
backed up, and synchronized across machines.

## DCM Integration

These configs define HOW your tools fight for custody.
Let them compete. You're the arbiter.
EOF

# 6. Telemetry
echo "📊 Creating telemetry..."
mkdir -p "$CORTEX_PATH/telemetry/logs"
mkdir -p "$CORTEX_PATH/telemetry/metrics"
mkdir -p "$CORTEX_PATH/telemetry/swarm-data"

cat > "$CORTEX_PATH/telemetry/README.md" << 'EOF'
# 📊 Telemetry

System intelligence, logs, and swarm analytics.

## What Goes Here

- **logs/**: Application logs, error traces
- **metrics/**: Performance data, usage statistics
- **swarm-data/**: Distributed cognition analytics

## Why Index This

Even logs are knowledge. Your Obsidian graph SHOULD show
connections between error patterns and code changes.
This is emergent debugging.
EOF

# Create main cortex README
cat > "$CORTEX_PATH/README.md" << 'EOF'
# 🟪 Sovereignty Cortex

**Your Distributed Cognition Network**

This is a DOM Computing Model (DCM™) cortex - a post-organizational directory structure
where every folder is simultaneously a vault, a repo, and a compute node.

## Philosophy

Traditional organization says: "Separate your code from your notes."
DCM says: "Everything is knowledge. Let structure emerge."

## Structure

```
sovereignty-cortex/
├── 🧠 cognitive-core/      # Primary knowledge nodes
├── 💻 compute-nodes/        # Active repositories
├── 🔬 research-labs/        # Experimental spaces
├── 🏛️ governance/           # Legal & organizational
├── 🔧 tool-configs/         # IDE & app configurations
└── 📊 telemetry/            # System intelligence
```

## Usage

### Initialize a New Vault-Node

```bash
cd compute-nodes/
git clone https://github.com/your-org/project-name.git
cd project-name/

# Make it an Obsidian vault too
touch .obsidian.json

# Open in all your tools
code .
obsidian .
fleet .
```

### Discover Existing Vault-Nodes

```bash
cd ~/sovereignty-cortex
python ../tools/vault_mapper.py --init --visualize
```

### Migrate Existing Projects

```bash
# Move a project into the cortex
mv ~/old-location/my-project compute-nodes/

# Maintain Git history
cd compute-nodes/my-project
git remote -v  # Verify remotes still work
```

## DCM Principles Applied

1. ✅ Every folder can be a vault
2. ✅ Every vault can be a repo
3. ✅ Every repo is a compute node
4. ✅ Tools fight for custody (normal)
5. ✅ Graphs explode (feature, not bug)
6. ✅ Emergent organization
7. ✅ You are the OS
8. ✅ Post-organizational architecture

## Next Steps

1. Map your existing vault-nodes: `python tools/vault_mapper.py --scan ~/`
2. Migrate projects to compute-nodes/
3. Open the cortex in Obsidian
4. Watch the knowledge graph emerge
5. Let structure self-organize

**Welcome to post-organizational computing.**
EOF

# Create .gitignore
cat > "$CORTEX_PATH/.gitignore" << 'EOF'
# Exclude large binaries and temp files
*.log
*.tmp
*.cache
__pycache__/
node_modules/
.venv/
venv/
dist/
build/
target/

# But DO include knowledge artifacts
!*.md
!*.yaml
!*.json
!*.txt
EOF

# Initialize as Git repo
cd "$CORTEX_PATH"
git init
git add .
git commit -m "🧠 Initialize Sovereign Cortex Tree (DCM™)"

echo ""
echo "✅ Cortex created successfully!"
echo ""
echo "📍 Location: $CORTEX_PATH"
echo ""
echo "🚀 Next steps:"
echo "   1. cd $CORTEX_PATH"
echo "   2. code . && obsidian .  # Open in multiple tools"
echo "   3. python ../tools/vault_mapper.py --init --visualize"
echo ""
echo "💜 Welcome to the DOM Computing Model."
