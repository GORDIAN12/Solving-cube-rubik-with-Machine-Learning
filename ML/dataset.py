import random
import numpy as np
import torch
from torch.utils.data import Dataset
from .actions import ACTIONS, ACTION_TO_IDX, INV

class RubikImitationDataset(Dataset):
    def __init__(self, sim_factory, n_episodes=20000, max_scramble=10):
        X, y = [], []

        for _ in range(n_episodes):
            sim = sim_factory()
            sim.reset()

            k = random.randint(1, max_scramble)
            moves = [random.choice(ACTIONS) for _ in range(k)]

            for m in moves:
                # input: estado actual (antes del scramble move)
                X.append(sim.state.copy())

                # label: el movimiento que lo "deshace"
                y.append(ACTION_TO_IDX[INV[m]])

                # avanzar en scramble
                sim.apply(m)

        self.X = np.stack(X).astype(np.int64)  # (N,54)
        self.y = np.array(y).astype(np.int64)  # (N,)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        return torch.from_numpy(self.X[i]), torch.tensor(self.y[i])
