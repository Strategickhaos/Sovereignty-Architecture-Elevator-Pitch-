---
id: UNI-075
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric

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
- [[UNI-182]] (chess_to_flame, weight: 0.88)
- [[UNI-049]] (chess_to_lqg, weight: 0.75)
- [[UNI-190]] (chess_to_flame, weight: 0.67)

### Incoming Synapses
- [[UNI-185]] (chess_to_flame, weight: 0.13)
- [[UNI-141]] (chess_to_pipe, weight: 0.21)
- [[UNI-174]] (chess_to_rubik, weight: 0.61)
- [[UNI-142]] (chess_to_pipe, weight: 0.49)
- [[UNI-102]] (chess_to_chess, weight: 0.11)
- [[UNI-192]] (chess_to_flame, weight: 0.59)
- [[UNI-077]] (chess_to_chess, weight: 0.92)
- [[UNI-052]] (lqg_to_chess, weight: 0.43)

## Tags

#node/unified #lobe/chess #chess/tactic
