---
id: UNI-046
domain: ["lqg", "gravity"]
role: Spatial Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Volume Operator 2

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
- [[UNI-097]] (lqg_to_chess, weight: 0.97)
- [[UNI-137]] (lqg_to_pipe, weight: 0.38)
- [[UNI-091]] (lqg_to_chess, weight: 0.31)
- [[UNI-003]] (lqg_to_quantum, weight: 0.61)
- [[UNI-047]] (lqg_to_lqg, weight: 0.71)
- [[UNI-172]] (lqg_to_rubik, weight: 0.68)
- [[UNI-134]] (lqg_to_pipe, weight: 0.96)
- [[UNI-011]] (lqg_to_quantum, weight: 0.8)
- [[UNI-162]] (lqg_to_rubik, weight: 0.6)

### Incoming Synapses
- [[UNI-143]] (lqg_to_pipe, weight: 0.64)
- [[UNI-197]] (flame_to_lqg, weight: 0.38)
- [[UNI-068]] (lqg_to_lqg, weight: 0.91)
- [[UNI-081]] (chess_to_lqg, weight: 0.82)
- [[UNI-060]] (lqg_to_lqg, weight: 0.69)

## Tags

#node/unified #lobe/lqg #lqg/geometry
