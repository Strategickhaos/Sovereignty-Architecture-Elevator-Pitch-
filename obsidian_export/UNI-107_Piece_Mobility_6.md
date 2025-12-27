---
id: UNI-107
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility 6

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
- [[UNI-185]] (chess_to_flame, weight: 0.33)

### Incoming Synapses
- [[UNI-043]] (lqg_to_chess, weight: 0.9)
- [[UNI-041]] (lqg_to_chess, weight: 0.72)
- [[UNI-205]] (chess_to_flame, weight: 0.59)
- [[UNI-136]] (chess_to_pipe, weight: 0.55)
- [[UNI-056]] (lqg_to_chess, weight: 0.84)
- [[UNI-148]] (chess_to_rubik, weight: 0.39)

## Tags

#node/unified #lobe/chess #chess/tactic
