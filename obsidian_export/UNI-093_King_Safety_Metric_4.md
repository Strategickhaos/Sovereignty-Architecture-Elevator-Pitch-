---
id: UNI-093
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric 4

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
- [[UNI-165]] (chess_to_rubik, weight: 0.28)
- [[UNI-147]] (chess_to_rubik, weight: 0.44)
- [[UNI-129]] (chess_to_pipe, weight: 0.77)
- [[UNI-198]] (chess_to_flame, weight: 0.47)

### Incoming Synapses
- [[UNI-156]] (chess_to_rubik, weight: 0.55)
- [[UNI-196]] (chess_to_flame, weight: 0.25)
- [[UNI-216]] (chess_to_flame, weight: 0.59)
- [[UNI-149]] (chess_to_rubik, weight: 0.31)
- [[UNI-213]] (chess_to_flame, weight: 0.52)
- [[UNI-032]] (quantum_to_chess, weight: 0.36)

## Tags

#node/unified #lobe/chess #chess/tactic
