import hashlib
from rag.embedding.base import BaseEmbedding

class LocalEmbedding(BaseEmbedding):

    def embed(self, text: str):
        return [int(hashlib.md5(text.encode()).hexdigest(), 16) % 1000000]