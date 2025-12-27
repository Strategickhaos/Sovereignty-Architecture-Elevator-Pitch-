---
id: UNI-072
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint 6

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
- [[UNI-022]] (lqg_to_quantum, weight: 0.73)
- [[UNI-008]] (lqg_to_quantum, weight: 0.55)
- [[UNI-183]] (lqg_to_flame, weight: 0.6)
- [[UNI-208]] (lqg_to_flame, weight: 0.58)
- [[UNI-099]] (lqg_to_chess, weight: 0.22)
- [[UNI-092]] (lqg_to_chess, weight: 0.65)

### Incoming Synapses
- [[UNI-193]] (flame_to_lqg, weight: 0.55)
- [[UNI-208]] (flame_to_lqg, weight: 0.94)
- [[UNI-119]] (lqg_to_pipe, weight: 0.88)
- [[UNI-077]] (chess_to_lqg, weight: 0.35)
- [[UNI-034]] (quantum_to_lqg, weight: 0.93)

## Tags

#node/unified #lobe/lqg #lqg/geometry
