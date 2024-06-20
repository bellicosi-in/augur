import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim

class ChessDataset(Dataset):
    def __init__(self):
        dat = np.load("processed/dataset_100k.npz")
        self.X = dat['arr_0']
        self.Y = dat['arr_1']
        self.X = self.X.reshape(-1, 5, 4, 2)

         
        print("loaded", self.X.shape,self.Y.shape)
    
    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self,idx):
        return (self.X[idx], self.Y[idx])


class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.a1 = nn.Conv2d(5,16,kernel_size = 3, padding = 1)
        self.a2 = nn.Conv2d(16,16, kernel_size =  3, padding = 1)
        self.a3 = nn.Conv2d(16,32, kernel_size =  3, padding = 1)

        self.b1 = nn.Conv2d(32,32, kernel_size =  3, padding = 1)
        self.b2 = nn.Conv2d(32,64, kernel_size =  3, padding = 1)
        self.b3 = nn.Conv2d(64,128, kernel_size =  3, padding = 1)

        self.c1 = nn.Conv2d(128, 128, kernel_size=1)
        self.c2 = nn.Conv2d(128, 128, kernel_size=1)
        self.c3 = nn.Conv2d(128, 128, kernel_size=1)

        
        self.last = nn.Linear(128,1)
    
    def forward(self,x):
        # x = x.permute(0,3,1,2)
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))
        # x = F.max_pool2d(x,2)

        # 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))
        # x = F.max_pool2d(x, 2)i

        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))

        # Add an adaptive pooling layer to adjust the feature map size to (1, 1)
        x = F.adaptive_avg_pool2d(x, (1, 1))
        # print("Shape after adaptive pooling:", x.shape)  # Debugging statement

        x = x.view(x.size(0), -1)  # Flatten the output
        # print("Shape after view:", x.shape)  # Debugging statement

        x = self.last(x)

        return F.tanh(x)
    

if __name__ == "__main__":
    

    chess_dataset = ChessDataset()
    # print(chess_dataset.X)
    train_loader = torch.utils.data.DataLoader(chess_dataset, batch_size = 256, shuffle = True)
    model = Net()
    optimizer = optim.Adam(model.parameters())
    floss = nn.MSELoss()

    device = (
        "cpu"
    )


    model.train()

    for epoch in range(50):
        all_loss = 0
        num_loss = 0
        for batch_idx, (data,target) in enumerate(train_loader):
            target = target.unsqueeze(-1)
            data, target = data.to(device), target.to(device)
            data = data.float()
            # data = data.reshape((1,256,5,8))
            target = target.float()
            
            optimizer.zero_grad()
            output = model(data)
            
            loss = floss(output,target)
            loss.backward()
            optimizer.step()

            all_loss += loss.item()
            num_loss += 1
        print(f"{epoch}, {all_loss/num_loss}")

    torch.save(model.state_dict(),"nets/value.pth")

