from abc import ABC, abstractmethod


class BaseToolAdapter(ABC):

    @abstractmethod
    def handle(self, response, memory, session_id) -> bool:
        """
        处理 tool 调用

        返回：
        True  -> 已处理 tool（需要继续 loop）
        False -> 没有 tool（可以结束）
        """
        pass