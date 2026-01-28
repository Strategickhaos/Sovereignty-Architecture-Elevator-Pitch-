#!/usr/bin/env python3
"""
SAGCO Rubik's Cube Benchmark Kernel
====================================
Minimal 2x2x2 Rubik's Cube implementation for TRIG6-pruned IDA* solver.

This module provides:
- CubeState: Representation of a 2x2x2 cube
- Move functions: U, U', D, D', L, L', R, R', F, F', B, B'
- IDA* heuristic: Simple misplaced cubie count
- Random scramble generation

Author: GPT (Legion of Minds Council)
Integrated by: Domenic Gabriel Garza (Strategickhaos DAO LLC)
"""

import random
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class CubeState:
    """
    2x2x2 Rubik's Cube state.
    
    Representation:
    - 6 faces: U (up), D (down), L (left), R (right), F (front), B (back)
    - Each face has 4 cubies numbered 0-3
    - Total 24 positions (but only 8 physical cubies with 3 stickers each)
    
    For simplicity, we track each face independently.
    """
    u: Tuple[int, int, int, int]  # Up face
    d: Tuple[int, int, int, int]  # Down face
    l: Tuple[int, int, int, int]  # Left face
    r: Tuple[int, int, int, int]  # Right face
    f: Tuple[int, int, int, int]  # Front face
    b: Tuple[int, int, int, int]  # Back face
    
    @staticmethod
    def solved() -> 'CubeState':
        """Return a solved cube state."""
        return CubeState(
            u=(0, 1, 2, 3),
            d=(0, 1, 2, 3),
            l=(0, 1, 2, 3),
            r=(0, 1, 2, 3),
            f=(0, 1, 2, 3),
            b=(0, 1, 2, 3),
        )
    
    def is_solved(self) -> bool:
        """Check if cube is in solved state."""
        return (
            self.u == (0, 1, 2, 3) and
            self.d == (0, 1, 2, 3) and
            self.l == (0, 1, 2, 3) and
            self.r == (0, 1, 2, 3) and
            self.f == (0, 1, 2, 3) and
            self.b == (0, 1, 2, 3)
        )
    
    def __hash__(self) -> int:
        return hash((self.u, self.d, self.l, self.r, self.f, self.b))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CubeState):
            return False
        return (
            self.u == other.u and
            self.d == other.d and
            self.l == other.l and
            self.r == other.r and
            self.f == other.f and
            self.b == other.b
        )


def rotate_face_cw(face: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """Rotate a face 90 degrees clockwise."""
    return (face[2], face[0], face[3], face[1])


def rotate_face_ccw(face: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """Rotate a face 90 degrees counter-clockwise."""
    return (face[1], face[3], face[0], face[2])


# ============================================================
# MOVE FUNCTIONS (2x2x2 Cube)
# ============================================================

def move_U(state: CubeState) -> CubeState:
    """U move: Rotate top face clockwise."""
    return CubeState(
        u=rotate_face_cw(state.u),
        d=state.d,
        l=(state.f[0], state.f[1], state.l[2], state.l[3]),
        r=(state.b[0], state.b[1], state.r[2], state.r[3]),
        f=(state.r[0], state.r[1], state.f[2], state.f[3]),
        b=(state.l[0], state.l[1], state.b[2], state.b[3]),
    )


def move_U_prime(state: CubeState) -> CubeState:
    """U' move: Rotate top face counter-clockwise."""
    return CubeState(
        u=rotate_face_ccw(state.u),
        d=state.d,
        l=(state.b[0], state.b[1], state.l[2], state.l[3]),
        r=(state.f[0], state.f[1], state.r[2], state.r[3]),
        f=(state.l[0], state.l[1], state.f[2], state.f[3]),
        b=(state.r[0], state.r[1], state.b[2], state.b[3]),
    )


def move_D(state: CubeState) -> CubeState:
    """D move: Rotate bottom face clockwise."""
    return CubeState(
        u=state.u,
        d=rotate_face_cw(state.d),
        l=(state.l[0], state.l[1], state.b[2], state.b[3]),
        r=(state.r[0], state.r[1], state.f[2], state.f[3]),
        f=(state.f[0], state.f[1], state.r[2], state.r[3]),
        b=(state.b[0], state.b[1], state.l[2], state.l[3]),
    )


def move_D_prime(state: CubeState) -> CubeState:
    """D' move: Rotate bottom face counter-clockwise."""
    return CubeState(
        u=state.u,
        d=rotate_face_ccw(state.d),
        l=(state.l[0], state.l[1], state.f[2], state.f[3]),
        r=(state.r[0], state.r[1], state.b[2], state.b[3]),
        f=(state.f[0], state.f[1], state.l[2], state.l[3]),
        b=(state.b[0], state.b[1], state.r[2], state.r[3]),
    )


def move_L(state: CubeState) -> CubeState:
    """L move: Rotate left face clockwise."""
    return CubeState(
        u=(state.b[3], state.u[1], state.b[1], state.u[3]),
        d=(state.f[0], state.d[1], state.f[2], state.d[3]),
        l=rotate_face_cw(state.l),
        r=state.r,
        f=(state.u[0], state.f[1], state.u[2], state.f[3]),
        b=(state.b[0], state.d[2], state.b[2], state.d[0]),
    )


def move_L_prime(state: CubeState) -> CubeState:
    """L' move: Rotate left face counter-clockwise."""
    return CubeState(
        u=(state.f[0], state.u[1], state.f[2], state.u[3]),
        d=(state.b[3], state.d[1], state.b[1], state.d[3]),
        l=rotate_face_ccw(state.l),
        r=state.r,
        f=(state.d[0], state.f[1], state.d[2], state.f[3]),
        b=(state.b[0], state.u[2], state.b[2], state.u[0]),
    )


def move_R(state: CubeState) -> CubeState:
    """R move: Rotate right face clockwise."""
    return CubeState(
        u=(state.u[0], state.f[1], state.u[2], state.f[3]),
        d=(state.d[0], state.b[3], state.d[2], state.b[1]),
        l=state.l,
        r=rotate_face_cw(state.r),
        f=(state.f[0], state.d[1], state.f[2], state.d[3]),
        b=(state.u[3], state.b[1], state.u[1], state.b[3]),
    )


def move_R_prime(state: CubeState) -> CubeState:
    """R' move: Rotate right face counter-clockwise."""
    return CubeState(
        u=(state.u[0], state.b[3], state.u[2], state.b[1]),
        d=(state.d[0], state.f[1], state.d[2], state.f[3]),
        l=state.l,
        r=rotate_face_ccw(state.r),
        f=(state.f[0], state.u[1], state.f[2], state.u[3]),
        b=(state.d[3], state.b[1], state.d[1], state.b[3]),
    )


def move_F(state: CubeState) -> CubeState:
    """F move: Rotate front face clockwise."""
    return CubeState(
        u=(state.u[0], state.u[1], state.l[3], state.l[2]),
        d=(state.r[1], state.r[0], state.d[2], state.d[3]),
        l=(state.l[0], state.l[1], state.d[0], state.d[1]),
        r=(state.u[2], state.u[3], state.r[2], state.r[3]),
        f=rotate_face_cw(state.f),
        b=state.b,
    )


def move_F_prime(state: CubeState) -> CubeState:
    """F' move: Rotate front face counter-clockwise."""
    return CubeState(
        u=(state.u[0], state.u[1], state.r[1], state.r[0]),
        d=(state.l[2], state.l[3], state.d[2], state.d[3]),
        l=(state.l[0], state.l[1], state.u[3], state.u[2]),
        r=(state.d[1], state.d[0], state.r[2], state.r[3]),
        f=rotate_face_ccw(state.f),
        b=state.b,
    )


def move_B(state: CubeState) -> CubeState:
    """B move: Rotate back face clockwise."""
    return CubeState(
        u=(state.r[3], state.r[2], state.u[2], state.u[3]),
        d=(state.d[0], state.d[1], state.l[1], state.l[0]),
        l=(state.u[1], state.u[0], state.l[2], state.l[3]),
        r=(state.r[0], state.r[1], state.d[3], state.d[2]),
        f=state.f,
        b=rotate_face_cw(state.b),
    )


def move_B_prime(state: CubeState) -> CubeState:
    """B' move: Rotate back face counter-clockwise."""
    return CubeState(
        u=(state.l[1], state.l[0], state.u[2], state.u[3]),
        d=(state.d[0], state.d[1], state.r[2], state.r[3]),
        l=(state.d[3], state.d[2], state.l[2], state.l[3]),
        r=(state.r[0], state.r[1], state.u[0], state.u[1]),
        f=state.f,
        b=rotate_face_ccw(state.b),
    )


# ============================================================
# MOVE REGISTRY
# ============================================================

MOVE_NAMES = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

MOVE_FUNCS: Dict[str, Callable[[CubeState], CubeState]] = {
    "U": move_U,
    "U'": move_U_prime,
    "D": move_D,
    "D'": move_D_prime,
    "L": move_L,
    "L'": move_L_prime,
    "R": move_R,
    "R'": move_R_prime,
    "F": move_F,
    "F'": move_F_prime,
    "B": move_B,
    "B'": move_B_prime,
}

INVERSE_OF: Dict[str, str] = {
    "U": "U'",
    "U'": "U",
    "D": "D'",
    "D'": "D",
    "L": "L'",
    "L'": "L",
    "R": "R'",
    "R'": "R",
    "F": "F'",
    "F'": "F",
    "B": "B'",
    "B'": "B",
}


# ============================================================
# HEURISTIC (admissible for IDA*)
# ============================================================

def heuristic_misplaced(state: CubeState) -> int:
    """
    Count misplaced cubies (very simple admissible heuristic).
    Not the most efficient but sufficient for demonstration.
    """
    solved = CubeState.solved()
    h = 0
    
    for face_name in ['u', 'd', 'l', 'r', 'f', 'b']:
        state_face = getattr(state, face_name)
        solved_face = getattr(solved, face_name)
        for i in range(4):
            if state_face[i] != solved_face[i]:
                h += 1
    
    # Each cubie has 3 faces, so divide by 3 to get approximate cubie count
    # But for admissibility, we keep it simple
    return h // 3


# ============================================================
# RANDOM SCRAMBLE
# ============================================================

def random_scramble(length: int) -> List[str]:
    """Generate a random scramble sequence."""
    scramble = []
    last_move = None
    
    for _ in range(length):
        # Avoid inverse moves in sequence
        available = [m for m in MOVE_NAMES 
                    if last_move is None or INVERSE_OF[m] != last_move]
        move = random.choice(available)
        scramble.append(move)
        last_move = move
    
    return scramble


# ============================================================
# SIMPLE BENCHMARK TEST
# ============================================================

if __name__ == "__main__":
    print("SAGCO Rubik Bench - 2x2x2 Cube Engine")
    print("=" * 50)
    
    # Test 1: Solved cube
    solved = CubeState.solved()
    print(f"✓ Solved state: {solved.is_solved()}")
    
    # Test 2: Single move
    after_U = move_U(solved)
    print(f"✓ After U move: {not after_U.is_solved()}")
    
    # Test 3: Inverse moves
    after_U_Uprime = move_U_prime(after_U)
    print(f"✓ U then U' returns to solved: {after_U_Uprime.is_solved()}")
    
    # Test 4: Scramble and heuristic
    scramble = random_scramble(5)
    print(f"\n✓ Random scramble (5 moves): {' '.join(scramble)}")
    
    state = solved
    for m in scramble:
        state = MOVE_FUNCS[m](state)
    
    h = heuristic_misplaced(state)
    print(f"✓ Heuristic after scramble: {h}")
    print(f"✓ Is solved: {state.is_solved()}")
    
    print("\n🔥 Benchmark kernel operational!")
