import os

base_dir = os.path.dirname(os.path.abspath(__file__))
base_embedding_dir = os.path.join(base_dir, '.cache', 'embedding')
base_tiktoken_dir = os.path.join(base_dir, '.cache', 'tiktoken')
base_local_vector_base_dir = os.path.join(base_dir, 'storage', 'local')
base_data_dir = os.path.join(base_dir, 'data')

PROMPT_TEMPLATE = dict(
    InternLM_PROMPT_TEMPALTE="""先对上下文进行内容总结,再使用上下文来回答用户的问题。如果你不知道答案，就说你不知道。总是使用中文回答。
        问题: {question}
        可参考的上下文：
        ···
        {context}
        ···
        如果给定的上下文无法让你做出回答，请回答数据库中没有这个内容，你不知道。
        有用的回答:"""
)
