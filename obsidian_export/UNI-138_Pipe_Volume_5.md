---
id: UNI-138
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume 5

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
- [[UNI-198]] (pipefitter_to_flame, weight: 0.53)
- [[UNI-103]] (chess_to_pipe, weight: 0.35)
- [[UNI-054]] (lqg_to_pipe, weight: 0.13)
- [[UNI-171]] (pipe_to_rubik, weight: 0.13)
- [[UNI-007]] (pipefitter_to_quantum, weight: 0.76)
- [[UNI-146]] (pipe_to_rubik, weight: 0.6)

### Incoming Synapses
- [[UNI-192]] (flame_to_pipefitter, weight: 0.76)
- [[UNI-082]] (chess_to_pipe, weight: 0.83)
- [[UNI-099]] (chess_to_pipe, weight: 0.31)
- [[UNI-140]] (pipefitter_to_pipefitter, weight: 0.2)

## Tags

#node/unified #lobe/pipe #pipe/flow
