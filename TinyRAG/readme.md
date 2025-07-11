# 目录

- [项目介绍](#项目介绍)
- [项目结构](#项目结构)
- [博文](#博文)
- [参考资料](#参考资料)

# 项目介绍

TinyRAG是一个轻量级的RAG（Retrieval-Augmented Generation）框架(暂未实现)

| 需要实现的功能   | 功能描述               | 完成情况 | 备注              |
|-----------|--------------------|------|-----------------|
| 向量化模块     | 将文档片段向量化           | 完成   |                 |
| 文档加载和切分模块 | 加载文档并切分成文档片段       | 勉强实现 | 后续在完成爬虫然后联网搜索功能 |
| 数据库模块     | 存放文档片段和对应的向量表示     | 基本完成 | 线上版未完成          |
| 检索模块      | 根据 Query 检索相关的文档片段 | 未实现  |                 |
| 大模型模块     | 根据检索出来的文档回答用户的问题   | 未实现  |                 |

# 环境准备

## embedding 环境准备

~~~bash 
pip install transformers
pip install sentence-transformers
~~~

## 文档切分环境准备

```bash
pip install PyPDF2 markdown html2text tiktoken
```

# 博文

- [6.0 手动实现一个RAG工程开始](https://blog.csdn.net/Leezed525/article/details/148999508?spm=1001.2014.3001.5501)
- [6.1 实现Embeding模块](https://blog.csdn.net/Leezed525/article/details/149027973?spm=1001.2014.3001.5501)
- [6.2 实现文档加载和切分和简易向量数据库的功能](https://blog.csdn.net/Leezed525/article/details/149054143?spm=1001.2014.3001.5501)

# 参考资料

[动手实现一个最小RAG——TinyRAG https://zhuanlan.zhihu.com/p/685989556](https://zhuanlan.zhihu.com/p/685989556)


