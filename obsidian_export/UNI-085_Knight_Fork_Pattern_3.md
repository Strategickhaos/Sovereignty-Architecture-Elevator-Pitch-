---
id: UNI-085
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern 3

**Domain:** chess, kinesthetic

**Role:** Tactical Motif

**LaTeX:** $$N_{x,y} \to (x\pm2, y\pm1)$$

## Explanation

L-shaped move creates dual threats; maps to quantum superposition

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-211]] (chess_to_flame, weight: 0.98)

### Incoming Synapses
- [[UNI-152]] (chess_to_rubik, weight: 0.48)
- [[UNI-146]] (chess_to_rubik, weight: 0.84)
- [[UNI-024]] (quantum_to_chess, weight: 0.72)
- [[UNI-180]] (chess_to_rubik, weight: 0.84)
- [[UNI-003]] (quantum_to_chess, weight: 0.63)
- [[UNI-035]] (quantum_to_chess, weight: 0.42)
- [[UNI-207]] (chess_to_flame, weight: 0.51)
- [[UNI-216]] (chess_to_flame, weight: 0.19)
- [[UNI-056]] (lqg_to_chess, weight: 0.32)

## Tags

#node/unified #lobe/chess #chess/tactic
