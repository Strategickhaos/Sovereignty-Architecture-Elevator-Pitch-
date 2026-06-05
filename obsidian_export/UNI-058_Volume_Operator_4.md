---
id: UNI-058
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator 4

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
- [[UNI-064]] (lqg_to_lqg, weight: 0.66)
- [[UNI-087]] (lqg_to_chess, weight: 0.22)
- [[UNI-091]] (lqg_to_chess, weight: 0.67)
- [[UNI-096]] (lqg_to_chess, weight: 0.63)
- [[UNI-195]] (lqg_to_flame, weight: 0.17)

### Incoming Synapses
- [[UNI-175]] (lqg_to_rubik, weight: 0.45)
- [[UNI-009]] (quantum_to_lqg, weight: 0.37)
- [[UNI-151]] (lqg_to_rubik, weight: 0.91)

## Tags

#node/unified #lobe/lqg #lqg/geometry
