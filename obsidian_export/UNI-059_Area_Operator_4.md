---
id: UNI-059
domain: ["lqg", "gravity"]
role: Surface Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Area Operator 4

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
- [[UNI-023]] (lqg_to_quantum, weight: 0.11)
- [[UNI-033]] (lqg_to_quantum, weight: 0.14)
- [[UNI-125]] (lqg_to_pipe, weight: 0.35)
- [[UNI-146]] (lqg_to_rubik, weight: 0.14)
- [[UNI-036]] (lqg_to_quantum, weight: 0.49)

### Incoming Synapses
- [[UNI-035]] (quantum_to_lqg, weight: 0.16)
- [[UNI-037]] (lqg_to_lqg, weight: 0.3)
- [[UNI-081]] (chess_to_lqg, weight: 0.53)

## Tags

#node/unified #lobe/lqg #lqg/geometry
