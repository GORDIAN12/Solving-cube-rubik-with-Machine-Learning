import torch
from rubik_sim import RubikSim
from ml.model import PolicyNet
from ml.solver import beam_solve
from ml.actions import INV  # si quieres evitar inversos inmediatos

sim = RubikSim()
sim.reset(scramble_k=8)  # o como lo tengas

model = PolicyNet()
model.load_state_dict(torch.load("policy.pt", map_location="cpu"))
model.eval()

solution = beam_solve(
    sim,
    model,
    max_steps=40,
    beam_width=80,
    topk=6,
    avoid_immediate_inverse=True,
    inv_map=INV,
)

print(solution)
