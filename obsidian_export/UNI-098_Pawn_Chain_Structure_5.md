---
id: UNI-098
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure 5

**Domain:** chess, kinesthetic

**Role:** Strategic Formation

**LaTeX:** $$P_n = P_{n-1} + (1,1)$$

## Explanation

Diagonal support structure; correlates to LQG spin networks

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-176]] (chess_to_rubik, weight: 0.81)
- [[UNI-186]] (chess_to_flame, weight: 0.91)
- [[UNI-211]] (chess_to_flame, weight: 0.84)

### Incoming Synapses
- [[UNI-018]] (quantum_to_chess, weight: 0.36)
- [[UNI-044]] (lqg_to_chess, weight: 0.86)
- [[UNI-067]] (lqg_to_chess, weight: 0.31)
- [[UNI-021]] (quantum_to_chess, weight: 0.26)
- [[UNI-026]] (quantum_to_chess, weight: 0.21)

## Tags

#node/unified #lobe/chess #chess/tactic
