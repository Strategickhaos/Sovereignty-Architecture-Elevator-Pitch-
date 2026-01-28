#!/usr/bin/env python3
"""
STRATEGICKHAOS SAGCO-RUBIK TRIG6 BENCHMARK
==========================================

Core goals in this file:

1. Cube core:
   - Facelet-based 3x3x3 cube (54 stickers).
   - 18 moves: U, U2, U', D, D2, D', R, R2, R', L, L2, L',
                F, F2, F', B, B2, B'.

2. Two solvers (same algorithm, different pruning):
   - baseline_ida_solve: pure IDA* with a simple heuristic.
   - trig6_ida_solve   : same IDA* + TRIG6-based pruning.

3. Benchmark harness:
   - Generate N random scrambles of length K.
   - Solve with both solvers.
   - Print timing + node counts + average speedup.

This is *not* tuned to be a production cube solver; it's a
reference implementation to measure the architectural effect
of TRIG6 pruning vs a baseline search on the same code.

Author: Domenic Gabriel Garza (Strategickhaos DAO LLC)
"""

import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Optional

# ============================================================
# TRIG6 CORE
# ============================================================

PI = math.pi
EPS = 1e-12

def trig6(theta: float) -> List[float]:
    """Return [sin, cos, tan, csc, sec, cot] with singularities as inf."""
    s = math.sin(theta)
    c = math.cos(theta)
    t  = s / c if abs(c) > EPS else float("inf")
    cs = 1 / s if abs(s) > EPS else float("inf")
    sc = 1 / c if abs(c) > EPS else float("inf")
    ct = c / s if abs(s) > EPS else float("inf")
    return [s, c, t, cs, sc, ct]

def trig6_norm_sq(theta: float) -> float:
    v = trig6(theta)
    return sum(x * x for x in v if abs(x) < 1e10)


# ============================================================
# CUBE CORE (FACELET REPRESENTATION)
# ============================================================

FACE_NAMES = ["U", "R", "F", "D", "L", "B"]

@dataclass(frozen=True)
class CubeState:
    stickers: Tuple[int, ...]  # length 54

    def is_solved(self) -> bool:
        """All 9 stickers of each face have the same color index."""
        for f in range(6):
            face = self.stickers[9*f:9*f+9]
            if len(set(face)) != 1:
                return False
        return True

    @staticmethod
    def solved() -> "CubeState":
        """Canonical solved cube: face f has color f."""
        arr = []
        for f in range(6):
            arr.extend([f] * 9)
        return CubeState(tuple(arr))


# ------------------------------------------------------------
# Move definitions
# ------------------------------------------------------------

ROT_CW = [6, 3, 0, 7, 4, 1, 8, 5, 2]
ROT_CCW = [2, 5, 8, 1, 4, 7, 0, 3, 6]

def rotate_face(face_vals: List[int], cw: bool = True) -> List[int]:
    mapping = ROT_CW if cw else ROT_CCW
    return [face_vals[mapping[i]] for i in range(9)]

def make_move_functions() -> Dict[str, Callable[[CubeState], CubeState]]:
    """Define 6 basic quarter-turn moves and derive the 18-move set."""

    def clone(stickers: Tuple[int, ...]) -> List[int]:
        return list(stickers)

    def move_U(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        u_indices = [0,1,2,3,4,5,6,7,8]
        u_vals = [s[i] for i in u_indices]
        u_rot = rotate_face(u_vals, cw=True)
        for i, idx in enumerate(u_indices):
            s[idx] = u_rot[i]
        f_row = [s[18], s[19], s[20]]
        r_row = [s[9],  s[10], s[11]]
        b_row = [s[45], s[46], s[47]]
        l_row = [s[36], s[37], s[38]]
        s[9:12]   = f_row
        s[45:48]  = r_row
        s[36:39]  = b_row
        s[18:21]  = l_row
        return CubeState(tuple(s))

    def move_D(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        d_indices = [27,28,29,30,31,32,33,34,35]
        d_vals = [s[i] for i in d_indices]
        d_rot = rotate_face(d_vals, cw=True)
        for i, idx in enumerate(d_indices):
            s[idx] = d_rot[i]
        f_row = [s[24], s[25], s[26]]
        l_row = [s[42], s[43], s[44]]
        b_row = [s[51], s[52], s[53]]
        r_row = [s[15], s[16], s[17]]
        s[42:45]  = f_row
        s[51:54]  = l_row
        s[15:18]  = b_row
        s[24:27]  = r_row
        return CubeState(tuple(s))

    def move_R(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        r_indices = [9,10,11,12,13,14,15,16,17]
        r_vals = [s[i] for i in r_indices]
        r_rot = rotate_face(r_vals, cw=True)
        for i, idx in enumerate(r_indices):
            s[idx] = r_rot[i]
        u_pos = [2,5,8]
        f_pos = [20,23,26]
        d_pos = [29,32,35]
        b_pos = [47,50,53]
        u_vals = [s[i] for i in u_pos]
        f_vals = [s[i] for i in f_pos]
        d_vals = [s[i] for i in d_pos]
        b_vals = [s[i] for i in b_pos]
        for i, idx in enumerate(f_pos):
            s[idx] = u_vals[i]
        for i, idx in enumerate(d_pos):
            s[idx] = f_vals[i]
        for i, idx in enumerate(b_pos):
            s[idx] = d_vals[2 - i]
        for i, idx in enumerate(u_pos):
            s[idx] = b_vals[2 - i]
        return CubeState(tuple(s))

    def move_L(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        l_indices = [36,37,38,39,40,41,42,43,44]
        l_vals = [s[i] for i in l_indices]
        l_rot = rotate_face(l_vals, cw=True)
        for i, idx in enumerate(l_indices):
            s[idx] = l_rot[i]
        u_pos = [0,3,6]
        f_pos = [18,21,24]
        d_pos = [27,30,33]
        b_pos = [45+8,45+5,45+2]
        u_vals = [s[i] for i in u_pos]
        f_vals = [s[i] for i in f_pos]
        d_vals = [s[i] for i in d_pos]
        b_vals = [s[i] for i in b_pos]
        for i, idx in enumerate(b_pos):
            s[idx] = u_vals[2 - i]
        for i, idx in enumerate(d_pos):
            s[idx] = b_vals[2 - i]
        for i, idx in enumerate(f_pos):
            s[idx] = d_vals[i]
        for i, idx in enumerate(u_pos):
            s[idx] = f_vals[i]
        return CubeState(tuple(s))

    def move_F(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        f_indices = [18,19,20,21,22,23,24,25,26]
        f_vals = [s[i] for i in f_indices]
        f_rot = rotate_face(f_vals, cw=True)
        for i, idx in enumerate(f_indices):
            s[idx] = f_rot[i]
        u_pos = [6,7,8]
        r_pos = [9,12,15]
        d_pos = [29,28,27]
        l_pos = [44,41,38]
        u_vals = [s[i] for i in u_pos]
        r_vals = [s[i] for i in r_pos]
        d_vals = [s[i] for i in d_pos]
        l_vals = [s[i] for i in l_pos]
        for i, idx in enumerate(r_pos):
            s[idx] = u_vals[i]
        for i, idx in enumerate(d_pos):
            s[idx] = r_vals[i]
        for i, idx in enumerate(l_pos):
            s[idx] = d_vals[i]
        for i, idx in enumerate(u_pos):
            s[idx] = l_vals[i]
        return CubeState(tuple(s))

    def move_B(c: CubeState) -> CubeState:
        s = clone(c.stickers)
        b_indices = [45,46,47,48,49,50,51,52,53]
        b_vals = [s[i] for i in b_indices]
        b_rot = rotate_face(b_vals, cw=True)
        for i, idx in enumerate(b_indices):
            s[idx] = b_rot[i]
        u_pos = [0,1,2]
        l_pos = [36,39,42]
        d_pos = [35,34,33]
        r_pos = [17,14,11]
        u_vals = [s[i] for i in u_pos]
        l_vals = [s[i] for i in l_pos]
        d_vals = [s[i] for i in d_pos]
        r_vals = [s[i] for i in r_pos]
        for i, idx in enumerate(l_pos):
            s[idx] = u_vals[i]
        for i, idx in enumerate(d_pos):
            s[idx] = l_vals[i]
        for i, idx in enumerate(r_pos):
            s[idx] = d_vals[i]
        for i, idx in enumerate(u_pos):
            s[idx] = r_vals[i]
        return CubeState(tuple(s))

    base_moves: Dict[str, Callable[[CubeState], CubeState]] = {
        "U": move_U, "D": move_D, "R": move_R,
        "L": move_L, "F": move_F, "B": move_B,
    }

    moves: Dict[str, Callable[[CubeState], CubeState]] = {}

    def compose(m1, m2):
        return lambda c: m1(m2(c))

    for name, fn in base_moves.items():
        moves[name] = fn
        moves[name + "2"] = compose(fn, fn)
        moves[name + "'"] = compose(fn, compose(fn, fn))

    return moves


MOVE_FUNCS = make_move_functions()
MOVE_NAMES: List[str] = list(MOVE_FUNCS.keys())
MOVE_NAMES.sort(key=lambda s: "UDRLFB".index(s[0]) * 3 + ("", "2", "'").index(s[1:] or ""))

FACE_INDEX = {name: "UDRLFB".index(name[0]) for name in MOVE_NAMES}
INVERSE_OF: Dict[str, str] = {
    "U": "U'", "U'": "U", "U2": "U2",
    "D": "D'", "D'": "D", "D2": "D2",
    "R": "R'", "R'": "R", "R2": "R2",
    "L": "L'", "L'": "L", "L2": "L2",
    "F": "F'", "F'": "F", "F2": "F2",
    "B": "B'", "B'": "B", "B2": "B2",
}


# ============================================================
# HEURISTIC
# ============================================================

def heuristic_misplaced(c: CubeState) -> int:
    """Count misplaced facelets divided by 8."""
    h = 0
    for f in range(6):
        face_offset = 9 * f
        center_color = c.stickers[face_offset + 4]
        for i in range(9):
            if c.stickers[face_offset + i] != center_color:
                h += 1
    return h // 8


# ============================================================
# IDA* FRAMEWORK
# ============================================================

@dataclass
class SearchStats:
    nodes_expanded: int = 0

def ida_search(
    start: CubeState,
    max_depth: int,
    use_trig6: bool = False,
) -> Tuple[Optional[List[str]], SearchStats]:
    """IDA* from start up to max_depth."""

    stats = SearchStats()

    def trig6_prune(depth: int, move_idx: int, last_move: Optional[str]) -> bool:
        name = MOVE_NAMES[move_idx]
        if last_move is not None:
            if INVERSE_OF[name] == last_move:
                return True
        theta = depth * PI / 32.0 + move_idx * PI / 18.0
        t6 = trig6(theta)
        ns = sum(x*x for x in t6 if abs(x) < 1e10)
        if abs(t6[2]) > 10.0:
            return True
        if ns > 50.0:
            return True
        return False

    def search(node: CubeState, g: int, bound: int, path: List[str], last_move: Optional[str]) -> Tuple[int, Optional[List[str]]]:
        stats.nodes_expanded += 1
        f = g + heuristic_misplaced(node)
        if f > bound:
            return f, None
        if node.is_solved():
            return f, list(path)
        if g == max_depth:
            return float("inf"), None

        min_bound = float("inf")

        for mi, move_name in enumerate(MOVE_NAMES):
            if use_trig6 and trig6_prune(g, mi, last_move):
                continue

            next_state = MOVE_FUNCS[move_name](node)
            path.append(move_name)
            t, res_path = search(next_state, g + 1, bound, path, move_name)
            if res_path is not None:
                return t, res_path
            path.pop()
            if t < min_bound:
                min_bound = t

        return min_bound, None

    bound = heuristic_misplaced(start)
    while bound <= max_depth:
        t, res = search(start, 0, bound, [], None)
        if res is not None:
            return res, stats
        if t == float("inf"):
            break
        bound = int(t)
    return None, stats

def baseline_ida_solve(start: CubeState, max_depth: int) -> Tuple[Optional[List[str]], SearchStats]:
    return ida_search(start, max_depth=max_depth, use_trig6=False)

def trig6_ida_solve(start: CubeState, max_depth: int) -> Tuple[Optional[List[str]], SearchStats]:
    return ida_search(start, max_depth=max_depth, use_trig6=True)


# ============================================================
# SCRAMBLE / BENCHMARK HARNESS
# ============================================================

def apply_sequence(state: CubeState, seq: List[str]) -> CubeState:
    s = state
    for m in seq:
        s = MOVE_FUNCS[m](s)
    return s

def random_scramble(length: int = 8) -> List[str]:
    """Generate a random sequence of moves."""
    scramble: List[str] = []
    last_move: Optional[str] = None
    for _ in range(length):
        candidates = MOVE_NAMES.copy()
        if last_move is not None:
            inv = INVERSE_OF[last_move]
            candidates = [m for m in candidates if m != inv]
        move = random.choice(candidates)
        scramble.append(move)
        last_move = move
    return scramble

def benchmark(
    num_scrambles: int = 20,
    scramble_len: int = 8,
    max_depth: int = 12,
    seed: int = 42,
) -> None:
    random.seed(seed)

    base_times: List[float] = []
    trig_times: List[float] = []
    base_nodes: List[int] = []
    trig_nodes: List[int] = []

    print(f"Running benchmark: {num_scrambles} scrambles, length={scramble_len}, max_depth={max_depth}")
    for i in range(num_scrambles):
        scramble = random_scramble(scramble_len)
        start = apply_sequence(CubeState.solved(), scramble)

        print(f"\n[{i+1}/{num_scrambles}] Scramble: {' '.join(scramble)}")

        t0 = time.perf_counter()
        sol_base, stats_base = baseline_ida_solve(start, max_depth=max_depth)
        t1 = time.perf_counter()
        base_ms = (t1 - t0) * 1000.0

        t2 = time.perf_counter()
        sol_trig, stats_trig = trig6_ida_solve(start, max_depth=max_depth)
        t3 = time.perf_counter()
        trig_ms = (t3 - t2) * 1000.0

        base_times.append(base_ms)
        trig_times.append(trig_ms)
        base_nodes.append(stats_base.nodes_expanded)
        trig_nodes.append(stats_trig.nodes_expanded)

        print(f"  Baseline: time={base_ms:.2f} ms, nodes={stats_base.nodes_expanded}, solved={sol_base is not None}")
        print(f"  TRIG6   : time={trig_ms:.2f} ms, nodes={stats_trig.nodes_expanded}, solved={sol_trig is not None}")

    def avg(xs):
        return sum(xs) / len(xs) if xs else 0.0

    avg_base_t = avg(base_times)
    avg_trig_t = avg(trig_times)
    avg_base_n = avg(base_nodes)
    avg_trig_n = avg(trig_nodes)

    print("\n===== SUMMARY =====")
    print(f"Average Baseline time: {avg_base_t:.2f} ms")
    print(f"Average TRIG6 time   : {avg_trig_t:.2f} ms")
    if avg_trig_t > 0:
        print(f"Time speedup (baseline / TRIG6): {avg_base_t / avg_trig_t:.2f}x")
    print(f"Average Baseline nodes: {avg_base_n:.1f}")
    print(f"Average TRIG6 nodes   : {avg_trig_n:.1f}")
    if avg_trig_n > 0:
        print(f"Node expansion reduction: {avg_base_n / avg_trig_n:.2f}x")


if __name__ == "__main__":
    benchmark(num_scrambles=10, scramble_len=7, max_depth=10, seed=2026)
