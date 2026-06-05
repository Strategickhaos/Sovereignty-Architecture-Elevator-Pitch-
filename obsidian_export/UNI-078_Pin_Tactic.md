---
id: UNI-078
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic

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
- [[UNI-196]] (chess_to_flame, weight: 0.59)
- [[UNI-180]] (chess_to_rubik, weight: 0.15)
- [[UNI-171]] (chess_to_rubik, weight: 0.13)

### Incoming Synapses
- [[UNI-011]] (quantum_to_chess, weight: 0.96)
- [[UNI-196]] (chess_to_flame, weight: 0.23)
- [[UNI-006]] (quantum_to_chess, weight: 0.86)
- [[UNI-033]] (quantum_to_chess, weight: 0.77)

## Tags

#node/unified #lobe/chess #chess/tactic
