"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/6/30 23:23 
"""
import os

from TinyRAG.VectorBase.VectorBase import VectorStore
from TinyRAG import base_local_vector_base_dir


class LocalVectorBase(VectorStore):
    def __init__(self, path=base_local_vector_base_dir):
        """
        初始化本地向量存储类
        :param path: 存储路径
        """
        super().__init__()
        self.path = path
        # 检查当前目录是否存在
        if not self.path.endswith('/'):
            self.path += '/'

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"Directory {self.path} created.")


    def get_vector(self, EmbeddingModel: BaseEmbedding) -> List[List[float]]:
        """
        获得文档的向量表示
        :param EmbeddingModel: 嵌入模型
        :return: 文档向量列表
        """
        raise NotImplementedError("This method should be overridden by subclasses.")


if __name__ == '__main__':
    local_vector_base = LocalVectorBase()
    print(f"Local vector base initialized at: {local_vector_base.path}")
