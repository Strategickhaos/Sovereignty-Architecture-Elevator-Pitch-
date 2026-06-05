---
id: UNI-082
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control 2

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
- [[UNI-069]] (chess_to_lqg, weight: 0.92)
- [[UNI-138]] (chess_to_pipe, weight: 0.83)
- [[UNI-183]] (chess_to_flame, weight: 0.95)
- [[UNI-157]] (chess_to_rubik, weight: 0.3)
- [[UNI-172]] (chess_to_rubik, weight: 0.17)

### Incoming Synapses
- [[UNI-159]] (chess_to_rubik, weight: 0.62)
- [[UNI-076]] (chess_to_chess, weight: 0.51)
- [[UNI-024]] (quantum_to_chess, weight: 0.16)
- [[UNI-173]] (chess_to_rubik, weight: 0.95)
- [[UNI-181]] (chess_to_flame, weight: 0.72)
- [[UNI-201]] (chess_to_flame, weight: 0.48)

## Tags

#node/unified #lobe/chess #chess/tactic
