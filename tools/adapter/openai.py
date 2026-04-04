import json
from tools.adapter.base import BaseToolAdapter


class OpenAIToolAdapter(BaseToolAdapter):

    def __init__(self, tool_map):
        self.tool_map = tool_map

    def handle(self, response, memory, session_id) -> bool:
        tool_calls = response.get("tool_calls", [])

        if not tool_calls:
            return False

        for tool_call in tool_calls:
            tool_id = tool_call.id
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments  # 是 JSON 字符串

            # 根据工具类型执行对应操作，这里以 bash 为例
            tool = self.tool_map.get(tool_name)

            if not tool:
                raise Exception(f"Tool {tool_name} not found")

            output = tool.run(arguments)

            memory.backend.append(session_id, {
                "role": "tool",
                "tool_call_id": tool_id,
                "name": tool_name,
                "content": str(output)
            })

        return True