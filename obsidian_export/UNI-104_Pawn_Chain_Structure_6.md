---
id: UNI-104
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure 6

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
- [[UNI-022]] (chess_to_quantum, weight: 0.16)
- [[UNI-063]] (chess_to_lqg, weight: 0.97)

### Incoming Synapses
- [[UNI-049]] (lqg_to_chess, weight: 0.29)
- [[UNI-011]] (quantum_to_chess, weight: 0.76)

## Tags

#node/unified #lobe/chess #chess/tactic
