---
id: UNI-089
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility 3

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
- [[UNI-186]] (chess_to_flame, weight: 0.33)

### Incoming Synapses
- [[UNI-209]] (chess_to_flame, weight: 0.13)
- [[UNI-133]] (chess_to_pipe, weight: 0.13)
- [[UNI-022]] (quantum_to_chess, weight: 0.37)
- [[UNI-211]] (chess_to_flame, weight: 0.64)
- [[UNI-101]] (chess_to_chess, weight: 0.52)
- [[UNI-198]] (chess_to_flame, weight: 0.97)

## Tags

#node/unified #lobe/chess #chess/tactic
