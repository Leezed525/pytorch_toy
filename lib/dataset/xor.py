import torch
from torch.utils.data import Dataset

class xor(Dataset):
    def __init__(self, split='train',bit_dim=16):
        self.data = []
        with open(f'./dataset_file/xor/{split}.txt', 'r') as f:
            for line in f:
                # 假设数据格式为 a,b,c
                parts = line.strip().split(' ')
                a = float(parts[0])
                b = float(parts[1])
                c = float(parts[2])
                # 将数据转换为bit_dim位二进制
                a = [int(x) for x in bin(int(a))[2:]]
                b = [int(x) for x in bin(int(b))[2:]]
                c = [int(x) for x in bin(int(c))[2:]]
                while len(a) < bit_dim:
                    a = [0] + a
                while len(b) < bit_dim:
                    b = [0] + b
                while len(c) < bit_dim:
                    c = [0] + c
                x = a + b
                self.data.append((x, c))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x, c = self.data[idx]
        return torch.tensor(x), torch.tensor(c)
