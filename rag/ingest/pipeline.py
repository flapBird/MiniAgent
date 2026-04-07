class RAGIngestPipeline:

    def __init__(self, loader, chunker, embedding, store):
        self.loader = loader
        self.chunker = chunker
        self.embedding = embedding
        self.store = store  # 👈 依赖抽象

    def run(self, docs_path):

        docs = self.loader(docs_path)

        # 从 store 获取已有数据（避免重复）
        existing_docs = self.store.get_all_docs()
        existing_texts = set([d["text"] for d in existing_docs])

        new_chunks = 0

        for doc in docs:
            chunks = self.chunker.split(doc["content"])

            for i, chunk in enumerate(chunks):

                if chunk in existing_texts:
                    continue

                vector = self.embedding.embed(chunk)

                self.store.add({
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_id": i
                }, vector)

                new_chunks += 1

        self.store.save()

        return new_chunks