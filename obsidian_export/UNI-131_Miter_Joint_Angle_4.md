---
id: UNI-131
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle 4

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
- [[UNI-018]] (pipefitter_to_quantum, weight: 0.39)
- [[UNI-036]] (pipefitter_to_quantum, weight: 0.93)
- [[UNI-118]] (pipefitter_to_pipefitter, weight: 0.31)
- [[UNI-209]] (pipefitter_to_flame, weight: 0.18)
- [[UNI-181]] (pipefitter_to_flame, weight: 0.52)

### Incoming Synapses
- [[UNI-034]] (quantum_to_pipefitter, weight: 0.35)

## Tags

#node/unified #lobe/pipe #pipe/flow
