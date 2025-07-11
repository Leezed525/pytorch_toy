"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/6/30 23:21 
"""
from typing import List


class VectorStore:
    def __init__(self) -> None:
        """
        初始化向量存储类
        """
        pass

    def persist(self, file_path):
        # 数据库持久化，本地保存
        raise NotImplementedError("This method should be overridden by subclasses.")

    def load_vector(self):
        # 从本地加载数据库
        raise NotImplementedError("This method should be overridden by subclasses.")

    def query(self, query: str,  k: int = 1) -> List[str]:
        # 根据问题检索相关的文档片段
        raise NotImplementedError("This method should be overridden by subclasses.")
