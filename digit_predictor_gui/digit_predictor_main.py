import sys
# 导入 PyQt6 相关的模块
# QtWidgets 包含了 GUI 控件，如 QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
# QtGui 包含了绘图相关的类，如 QPainter, QPen, QColor, QImage
from PyQt6.QtGui import QPainter, QPen, QColor, QImage
# QtCore 包含了核心的非 GUI 功能，如 Qt, QPoint
from PyQt6.QtCore import Qt, QPoint


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
        self.pen_size = 5

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
        """
        鼠标按下事件处理函数。
        当用户按下鼠标按钮时触发。
        """
        # 检查是否是鼠标左键被按下。
        # 在 PyQt6 中，鼠标按钮常量通过 Qt.MouseButton 枚举访问。
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
            # 设置画笔的属性：颜色、粗细、线条样式、笔帽样式和连接样式。
            # 在 PyQt6 中，这些样式常量现在分别通过 Qt.PenStyle, Qt.PenCapStyle, Qt.PenJoinStyle 枚举访问。
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

    def set_pen_color(self, color_name):
        """
        根据传入的颜色名称字符串设置画笔颜色。
        """
        color_map = {
            "black": Qt.GlobalColor.black,
            "red": Qt.GlobalColor.red,
            "blue": Qt.GlobalColor.blue,
            "green": Qt.GlobalColor.green,
            "yellow": Qt.GlobalColor.yellow
        }
        # 从映射中获取颜色，如果找不到则默认为黑色
        self.pen_color = color_map.get(color_name, Qt.GlobalColor.black)

    def set_pen_size(self, size):
        """
        设置画笔粗细。
        """
        self.pen_size = size


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        predict_label = QLabel("预测结果: ")  # 创建一个标签，显示预测结果
        right_operation_layer.addWidget(predict_label)
        predict_digit_labels = []
        for i in range(10):
            predict_digit_label = QLabel(f"数字 {i}: 0.00%")  # 创建标签显示每个数字的预测概率
            predict_digit_labels.append(predict_digit_label)  # 将标签添加到列表中
        for label in predict_digit_labels:
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
        predict_button.clicked.connect(self.canvas.clear_canvas)  # 连接按钮的点击信号到清空画布方法

        button_layout.addStretch(6)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(predict_button)

        layout.addLayout(button_layout)  # 将按钮布局添加到主布局中


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建 QApplication 实例，每个 PyQt 应用都必须有
    window = MainWindow()  # 创建主窗口实例
    window.show()  # 显示主窗口
    sys.exit(app.exec())
