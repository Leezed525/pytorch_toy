"""
使用矩阵乘法来计算卷积
-*- coding: utf-8 -*-
@Author : Leezed
@Time : 2025/6/27 23:18
"""
import numpy as np
from manual.conv.slide_window import ManualSlideWindowConv


class ManualMatMulConv():
    """
    手动实现卷积操作，使用卷积乘法方式
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
        # 将权重转换为矩阵形式
        weight_matrix = self.weight.reshape(self.out_channel, -1)  # shape (out_channel, in_channel * kernel_size * kernel_size)
        # 将输入转为矩阵形式 手写unfold方式
        unfolded_x = []
        for i in range(0, height - kernel_size + 1, self.stride):
            for j in range(0, width - kernel_size + 1, self.stride):
                # 取出图像的滑动窗口 转成矩阵形式
                window = x[:, :, i:i + kernel_size, j:j + kernel_size].reshape(batch_size, -1)
                unfolded_x.append(window)

        unfolded_x = np.array(unfolded_x)  # shape: (num_windows, batch_size, in_channel * kernel_size * kernel_size)
        unfolded_x = np.transpose(unfolded_x, (1, 0, 2))  # shape: (batch_size, num_windows, in_channel * kernel_size * kernel_size)
        # 使用矩阵乘法计算卷积
        output = np.matmul(unfolded_x, weight_matrix.T)  # shape (batch_size, num_windows, out_channel)

        output = np.transpose(output, (0, 2, 1))  # shape (batch_size, out_channel, num_windows)
        output = output.reshape(batch_size, self.out_channel, out_height, out_width)
        # 添加bias
        if self.bias is not None:
            output += self.bias.reshape(1, -1, 1, 1)
        # 输出结果

        return output


if __name__ == '__main__':
    # 测试代码
    conv = ManualMatMulConv(kernel_size=3, in_channel=3, out_channel=2, stride=1, padding=0, bias=False)
    slide_window_conv = ManualSlideWindowConv(kernel_size=3, in_channel=3, out_channel=2, stride=1, padding=0, bias=False)
    conv.set_weight(slide_window_conv.get_weight())

    x = np.random.randn(1, 3, 5, 5)  # 输入形状 (batch_size, in_channel, height, width)

    output = conv(x)

    slide_window_output = slide_window_conv(x)

    print("Output shape:", output.shape)
    print("slide_window_output shape:", slide_window_output.shape)

    assert np.allclose(conv.get_weight(), slide_window_conv.get_weight()), "Weights do not match!"
    print("output:")
    print(output)
    print("slide_window_output:")
    print(slide_window_output)

    # 校验是否相同
    assert np.allclose(output, slide_window_output), "Outputs do not match!"
    print("Outputs match!")
