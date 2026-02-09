import numpy as np

ACTIONS = ["U","U'","D","D'","L","L'","R","R'","F","F'","B","B'"]

def is_solved(state: np.ndarray, SOLVED_STATE: np.ndarray) -> bool:
    return np.array_equal(state, SOLVED_STATE)

def step(state: np.ndarray, action: str, PERM: dict) -> np.ndarray:

    face = action[0]
    turns = 3 if action.endswith("'") else 1  # ' = 3 giros de 90°
    out = state
    for _ in range(turns):
        out = out[PERM[face]]
    return out

def iddfs_solve(start_state: np.ndarray, PERM: dict, SOLVED_STATE: np.ndarray, max_depth: int = 10):
    def inverse_action(a):
        return a[:-1] if a.endswith("'") else a + "'"
    """
    Devuelve una lista de acciones (ej: ["R", "U'", "F"]) o None si no encontró.
    """
    def dfs(state, depth, last_action, path):
        if is_solved(state, SOLVED_STATE):
            return path
        if depth == 0:
            return None

        for a in ACTIONS:
            if last_action is not None and a ==inverse_action(last_action):
                continue

            nxt = step(state, a, PERM)
            res = dfs(nxt, depth - 1, a, path + [a])
            if res is not None:
                return res
        return None

    for d in range(max_depth + 1):
        res = dfs(start_state, d, None, [])
        if res is not None:
            return res
    return None