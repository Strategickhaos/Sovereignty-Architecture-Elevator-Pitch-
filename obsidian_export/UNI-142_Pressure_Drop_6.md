---
id: UNI-142
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop 6

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
- [[UNI-028]] (pipefitter_to_quantum, weight: 0.23)
- [[UNI-014]] (pipefitter_to_quantum, weight: 0.72)
- [[UNI-075]] (chess_to_pipe, weight: 0.49)
- [[UNI-041]] (lqg_to_pipe, weight: 0.46)
- [[UNI-196]] (pipefitter_to_flame, weight: 0.29)
- [[UNI-118]] (pipefitter_to_pipefitter, weight: 0.45)

### Incoming Synapses
- [[UNI-191]] (flame_to_pipefitter, weight: 0.72)
- [[UNI-156]] (pipe_to_rubik, weight: 0.69)
- [[UNI-164]] (pipe_to_rubik, weight: 0.24)

## Tags

#node/unified #lobe/pipe #pipe/flow
