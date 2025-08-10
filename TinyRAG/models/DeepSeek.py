"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/8/10 11:59 
"""
import os.path

from TinyRAG.models.BaseModel import BaseModel
from openai import OpenAI
from utils.CFGLoader import CFGLoader, get_cfg


class DeepSeek(BaseModel):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.model_name = "deepseek-chat"
        self.path = "https://api.deepseek.com"
        self.history = []
        self.client = None
        self.load_model()

    def load_model(self):
        self.client = OpenAI(api_key=self.cfg.api.key.DeepSeek, base_url=self.path)

    def new_session(self):
        self.history = []

    def chat(self, query, **kwargs):
        messages = self.history + [{"role": "user", "content": query}]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        result = response.choices[0].message.content
        self.history = self.history + [{"role": "user", "content": query}, {"role": "system", "content": result}]
        return result, self.history


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config')

    cfg = CFGLoader(get_cfg(config_path, "RAG"))
    model = DeepSeek(cfg)
    result, history = model.chat("你好，DeepSeek！")
    print(result)
