---
id: UNI-095
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility 4

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
- [[UNI-021]] (chess_to_quantum, weight: 0.98)
- [[UNI-171]] (chess_to_rubik, weight: 0.94)
- [[UNI-194]] (chess_to_flame, weight: 0.97)
- [[UNI-065]] (chess_to_lqg, weight: 0.23)

### Incoming Synapses
- [[UNI-189]] (chess_to_flame, weight: 0.46)
- [[UNI-198]] (chess_to_flame, weight: 0.85)

## Tags

#node/unified #lobe/chess #chess/tactic
