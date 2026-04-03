from llm.factory import get_llm
from agent.core import Agent
from tools.init import get_all_tools
from dotenv import load_dotenv
import os

def main():
    # 选择模型
    load_dotenv()
    llm = get_llm(
        provider = os.getenv("LLM_PROVIDER", "openai"),  # 选择模型
        api_key = os.getenv("LLM_API_KEY"),  # API Key
        model_name  = os.getenv("LLM_MODEL", default="openai/gpt-oss-20b")  # 模型名称
    )
    tool_map, tool_schemas = get_all_tools()
    agent = Agent(llm, tool_map, tool_schemas)
    print("\n请输入对话，输入 'exit' 或 'quit' 退出。")

    while True:
        user_input = input("\n你: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        print("\nAI:", end=" ")
        print(agent.run(user_input))

if __name__ == "__main__":
    main()