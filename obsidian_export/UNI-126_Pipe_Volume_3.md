---
id: UNI-126
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume 3

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
- [[UNI-193]] (pipefitter_to_flame, weight: 0.65)
- [[UNI-049]] (lqg_to_pipe, weight: 0.61)

### Incoming Synapses
- [[UNI-160]] (pipe_to_rubik, weight: 0.75)
- [[UNI-022]] (quantum_to_pipefitter, weight: 0.38)
- [[UNI-145]] (pipe_to_rubik, weight: 0.69)
- [[UNI-097]] (chess_to_pipe, weight: 0.92)
- [[UNI-137]] (pipefitter_to_pipefitter, weight: 0.73)
- [[UNI-037]] (lqg_to_pipe, weight: 0.89)
- [[UNI-096]] (chess_to_pipe, weight: 0.72)

## Tags

#node/unified #lobe/pipe #pipe/flow
