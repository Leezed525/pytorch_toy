import numpy as np


class BaseEmbedding:
    def __init__(self,
                 path: str = None,
                 device: str = 'cpu'):
        self.path = path
        self.device = device

    def get_embedding(self,text):
        """
        Get the embedding of the text.
        :param text: The text to get the embedding for.
        :return: The embedding of the text.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")



