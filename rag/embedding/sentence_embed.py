from sentence_transformers import SentenceTransformer
from rag.embedding.base import BaseEmbedding

class LocalSentenceEmbedding(BaseEmbedding):

    def __init__(self, model_name="BAAI/bge-small-zh"):
        """
        model_name:
            中文推荐: BAAI/bge-small-zh
            英文推荐: all-MiniLM-L6-v2
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        """
        输入: 单条文本
        输出: embedding vector (list[float])
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True  # 直接做 cosine 标准化
        )

        return embedding.tolist()