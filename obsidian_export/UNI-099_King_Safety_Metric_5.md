---
id: UNI-099
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric 5

**Domain:** chess, kinesthetic

**Role:** Evaluation Function

**LaTeX:** $$S_K = \sum_i w_i \cdot f_i$$

## Explanation

Weighted safety factors; maps to conservation gates

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-114]] (chess_to_pipe, weight: 0.36)
- [[UNI-138]] (chess_to_pipe, weight: 0.31)
- [[UNI-212]] (chess_to_flame, weight: 0.66)

### Incoming Synapses
- [[UNI-014]] (quantum_to_chess, weight: 0.32)
- [[UNI-007]] (quantum_to_chess, weight: 0.36)
- [[UNI-197]] (chess_to_flame, weight: 0.63)
- [[UNI-188]] (chess_to_flame, weight: 0.25)
- [[UNI-090]] (chess_to_chess, weight: 0.84)
- [[UNI-072]] (lqg_to_chess, weight: 0.22)
- [[UNI-134]] (chess_to_pipe, weight: 0.2)

## Tags

#node/unified #lobe/chess #chess/tactic
