from rag.embedding.base import BaseEmbedding

class OpenAIEmbedding(BaseEmbedding):

    def __init__(self, client):
        self.client = client

    def embed(self, text: str):
        resp = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return resp.data[0].embedding