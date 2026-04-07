from rag.reranker.base import BaseReranker

class SimpleReranker(BaseReranker):

    def rerank(self, query, docs, top_k):
        # 简单按长度排序
        docs_sorted = sorted(docs, key=lambda x: len(x))
        return docs_sorted[:top_k]