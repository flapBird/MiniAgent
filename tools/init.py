from tools.bash import BashTool
from tools.rag_tool import RagTool
from rag.embedding.local import LocalEmbedding
from rag.store.memory import MemoryVectorStore
from rag.retriever import Retriever
from rag.reranker.cross_encoder import CrossEncoderReranker

def get_all_tools():
    retriever = build_rag()

    #工具注册
    tools = [
        BashTool(),
        # RagTool(retriever)
    ]

    tool_map = {tool.name: tool for tool in tools}
    tool_schemas = [tool.to_schema() for tool in tools]

    return tool_map, tool_schemas


def build_rag():
    embedding = LocalEmbedding()
    store = MemoryVectorStore()
    reranker = CrossEncoderReranker()

    retriever = Retriever(
        embedding=embedding,
        store=store,
        reranker=reranker
    )

    return retriever