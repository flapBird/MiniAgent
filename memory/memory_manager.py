from memory.in_memory import InMemory


class MemoryManager:

    def __init__(self, backend=None):
        # 支持依赖注入（可换 Redis / DB）
        self.backend = backend or InMemory()

    def get_messages(self, session_id: str):
        return self.backend.get_messages(session_id)

    def add_user_message(self, session_id: str, content: str):
        self.backend.append(session_id, {
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, session_id: str, content: str):
        self.backend.append(session_id, {
            "role": "assistant",
            "content": content
        })

    def clear(self, session_id: str):
        self.backend.clear(session_id)