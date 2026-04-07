from abc import ABC, abstractmethod
from typing import List


class BaseVectorStore(ABC):

    @abstractmethod
    def add(self, text: str, vector: List[float]):
        pass

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int):
        pass