from abc import ABC, abstractmethod
from typing import List


class BaseReranker(ABC):

    @abstractmethod
    def rerank(self, query: str, docs: List[str], top_k: int) -> List[str]:
        """
        输入：
            query: 用户问题
            docs: 候选文档（Recall阶段结果）
            top_k: 最终返回数量

        输出：
            排序后的文档列表（长度 <= top_k）
        """
        pass