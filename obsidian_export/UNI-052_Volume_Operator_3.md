---
id: UNI-052
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator 3

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
- [[UNI-164]] (lqg_to_rubik, weight: 0.94)
- [[UNI-147]] (lqg_to_rubik, weight: 0.92)
- [[UNI-075]] (lqg_to_chess, weight: 0.43)

### Incoming Synapses
- [[UNI-200]] (flame_to_lqg, weight: 0.48)
- [[UNI-024]] (quantum_to_lqg, weight: 0.86)

## Tags

#node/unified #lobe/lqg #lqg/geometry
