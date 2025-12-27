---
id: UNI-053
domain: ["lqg", "gravity"]
role: Surface Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Area Operator 3

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
- [[UNI-189]] (lqg_to_flame, weight: 0.24)
- [[UNI-158]] (lqg_to_rubik, weight: 0.15)

### Incoming Synapses
- [[UNI-064]] (lqg_to_lqg, weight: 0.2)
- [[UNI-092]] (chess_to_lqg, weight: 0.16)
- [[UNI-040]] (lqg_to_lqg, weight: 0.66)
- [[UNI-190]] (flame_to_lqg, weight: 0.24)
- [[UNI-125]] (lqg_to_pipe, weight: 0.56)
- [[UNI-113]] (lqg_to_pipe, weight: 0.28)

## Tags

#node/unified #lobe/lqg #lqg/geometry
