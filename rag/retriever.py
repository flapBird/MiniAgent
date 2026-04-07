class Retriever:

    def __init__(self, embedding, store, reranker=None):
        self.embedding = embedding
        self.store = store
        self.reranker = reranker

    def search(self, query: str, top_k: int = 3):

        query_vec = self.embedding.embed(query)

        # ① Recall（多取一点）
        candidates = self.store.search(query_vec, top_k=10)

        # ② Rerank
        if self.reranker:
            reranked = self.reranker.rerank(query, candidates, top_k)

            # 如果返回 dict（带 score）
            if isinstance(reranked[0], dict):
                return [item["doc"] for item in reranked]

            return reranked

        return candidates[:top_k]