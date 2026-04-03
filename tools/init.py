from tools.bash import BashTool


def get_all_tools():
    tools = [
        BashTool()
    ]

    tool_map = {tool.name: tool for tool in tools}
    tool_schemas = [tool.to_schema() for tool in tools]

    return tool_map, tool_schemas