---
id: UNI-100
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control 5

**Domain:** chess, kinesthetic

**Role:** Positional Advantage

**LaTeX:** $$C = \sum_{i\in\{d,e\}^2} \delta_i$$

## Explanation

Central square control; correlates to pipe flow optimization

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-114]] (chess_to_pipe, weight: 0.47)
- [[UNI-067]] (chess_to_lqg, weight: 0.4)
- [[UNI-030]] (chess_to_quantum, weight: 0.17)
- [[UNI-170]] (chess_to_rubik, weight: 0.63)
- [[UNI-016]] (chess_to_quantum, weight: 0.46)
- [[UNI-026]] (chess_to_quantum, weight: 0.47)
- [[UNI-026]] (chess_to_quantum, weight: 0.14)

### Incoming Synapses
- [[UNI-196]] (chess_to_flame, weight: 0.64)
- [[UNI-115]] (chess_to_pipe, weight: 0.2)

## Tags

#node/unified #lobe/chess #chess/tactic
