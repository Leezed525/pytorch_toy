# 项目介绍

    这个项目主要包含了一些简单的关于AI的应用实例，大部分是以jupyter notebook的形式来写的，方便调试

    写这个项目的初衷第一个是为了把一些比较基础的知识点通过实践的方式来加强印象，
    第二个就是有时候学了太多高层的知识点反倒忘记了基础的东西，所以这个项目也可以作为一个复习的资料。

# 目录

- [项目介绍](#项目介绍)
- [目录](#目录)
- [项目结构](#项目结构)
- [博文](#博文)

# 项目结构

```
.
├── dataset_file  #默认用来存放数据集的文件夹
├── digit_predictor_gui # 基于PyQt5的手写数字识别GUI
│   ├── digit_predictor_main.py # 主程序包含了PyQt5的GUI
├── GAN # 生成对抗网络相关的代码
│   ├── Mnist_CGAN # MNIST数据集的条件生成对抗网络
│   │   ├── Gan.ipynb # MNIST数据集的条件生成对抗网络的实现
│   ├── Mnist_GAN # MNIST数据集的生成对抗网络
│   │   ├── Gan.ipynb # MNIST数据集的生成对抗网络的实现
├── lib # 代码仓库，一些可以共用的东西我就塞里面
├── tmp # 临时文件夹，存放一些临时文件
├── README.md # 这个文件
├── digit_predictor.ipynb # 手写数字识别的jupyter notebook
├── function_chart.ipynb # 根据函数生成图像的jupyter notebook(主要是通过可视化的方式直观地展示函数的变化
├── line_chart.ipynb  # 根据数据生成折线图的jupyter notebook(做算法题的时候为了更直观地展示数据的变化)
├── xor_predictor.ipynb # 基于神经网络的异或预测器的jupyter notebook
└── requirements.txt # 依赖包列表
```

# 博文

- [神经网络拟合异或操作](https://blog.csdn.net/Leezed525/article/details/145833370?spm=1001.2014.3001.5501)
- [手写数字识别](https://blog.csdn.net/Leezed525/article/details/148344780?spm=1001.2014.3001.5501)
- [手写数字gui版](https://blog.csdn.net/Leezed525/article/details/148352169?spm=1001.2014.3001.5501)
- [生成对抗网络生成手写数字(gan)](https://blog.csdn.net/Leezed525/article/details/148587180?spm=1001.2014.3001.5501)
- [条件生成对抗网络生成手写数字(cgan)](https://blog.csdn.net/Leezed525/article/details/148738971?spm=1001.2014.3001.5501)