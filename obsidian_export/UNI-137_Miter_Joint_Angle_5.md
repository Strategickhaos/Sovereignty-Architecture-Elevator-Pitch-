---
id: UNI-137
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle 5

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
- [[UNI-061]] (lqg_to_pipe, weight: 0.43)
- [[UNI-187]] (pipefitter_to_flame, weight: 0.95)
- [[UNI-049]] (lqg_to_pipe, weight: 0.42)
- [[UNI-126]] (pipefitter_to_pipefitter, weight: 0.73)
- [[UNI-146]] (pipe_to_rubik, weight: 0.88)
- [[UNI-192]] (pipefitter_to_flame, weight: 0.46)
- [[UNI-195]] (pipefitter_to_flame, weight: 0.45)

### Incoming Synapses
- [[UNI-064]] (lqg_to_pipe, weight: 0.2)
- [[UNI-029]] (quantum_to_pipefitter, weight: 0.48)
- [[UNI-046]] (lqg_to_pipe, weight: 0.38)
- [[UNI-140]] (pipefitter_to_pipefitter, weight: 0.95)
- [[UNI-136]] (pipefitter_to_pipefitter, weight: 0.27)
- [[UNI-200]] (flame_to_pipefitter, weight: 0.31)
- [[UNI-172]] (pipe_to_rubik, weight: 0.43)
- [[UNI-103]] (chess_to_pipe, weight: 0.89)

## Tags

#node/unified #lobe/pipe #pipe/flow
