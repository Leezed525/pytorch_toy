@[toc]


# embedding 环境准备

    本来是想用api方式来获取embedding的，但是目前大部门的api都要收费，
    所以只能自己搭建embedding的环境。

## GTE-Base

GTE模型是阿里巴巴达摩院开源的一个多语言文本嵌入模型，支持中文、英文等多种语言。
基于BERT框架，参数规模小但性能卓越，支持代码检索、文本检索等任务。


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
q_embeddings = model.encode([instruction+q for q in queries], normalize_embeddings=True)
p_embeddings = model.encode(passages, normalize_embeddings=True)
scores = q_embeddings @ p_embeddings.T

```
