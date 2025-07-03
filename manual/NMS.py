"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/7/3 16:59 
"""
import numpy as np


def nms_np(boxes, scores, iou_threshold=0.5):
    """
    使用np来实现非极大值抑制（NMS）
    :param boxes: 形状为 (N, 4) 的数组，表示 N 个边界框，每个边界框由四个坐标值 (x1, y1, x2, y2) 表示。
    :param scores: 形状为 (N,) 的数组，表示每个边界框的置信度分数。
    :param iou_threshold: 浮点数，表示用于抑制的交并比（IoU）阈值。
    :return:
    """
    if len(boxes) == 0:
        return np.array([])

    # 取出边界框的坐标
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # 计算边界框的面积
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # 排序scores
    indices = np.argsort(scores)[::-1]  # 从大到小排序
    # 保留的检测框索引
    selected_indices = []
    while len(indices) > 0:
        # 取出当前分数最高的边界框
        current_index = indices[0]
        selected_indices.append(current_index)

        # 取出当前边界框的坐标
        current_box = boxes[current_index]
        cx1, cy1, cx2, cy2 = current_box
        current_area = areas[current_index]

        # 计算其他边界框与当前边界框的交集
        xx1 = np.maximum(x1[indices[1:]], cx1)
        yy1 = np.maximum(y1[indices[1:]], cy1)
        xx2 = np.minimum(x2[indices[1:]], cx2)
        yy2 = np.minimum(y2[indices[1:]], cy2)

        # 计算交集面积
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        inter_areas = w * h
        # 计算交并比（IoU）
        ious = inter_areas / (current_area + areas[indices[1:]] - inter_areas)

        # 保留交并比小于阈值的边界框
        id = np.where(ious <= iou_threshold)[0] + 1  # +1 是因为我们从 indices[1:] 开始
        indices = indices[id]
    return np.array(selected_indices)


if __name__ == '__main__':
    boxes = np.array([[10, 10, 20, 20],
                      [12, 12, 22, 22],
                      [15, 15, 25, 25],
                      [30, 30, 40, 40]])
    scores = np.array([0.9, 0.8, 0.7, 0.6])
    iou_threshold = 0.5

    selected_indices = nms_np(boxes, scores, iou_threshold)
    print("Selected indices:", selected_indices)
    print("Selected boxes:", boxes[selected_indices])
    print("Selected scores:", scores[selected_indices])

