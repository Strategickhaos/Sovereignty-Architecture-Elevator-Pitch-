---
id: UNI-102
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic 5

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
- [[UNI-180]] (chess_to_rubik, weight: 0.83)
- [[UNI-006]] (chess_to_quantum, weight: 0.11)
- [[UNI-075]] (chess_to_chess, weight: 0.11)
- [[UNI-088]] (chess_to_chess, weight: 0.89)
- [[UNI-176]] (chess_to_rubik, weight: 0.2)

### Incoming Synapses
- [[UNI-056]] (lqg_to_chess, weight: 0.65)
- [[UNI-035]] (quantum_to_chess, weight: 0.41)
- [[UNI-030]] (quantum_to_chess, weight: 0.32)
- [[UNI-128]] (chess_to_pipe, weight: 0.25)
- [[UNI-027]] (quantum_to_chess, weight: 0.21)
- [[UNI-179]] (chess_to_rubik, weight: 0.85)
- [[UNI-005]] (quantum_to_chess, weight: 0.95)

## Tags

#node/unified #lobe/chess #chess/tactic
