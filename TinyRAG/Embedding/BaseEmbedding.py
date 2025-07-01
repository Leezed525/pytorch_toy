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


    def similarity(self, query_embedding, passage_embedding):
        """
        Compute the similarity between a query embedding and a passage embedding.
        :param query_embedding: The embedding of the query.
        :param passage_embedding: The embedding of the passage.
        :return: The similarity score.
        """
        return np.dot(passage_embedding, query_embedding)



