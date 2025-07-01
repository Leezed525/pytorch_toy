#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/02/11 09:52:26
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''
import os
from typing import Dict, List, Optional, Tuple, Union

import PyPDF2
import markdown
import html2text
import json
from tqdm import tqdm
import tiktoken
from bs4 import BeautifulSoup
import re
from TinyRAG import base_tiktoken_dir
from TinyRAG.Embedding.BGE_base_zh import BGEBaseZH

os.environ["TIKTOKEN_CACHE_DIR"] = base_tiktoken_dir
enc = tiktoken.get_encoding("cl100k_base") # 用于计算文本长度的编码器


class ReadFiles:
    """
    class to read files
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self.file_list = self.get_files()

    def get_files(self):
        # args：dir_path，目标文件夹路径
        file_list = []
        for filepath, dirnames, filenames in os.walk(self._path):
            # os.walk 函数将递归遍历指定文件夹
            for filename in filenames:
                # 通过后缀名判断文件类型是否满足要求
                if filename.endswith(".md"):
                    # 如果满足要求，将其绝对路径加入到结果列表
                    file_list.append(os.path.join(filepath, filename))
                elif filename.endswith(".txt"):
                    file_list.append(os.path.join(filepath, filename))
                elif filename.endswith(".pdf"):
                    file_list.append(os.path.join(filepath, filename))
        return file_list

    def get_content(self, max_token_len: int = 600, cover_content: int = 150):
        docs = []
        # 读取文件内容
        for file in self.file_list:
            content = self.read_file_content(file)
            chunk_content = self.get_chunk(content, max_token_len=max_token_len, cover_content=cover_content)
            docs.extend(chunk_content)
        return docs

    @classmethod
    def get_chunk(cls, text: str, max_token_len: int = 600, cover_content: int = 150):
        chunk_text = []

        curr_len = 0
        curr_chunk = ''

        token_len = max_token_len - cover_content
        lines = text.splitlines()  # 假设以换行符分割文本为行

        for line in lines:
            # line = line.replace(' ', '') # 注释掉这行 保留空格
            line_len = len(enc.encode(line))
            # print(line_len, line)
            if line_len > max_token_len:
                # 如果单行长度就超过限制，则将其分割成多个块
                num_chunks = (line_len + token_len - 1) // token_len
                for i in range(num_chunks):
                    start = i * token_len
                    end = start + token_len
                    # 避免跨单词分割
                    while not line[start:end].rstrip().isspace():
                        start += 1
                        end += 1
                        if start >= line_len:
                            break
                    curr_chunk = curr_chunk[-cover_content:] + line[start:end]
                    chunk_text.append(curr_chunk)
                # 处理最后一个块
                start = (num_chunks - 1) * token_len
                curr_chunk = curr_chunk[-cover_content:] + line[start:end]
                chunk_text.append(curr_chunk)

            if curr_len + line_len <= token_len:
                curr_chunk += line
                curr_chunk += '\n'
                curr_len += line_len
                curr_len += 1
            else:
                chunk_text.append(curr_chunk)
                curr_chunk = curr_chunk[-cover_content:] + line
                curr_len = line_len + cover_content

        if curr_chunk:
            chunk_text.append(curr_chunk)

        return chunk_text

    @classmethod
    def read_file_content(cls, file_path: str):
        # 根据文件扩展名选择读取方法
        if file_path.endswith('.pdf'):
            return cls.read_pdf(file_path)
        elif file_path.endswith('.md'):
            return cls.read_markdown(file_path)
        elif file_path.endswith('.txt'):
            return cls.read_text(file_path)
        else:
            raise ValueError("Unsupported file type")

    @classmethod
    def read_pdf(cls, file_path: str):
        # 读取PDF文件
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            return text

    @classmethod
    def read_markdown(cls, file_path: str):
        # 读取Markdown文件
        with open(file_path, 'r', encoding='utf-8') as file:
            md_text = file.read()
            html_text = markdown.markdown(md_text)
            # 使用BeautifulSoup从HTML中提取纯文本
            soup = BeautifulSoup(html_text, 'html.parser')
            plain_text = soup.get_text()
            # 使用正则表达式移除网址链接
            text = re.sub(r'http\S+', '', plain_text)
            return text

    @classmethod
    def read_text(cls, file_path: str):
        # 读取文本文件
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


class Documents:
    """
        获取已分好类的json格式文档
    """

    def __init__(self, path: str = '') -> None:
        self.path = path

    def get_content(self):
        with open(self.path, mode='r', encoding='utf-8') as f:
            content = json.load(f)
        return content



if __name__ == '__main__':

    s = """
    这是一个测试文本，用于检查文本分割功能。
    这段文本应该被分割成多个块，以便适应指定的最大长度。
    每个块的长度不应超过600个token，且每个块的前150个字符应被覆盖。
    这段文本的长度应该足够长，以便测试分割功能的有效性。
    随机生成一段超过600个字符的长文本
    以确保分割功能能够正确处理长文本。
    
    用户刚刚问我是否会保留空格，我得先回顾一下之前的对话内容，用户之前关注的是不同模型对文本的处理方式以及空格和符号的处理。在这个背景下，我被问到是否保留空格，这表明用户想要了解我自身的文本处理机制，可能对我处理文本的具体细节感兴趣或者想进一步比较不同模型的处理方式。
我清楚地知道，我作为一个人工智能助手，我的文本处理机制是按照既定的规则和模型架构设计的，这些设计就是在服务用户的过程中经过大量数据训练和优化而来的。对于用户的这个问题，我的回答要基于我自身的模型架构和设计目标，同时也要符合实际情况，不能夸大或者虚构我的功能。
在分析了用户的问题后，我决定从我自身的设计和功能出发，直白且准确地回答用户的问题。我思考着，既然我的设计决定了我在处理用户输入时会保留空格，那我就直接告诉用户这个事实，这样可以满足用户对我的文本处理机制的好奇，也能体现出我的回答是基于实际情况的，而不是无端猜测或者随意编造的。
我准备直接回答用户的问题，把我的处理方式说明清楚，这样既能满足用户的好奇心，也能体现出我的诚实和可靠。
    This is a test text to check the text segmentation function.
    This text should be split into multiple chunks to fit the specified maximum length.
    Each chunk should not exceed 600 tokens, and the first 150 characters of each chunk should be covered.
    This text should be long enough to test the effectiveness of the segmentation function.
    Randomly generate a long text that exceeds 600 characters
    to ensure that the segmentation function can correctly handle long texts.
    The user just asked me if I would keep spaces, and I need to review the previous conversation content first. The user was previously concerned about how different models handle text, including spaces and punctuation. In this context, I was asked whether I retain spaces, indicating that the user is interested in understanding my own text processing mechanism, possibly to compare it with other models.
I clearly know that as an AI assistant, my text processing mechanism is designed according to established rules and model architecture, which have been trained and optimized through a large amount of data in the process of serving users. Regarding the user's question, my answer should be based on my own model architecture and design goals, while also conforming to the actual situation, without exaggerating or fabricating my capabilities.
I analyzed the user's question and decided to answer it directly and accurately based on my own design and functionality. I thought, since my design determines that I will retain spaces when processing user input, I would just tell the user this fact, which can satisfy the user's curiosity about my text processing mechanism and also reflect that my answer is based on actual conditions, rather than unfounded speculation or random fabrication.
    """

    res = ReadFiles.get_chunk(s, max_token_len=600, cover_content=150)

    embedding_model = BGEBaseZH()

    embeddings = embedding_model.get_embedding(res)
    print(embeddings.shape)

    # for i, r in enumerate(res):
    #     print(f"Processing chunk {i+1}/{len(res)}")
    #     print(f"Chunk content{i + 1}: {r}")
    #     embedding = embedding_model.get_embedding(r)
    #     embeddings.append(embedding)
    #     print(embedding.shape)

    print("All chunks processed.")


