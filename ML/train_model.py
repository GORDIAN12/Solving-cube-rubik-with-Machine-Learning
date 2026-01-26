import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

def to_onehot(x,num_colors=6):
    x=torch.as_tensor(x,dtype=torch.long)
    oh=torch.nn.functional.one_hot(x,num_classes=num_colors).float()
    return oh.view(x.shape[0],-1)

class HeuristicNet(nn.Module):
    def __init__(self,in_dim, out_classes):
        super().__init__()
        self.net=nn.Sequential(
            nn.Linear(in_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, out_classes)
        )
    def forward(self,x):
        return self.net(x)

def train_heuristic(x,y,N, epochs=5, batch_size=256, lr=1e-3, device="cpu"):
    y2=y.copy()
    y2=y2
    out_classes=N+1
    Xoh=to_onehot(x)
    y_t=torch.as_tensor(y2,dtype=torch.long)
    ds=TensorDataset(Xoh,y_t)
    dl=DataLoader(ds,batch_size=batch_size, shuffle=True, drop_last=True)
    model=HeuristicNet(in_dim=Xoh.shape[1], out_classes=out_classes).to(device)
    opt=torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn=nn.CrossEntropyLoss()

    model.train()
    for ep in range(epochs):
        total=0.0
        for xb, yb in dl:
            xb=xb.to(device)
            yb=yb.to(device)
            logits=model(xb)
            loss=loss_fn(logits,yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total+=loss.item()
        print(f"Epoch {ep+1}, loss: {total/len(dl):.4f}")
    return model


@torch.no_grad()
def h_model(model, state, device="cpu"):
    model.eval()
    xoh=to_onehot(np.expand_dims(state,0)).to(device)
    logits=model(xoh)
    pred=int(torch.argmax(logits, dim=1).item())
    return pred

