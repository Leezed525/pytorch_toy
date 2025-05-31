import sys
# 导入 PyQt6 相关的模块
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QImage
from PyQt6.QtCore import Qt, QPoint

import qimage2ndarray  # 用于将 QImage 转换为 NumPy 数组

import torch
from lib.model.DigitModel import DigitCNN

import matplotlib

try:
    matplotlib.use('QtAgg')  # 尝试使用 QtAgg 后端
except ImportError:
    matplotlib.use('TkAgg')  # 如果 QtAgg 不可用，则回退到 TkAgg
import matplotlib.pyplot as plt  # 用于显示图像


class DrawingCanvas(QWidget):
    """
    一个自定义的 QWidget 类，用作绘图画布。
    用户可以在此画布上用鼠标点击并拖动来绘制线条。
    """

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类 QWidget 的构造函数
        self.setWindowTitle("绘图画布")  # 设置窗口标题
        self.setGeometry(100, 100, 280, 280)  # 设置窗口的初始位置和大小 (x, y, width, height)
        self.setMinimumSize(280, 280)

        # 创建一个 QImage 对象作为绘图缓冲区
        # 所有的绘图操作都在这个 QImage 上进行，然后整体绘制到屏幕，可以避免闪烁。
        # QImage.Format.Format_RGB32 是 PyQt6 中推荐的 RGBA 格式，支持透明度。
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        # 将 QImage 填充为白色。
        self.image.fill(Qt.GlobalColor.white)

        self.drawing = False  # 一个布尔标志，指示当前是否正在进行鼠标拖拽绘图
        self.last_point = QPoint()  # 存储鼠标上次的位置，用于绘制连续的线条

        # 同样，颜色常量需要通过 Qt.GlobalColor 访问。
        self.pen_color = Qt.GlobalColor.black
        self.pen_size = 20

    def paintEvent(self, event):
        """
        绘制事件处理函数。
        每当窗口需要被重新绘制时（例如，首次显示、窗口大小改变、调用 update() 时），
        Qt 就会自动调用这个方法。
        """
        painter = QPainter(self)  # 创建一个 QPainter 对象，指定在当前 QWidget (self) 上进行绘制
        # 将 self.image (绘图缓冲区) 的内容绘制到当前 QWidget 的整个矩形区域内。
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        # 检查是否是鼠标左键被按下。
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True  # 设置绘图标志为 True
            self.last_point = event.pos()  # 记录当前鼠标位置作为线条的起始点

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理函数。
        当鼠标在窗口内移动时触发。
        """
        # 只有当正在绘图 (self.drawing 为 True) 并且鼠标左键被按住时才执行绘图操作。
        # event.buttons() 返回当前按下的所有鼠标按钮的位掩码，Qt.MouseButton.LeftButton 用于检查左键是否按下。
        if self.drawing and event.buttons() & Qt.MouseButton.LeftButton:
            painter = QPainter(self.image)  # 在 QImage (绘图缓冲区) 上创建 QPainter 进行绘制
            # 设置画笔的颜色、粗细和样式。
            painter.setPen(QPen(QColor(self.pen_color), self.pen_size,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            # 绘制从上次记录的点到当前鼠标位置的直线
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()  # 更新 last_point 为当前鼠标位置，为下一次绘制做准备
            self.update()  # 请求窗口重绘。这会间接调用 paintEvent，将 QImage 的最新内容显示到屏幕上。

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理函数。
        当用户释放鼠标按钮时触发。
        """
        # 检查是否是鼠标左键被释放。
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False  # 停止绘图

    def resizeEvent(self, event):
        """
        窗口大小改变事件处理函数。
        当窗口大小改变时触发。
        """
        # 如果新窗口的宽度或高度大于当前 QImage 的尺寸，则需要创建一个新的 QImage。
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_image = QImage(self.size(), QImage.Format.Format_RGB32)
            # 填充新图像为白色
            new_image.fill(Qt.GlobalColor.white)
            painter = QPainter(new_image)
            # 将旧图像的内容绘制到新图像上，以保留已有的绘图。
            painter.drawImage(QPoint(0, 0), self.image)
            self.image = new_image  # 更新 self.image 为新的 QImage
            self.update()  # 请求重绘窗口

    def clear_canvas(self):
        """
        清空画布内容，将整个 QImage 重新填充为白色。
        """
        self.image.fill(Qt.GlobalColor.white)
        self.update()  # 请求重绘以显示空白画布

    def set_pen_size(self, size):
        """
        设置画笔粗细。
        """
        self.pen_size = size


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.net = self.get_net()  # 获取数字预测模型
        self.setWindowTitle("PyQt 数字预测")
        self.setGeometry(100, 100, 500, 550)  # 设置主窗口的初始位置和大小，留出空间给按钮

        self.setFixedSize(500, 550)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        central_widget = QWidget()  # 创建一个中央 QWidget
        self.setCentralWidget(central_widget)  # 设置中央 QWidget 为主窗口的中心部件
        layout = QVBoxLayout(central_widget)  # 为中央 QWidget 创建一个垂直布局

        # 创建一个水平布局
        operation_layer = QHBoxLayout()  # 创建一个水平布局用于放置操作区域
        left_operation_layer = QVBoxLayout()
        right_operation_layer = QVBoxLayout()

        self.canvas = DrawingCanvas(self)  # 创建 DrawingCanvas 实例
        canvas_label = QLabel("请在此处绘制数字")  # 创建一个标签，提示用户在画布上绘制数字
        canvas_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        canvas_label.setStyleSheet("font-size: 20px;")  # 设置标签的样式
        left_operation_layer.addWidget(canvas_label)  # 将标签添加到左侧操作区域布局中
        left_operation_layer.addWidget(self.canvas)

        left_operation_layer.setStretch(0, 1)
        left_operation_layer.setStretch(1, 10)  # 设置画布的伸缩比例，使其占据更多空间

        operation_layer.addLayout(left_operation_layer)  # 将左侧操作区域布局添加到操作层布局中
        # 右侧操作区域

        self.predict_label = QLabel("预测结果: ")  # 创建一个标签，显示预测结果
        right_operation_layer.addWidget(self.predict_label)
        self.predict_digit_labels = []
        for i in range(10):
            predict_digit_label = QLabel(f"数字 {i}: 0.00%")  # 创建标签显示每个数字的预测概率
            self.predict_digit_labels.append(predict_digit_label)  # 将标签添加到列表中
        for label in self.predict_digit_labels:
            right_operation_layer.addWidget(label)

        operation_layer.addLayout(right_operation_layer)  # 将右侧操作区域布局添加到操作层布局中
        operation_layer.setStretch(0, 10)
        operation_layer.setStretch(1, 1)

        layout.addLayout(operation_layer)  # 将操作层布局添加到主布局中
        # 按钮区布局
        button_layout = QHBoxLayout()  # 创建一个垂直布局用于放置按钮

        clear_button = QPushButton("清空画布")  # 清空画布按钮
        clear_button.clicked.connect(self.canvas.clear_canvas)  # 连接按钮的点击信号到清空画布方法

        predict_button = QPushButton("预测")  # 清空画布按钮
        predict_button.clicked.connect(self.predict)  # 连接按钮的点击信号到预测方法

        button_layout.addStretch(6)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(predict_button)

        layout.addLayout(button_layout)  # 将按钮布局添加到主布局中

    def get_image(self):
        """
        获取当前画布上的图像数据。
        返回一个 QImage 对象，包含当前画布的绘图内容。
        """
        image = self.canvas.image
        # 将图像缩放到 28x28 像素并转换为灰度图
        scaled_image = image.scaled(
            28, 28,
            Qt.AspectRatioMode.IgnoreAspectRatio,  # 不保持宽高比
            Qt.TransformationMode.SmoothTransformation  # 平滑缩放
        )
        # 转换为 8 位灰度图
        grayscale_image = scaled_image.convertToFormat(QImage.Format.Format_Grayscale8)

        # 使用 qimage2ndarray.byte_view() 获取 NumPy 数组
        arr_3d = qimage2ndarray.byte_view(grayscale_image)
        arr = arr_3d.squeeze()

        # 将 NumPy 数组转换为 PyTorch 张量
        tensor_image = torch.from_numpy(arr).float()

        # --- 关键修正：添加颜色反转和标准化 ---
        # 1. 将像素值从 [0, 255] 归一化到 [0.0, 1.0]
        tensor_image = tensor_image / 255.0

        # 2. 颜色反转：如果你的模型是基于白色数字黑色背景训练的 而画布是黑色数字白色背景，则需要反转颜色
        tensor_image = 1.0 - tensor_image

        # 3. 标准化：应用训练时使用的均值和标准差
        # MNIST 均值和标准差
        mean = 0.1307
        std = 0.3081
        tensor_image = (tensor_image - mean) / std

        # 添加批次维度和通道维度，使形状变为 (1, 1, 28, 28)
        tensor_image = tensor_image.unsqueeze(0).unsqueeze(0).cuda()

        # --- 可视化 PyTorch 张量 ---
        # 为了可视化，我们先将其恢复到 [0,1] 范围，否则标准化后的值可能很难看
        # 逆标准化 (用于可视化，不影响模型输入)
        # visual_tensor = tensor_image * std + mean
        # # 确保在 [0,1] 范围内
        # visual_tensor = torch.clamp(visual_tensor, 0.0, 1.0)
        # plt.figure(figsize=(2, 2))
        # plt.imshow(visual_tensor.cpu().squeeze().numpy(), cmap='gray')
        # plt.title("input")
        # plt.axis('off')
        # plt.show()
        return tensor_image

    def predict(self):
        """
        预测当前画布上绘制的数字。
        这里可以调用模型进行预测，并更新预测结果标签。
        """
        input = self.get_image()  # 获取当前画布上的图像数据
        # 使用模型进行预测
        with torch.no_grad():
            output = self.net(input)
        # 获取预测结果
        self.update_predict_result(output)

    def update_predict_result(self, output):
        _, predict = output.max(1)  # 获取预测的数字类别
        predict = predict.cpu().numpy()[0]
        # 更新预测结果标签
        self.predict_label.setText(f"预测结果: {predict}")
        # 更新每个数字的预测概率
        probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]
        for i, label in enumerate(self.predict_digit_labels):
            label.setText(f"数字 {i}: {probabilities[i] * 100:.2f}%")

    def get_net(self):
        """
        获取数字预测模型。
        返回一个 DigitCNN 模型实例。
        """
        # 创建并返回一个 DigitCNN 模型实例
        net = DigitCNN()
        net.eval()
        net.cuda()
        net.load_state_dict(torch.load('./digit_CNN.pth'))
        return net


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建 QApplication 实例，每个 PyQt 应用都必须有
    window = MainWindow()  # 创建主窗口实例
    window.show()  # 显示主窗口
    sys.exit(app.exec())
