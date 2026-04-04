from memory.memory_manager import MemoryManager


class Agent:

    def __init__(self, llm, adapter, tool_map, tools):
        self.llm = llm
        self.tool_map = tool_map
        self.tools = tools
        self.memory = MemoryManager()
        self.adapter = adapter

    def run(self, session_id, user_input: str):
        self.memory.add_user_message(session_id, user_input)

        while True:
            # 取出会话中之前的消息
            messages = self.memory.get_messages(session_id)

            response = self.llm.chat(messages, tools= self.tools)

            content = response.get("content", "")

            if content:
                self.memory.add_assistant_message(session_id, content)

            handled = self.adapter.handle(response, self.memory, session_id)
            if not handled:
                return content

            # if not response["tool_calls"]:
            #     return content
            #
            # for tool_call in response["tool_calls"]:
            #     tool_id = tool_call.id
            #     tool_name = tool_call.function.name
            #     arguments = tool_call.function.arguments  # 是 JSON 字符串
            #
            #     # 根据工具类型执行对应操作，这里以 bash 为例
            #     tool = self.tool_map.get(tool_name)
            #
            #     if not tool:
            #         return f"Tool {tool_name} not found"
            #
            #     output = tool.run(arguments)
            #     # 写入 tool 结果
            #     self.memory.backend.append(session_id, {
            #         "role": "tool",
            #         "tool_call_id": tool_id,
            #         "content": output
            #     })

            #     results.append({
            #         "type": "tool_result",
            #         "tool_use_id": tool_id,
            #         "content": output,
            #     })
            #
            # # 可以将结果作为消息追加到 messages
            # results_str = json.dumps(results, ensure_ascii=False)
            # messages.append({"role": "user", "content": results_str})
