import os

base_dir = os.path.dirname(os.path.abspath(__file__))
base_embedding_dir = os.path.join(base_dir, '.cache', 'embedding')
base_tiktoken_dir = os.path.join(base_dir, '.cache', 'tiktoken')
base_local_vector_base_dir = os.path.join(base_dir, 'storage', 'local')