from rag.ingest.pipeline import RAGIngestPipeline
from rag.ingest.chunker import Chunker
from rag.ingest.loader import load_documents
from rag.retriever import Retriever
from rag.store.memory import MemoryVectorStore
from rag.embedding.openai import OpenAIEmbedding
from rag.reranker.cross_encoder import CrossEncoderReranker
import os

def build_rag(client):
    embedding = OpenAIEmbedding(client)
    store = MemoryVectorStore()

    pipeline = RAGIngestPipeline(
        loader=load_documents,
        chunker=Chunker(),
        embedding=embedding,
        store=store
    )

    base_dir = os.getcwd()
    docs_dir = os.path.join(base_dir, "docs")
    pipeline.run(docs_dir)

    retriever = Retriever(
        embedding=embedding,
        store=store,
        reranker=CrossEncoderReranker()
    )

    return retriever
