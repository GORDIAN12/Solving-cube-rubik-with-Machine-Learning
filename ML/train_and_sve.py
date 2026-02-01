import torch
from ML.train_model import train_heuristic
from ML.gen_data import generate_dataset

ALL_MOVES = [
    "U","U'","U2","D","D'","D2","L","L'","L2",
    "R","R'","R2","F","F'","F2","B","B'","B2"
]

N = 15
X, y = generate_dataset(ALL_MOVES, N=N, samples=100000, seed=0)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = train_heuristic(X, y, N=N, epochs=30, device=device)

# ✅ guarda pesos + N (para reconstruir)
torch.save({"state_dict": model.state_dict(), "N": N}, "heuristic.pt")
print("Modelo guardado en heuristic.pt")
