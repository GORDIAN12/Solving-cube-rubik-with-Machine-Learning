import copy
import math
import numpy as np
import torch

from .actions import IDX_TO_ACTION

@torch.no_grad()
def _policy_probs(model, state54: np.ndarray, device):
    """
    state54: np.array shape (54,) dtype int (0..5)
    returns: np.array shape (12,) probs
    """
    x = torch.from_numpy(state54.astype(np.int64)).unsqueeze(0).to(device)  # (1,54)
    logits = model(x)[0]  # (12,)
    probs = torch.softmax(logits, dim=0).cpu().numpy()
    return probs

def beam_solve(
    sim,
    model,
    max_steps=40,
    beam_width=50,
    topk=6,
    avoid_immediate_inverse=False,
    inv_map=None,
):
    """
    sim: RubikSim instance (must support copy via deepcopy OR provide sim.copy())
         required methods/attrs:
           - sim.state -> np.array (54,)
           - sim.apply(move_str)
           - sim.is_solved() -> bool
    model: PyTorch policy network that outputs logits over 12 actions.

    Returns:
      list[str] moves if solved else None
    """
    device = next(model.parameters()).device

    # beam entries: (score, sim_state, moves_list)
    # score = sum log(prob(action_t))
    start_sim = copy.deepcopy(sim)
    beam = [(0.0, start_sim, [])]

    for _ in range(max_steps):
        new_beam = []

        for score, s, moves in beam:
            if s.is_solved():
                return moves

            probs = _policy_probs(model, s.state, device)
            best_actions = np.argsort(probs)[::-1][:topk]

            last_move = moves[-1] if moves else None

            for a in best_actions:
                move = IDX_TO_ACTION[int(a)]

                # opcional: evitar deshacer inmediatamente el último movimiento (ej R seguido de R')
                if avoid_immediate_inverse and last_move and inv_map:
                    if inv_map.get(last_move) == move:
                        continue

                s2 = copy.deepcopy(s)
                s2.apply(move)

                # acumulamos log prob
                score2 = score + math.log(float(probs[a]) + 1e-12)
                new_beam.append((score2, s2, moves + [move]))

        if not new_beam:
            return None

        # quedarnos con las mejores rutas
        new_beam.sort(key=lambda t: t[0], reverse=True)
        beam = new_beam[:beam_width]

    return None
