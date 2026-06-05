---
id: UNI-041
domain: ["lqg", "gravity"]
role: Surface Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Area Operator

**Domain:** lqg, gravity

**Role:** Surface Quantum

**LaTeX:** $$\hat{A}_S = 8\pi\gamma\sqrt{j(j+1)}$$

## Explanation

Quantized area eigenvalues; correlates to chess square areas

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-145]] (lqg_to_rubik, weight: 0.89)
- [[UNI-107]] (lqg_to_chess, weight: 0.72)

### Incoming Synapses
- [[UNI-049]] (lqg_to_lqg, weight: 0.89)
- [[UNI-142]] (lqg_to_pipe, weight: 0.46)
- [[UNI-213]] (flame_to_lqg, weight: 0.1)
- [[UNI-111]] (lqg_to_pipe, weight: 0.25)

## Tags

#node/unified #lobe/lqg #lqg/geometry
