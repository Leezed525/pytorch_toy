"""
-*- coding: utf-8 -*-
使用滑动窗口方式的手动卷积
@Author : Leezed
@Time : 2025/6/27 15:33
"""

import numpy as np


class ManualSlideWindowConv():
    """
    手动实现卷积操作，使用滑动窗口方式
    没有实现反向传播功能
    """

    def __init__(self, kernel_size, in_channel, out_channel, stride=1, padding=0, bias=True):
        self.kernel_size = kernel_size
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.stride = stride
        self.padding = padding
        self.bias = bias

        self.weight = np.random.randn(out_channel, in_channel, kernel_size, kernel_size)

        if bias:
            self.bias = np.random.randn(out_channel)
        else:
            self.bias = None

    def print_weight(self):
        print("Weight shape:", self.weight.shape)
        print("Weight values:\n", self.weight)

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        if weight.shape != self.weight.shape:
            raise ValueError(f"Weight shape mismatch: expected {self.weight.shape}, got {weight.shape}")
        self.weight = weight

    def __call__(self, x, *args, **kwargs):
        if self.padding > 0:
            x = np.pad(x, ((0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)), mode='constant')  # 在四周填充0
        batch_size, in_channel, height, width = x.shape
        kernel_size = self.kernel_size
        # 计算输出的高度和宽度
        out_height = (height - kernel_size) // self.stride + 1
        out_width = (width - kernel_size) // self.stride + 1
        output = np.zeros((batch_size, self.out_channel, out_height, out_width))
        for channel in range(self.out_channel):
            # 取出当前输出通道的权重
            kernel = self.weight[channel, :, :, :]
            for i, end_height in enumerate(range(kernel_size - 1, height, self.stride)):
                for j, end_width in enumerate(range(kernel_size - 1, width, self.stride)):
                    # 取出图像的滑动窗口
                    start_height = end_height - kernel_size + 1
                    start_width = end_width - kernel_size + 1
                    window = x[:, :, start_height:end_height + 1, start_width:end_width + 1]
                    # 计算卷积
                    result = np.sum(kernel * window, axis=(1, 2, 3))
                    output[:, channel, i, j] += result

        if self.bias is not None:
            # 偏置的形状是 (out_channel,)
            # 我们需要将其广播到 (batch_size, out_channel, out_height, out_width)
            output += self.bias.reshape(1, -1, 1, 1)  # 1, -1, 1, 1 表示在 out_channel 维度上展开，其他维度广播

        return output



if __name__ == '__main__':
    # 测试代码
    x = np.random.randn(2, 3, 5, 5)  # batch_size=2, in_channel=3, height=5, width=5
    conv_layer = ManualSlideWindowConv(kernel_size=3, in_channel=3, out_channel=2, stride=1, padding=1)
    output = conv_layer(x)
    print("Output shape:", output.shape)
    conv_layer.print_weight()
