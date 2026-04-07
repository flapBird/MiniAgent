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
