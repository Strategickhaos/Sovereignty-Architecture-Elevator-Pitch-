---
id: UNI-096
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic 4

**Domain:** chess, kinesthetic

**Role:** Constraint Pattern

**LaTeX:** $$\vec{P} \parallel \vec{K}$$

## Explanation

Collinear piece restriction; correlates to FlameLang dependencies

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-157]] (chess_to_rubik, weight: 0.16)
- [[UNI-170]] (chess_to_rubik, weight: 0.13)
- [[UNI-117]] (chess_to_pipe, weight: 0.15)
- [[UNI-136]] (chess_to_pipe, weight: 0.38)
- [[UNI-126]] (chess_to_pipe, weight: 0.72)

### Incoming Synapses
- [[UNI-069]] (lqg_to_chess, weight: 0.7)
- [[UNI-135]] (chess_to_pipe, weight: 0.63)
- [[UNI-109]] (chess_to_pipe, weight: 0.35)
- [[UNI-198]] (chess_to_flame, weight: 0.18)
- [[UNI-109]] (chess_to_pipe, weight: 0.52)
- [[UNI-058]] (lqg_to_chess, weight: 0.63)

## Tags

#node/unified #lobe/chess #chess/tactic
