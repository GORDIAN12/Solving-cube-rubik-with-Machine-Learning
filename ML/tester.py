from ML.train_model import train_heuristic
from scramble import move_scram
from ML.gen_data import generate_dataset  # ajusta al nombre real
import torch
from ML.ida_star import ida_star
import numpy as np
# 1) lista fija de acciones compatibles con tu parser
all_moves = [
    "U","U'","U2",
    "D","D'","D2",
    "L","L'","L2",
    "R","R'","R2",
    "F","F'","F2",
    "B","B'","B2"
]

N = 15
X, y = generate_dataset(all_moves, N=N, samples=100000, seed=0)

device = "cuda" if torch.cuda.is_available() else "cpu"
print("== INICIO ==")

# entrenamiento
model = train_heuristic(X, y, N=N, epochs=30, device=device)
print("== ENTRENAMIENTO TERMINADO ==")

# scramble
scramble = move_scram.generate_movs(5)
if isinstance(scramble, list):
    scramble = " ".join(scramble)

print("scramble:", scramble)

state = move_scram.apply_scramble(
    move_scram.SOLVED_STATE.copy(),
    scramble,
    move_scram.PERM
)
print("estado listo")

print("== INICIANDO IDA* ==")
sol = ida_star(state, all_moves, model, device=device)

print("== IDA* TERMINÓ ==")
print("sol:", sol)

test = state.copy()
for m in sol:
    test = move_scram.apply_scramble(test, m, move_scram.PERM)

print("¿Resuelto?", np.array_equal(test, move_scram.SOLVED_STATE))