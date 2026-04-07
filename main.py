from llm.factory import get_llm
from agent.core import Agent
from tools.init import get_all_tools
from dotenv import load_dotenv
from tools.adapter.openai import OpenAIToolAdapter
from tools.adapter.claude import ClaudeToolAdapter
from rag.ingest.builder import build_rag
from openai import OpenAI
import os, uuid


def main():
    # 加载环境变量
    load_dotenv()

    # 加载LLM模型
    provider = os.getenv("LLM_PROVIDER", "openai")  # 选择LLM提供商
    api_key = os.getenv("LLM_API_KEY") #API Key
    base_url = os.getenv("LLM_BASE_URL", default="https://api.openai.com/v1")  # API地址
    llm = get_llm(
        provider = provider.__str__(),
        api_key = api_key,
        model_name  = os.getenv("LLM_MODEL", default="openai/gpt-oss-20b"), # 模型名称
        base_url = base_url
    )

    # 导入知识库
    retriever = build_rag(OpenAI(api_key=api_key, base_url=base_url))

    # 加载工具
    tool_map, tool_schemas = get_all_tools(retriever)

    # 适配工具
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