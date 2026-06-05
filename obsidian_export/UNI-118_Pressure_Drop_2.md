---
id: UNI-118
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop 2

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
- [[UNI-038]] (lqg_to_pipe, weight: 0.69)
- [[UNI-004]] (pipefitter_to_quantum, weight: 0.67)
- [[UNI-202]] (pipefitter_to_flame, weight: 0.66)

### Incoming Synapses
- [[UNI-112]] (pipefitter_to_pipefitter, weight: 0.38)
- [[UNI-183]] (flame_to_pipefitter, weight: 0.23)
- [[UNI-155]] (pipe_to_rubik, weight: 0.21)
- [[UNI-131]] (pipefitter_to_pipefitter, weight: 0.31)
- [[UNI-142]] (pipefitter_to_pipefitter, weight: 0.45)

## Tags

#node/unified #lobe/pipe #pipe/flow
