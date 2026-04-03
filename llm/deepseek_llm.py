import requests
from typing import List, Dict, Any, Generator
from .base import BaseLLM


class DeepSeekLLM(BaseLLM):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.deepseek.com/chat/completions"

    def chat(self, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        resp = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": messages
            }
        )

        data = resp.json()

        return {
            "content": data["choices"][0]["message"]["content"],
            "usage": data.get("usage")
        }

    def stream_chat(self, messages: List[Dict], **kwargs) -> Generator[str, None, None]:
        # DeepSeek 简化版（有些接口支持 stream，这里先占位）
        yield self.chat(messages)["content"]