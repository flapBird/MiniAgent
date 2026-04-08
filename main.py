from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from agent.core import Agent
from tools.adapter.openai import OpenAIToolAdapter
from tools.init import get_all_tools
from rag.ingest.builder import build_rag
import os
from dotenv import load_dotenv

# ------------------ 环境变量 ------------------
load_dotenv()
provider = os.getenv("LLM_PROVIDER", "openai")  # 选择LLM提供商
api_key = os.getenv("LLM_API_KEY")  # API Key
base_url = os.getenv("LLM_BASE_URL", default="https://api.openai.com/v1")
model_name = os.getenv("LLM_MODEL", default="openai/gpt-oss-20b")

# ------------------ 初始化 LLM ------------------
from llm.factory import get_llm
llm = get_llm(
    provider=provider.__str__(),
    api_key=api_key,
    model_name=os.getenv("LLM_MODEL", default="openai/gpt-oss-20b"),  # 模型名称
    base_url=base_url
)

# ------------------ 导入知识库 ------------------
retriever = build_rag()

# ------------------ 初始化工具 ------------------
tool_map, tool_schemas = get_all_tools(retriever)
if provider == "openai":
    adapter = OpenAIToolAdapter(tool_map)
else:
    raise ValueError(f"Unsupported provider: {provider}")

# ------------------ 初始化 Agent ------------------
agent = Agent(llm=llm, adapter=adapter, tool_map=tool_map, tools=tool_schemas)

# ------------------ FastAPI ------------------
app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/message")
async def message(payload: dict):
    session_id = payload.get("session_id", "default")
    user_input = payload.get("user_input", "")
    print("Received input:", user_input)
    response = agent.run(session_id, user_input)
    print("Agent response:", response)
    return {"response": response}