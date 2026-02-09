import torch
from ML.ida_star import ida_star
from ML.train_model import HeuristicNet

ALL_MOVES = [
    "U","U'","U2","D","D'","D2","L","L'","L2",
    "R","R'","R2","F","F'","F2","B","B'","B2"
]

device = "cuda" if torch.cuda.is_available() else "cpu"

_ckpt = torch.load("ML/heuristic.pt", map_location=device)
N = _ckpt["N"]
out_classes = N + 1  # porque tu train_heuristic original usa N+1 clases
_model = HeuristicNet(in_dim=54*6, out_classes=out_classes).to(device)
_model.load_state_dict(_ckpt["state_dict"])
_model.eval()


def solve_state(state):
    """Recibe np.array (54,) y devuelve lista de movimientos."""
    return ida_star(state, ALL_MOVES, _model, device=device, verbose=True)
