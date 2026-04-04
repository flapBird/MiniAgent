from .base import BaseToolAdapter


class ClaudeToolAdapter(BaseToolAdapter):

    def __init__(self, tool_map):
        self.tool_map = tool_map

    def handle(self, response, memory, session_id) -> bool:
        contents = response.content or []

        results = []

        for block in contents:
            if block["type"] == "tool_use":
                tool_name = block["name"]
                tool_input = block["input"]

                tool = self.tool_map.get(tool_name)
                if not tool:
                    raise Exception(f"Tool {tool_name} not found")

                output = tool.run(tool_input)

                results.append({
                    "type": "tool_result",
                    "tool_use_id": block["id"],
                    "content": str(output),
                })

        if results:
            memory.backend.append(session_id, {
                "role": "user",
                "content": results
            })
            return True

        return False