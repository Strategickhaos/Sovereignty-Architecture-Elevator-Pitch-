---
id: UNI-097
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern 5

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
- [[UNI-126]] (chess_to_pipe, weight: 0.92)
- [[UNI-038]] (chess_to_lqg, weight: 0.75)
- [[UNI-190]] (chess_to_flame, weight: 0.77)

### Incoming Synapses
- [[UNI-046]] (lqg_to_chess, weight: 0.97)
- [[UNI-009]] (quantum_to_chess, weight: 0.16)
- [[UNI-066]] (lqg_to_chess, weight: 0.69)
- [[UNI-105]] (chess_to_chess, weight: 0.17)
- [[UNI-178]] (chess_to_rubik, weight: 0.43)
- [[UNI-124]] (chess_to_pipe, weight: 0.55)

## Tags

#node/unified #lobe/chess #chess/tactic
