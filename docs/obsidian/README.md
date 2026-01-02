# Obsidian Vault Setup for DOM Mapping

This directory contains instructions and templates for setting up an Obsidian vault to visualize the DOM Mapping mathematical formulas.

## Quick Setup

1. **Create New Vault**: Open Obsidian → Create new vault named "Sovereignty-DOM-Mapping"

2. **Copy Files**: Import the `DOM_MAPPING_MATHEMATICAL_FORMULAS.md` into your vault

3. **Enable LaTeX**: 
   - Settings → Editor → Math support (should be enabled by default)
   - LaTeX rendering uses MathJax

4. **Install Recommended Plugins**:
   - Excalidraw (for visual diagrams)
   - Dataview (for querying formulas)
   - Graph Analysis (for enhanced graph view)

## Vault Structure

```
Sovereignty-DOM-Mapping/
├── Index.md                           # Main navigation hub
├── Levels/
│   ├── Level-1-Subatomic.md          # Schrödinger equation
│   ├── Level-2-Atomic.md              # Periodic table
│   ├── Level-3-Molecular.md           # DNA & Code
│   ├── Level-4-Cellular.md            # VMs & Containers
│   ├── Level-5-Immune.md              # Security
│   ├── Level-6-Nervous.md             # Network
│   ├── Level-7-Brain.md               # Compute distribution
│   ├── Level-8-Ramanujan.md           # Intuitive algorithms
│   └── Level-9-Blood.md               # Data flow
├── Formulas/
│   ├── Physics/                       # Physics formulas
│   ├── Biology/                       # Biology formulas
│   └── Infrastructure/                # Infrastructure analogies
├── Diagrams/
│   └── DOM-Architecture.excalidraw    # Visual map
└── Templates/
    └── level-template.md              # Template for new levels
```

## Usage Examples

### Creating Level Notes

See the `Templates/` directory for note templates with proper frontmatter and linking structure.

### Graph View Tips

1. **Filter by Tags**: Use `#physics`, `#biology`, `#infrastructure` to filter nodes
2. **Color Groups**: Settings → Graph View → Color by tag
3. **Show Only Connected**: Toggle to focus on linked formulas

### Search Examples

- Find all Schrödinger mentions: `/Schrödinger/`
- Find infrastructure analogies: `tag:#infrastructure`
- Find specific operators: `/\\nabla/` (for ∇)

## LaTeX Quick Reference

### Display Math (Centered)
```markdown
$$
\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)
$$
```

### Inline Math
```markdown
The wave function $\psi$ evolves according to $\hat{H}\psi = E\psi$.
```

### Common Symbols
- Derivatives: `\frac{\partial f}{\partial x}`, `\frac{d}{dt}`
- Operators: `\nabla` (∇), `\nabla^2` (∇²), `\Delta` (Δ)
- Greek: `\alpha`, `\beta`, `\gamma`, `\omega`, `\psi`, `\phi`
- Vectors: `\mathbf{u}`, `\vec{v}`
- Summation: `\sum_{i=1}^{n}`
- Integrals: `\int_{a}^{b} f(x) \, dx`

## Integration with Main Documentation

Link to main repository documentation:
- [[README.md]] - Main sovereignty architecture
- [[UNIFIED_SOVEREIGNTY_ARCHITECTURE]] - System overview
- [[OBSIDIAN_ARSENAL_COMPLETE]] - Obsidian tools & commands

## Next Steps

1. Create individual level notes from the main document
2. Build Excalidraw diagram connecting all levels
3. Add cross-references between physics/biology/infrastructure
4. Create dataview queries for formula search
5. Export graph view for presentations

## Resources

- [Obsidian LaTeX Guide](https://help.obsidian.md/Editing+and+formatting/Advanced+formatting+syntax#Math)
- [MathJax Documentation](https://www.mathjax.org/)
- [Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
