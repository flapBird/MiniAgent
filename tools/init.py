from tools.bash import BashTool
from tools.rag_tool import RagTool

def get_all_tools(retriever):
    # 工具注册
    tools = [
        BashTool(),
        RagTool(retriever)
    ]

    tool_map = {tool.name: tool for tool in tools}
    tool_schemas = [tool.to_schema() for tool in tools]

    return tool_map, tool_schemas