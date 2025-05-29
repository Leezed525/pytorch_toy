import torch
import torch.nn as nn


class DigitLinear(nn.Module):
    def __init__(self):
        super(DigitLinear, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 1000)
        self.fc2 = nn.Linear(1000, 500)
        self.dropout = nn.Dropout(0.3)
        self.fc3 = nn.Linear(500, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        return x
