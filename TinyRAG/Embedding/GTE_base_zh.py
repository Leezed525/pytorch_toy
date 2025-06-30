from sentence_transformers import SentenceTransformer
from TinyRAG.Embedding.BaseEmbedding import BaseEmbedding
from TinyRAG import base_embedding_dir


class BGEBaseZH(BaseEmbedding):
    def __init__(self):
        super().__init__(path=base_embedding_dir, device='cpu')
        self.model = SentenceTransformer('thenlper/gte-base-zh', cache_folder=self.path,device=self.device)
        self.max_sequence_length = 512

    def get_embedding(self, text):
        """
        Get the embedding of the text.
        :param text: The text to get the embedding for.
        :return: The embedding of the text.
        """
        return self.model.encode(text, normalize_embeddings=True)

    def compute_similarity(self, query_embedding, passage_embedding):
        """
        Compute the similarity between a query embedding and a passage embedding.
        :param query_embedding: The embedding of the query.
        :param passage_embedding: The embedding of the passage.
        :return: The similarity score.
        """
        return query_embedding @ passage_embedding.T


if __name__ == '__main__':
    queries = ['query_1', 'query_2']
    passages = ["样例文档-1", "样例文档-2"]
    instruction = "为这个句子生成表示以用于检索相关文章："

    BGE = BGEBaseZH()

    q_embeddings = BGE.get_embedding([instruction + q for q in queries])
    p_embeddings = BGE.get_embedding(passages)
    scores = q_embeddings @ p_embeddings.T
    print(scores)
