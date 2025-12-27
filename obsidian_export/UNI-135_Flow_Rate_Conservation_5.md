---
id: UNI-135
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation 5

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
- [[UNI-195]] (pipefitter_to_flame, weight: 0.97)
- [[UNI-096]] (chess_to_pipe, weight: 0.63)
- [[UNI-007]] (pipefitter_to_quantum, weight: 0.37)

### Incoming Synapses
- [[UNI-208]] (flame_to_pipefitter, weight: 0.51)
- [[UNI-073]] (chess_to_pipe, weight: 0.34)
- [[UNI-162]] (pipe_to_rubik, weight: 0.84)
- [[UNI-199]] (flame_to_pipefitter, weight: 0.13)
- [[UNI-081]] (chess_to_pipe, weight: 0.4)
- [[UNI-018]] (quantum_to_pipefitter, weight: 0.77)

## Tags

#node/unified #lobe/pipe #pipe/flow
