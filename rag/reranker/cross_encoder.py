import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from sentence_transformers import CrossEncoder
from rag.reranker.base import BaseReranker

class CrossEncoderReranker(BaseReranker):
        def __init__(self, model_name="BAAI/bge-reranker-base"):
            self.model = CrossEncoder(model_name)

        def rerank(self, query, docs, top_k=3):
            pairs = [(query, doc) for doc in docs]
            scores = self.model.predict(pairs)

            scored_docs = [
                {"doc": doc, "score": float(score)}
                for doc, score in zip(docs, scores)
            ]

            scored_docs.sort(key=lambda x: x["score"], reverse=True)

            return scored_docs[:top_k]