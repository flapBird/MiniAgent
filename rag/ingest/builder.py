from rag.ingest.pipeline import RAGIngestPipeline
from rag.ingest.chunker import Chunker
from rag.ingest.loader import load_documents
from rag.retriever import Retriever
from rag.store.faiss_store import FaissVectorStore
from rag.embedding.sentence_embed import LocalSentenceEmbedding
from rag.reranker.cross_encoder import CrossEncoderReranker
import os

def build_rag():
    embedding = LocalSentenceEmbedding(model_name="BAAI/bge-small-zh")
    store = FaissVectorStore(embedding.model.get_sentence_embedding_dimension())

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
