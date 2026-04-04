from abc import ABC, abstractmethod
from typing import List, Dict


class BaseMemory(ABC):

    @abstractmethod
    def get_messages(self, session_id: str) -> List[Dict]:
        pass

    @abstractmethod
    def append(self, session_id: str, message: Dict):
        pass

    @abstractmethod
    def clear(self, session_id: str):
        pass