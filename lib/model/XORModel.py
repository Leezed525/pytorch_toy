import torch
import torch.nn as nn


class xorModel(nn.Module):
    def __init__(self):
        super(xorModel, self).__init__()
        self.fc1 = nn.Linear(32, 64)
        self.xor = nn.Linear(64, 64)
        self.output = nn.Linear(64, 16)
        self.relu = nn.LeakyReLU()
        self.sigmoid = nn.Sigmoid()
        # self.output = nn.Linear(16, 1)

    def forward(self, x):
        x = x.flatten(start_dim=1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.xor(x)
        x = self.relu(x)
        x = self.output(x)
        x = self.sigmoid(x)
        # x = self.output(x)
        return x
