from rag.store.base import BaseVectorStore

class MemoryVectorStore(BaseVectorStore):

    def __init__(self):
        self.data = []

    def add(self, text, vector):
        self.data.append((text, vector))

    def search(self, query_vector, top_k):
        scored = [
            (text, abs(vector[0] - query_vector[0]))
            for text, vector in self.data
        ]

        scored.sort(key=lambda x: x[1])

        return [text for text, _ in scored[:top_k]]