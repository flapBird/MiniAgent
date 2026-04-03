from .openai_llm import OpenAILLM
from .deepseek_llm import DeepSeekLLM


def get_llm(provider: str, **kwargs):
    if provider == "openai":
        return OpenAILLM(**kwargs)

    elif provider == "deepseek":
        return DeepSeekLLM(**kwargs)

    else:
        raise ValueError(f"Unsupported provider: {provider}")