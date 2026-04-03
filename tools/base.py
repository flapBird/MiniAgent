from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str
    description: str
    parameters: dict

    @abstractmethod
    def run(self, **kwargs):
        pass

    def to_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }