"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/6/30 23:21 
"""

from typing import List
from TinyRAG.Embedding.BaseEmbedding import BaseEmbedding


class VectorStore:
    def __init__(self) -> None:
        """
        初始化向量存储类
        """
        pass

    def get_vector(self, EmbeddingModel: BaseEmbedding) -> List[List[float]]:
        # 获得文档的向量表示
        raise NotImplementedError("This method should be overridden by subclasses.")

    def persist(self, path: str = 'storage'):
        # 数据库持久化，本地保存
        raise NotImplementedError("This method should be overridden by subclasses.")

    def load_vector(self, path: str = 'storage'):
        # 从本地加载数据库
        raise NotImplementedError("This method should be overridden by subclasses.")

    def query(self, query: str, EmbeddingModel: BaseEmbedding, k: int = 1) -> List[str]:
        # 根据问题检索相关的文档片段
        raise NotImplementedError("This method should be overridden by subclasses.")
