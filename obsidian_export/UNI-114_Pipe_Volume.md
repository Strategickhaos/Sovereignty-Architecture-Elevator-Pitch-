---
id: UNI-114
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume

**Domain:** pipefitter, hydraulic

**Role:** Block Size 64

**LaTeX:** $$V = \pi r^2 L = 2^6$$

## Explanation

Universal 64-chunk volume; correlates to chess squares

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-049]] (lqg_to_pipe, weight: 0.93)
- [[UNI-200]] (pipefitter_to_flame, weight: 0.94)
- [[UNI-133]] (pipefitter_to_pipefitter, weight: 0.97)
- [[UNI-183]] (pipefitter_to_flame, weight: 0.44)
- [[UNI-013]] (pipefitter_to_quantum, weight: 0.63)

### Incoming Synapses
- [[UNI-100]] (chess_to_pipe, weight: 0.47)
- [[UNI-201]] (flame_to_pipefitter, weight: 0.45)
- [[UNI-099]] (chess_to_pipe, weight: 0.36)
- [[UNI-190]] (flame_to_pipefitter, weight: 0.2)

## Tags

#node/unified #lobe/pipe #pipe/flow
