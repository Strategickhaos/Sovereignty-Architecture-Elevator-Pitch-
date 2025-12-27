---
id: UNI-130
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop 4

**Domain:** pipefitter, hydraulic

**Role:** Friction Loss

**LaTeX:** $$\Delta P = f\frac{L}{D}\frac{\rho v^2}{2}$$

## Explanation

Darcy-Weisbach equation; correlates to Rubik move cost

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-087]] (chess_to_pipe, weight: 0.7)
- [[UNI-189]] (pipefitter_to_flame, weight: 0.31)
- [[UNI-077]] (chess_to_pipe, weight: 0.7)
- [[UNI-057]] (lqg_to_pipe, weight: 0.62)
- [[UNI-125]] (pipefitter_to_pipefitter, weight: 0.66)
- [[UNI-185]] (pipefitter_to_flame, weight: 0.93)
- [[UNI-002]] (pipefitter_to_quantum, weight: 0.51)

### Incoming Synapses
- [[UNI-020]] (quantum_to_pipefitter, weight: 0.12)
- [[UNI-147]] (pipe_to_rubik, weight: 0.4)

## Tags

#node/unified #lobe/pipe #pipe/flow
