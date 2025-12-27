---
id: UNI-066
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint 5

**Domain:** lqg, gravity

**Role:** Hamiltonian Evolution

**LaTeX:** $$\hat{H}[N]$$

## Explanation

Time evolution constraint; maps to Rubik move sequences

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-064]] (lqg_to_lqg, weight: 0.71)
- [[UNI-047]] (lqg_to_lqg, weight: 0.39)
- [[UNI-158]] (lqg_to_rubik, weight: 0.95)
- [[UNI-097]] (lqg_to_chess, weight: 0.69)

### Incoming Synapses
- [[UNI-017]] (quantum_to_lqg, weight: 0.28)
- [[UNI-001]] (quantum_to_lqg, weight: 0.65)
- [[UNI-127]] (lqg_to_pipe, weight: 0.98)

## Tags

#node/unified #lobe/lqg #lqg/geometry
