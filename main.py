from llm.factory import get_llm
from agent.core import Agent
from tools.init import get_all_tools
from dotenv import load_dotenv
from tools.adapter.openai import OpenAIToolAdapter
from tools.adapter.claude import ClaudeToolAdapter
import os, uuid


def main():
    # 加载环境变量
    load_dotenv()

    # 加载LLM模型
    llm = get_llm(
        provider = os.getenv("LLM_PROVIDER", "openai"),  # 选择模型
        api_key = os.getenv("LLM_API_KEY"),  # API Key
        model_name  = os.getenv("LLM_MODEL", default="openai/gpt-oss-20b")  # 模型名称
    )

    # 加载工具
    tool_map, tool_schemas = get_all_tools()

    # 适配工具
    provider = os.getenv("LLM_PROVIDER", "openai")

    if provider == "openai":
        adapter = OpenAIToolAdapter(tool_map)
    elif provider == "claude":
        adapter = ClaudeToolAdapter(tool_map)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    agent = Agent(llm, adapter, tool_map, tool_schemas)

    session_id = str(uuid.uuid4())

    print("\n请输入对话，输入 'exit' 或 'quit' 退出。")

    while True:
        user_input = input("\n你: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        print("\nAI:", end=" ")
        print(agent.run(session_id, user_input))

if __name__ == "__main__":
    main()