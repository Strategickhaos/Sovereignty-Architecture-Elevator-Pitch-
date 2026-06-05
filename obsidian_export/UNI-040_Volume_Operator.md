---
id: UNI-040
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator

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
- [[UNI-205]] (lqg_to_flame, weight: 0.26)
- [[UNI-086]] (lqg_to_chess, weight: 0.45)
- [[UNI-025]] (lqg_to_quantum, weight: 0.68)
- [[UNI-045]] (lqg_to_lqg, weight: 0.28)
- [[UNI-053]] (lqg_to_lqg, weight: 0.66)
- [[UNI-150]] (lqg_to_rubik, weight: 0.38)
- [[UNI-191]] (lqg_to_flame, weight: 0.25)
- [[UNI-049]] (lqg_to_lqg, weight: 0.13)

### Incoming Synapses
- [[UNI-168]] (lqg_to_rubik, weight: 0.9)
- [[UNI-191]] (flame_to_lqg, weight: 0.39)
- [[UNI-025]] (quantum_to_lqg, weight: 0.99)
- [[UNI-116]] (lqg_to_pipe, weight: 0.71)
- [[UNI-154]] (lqg_to_rubik, weight: 0.85)
- [[UNI-009]] (quantum_to_lqg, weight: 0.82)
- [[UNI-070]] (lqg_to_lqg, weight: 0.87)

## Tags

#node/unified #lobe/lqg #lqg/geometry
