---
id: UNI-123
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation 3

**Domain:** pipefitter, hydraulic

**Role:** Continuity

**LaTeX:** $$A_1 v_1 = A_2 v_2$$

## Explanation

Volume flow preservation; maps to LQG area quantization

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-153]] (pipe_to_rubik, weight: 0.84)
- [[UNI-045]] (lqg_to_pipe, weight: 0.48)
- [[UNI-196]] (pipefitter_to_flame, weight: 0.52)

### Incoming Synapses
- [[UNI-213]] (flame_to_pipefitter, weight: 0.14)
- [[UNI-132]] (pipefitter_to_pipefitter, weight: 0.54)
- [[UNI-167]] (pipe_to_rubik, weight: 0.11)
- [[UNI-065]] (lqg_to_pipe, weight: 0.38)

## Tags

#node/unified #lobe/pipe #pipe/flow
