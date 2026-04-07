class RAGIngestPipeline:

    def __init__(self, loader, chunker, embedding, store):
        self.loader = loader
        self.chunker = chunker
        self.embedding = embedding
        self.store = store

    def run(self, docs_path):

        docs = self.loader(docs_path)

        new_chunks = 0

        for doc in docs:
            chunks = self.chunker.split(doc["content"])

            for i, chunk in enumerate(chunks):
                vector = self.embedding.embed(chunk)

                self.store.add({
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_id": i
                }, vector)

                new_chunks += 1

        self.store.save()

        return new_chunks