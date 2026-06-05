---
id: UNI-136
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop 5

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
- [[UNI-185]] (pipefitter_to_flame, weight: 0.7)
- [[UNI-037]] (lqg_to_pipe, weight: 0.16)
- [[UNI-137]] (pipefitter_to_pipefitter, weight: 0.27)
- [[UNI-215]] (pipefitter_to_flame, weight: 0.82)
- [[UNI-051]] (lqg_to_pipe, weight: 0.89)
- [[UNI-201]] (pipefitter_to_flame, weight: 0.6)
- [[UNI-107]] (chess_to_pipe, weight: 0.55)
- [[UNI-111]] (pipefitter_to_pipefitter, weight: 0.77)
- [[UNI-023]] (pipefitter_to_quantum, weight: 0.76)

### Incoming Synapses
- [[UNI-198]] (flame_to_pipefitter, weight: 0.23)
- [[UNI-178]] (pipe_to_rubik, weight: 0.81)
- [[UNI-101]] (chess_to_pipe, weight: 0.68)
- [[UNI-096]] (chess_to_pipe, weight: 0.38)
- [[UNI-044]] (lqg_to_pipe, weight: 0.61)
- [[UNI-074]] (chess_to_pipe, weight: 0.86)
- [[UNI-074]] (chess_to_pipe, weight: 0.94)
- [[UNI-199]] (flame_to_pipefitter, weight: 0.67)

## Tags

#node/unified #lobe/pipe #pipe/flow
