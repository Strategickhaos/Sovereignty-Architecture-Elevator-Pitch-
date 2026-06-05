---
id: UNI-070
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator 6

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
- [[UNI-040]] (lqg_to_lqg, weight: 0.87)

### Incoming Synapses
- [[UNI-189]] (flame_to_lqg, weight: 0.23)
- [[UNI-186]] (flame_to_lqg, weight: 0.63)
- [[UNI-045]] (lqg_to_lqg, weight: 0.85)
- [[UNI-101]] (chess_to_lqg, weight: 0.13)
- [[UNI-182]] (flame_to_lqg, weight: 0.88)

## Tags

#node/unified #lobe/lqg #lqg/geometry
