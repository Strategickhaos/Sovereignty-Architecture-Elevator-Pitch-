---
id: UNI-144
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume 6

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
- [[UNI-141]] (pipefitter_to_pipefitter, weight: 0.52)
- [[UNI-187]] (pipefitter_to_flame, weight: 0.24)
- [[UNI-105]] (chess_to_pipe, weight: 0.2)
- [[UNI-204]] (pipefitter_to_flame, weight: 0.28)
- [[UNI-077]] (chess_to_pipe, weight: 0.57)
- [[UNI-186]] (pipefitter_to_flame, weight: 0.77)
- [[UNI-177]] (pipe_to_rubik, weight: 0.17)
- [[UNI-185]] (pipefitter_to_flame, weight: 0.15)

### Incoming Synapses
- [[UNI-026]] (quantum_to_pipefitter, weight: 0.22)
- [[UNI-209]] (flame_to_pipefitter, weight: 0.6)
- [[UNI-090]] (chess_to_pipe, weight: 0.97)
- [[UNI-148]] (pipe_to_rubik, weight: 0.69)

## Tags

#node/unified #lobe/pipe #pipe/flow
