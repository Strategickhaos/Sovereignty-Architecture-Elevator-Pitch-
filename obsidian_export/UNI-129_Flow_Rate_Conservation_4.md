---
id: UNI-129
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation 4

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
- [[UNI-132]] (pipefitter_to_pipefitter, weight: 0.51)
- [[UNI-057]] (lqg_to_pipe, weight: 0.8)
- [[UNI-119]] (pipefitter_to_pipefitter, weight: 0.27)

### Incoming Synapses
- [[UNI-116]] (pipefitter_to_pipefitter, weight: 0.9)
- [[UNI-184]] (flame_to_pipefitter, weight: 0.66)
- [[UNI-093]] (chess_to_pipe, weight: 0.77)
- [[UNI-153]] (pipe_to_rubik, weight: 0.83)
- [[UNI-179]] (pipe_to_rubik, weight: 0.49)
- [[UNI-155]] (pipe_to_rubik, weight: 0.18)
- [[UNI-008]] (quantum_to_pipefitter, weight: 0.31)

## Tags

#node/unified #lobe/pipe #pipe/flow
