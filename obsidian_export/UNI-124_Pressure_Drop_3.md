---
id: UNI-124
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop 3

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
- [[UNI-200]] (pipefitter_to_flame, weight: 0.57)
- [[UNI-045]] (lqg_to_pipe, weight: 0.93)
- [[UNI-097]] (chess_to_pipe, weight: 0.55)

### Incoming Synapses
- [[UNI-061]] (lqg_to_pipe, weight: 0.41)
- [[UNI-113]] (pipefitter_to_pipefitter, weight: 0.34)
- [[UNI-201]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-076]] (chess_to_pipe, weight: 0.63)
- [[UNI-088]] (chess_to_pipe, weight: 0.63)

## Tags

#node/unified #lobe/pipe #pipe/flow
