import torch.nn as nn
import torch.nn.functional as F

class PolicyNet(nn.Module):
    def __init__(self, n_actions=12, n_colors=6, embed_dim=16, hidden=256):
        super().__init__()
        self.emb = nn.Embedding(n_colors, embed_dim)
        self.fc1 = nn.Linear(54 * embed_dim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.out = nn.Linear(hidden, n_actions)

    def forward(self, x):
        x = self.emb(x)              # (B,54,E)
        x = x.reshape(x.size(0), -1) # (B,54E)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)           # (B,12)
