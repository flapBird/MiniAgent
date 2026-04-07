import pickle
import os
import numpy as np

class FileVectorStore:

    def __init__(self, path="data/vector_store.pkl"):
        self.path = path
        self.vectors = []
        self.docs = []

    def add(self, doc, vector):
        self.docs.append(doc)
        self.vectors.append(vector)

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with open(self.path, "wb") as f:
            pickle.dump({
                "docs": self.docs,
                "vectors": self.vectors
            }, f)

    def load(self):
        if not os.path.exists(self.path):
            return False

        with open(self.path, "rb") as f:
            data = pickle.load(f)
            self.docs = data["docs"]
            self.vectors = data["vectors"]

        return True

    def search(self, query_vector, top_k=5):
        if not self.vectors:
            return []

        sims = []

        for vec in self.vectors:
            sim = np.dot(query_vector, vec) / (
                np.linalg.norm(query_vector) * np.linalg.norm(vec)
            )
            sims.append(sim)

        top_indices = np.argsort(sims)[::-1][:top_k]

        return [self.docs[i]["text"] for i in top_indices]