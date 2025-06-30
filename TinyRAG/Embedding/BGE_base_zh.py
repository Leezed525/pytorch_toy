from sentence_transformers import SentenceTransformer
from TinyRAG.Embedding.BaseEmbedding import BaseEmbedding
from TinyRAG import base_embedding_dir


class BGEBaseZH(BaseEmbedding):
    def __init__(self):
        super().__init__(path=base_embedding_dir, device='cpu')
        self.model = SentenceTransformer('BAAI/bge-large-zh-v1.5', cache_folder=base_embedding_dir)


if __name__ == '__main__':
    queries = ['query_1', 'query_2']
    passages = ["样例文档-1", "样例文档-2"]
    instruction = "为这个句子生成表示以用于检索相关文章："

    BGE = BGEBaseZH()

    q_embeddings = BGE.model.encode([instruction + q for q in queries], normalize_embeddings=True)
    p_embeddings = BGE.model.encode(passages, normalize_embeddings=True)
    scores = q_embeddings @ p_embeddings.T
    print(scores)
