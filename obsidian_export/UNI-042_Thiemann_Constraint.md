---
id: UNI-042
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint

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
- [[UNI-201]] (lqg_to_flame, weight: 0.21)
- [[UNI-179]] (lqg_to_rubik, weight: 0.95)
- [[UNI-164]] (lqg_to_rubik, weight: 0.24)
- [[UNI-051]] (lqg_to_lqg, weight: 0.98)

### Incoming Synapses
- [[UNI-034]] (quantum_to_lqg, weight: 0.29)
- [[UNI-117]] (lqg_to_pipe, weight: 0.45)

## Tags

#node/unified #lobe/lqg #lqg/geometry
