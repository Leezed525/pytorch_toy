# 目录

- [embedding 环境准备](#embedding-环境准备)
- [GTE-Base](#gte-base)
    - [环境准备](#环境准备)
    - [下载模型](#下载模型)
    - [使用模型](#使用模型)

# embedding 环境准备

    本来是想用api方式来获取embedding的，但是目前大部门的api都要收费，
    所以只能自己搭建embedding的环境。

## GTE-Base

GTE模型是一个北京智源人工智能研究院（BAAI）发布的开源模型，旨在为中文文本生成高质量的向量表示。

### 环境准备

这里默认你已经安装了pytroch的基础的包

```bash
pip install transformers
pip install sentence-transformers
```

### 下载模型

[https://huggingface.co/BAAI/bge-base-zh-v1.5](https://huggingface.co/BAAI/bge-base-zh-v1.5)

### 使用模型

```python
from sentence_transformers import SentenceTransformer

queries = ['query_1', 'query_2']
passages = ["样例文档-1", "样例文档-2"]
instruction = "为这个句子生成表示以用于检索相关文章："

model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
q_embeddings = model.encode([instruction + q for q in queries], normalize_embeddings=True)
p_embeddings = model.encode(passages, normalize_embeddings=True)
scores = q_embeddings @ p_embeddings.T
```
