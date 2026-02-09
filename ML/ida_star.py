import math
import numpy as np
from ML.gen_data import apply_one_move
from scramble import move_scram
from ML.train_model import h_model
from ML import gen_data

def ida_star(start_state, all_moves, model, max_iters=50, device="cpu", verbose=False):
    # Cache: estado (bytes) -> heurística h
    h_cache = {}

    def H(state):
        key = state.tobytes()
        v = h_cache.get(key)
        if v is None:
            v = h_model(model, state, device=device)
            h_cache[key] = v
        return v

    bound = H(start_state)

    # (Opcional) contador para stats
    nodes = 0

    def search(state, g, bound, last_move):
        nonlocal nodes
        nodes += 1

        h = H(state)
        f = g + h

        if f > bound:
            return f, None

        if np.array_equal(state, move_scram.SOLVED_STATE):
            return f, []

        min_bound = math.inf
        for m in gen_data.filtered_moves(all_moves, last_move):
            nxt = apply_one_move(state, m)
            t, sol = search(nxt, g + 1, bound, m)

            if sol is not None:
                return t, [m] + sol

            if t < min_bound:
                min_bound = t

        return min_bound, None

    for it in range(1, max_iters + 1):
        nodes = 0
        t, sol = search(start_state, 0, bound, None)

        if verbose:
            print(f"[IDA*] iter={it} bound={bound} nodes={nodes} cache={len(h_cache)}", flush=True)

        if sol is not None:
            return sol
        if t == math.inf:
            return None
        bound = t

    return None
