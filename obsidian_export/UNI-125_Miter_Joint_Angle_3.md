---
id: UNI-125
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle 3

**Domain:** pipefitter, hydraulic

**Role:** Geometry Connection

**LaTeX:** $$\theta_{cut} = \frac{\theta_{pipe}}{2}$$

## Explanation

Cut angle for directional change; maps to FlameLang branching

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-019]] (pipefitter_to_quantum, weight: 0.72)
- [[UNI-053]] (lqg_to_pipe, weight: 0.56)
- [[UNI-011]] (pipefitter_to_quantum, weight: 0.5)

### Incoming Synapses
- [[UNI-209]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-059]] (lqg_to_pipe, weight: 0.35)
- [[UNI-160]] (pipe_to_rubik, weight: 0.66)
- [[UNI-130]] (pipefitter_to_pipefitter, weight: 0.66)

## Tags

#node/unified #lobe/pipe #pipe/flow
