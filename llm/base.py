from abc import ABC, abstractmethod
from typing import List, Dict


class BaseLLM(ABC):

    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> Dict:
        """普通对话"""
        pass

    @abstractmethod
    def stream_chat(self, messages: List[Dict], **kwargs):
        """流式输出"""
        pass