import faiss
import numpy as np


class FaissVectorStore:

    def __init__(self, dim: int):
        """
        dim: 向量维度
        """
        self.dim = dim

        # 使用 L2 距离（也可以换成 Inner Product）
        self.index = faiss.IndexFlatIP(dim)

        self.docs = []  # 存文档

    def add(self, doc, vector):
        """
        doc: {"text": "..."}
        vector: numpy array (dim,)
        """
        vector = np.array(vector).astype("float32")

        # FAISS 要求二维
        vector = np.expand_dims(vector, axis=0)

        # 如果用 cosine，需要 normalize
        faiss.normalize_L2(vector)

        self.index.add(vector)
        self.docs.append(doc)

    def add_batch(self, docs, vectors):
        """
        批量添加
        """
        vectors = np.array(vectors).astype("float32")

        faiss.normalize_L2(vectors)

        self.index.add(vectors)
        self.docs.extend(docs)

    def search(self, query_vector, top_k=5):
        if self.index.ntotal == 0:
            return []

        query_vector = np.array(query_vector).astype("float32")
        query_vector = np.expand_dims(query_vector, axis=0)

        faiss.normalize_L2(query_vector)

        # 搜索
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.docs[idx]["text"])

        return results