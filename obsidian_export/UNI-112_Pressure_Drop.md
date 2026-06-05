---
id: UNI-112
domain: ["pipefitter", "hydraulic"]
role: Friction Loss
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pressure Drop

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
- [[UNI-118]] (pipefitter_to_pipefitter, weight: 0.38)
- [[UNI-182]] (pipefitter_to_flame, weight: 0.71)
- [[UNI-043]] (lqg_to_pipe, weight: 0.23)

### Incoming Synapses
- [[UNI-216]] (flame_to_pipefitter, weight: 0.97)
- [[UNI-018]] (quantum_to_pipefitter, weight: 0.82)
- [[UNI-195]] (flame_to_pipefitter, weight: 0.49)
- [[UNI-111]] (pipefitter_to_pipefitter, weight: 0.6)

## Tags

#node/unified #lobe/pipe #pipe/flow
