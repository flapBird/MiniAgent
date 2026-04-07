from tools.base import BaseTool


class RagTool(BaseTool):
    name = "rag_search"

    description = """
    Search knowledge base for relevant information.
    Use this tool when the user asks about specific facts, documents, or domain knowledge.
    """

    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up in the knowledge base"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of relevant documents to return",
                "default": 3
            }
        },
        "required": ["query"]
    }

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, args):
        """
        args: dict
        {
            "query": "...",
            "top_k": 3
        }
        """

        try:
            query = args.get("query", "")
            top_k = args.get("top_k", 3)

            if not query:
                return "Query is empty"

            docs = self.retriever.search(query, top_k)

            if not docs:
                return "No relevant information found."

            # 格式化输出（让 LLM 更容易理解）
            result = "\n\n".join(
                [f"[Doc {i+1}]\n{doc}" for i, doc in enumerate(docs)]
            )

            return result

        except Exception as e:
            return f"RAG search failed: {str(e)}"