from typing import Dict, List
from memory.base import BaseMemory


class InMemory(BaseMemory):

    def __init__(self, max_history: int = 50):
        self.sessions: Dict[str, List[Dict]] = {}
        self.max_history = max_history

    def get_messages(self, session_id: str) -> List[Dict]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def append(self, session_id: str, message: Dict):
        msgs = self.get_messages(session_id)
        msgs.append(message)

        # 控制上下文长度
        if len(msgs) > self.max_history:
            self.sessions[session_id] = msgs[-self.max_history:]

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]