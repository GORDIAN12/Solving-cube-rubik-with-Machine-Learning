import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from .dataset import RubikImitationDataset
from .model import PolicyNet

def train_policy(sim_factory, max_scramble=10, n_episodes=20000, epochs=10):
    ds = RubikImitationDataset(sim_factory, n_episodes=n_episodes, max_scramble=max_scramble)
    dl = DataLoader(ds, batch_size=512, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PolicyNet().to(device)

    opt = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(1, epochs+1):
        model.train()
        total, correct, loss_sum = 0, 0, 0.0

        for X, y in dl:
            X, y = X.to(device), y.to(device)

            logits = model(X)
            loss = loss_fn(logits, y)

            opt.zero_grad()
            loss.backward()
            opt.step()

            loss_sum += loss.item() * X.size(0)
            correct += (logits.argmax(1) == y).sum().item()
            total += X.size(0)

        print(f"epoch {epoch} loss={loss_sum/total:.4f} acc={correct/total:.3f}")

    torch.save(model.state_dict(), "policy.pt")
    return model
