---
id: UNI-064
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator 5

**Domain:** lqg, gravity

**Role:** Spatial Quantum

**LaTeX:** $$\hat{V} = \sqrt{\det(q)}$$

## Explanation

Quantized spatial volume; maps to pipe block volumes

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-137]] (lqg_to_pipe, weight: 0.2)
- [[UNI-062]] (lqg_to_lqg, weight: 0.19)
- [[UNI-049]] (lqg_to_lqg, weight: 0.96)
- [[UNI-021]] (lqg_to_quantum, weight: 0.53)
- [[UNI-053]] (lqg_to_lqg, weight: 0.2)
- [[UNI-025]] (lqg_to_quantum, weight: 0.12)
- [[UNI-105]] (lqg_to_chess, weight: 0.94)
- [[UNI-121]] (lqg_to_pipe, weight: 0.17)

### Incoming Synapses
- [[UNI-066]] (lqg_to_lqg, weight: 0.71)
- [[UNI-086]] (chess_to_lqg, weight: 0.86)
- [[UNI-101]] (chess_to_lqg, weight: 0.61)
- [[UNI-149]] (lqg_to_rubik, weight: 0.58)
- [[UNI-058]] (lqg_to_lqg, weight: 0.66)

## Tags

#node/unified #lobe/lqg #lqg/geometry
