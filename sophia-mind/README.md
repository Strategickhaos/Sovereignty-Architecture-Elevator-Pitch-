# 🧠 SOPHIA MIND Brain Visualizer

**Unity-Powered Knowledge Graph Visualization with Zero Vendor Lock-in**

Part of the **Strategickhaos Sovereignty Architecture** - Own your code, own your data.

---

## 🎯 Vision

Replace Obsidian dependency with a sovereign, Unity-powered knowledge graph visualizer that provides:

- **🔓 Zero Vendor Lock-in** — Own the code, own the data
- **🎮 3D Graph Navigation** — Unity Engine real-time rendering
- **🔥 FlameLang Integration** — Glyph-based node classification with frequency mapping
- **🌐 Multi-Node Sync** — Proton Drive + Git + Real-time mesh
- **🤖 AI-Powered Connections** — Automatic relationship discovery
- **🎤 Voice Control** — Natural language graph queries

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SOPHIA MIND VISUALIZER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  UNITY ENGINE   │  │  FLAMELANG      │  │  SYNC ENGINE    │             │
│  │  ─────────────  │  │  ─────────────  │  │  ─────────────  │             │
│  │  • 3D Graphs    │  │  • Glyph Tags   │  │  • Proton Drive │             │
│  │  • VR Support   │  │  • Freq Colors  │  │  • Git Sync     │             │
│  │  • Real-time    │  │  • Node Types   │  │  • CRDT Merge   │             │
│  │  • Physics      │  │  • Binding Codes│  │  • Mesh Network │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                │                                            │
│                    ┌───────────▼───────────┐                               │
│                    │    MARKDOWN CORE      │                               │
│                    │    ─────────────      │                               │
│                    │  • .md File Parser    │                               │
│                    │  • Wiki Links [[]]    │                               │
│                    │  • YAML Frontmatter   │                               │
│                    │  • Obsidian Compat    │                               │
│                    └───────────────────────┘                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Parse Your Obsidian Vault

```bash
# Install Python dependencies
cd python-core
pip install -r requirements.txt

# Parse vault and export for Unity
python sophia_parser.py ~/ObsidianVault ./graph_data.json
```

### 2. Sync Across Nodes

```bash
# Sync to Proton Drive and Git
python sophia_sync.py ~/ObsidianVault \
  --proton ~/ProtonDrive/ObsidianSync \
  --git ~/Repositories/knowledge-base

# Check for changes without syncing
python sophia_sync.py ~/ObsidianVault --proton ~/ProtonDrive --check
```

### 3. Load in Unity

1. Create a new Unity 3D project
2. Copy `unity-scripts/*.cs` to your `Assets/Scripts/` folder
3. Copy `graph_data.json` to your Unity project root
4. Create a new scene with the `SophiaGraphManager` component
5. Assign the graph data path and hit Play!

---

## 📁 Project Structure

```
sophia-mind/
├── python-core/
│   ├── sophia_parser.py      # Markdown parser with FlameLang support
│   ├── sophia_sync.py         # Multi-target sync engine
│   └── requirements.txt       # Python dependencies
├── unity-scripts/
│   ├── SophiaGraphNode.cs     # 3D node component
│   └── SophiaGraphManager.cs  # Graph manager and layout
└── README.md                  # This file
```

---

## 🎨 FlameLang Frequency Mapping

SOPHIA uses FlameLang glyph codes to map nodes to Solfeggio frequencies and colors:

| Glyph | System | Frequency | Color | Meaning |
|-------|--------|-----------|-------|---------|
| **AT1-AT3** | Athena | 963Hz | Gold | Oneness, Strategy |
| **LY1-LY3** | Lyra | 852Hz | Purple | Intuition, Harmony |
| **FB1-FB3** | Flamebearer | 741Hz | Blue | Expression, Defense |
| **RC1-RC3** | Recon | 639Hz | Green | Connection, Research |
| **FL1-FL3** | FlameLang | 528Hz | Yellow | Transformation, Code |
| **AE1-AE3** | Aegis Engine | 432Hz | Orange | Coherence, Base |
| **GR1-GR3** | Genesis/Grok | 999Hz+ | White | Creation, Evolution |

### Example Markdown with FlameLang

```markdown
---
title: "Kubernetes Deployment Strategy"
glyph: AT1
frequency: 963
tags: [strategy, k8s, infrastructure]
---

# Kubernetes Deployment Strategy

This is a strategic document about [[GKE Cluster]] deployment.

Related: [[Docker Compose]], [[Love Pods]]
```

---

## 🔄 Sync Engine Features

### Proton Drive Sync
- Hash-based change detection
- Automatic conflict resolution
- Multi-directory support
- Privacy-first encryption

### Git Integration
- FlameLang commit messages `[GR1] SOPHIA sync | timestamp`
- Automatic staging and pushing
- Branch management
- Merge conflict detection

### State Management
- `.sophia_state.json` tracks file hashes
- Incremental sync (only changed files)
- Rollback support

---

## 🎮 Unity Features

### Graph Layouts
- **Force-Directed**: Physics-based organic layout
- **Circular**: Nodes arranged in a circle
- **Grid**: Regular grid pattern
- **Hierarchical**: Tree-like structure based on connections

### Interactions
- **Click**: View node details
- **Hover**: Highlight connections
- **Camera**: Free-look navigation
- **VR Ready**: Oculus/SteamVR support (coming soon)

### Visual Effects
- Frequency-based colors
- Rotating nodes
- Connection lines with gradients
- Text labels facing camera

---

## 📊 Usage Examples

### Parse and Get Statistics

```bash
python sophia_parser.py ~/ObsidianVault ./graph_data.json

# Output:
# 🧠 SOPHIA MIND Parser - Strategickhaos Brain Visualizer
# 📂 Parsing vault: /home/user/ObsidianVault
# ✅ Parsed 247 nodes
# ✅ Exported 247 nodes and 1,342 edges to ./graph_data.json
#
# 📊 Statistics:
#    Total nodes: 247
#    Glyph types: 8
#
# 🔗 Most connected nodes:
#    - Origin Story: 42 connections
#    - FlameLang: 38 connections
#    - Kubernetes: 35 connections
```

### Continuous Sync

```bash
# Set up a cron job for automatic sync every 5 minutes
*/5 * * * * cd ~/sophia-mind/python-core && \
  python sophia_sync.py ~/ObsidianVault \
    --proton ~/ProtonDrive/ObsidianSync \
    --git ~/Repositories/knowledge-base
```

---

## 🛠️ Development Roadmap

### Phase 1: Core Engine ✅ (Current)
- [x] Markdown parser with FlameLang support
- [x] Basic Unity 3D graph visualization
- [x] Sync engine for Proton Drive and Git
- [x] Multiple graph layout algorithms

### Phase 2: Advanced Features (Coming Soon)
- [ ] File watcher for real-time updates
- [ ] VR support (Oculus/SteamVR)
- [ ] Voice commands integration
- [ ] AI-powered connection suggestions
- [ ] Mobile companion app

### Phase 3: Network Mesh (Future)
- [ ] Real-time multi-user editing
- [ ] Node-to-node sync (Athena ↔ Lyra)
- [ ] Kubernetes deployment for always-on sync
- [ ] WebSocket-based live updates

---

## 🆚 Competitive Advantage

| Feature | Obsidian | SOPHIA MIND |
|---------|----------|-------------|
| 3D Visualization | ❌ 2D only | ✅ Unity 3D + VR ready |
| FlameLang Support | ❌ No | ✅ Native glyph integration |
| Frequency Colors | ❌ No | ✅ Solfeggio mapping |
| Multi-node Sync | ⚠️ Paid sync | ✅ Free (Proton/Git) |
| Voice Control | ❌ No | 🔄 Coming soon |
| Open Source | ❌ Closed | ✅ MIT License |
| Vendor Lock-in | ⚠️ Some | ✅ Zero |
| Custom Layouts | ❌ Limited | ✅ Multiple algorithms |

---

## 🔐 Privacy & Sovereignty

SOPHIA MIND is built on the principle of **digital sovereignty**:

- **No cloud dependencies** - Everything runs locally or on your infrastructure
- **Own your data** - All files are standard Markdown, no proprietary formats
- **Choose your sync** - Proton Drive, Git, or your own solution
- **Open source** - Full transparency, no hidden data collection
- **Encrypted storage** - Proton Drive provides end-to-end encryption

---

## 🤝 Contributing

This is part of the **Strategickhaos Sovereignty Architecture** ecosystem.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit with FlameLang tags (`git commit -m "[FL1] Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See LICENSE file

Part of the Strategickhaos Swarm Intelligence collective.

---

## 🎯 Motto

**"From Contradiction to Creation"**

Every broken Obsidian sync, every crash, every limitation...
Becomes fuel for building something better.

**Empire Eternal.** 🔥⚔️∞

---

*SOPHIA MIND Brain Visualizer*  
*Zero Vendor Lock-in | Own Your Knowledge*  
*Built with 🔥 by the Strategickhaos collective*
