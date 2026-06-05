---
id: UNI-101
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility 5

**Domain:** chess, kinesthetic

**Role:** Dynamic Potential

**LaTeX:** $$M_p = |\{s : p \to s\}|$$

## Explanation

Available move count; maps to Rubik state space

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-019]] (chess_to_quantum, weight: 0.27)
- [[UNI-089]] (chess_to_chess, weight: 0.52)
- [[UNI-179]] (chess_to_rubik, weight: 0.95)
- [[UNI-064]] (chess_to_lqg, weight: 0.61)
- [[UNI-070]] (chess_to_lqg, weight: 0.13)
- [[UNI-136]] (chess_to_pipe, weight: 0.68)

### Incoming Synapses
- [[UNI-158]] (chess_to_rubik, weight: 0.55)
- [[UNI-189]] (chess_to_flame, weight: 0.61)

## Tags

#node/unified #lobe/chess #chess/tactic
