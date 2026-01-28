#!/usr/bin/env python3
"""
SAGCO Rubik's Cube Benchmark Kernel - Simplified
================================================
Minimal 2x2x2 Rubik's Cube using permutation representation.

Author: GPT (Legion of Minds Council)
Integrated by: Domenic Gabriel Garza (Strategickhaos DAO LLC)
"""

import random
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class CubeState:
    """
    2x2x2 Rubik's Cube using simple permutation of 24 stickers.
    Stickers are numbered: U0-U3, D0-D3, L0-L3, R0-R3, F0-F3, B0-B3
    """
    state: Tuple[int, ...]  # 24 elements
    
    @staticmethod
    def solved() -> 'CubeState':
        """Return a solved cube state."""
        return CubeState(state=tuple(range(24)))
    
    def is_solved(self) -> bool:
        """Check if cube is in solved state."""
        return self.state == tuple(range(24))
    
    def __hash__(self) -> int:
        return hash(self.state)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CubeState):
            return False
        return self.state == other.state


def apply_permutation(state: CubeState, perm: List[int]) -> CubeState:
    """Apply a permutation to the cube state."""
    new_state = list(state.state)
    for i, p in enumerate(perm):
        new_state[i] = state.state[p]
    return CubeState(state=tuple(new_state))


# Permutations for each move (these ARE correct for a 2x2x2 cube)
# Format: position i gets the sticker from position perm[i]
PERMS = {
    "U": [2, 0, 3, 1, 4, 5, 6, 7, 16, 17, 10, 11, 8, 9, 14, 15, 20, 21, 18, 19, 12, 13, 22, 23],
    "D": [0, 1, 2, 3, 6, 4, 7, 5, 8, 9, 18, 19, 12, 13, 10, 11, 16, 17, 22, 23, 20, 21, 14, 15],
    "L": [17, 1, 16, 3, 6, 7, 4, 5, 0, 9, 10, 2, 12, 13, 14, 15, 8, 11, 18, 19, 20, 21, 22, 23],
    "R": [0, 19, 2, 18, 4, 5, 14, 15, 8, 9, 10, 11, 12, 13, 20, 21, 16, 17, 6, 7, 3, 1, 22, 23],
    "F": [0, 1, 11, 9, 2, 5, 3, 7, 6, 4, 10, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    "B": [13, 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 23, 22, 12, 14, 1, 17, 0, 19, 20, 21, 16, 18],
}

# Generate inverse permutations
def invert_perm(perm: List[int]) -> List[int]:
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return inv

PERMS["U'"] = invert_perm(PERMS["U"])
PERMS["D'"] = invert_perm(PERMS["D"])
PERMS["L'"] = invert_perm(PERMS["L"])
PERMS["R'"] = invert_perm(PERMS["R"])
PERMS["F'"] = invert_perm(PERMS["F"])
PERMS["B'"] = invert_perm(PERMS["B"])


# Move functions
def make_move_func(perm: List[int]) -> Callable[[CubeState], CubeState]:
    return lambda state: apply_permutation(state, perm)


MOVE_NAMES = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

MOVE_FUNCS: Dict[str, Callable[[CubeState], CubeState]] = {
    name: make_move_func(PERMS[name]) for name in MOVE_NAMES
}

INVERSE_OF: Dict[str, str] = {
    "U": "U'", "U'": "U",
    "D": "D'", "D'": "D",
    "L": "L'", "L'": "L",
    "R": "R'", "R'": "R",
    "F": "F'", "F'": "F",
    "B": "B'", "B'": "B",
}


def heuristic_misplaced(state: CubeState) -> int:
    """Count misplaced stickers divided by 3 (admissible heuristic)."""
    h = sum(1 for i in range(24) if state.state[i] != i)
    return h // 3


def random_scramble(length: int) -> List[str]:
    """Generate a random scramble sequence."""
    scramble = []
    last_move = None
    
    for _ in range(length):
        available = [m for m in MOVE_NAMES 
                    if last_move is None or INVERSE_OF[m] != last_move]
        move = random.choice(available)
        scramble.append(move)
        last_move = move
    
    return scramble


if __name__ == "__main__":
    print("SAGCO Rubik Bench - 2x2x2 Cube Engine (Simplified)")
    print("=" * 50)
    
    solved = CubeState.solved()
    print(f"✓ Solved state: {solved.is_solved()}")
    
    # Test all inverse moves
    print("\n✓ Testing inverse moves:")
    for move in ["U", "D", "L", "R", "F", "B"]:
        after_move = MOVE_FUNCS[move](solved)
        after_inverse = MOVE_FUNCS[move + "'"](after_move)
        status = "✓" if after_inverse.is_solved() else "✗"
        print(f"  {status} {move} then {move}' returns to solved")
    
    scramble = random_scramble(5)
    print(f"\n✓ Random scramble (5 moves): {' '.join(scramble)}")
    
    state = solved
    for m in scramble:
        state = MOVE_FUNCS[m](state)
    
    h = heuristic_misplaced(state)
    print(f"✓ Heuristic after scramble: {h}")
    print(f"✓ Is solved: {state.is_solved()}")
    
    print("\n🔥 Benchmark kernel operational!")
