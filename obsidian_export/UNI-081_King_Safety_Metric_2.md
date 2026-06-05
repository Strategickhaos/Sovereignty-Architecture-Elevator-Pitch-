---
id: UNI-081
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric 2

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
- [[UNI-049]] (chess_to_lqg, weight: 0.44)
- [[UNI-135]] (chess_to_pipe, weight: 0.4)
- [[UNI-046]] (chess_to_lqg, weight: 0.82)
- [[UNI-194]] (chess_to_flame, weight: 0.43)
- [[UNI-059]] (chess_to_lqg, weight: 0.53)
- [[UNI-010]] (chess_to_quantum, weight: 0.66)
- [[UNI-029]] (chess_to_quantum, weight: 0.56)

### Incoming Synapses
- [[UNI-195]] (chess_to_flame, weight: 0.65)
- [[UNI-199]] (chess_to_flame, weight: 0.96)
- [[UNI-193]] (chess_to_flame, weight: 0.29)
- [[UNI-189]] (chess_to_flame, weight: 0.19)
- [[UNI-152]] (chess_to_rubik, weight: 0.25)

## Tags

#node/unified #lobe/chess #chess/tactic
