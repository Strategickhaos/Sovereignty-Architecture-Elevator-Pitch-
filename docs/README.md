# DOM Mapping Documentation Index

This directory contains comprehensive documentation for the DOM (Domain Object Model) Mapping with mathematical formulas connecting physics, biology, and infrastructure.

## 📚 Main Documents

### Core Formula Document
- **[DOM_MAPPING_MATHEMATICAL_FORMULAS.md](../DOM_MAPPING_MATHEMATICAL_FORMULAS.md)** - Complete mathematical formulas for all 9 levels with LaTeX equations

## 🔧 Integration Guides

### Obsidian Integration
- **[obsidian/README.md](obsidian/README.md)** - Vault setup and LaTeX configuration
- **[obsidian/Templates/level-template.md](obsidian/Templates/level-template.md)** - Template for creating level notes

### GraphView Visualization
- **[graphview/GRAPHVIEW_GUIDE.md](graphview/GRAPHVIEW_GUIDE.md)** - Power BI, Visio, and graph visualization tools
- **[graphview/MERMAID_DIAGRAMS.md](graphview/MERMAID_DIAGRAMS.md)** - Mermaid diagrams for markdown-based visualization
- **[graphview/dom-nodes.csv](graphview/dom-nodes.csv)** - Node data for graph import
- **[graphview/dom-edges.csv](graphview/dom-edges.csv)** - Edge data for graph import

## 📖 Quick Start

### For Obsidian Users
1. Read [obsidian/README.md](obsidian/README.md)
2. Import [DOM_MAPPING_MATHEMATICAL_FORMULAS.md](../DOM_MAPPING_MATHEMATICAL_FORMULAS.md) into your vault
3. Use provided templates to create individual level notes
4. Enable Math support in Settings → Editor

### For Power BI / Visio Users
1. Read [graphview/GRAPHVIEW_GUIDE.md](graphview/GRAPHVIEW_GUIDE.md)
2. Import CSV files from `graphview/` directory
3. Configure network graph visualization
4. Add formula tooltips and interactive filters

### For Markdown/GitHub Users
1. View [graphview/MERMAID_DIAGRAMS.md](graphview/MERMAID_DIAGRAMS.md)
2. Copy Mermaid code blocks into your documents
3. Diagrams render automatically in GitHub
4. Export to PNG/SVG using Mermaid CLI

## 🎯 DOM Levels Overview

| Level | Domain | Key Formula | Document Section |
|-------|--------|-------------|------------------|
| 1 | Subatomic → Signals | Schrödinger equation | Physics |
| 2 | Atomic → Compute | Ionization energy | Physics |
| 3 | Molecular → Code | Shannon entropy | Biology |
| 4 | Cellular → VMs | Logistic growth | Biology |
| 5 | Immune → Security | SIR model | Biology |
| 6 | Nervous → Network | Hodgkin-Huxley | Bio/Infra |
| 7 | Brain → Distribution | Asymmetry index | Bio/Infra |
| 8 | Ramanujan → Algorithms | Pi series | Mathematics |
| 9 | Blood → Data Flow | Hagen-Poiseuille | Physics |

## 🔗 Related Documentation

- [README.md](../README.md) - Main repository README
- [UNIFIED_SOVEREIGNTY_ARCHITECTURE(2).md](../UNIFIED_SOVEREIGNTY_ARCHITECTURE(2).md) - System architecture overview
- [OBSIDIAN_ARSENAL_COMPLETE.md](../OBSIDIAN_ARSENAL_COMPLETE.md) - Obsidian integration tools

## 🛠️ Tools & Dependencies

### For Viewing LaTeX
- Obsidian (with Math plugin)
- VS Code (with Markdown+Math extension)
- GitHub (native rendering)
- MathJax-enabled browsers

### For Creating Graphs
- Power BI Desktop
- Microsoft Visio
- Obsidian (with Excalidraw plugin)
- Mermaid CLI (`npm install -g @mermaid-js/mermaid-cli`)

### For Editing
- Any text editor
- LaTeX knowledge helpful but not required
- CSV editor for graph data

## 📝 Contributing

To add a new level or formula:
1. Update [DOM_MAPPING_MATHEMATICAL_FORMULAS.md](../DOM_MAPPING_MATHEMATICAL_FORMULAS.md)
2. Add nodes/edges to CSV files in `graphview/`
3. Create Mermaid diagram representation
4. Update this index

## 🔍 Search & Navigation

### Find Specific Formulas
```bash
# In repository root
grep -r "Schrödinger" docs/
grep -r "Hodgkin-Huxley" docs/
```

### List All LaTeX Blocks
```bash
grep -E '\$\$.*\$\$' DOM_MAPPING_MATHEMATICAL_FORMULAS.md
```

### Validate LaTeX Syntax
```bash
python3 -c "import re; content = open('DOM_MAPPING_MATHEMATICAL_FORMULAS.md').read(); print(f'Found {len(re.findall(r\"\\$\\$.*?\\$\\$\", content, re.DOTALL))} display blocks')"
```

## 📊 Statistics

- **Total Levels**: 9
- **LaTeX Display Blocks**: 23
- **LaTeX Inline Expressions**: 108+
- **Graph Nodes**: 27 (9 levels + 18 formula nodes)
- **Graph Edges**: 41 (sequential, analogy, cross-level)
- **Domains Covered**: Physics, Biology, Mathematics, Infrastructure

## 🎓 Learning Path

1. **Start**: Read main formula document overview
2. **Understand**: Pick one level, study both physics/biology and infrastructure sides
3. **Visualize**: Create diagrams using Mermaid or GraphView
4. **Apply**: Map to your own infrastructure using templates
5. **Extend**: Add new levels or formulas as needed

## 📧 Support & Questions

For questions about:
- **LaTeX syntax**: Check Obsidian/MathJax documentation
- **Graph visualization**: See GraphView guide
- **Repository structure**: Refer to main README

---

**Last Updated**: 2026-01-02  
**Version**: 1.0  
**Status**: Complete ✅
