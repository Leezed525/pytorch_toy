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


class DigitCNN(nn.Module):
    def __init__(self):
        super(DigitCNN,self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(64*28*28, 128)
        self.dropout = nn.Dropout(0.1)
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        # print("x.shape:", x.shape)
        B,N,H,W = x.shape
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = x.view(B, -1)  # 展平
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x


