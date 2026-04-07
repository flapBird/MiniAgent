from openai import OpenAI
from .base import BaseLLM


class OpenAILLM(BaseLLM):
    def __init__(self, api_key, model_name, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model_name

    def chat(self, messages, **kwargs):
        # 构建请求参数
        params = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }

        resp = self.client.chat.completions.create(**params)

        # 检查是否有 tool calls
        message = resp.choices[0].message

        return {
            "content": message.content,
            "tool_calls": getattr(message, "tool_calls", None),
            "usage": resp.usage
        }

    def stream_chat(self, messages, **kwargs):
        params = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            **kwargs
        }

        stream = self.client.chat.completions.create(**params)

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            tool_calls = getattr(delta, "tool_calls", None)

            if content:
                yield {"type": "content", "data": content}
            if tool_calls:
                yield {"type": "tool_calls", "data": tool_calls}