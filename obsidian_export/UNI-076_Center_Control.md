---
id: UNI-076
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control

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
- [[UNI-017]] (chess_to_quantum, weight: 0.58)
- [[UNI-180]] (chess_to_rubik, weight: 0.81)
- [[UNI-176]] (chess_to_rubik, weight: 0.41)
- [[UNI-082]] (chess_to_chess, weight: 0.51)
- [[UNI-124]] (chess_to_pipe, weight: 0.63)
- [[UNI-128]] (chess_to_pipe, weight: 0.91)

### Incoming Synapses
- [[UNI-204]] (chess_to_flame, weight: 0.33)
- [[UNI-002]] (quantum_to_chess, weight: 0.11)

## Tags

#node/unified #lobe/chess #chess/tactic
