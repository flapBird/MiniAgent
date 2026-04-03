import json

from pyexpat.errors import messages


class Agent:

    def __init__(self, llm, tool_map, tools):
        self.llm = llm
        self.tool_map = tool_map
        self.tools = tools

    def run(self, user_input: str):

        messages = [
            {"role": "user", "content": user_input}
        ]

        while True:
            response = self.llm.chat(messages, tools= self.tools)

            messages.append({"role": "assistant", "content": response["content"] or ""})

            if not response["tool_calls"]:
                return response["content"]

            results = []

            for tool_call in response["tool_calls"]:
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments  # 是 JSON 字符串

                # 根据工具类型执行对应操作，这里以 bash 为例
                tool = self.tool_map.get(tool_name)

                if not tool:
                    return f"Tool {tool_name} not found"

                output = tool.run(arguments)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": output,
                })
            # 可以将结果作为消息追加到 messages
            results_str = json.dumps(results, ensure_ascii=False)
            messages.append({"role": "user", "content": results_str})
