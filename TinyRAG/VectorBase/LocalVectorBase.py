"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/6/30 23:23 
"""
import os

from TinyRAG.VectorBase.VectorBase import VectorStore
from TinyRAG import base_local_vector_base_dir,base_data_dir
from TinyRAG.VectorBase.utils import ReadFiles
import json
from TinyRAG.Embedding.BaseEmbedding import BaseEmbedding
from TinyRAG.Embedding.BGE_base_zh import BGEBaseZH
import hashlib
import numpy as np
from typing import List


class LocalVectorBase(VectorStore):
    def __init__(self, embedding_model: BaseEmbedding, path=base_local_vector_base_dir, json_file="vector.json"):
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

        # 判断目录下是否存在向量文件
        self.vector_file = os.path.join(self.path, json_file)
        if not os.path.exists(self.vector_file):
            with open(self.vector_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            print(f"Vector file {self.vector_file} created.")
        # 加载向量文件
        self.vectors = self.load_vector()
        # 嵌入模型
        self.embedding_model = embedding_model

    def persist(self, file_path):
        """
        数据库持久化，本地保存
        """
        # 这里实现将文件转成向量存储到本地
        files = ReadFiles(file_path)
        docs = files.get_content()
        vectors = {}
        embeddings = self.embedding_model.get_embedding(docs)
        for i, doc in enumerate(docs):
            vector = {
                "text": doc,
                "embedding": embeddings[i].tolist()  # 将numpy数组转换为列表以便于JSON序列化
            }
            # 根据doc的内容一个md5哈希值作为唯一标识符
            doc_hash = hashlib.md5(doc.encode('utf-8')).hexdigest()

            vectors[doc_hash] = vector
        # 检查目前的向量文件中是否已经存在相同的向量
        existing_vectors = self.load_vector()
        for key, value in vectors.items():
            if key not in existing_vectors:
                existing_vectors[key] = value
        # 保存向量到文件
        with open(self.vector_file, 'w', encoding='utf-8') as f:
            json.dump(existing_vectors, f, ensure_ascii=False, indent=4)

        self.vectors = existing_vectors

    def load_vector(self):
        """
        从本地加载数据库
        """
        with open(self.vector_file, 'r', encoding='utf-8') as f:
            vectors = json.load(f)
        return vectors

    def query(self, query: str, k: int = 1) -> List[str]:
        """
        根据问题检索相关的文档片段
        :param query: 查询字符串
        :param EmbeddingModel: 嵌入模型
        :param k: 返回的结果数量
        :return: 文档片段列表
        """
        query_embedding = self.embedding_model.get_embedding(query)
        # 取出self.vectors中的所有向量
        all_embeddings = np.array([vector['embedding'] for vector in self.vectors.values()])
        # 计算查询向量与所有向量的相似度
        # similarities = np.dot(all_embeddings, query_embedding)
        similarities = self.embedding_model.similarity(query_embedding,all_embeddings)
        # 获取相似度最高的k个索引
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        # 返回相似度最高的k个文档片段
        results = []
        docs = list(self.vectors.values())
        for index in top_k_indices:
            results.append(docs[index]['text'])

        return results




if __name__ == '__main__':
    embedding_model = BGEBaseZH()
    local_vector_base = LocalVectorBase(embedding_model)
    local_vector_base.persist(base_data_dir)

    query  = "请你讲讲git push的用法"

    res = local_vector_base.query(query,k = 3)
    for i, r in enumerate(res):
        print(f"Result {i + 1}: {r}")
    # print(res)
