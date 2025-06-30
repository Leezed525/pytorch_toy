# 目录

- [embedding 环境准备](#embedding-环境准备)
    - [环境准备](#环境准备)
- [BGE-Base](#BGE-base)
    - [下载模型](#下载模型)
    - [使用模型](#使用模型)
- [GTE-Base](#GTE-base)
    - [下载模型](#下载模型)
    - [使用模型](#使用模型)

# embedding 环境准备

    本来是想用api方式来获取embedding的，但是目前大部门的api都要收费，
    所以只能自己搭建embedding的环境。

## 环境准备

这里默认你已经安装了pytroch的基础的包

```bash
pip install transformers
pip install sentence-transformers
```

## BGE-Base

BGE模型是一个北京智源人工智能研究院（BAAI）发布的开源模型，旨在为中文文本生成高质量的向量表示。

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

## GTE-Base

GTE是阿里达摩院出品，基于BERT框架，参数规模小但性能卓越，支持代码检索

### 下载模型

[https://huggingface.co/thenlper/gte-base-zh](https://huggingface.co/thenlper/gte-base-zh)

###  

使用模型

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

sentences = ['中国的首都是哪里', '中国的首都是北京']

model = SentenceTransformer('thenlper/gte-base-zh')
embeddings = model.encode(sentences)
print(cos_sim(embeddings[0], embeddings[1]))
```