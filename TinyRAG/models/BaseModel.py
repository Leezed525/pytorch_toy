"""
-*- coding: UTF-8 -*-
@Author  ：Leezed
@Date    ：2025/8/10 11:31 
"""


class BaseModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = None
        pass

    def chat(self, query, history=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def load_model(self):
        raise NotImplementedError("Subclasses must implement this method")
