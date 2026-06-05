# DOM Mapping Quick Reference Card

**Subatomic-to-Empire: Mathematical Analogies for Infrastructure**

---

## Level 1: Subatomic → Electrons & Signals
**Physics:** $i \hbar \frac{\partial \psi}{\partial t} = \hat{H} \psi$ (Schrödinger)  
**Infra:** $s(t) = A e^{i(kx - \omega t)}$ (Wave packet)  
**Mapping:** Quantum wave → Network signal propagation

---

## Level 2: Atomic → Periodic Table of Compute
**Physics:** $IE \approx \frac{13.6 Z^2}{n^2}$ (Ionization energy)  
**Infra:** $R_i = \frac{C \cdot P_i}{\sum P_j}$ (Resource allocation)  
**Mapping:** Atomic properties → Compute element distribution

---

## Level 3: Molecular → DNA & Code
**Biology:** $H = -\sum p_i \log_2 p_i$ (Shannon entropy)  
**Infra:** $D = \sum |s_i - t_i|$ (Levenshtein distance)  
**Mapping:** DNA information → Code complexity

---

## Level 4: Cellular → VMs & Containers
**Biology:** $\frac{dN}{dt} = rN(1 - \frac{N}{K})$ (Logistic growth)  
**Infra:** $\min \sum b_j$ subject to constraints (Bin packing)  
**Mapping:** Population dynamics → Container scaling

---

## Level 5: Immune System → Security
**Biology:** $\frac{dI}{dt} = \beta SI - \gamma I$ (SIR model)  
**Infra:** $U = p(-L) + (1-p)(-C)$ (Expected utility)  
**Mapping:** Infection dynamics → Threat propagation

---

## Level 6: Nervous System → Network
**Biology:** $C\frac{dV}{dt} = -\sum g(V-E) + I$ (Hodgkin-Huxley)  
**Infra:** $L = D - A$ (Graph Laplacian)  
**Mapping:** Neural firing → Network flow

---

## Level 7: Brain Hemispheres → Compute Distribution
**Biology:** $AI = \frac{R - L}{R + L}$ (Asymmetry index)  
**Infra:** $\min \max_i \sum w_j$ (Load balancing)  
**Mapping:** Lateralization → Regional distribution

---

## Level 8: Ramanujan → Intuitive Algorithms
**Math:** $\frac{1}{\pi} = \frac{2\sqrt{2}}{9801}\sum_{k=0}^{\infty} \frac{(4k)!(1103+26390k)}{(k!)^4 396^{4k}}$  
**Infra:** $a_{n+1} = a_n + \frac{b_n}{q_n}$ (Continued fractions)  
**Mapping:** Rapid convergence → Heuristic optimization

---

## Level 9: Blood → Data Flow
**Physics:** $Q = \frac{\pi r^4 \Delta P}{8 \eta L}$ (Hagen-Poiseuille)  
**Infra:** $\frac{\partial u}{\partial t} + (u \cdot \nabla)u = -\frac{1}{\rho}\nabla p + \nu \nabla^2 u$ (Navier-Stokes)  
**Mapping:** Viscous flow → Congestion control

---

## Usage Guide

### In Obsidian
```markdown
Copy formulas with $...$ or $$...$$ syntax
Link levels: [[Level 1]], [[Level 2]], etc.
Use Graph View to visualize connections
```

### In GraphView (Power BI/Visio)
```csv
Import: docs/graphview/dom-nodes.csv
        docs/graphview/dom-edges.csv
Visualize: Network graph with 9 levels
```

### In Markdown
```mermaid
See: docs/graphview/MERMAID_DIAGRAMS.md
```

---

## Key Symbols Reference

| Symbol | Meaning | LaTeX |
|--------|---------|-------|
| ψ | Wave function | `\psi` |
| ∇ | Gradient/Del | `\nabla` |
| ∂ | Partial derivative | `\partial` |
| ℏ | Reduced Planck | `\hbar` |
| Σ | Summation | `\sum` |
| ∫ | Integral | `\int` |
| ≈ | Approximately | `\approx` |
| ∝ | Proportional to | `\propto` |

---

## Files Reference

- **Full Document:** `DOM_MAPPING_MATHEMATICAL_FORMULAS.md`
- **Obsidian Guide:** `docs/obsidian/README.md`
- **GraphView Guide:** `docs/graphview/GRAPHVIEW_GUIDE.md`
- **Diagrams:** `docs/graphview/MERMAID_DIAGRAMS.md`
- **Index:** `docs/README.md`

---

**Print this page for quick reference while building infrastructure!**

🔥 Sovereignty Architecture: Mathematically Formalized 🔥
