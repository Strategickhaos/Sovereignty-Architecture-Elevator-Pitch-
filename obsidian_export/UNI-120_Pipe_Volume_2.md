---
id: UNI-120
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume 2

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
- [[UNI-060]] (lqg_to_pipe, weight: 0.49)
- [[UNI-103]] (chess_to_pipe, weight: 0.13)
- [[UNI-035]] (pipefitter_to_quantum, weight: 0.39)
- [[UNI-213]] (pipefitter_to_flame, weight: 0.98)
- [[UNI-132]] (pipefitter_to_pipefitter, weight: 0.46)

### Incoming Synapses
- [[UNI-128]] (pipefitter_to_pipefitter, weight: 0.84)
- [[UNI-094]] (chess_to_pipe, weight: 0.83)
- [[UNI-199]] (flame_to_pipefitter, weight: 0.26)
- [[UNI-055]] (lqg_to_pipe, weight: 0.27)
- [[UNI-201]] (flame_to_pipefitter, weight: 0.85)

## Tags

#node/unified #lobe/pipe #pipe/flow
