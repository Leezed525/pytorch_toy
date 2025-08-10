"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/8/10 13:42 
"""
import os
from utils.CFGLoader import CFGLoader, get_cfg
import importlib
from TinyRAG.VectorBase.LocalVectorBase import LocalVectorBase
from TinyRAG.models.DeepSeek import DeepSeek
from TinyRAG import PROMPT_TEMPLATE


class TinyRAG:
    def __init__(self, config_name='RAG'):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TinyRAG/config')
        self.cfg = CFGLoader(get_cfg(config_path, config_name))

        self.embedding_model = self.get_embedding_model()
        self.database = LocalVectorBase(self.embedding_model)

        self.debug = False

        self.llm = DeepSeek(self.cfg)

    def get_embedding_model(self):
        embedding_name = self.cfg.model.embedding.name

        embedding_module = importlib.import_module(f"TinyRAG.Embedding.{embedding_name}")
        embedding_class = getattr(embedding_module, self.cfg.embeddings[embedding_name]["ClassName"])
        embedding_instance = embedding_class()
        return embedding_instance

    def debug_on(self):
        self.debug = True

    def debug_off(self):
        self.debug = False

    def get_db_content(self, question):
        '''
        根据提问去数据库中查询相关内容
        :param question: string
        :return:
        '''
        db_res = self.database.query(question, k=2)
        # 将content 压缩成 一段文本
        content = ""
        for s in db_res:
            content += s

        if self.debug:
            print("数据库查询结果：", content)

        return content

    def query(self, question):
        self.llm.new_session()
        content = self.get_db_content(question)
        prompted_question = PROMPT_TEMPLATE['InternLM_PROMPT_TEMPALTE'].format(question=question, context=content)
        if self.debug:
            print("Prompted Question:", prompted_question)
        res,his = self.llm.chat(prompted_question)
        return res



if __name__ == '__main__':
    tiny_rag = TinyRAG()
    question = "请你讲讲git push的用法"
    tiny_rag.debug_on()
    res = tiny_rag.query(question)
    print(res)


