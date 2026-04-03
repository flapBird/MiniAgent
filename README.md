# MiniAgent - 基于LLM的智能代理系统

MiniAgent是一个轻量级的智能代理系统，基于大语言模型（LLM）构建，支持工具调用和交互式对话。系统采用模块化设计，易于扩展和维护。

## 功能特性

- **多LLM支持**：支持OpenAI/Groq API和DeepSeek API
- **工具调用**：支持安全的bash命令执行工具
- **交互式对话**：提供命令行交互界面
- **模块化架构**：清晰的模块分离，易于扩展
- **安全控制**：对工具调用进行严格的安全限制

## 项目结构

```
MiniAgent/
├── main.py                    # 程序入口点
├── .env.example              # 环境变量示例
├── README.md                 # 项目文档
├── agent/                    # Agent核心模块
│   ├── __init__.py
│   └── core.py              # Agent类实现
├── llm/                      # LLM模块
│   ├── __init__.py
│   ├── base.py              # LLM基类
│   ├── factory.py           # LLM工厂
│   ├── openai_llm.py        # OpenAI/Groq实现
│   └── deepseek_llm.py      # DeepSeek实现
└── tools/                    # 工具模块
    ├── __init__.py
    ├── base.py              # 工具基类
    ├── bash.py              # Bash工具实现
    └── init.py              # 工具初始化
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+，然后安装依赖：

```bash
pip install openai requests python-dotenv
```

### 2. 配置环境变量

复制环境变量示例文件并配置：

```bash
cp .env.example .env
```

编辑`.env`文件，设置您的API密钥：

```env
LLM_API_KEY=your_api_key_here
LLM_PROVIDER=openai  # 可选：openai 或 deepseek
LLM_MODEL=openai/gpt-oss-20b
```

### 3. 运行程序

```bash
python main.py
```

程序启动后，输入对话内容与AI交互，输入`exit`或`quit`退出。

## 架构设计

### 核心组件

#### 1. LLM模块 (`llm/`)
- **BaseLLM**：抽象基类，定义`chat()`和`stream_chat()`接口
- **OpenAILLM**：使用OpenAI/Groq API的实现
- **DeepSeekLLM**：使用DeepSeek API的实现
- **factory.py**：工厂模式，根据配置创建LLM实例

#### 2. Agent模块 (`agent/`)
- **Agent类**：核心代理类，管理对话流程和工具调用
- 支持多轮对话和工具调用循环
- 将工具执行结果反馈给LLM进行后续处理

#### 3. 工具模块 (`tools/`)
- **BaseTool**：工具基类，定义工具接口和模式生成
- **BashTool**：安全的bash命令执行工具
- **init.py**：工具注册和初始化

### 工作流程

1. **初始化**：加载环境变量，创建LLM实例，注册工具
2. **对话循环**：接收用户输入，调用LLM生成响应
3. **工具调用**：如果LLM返回工具调用，执行相应工具
4. **结果反馈**：将工具执行结果作为消息追加，继续对话
5. **循环终止**：当LLM返回最终答案或无工具调用时结束

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| LLM_API_KEY | LLM API密钥 | 无 | sk-xxx |
| LLM_PROVIDER | LLM提供商 | openai | openai/deepseek |
| LLM_MODEL | 模型名称 | openai/gpt-oss-20b | deepseek-chat |

### 支持的LLM提供商

1. **OpenAI/Groq** (`provider="openai"`)
   - 使用OpenAI客户端，但配置为Groq API端点
   - 支持工具调用和流式输出

2. **DeepSeek** (`provider="deepseek"`)
   - 使用DeepSeek REST API
   - 支持基础对话功能

## 工具系统

### BashTool

BashTool提供安全的本地命令执行功能，严格限制可执行的命令和参数：

#### 允许的命令
- `ls`：列出目录内容（允许参数：`-l`, `-a`, `-la`）
- `pwd`：显示当前工作目录
- `echo`：输出文本
- `cat`：显示文件内容

#### 安全特性
1. **命令白名单**：只允许预定义的安全命令
2. **参数验证**：检查参数是否在允许范围内
3. **超时控制**：命令执行超时设置为5秒
4. **JSON解析**：安全解析LLM返回的命令参数

### 扩展新工具

要添加新工具，需要：

1. 创建新工具类，继承`BaseTool`
2. 实现`run()`方法
3. 在`tools/init.py`的`get_all_tools()`函数中注册

示例工具类结构：

```python
from tools.base import BaseTool

class MyTool(BaseTool):
    name = "my_tool"
    description = "工具描述"
    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数说明"}
        },
        "required": ["param1"]
    }
    
    def run(self, **kwargs):
        # 工具逻辑
        return "执行结果"
```

## 开发指南

### 添加新的LLM提供商

1. 在`llm/`目录下创建新的LLM类，继承`BaseLLM`
2. 实现`chat()`和`stream_chat()`方法
3. 在`llm/factory.py`的`get_llm()`函数中添加新的provider分支

### 调试与测试

#### 查看工具调用
系统会在控制台显示工具调用和执行结果，便于调试。

#### 环境变量调试
确保`.env`文件正确配置，或通过命令行设置环境变量：

```bash
export LLM_API_KEY=your_key
export LLM_PROVIDER=openai
python main.py
```

## 注意事项

### 安全性
1. **BashTool限制**：BashTool严格限制可执行命令，防止恶意操作
2. **API密钥保护**：不要将`.env`文件提交到版本控制系统
3. **输入验证**：用户输入直接传递给LLM，需注意提示注入风险

### 性能考虑
1. **工具调用延迟**：每次工具调用都会增加对话轮次
2. **API成本**：注意LLM API调用的token消耗
3. **超时设置**：BashTool有5秒超时限制，防止长时间阻塞

### 扩展性
1. **模块化设计**：各模块职责清晰，易于替换和扩展
2. **工厂模式**：LLM创建使用工厂模式，支持热切换
3. **工具注册**：工具系统支持动态注册新工具

## 故障排除

### 常见问题

1. **API连接失败**
   - 检查网络连接
   - 验证API密钥是否正确
   - 确认API服务是否可用

2. **工具调用失败**
   - 检查命令是否在允许列表中
   - 验证命令参数格式
   - 查看工具执行权限

3. **环境变量未加载**
   - 确保`.env`文件在项目根目录
   - 检查变量名是否正确
   - 尝试重启程序

### 日志查看
程序会在控制台输出关键信息，包括：
- LLM响应内容
- 工具调用请求
- 工具执行结果
- 错误信息

## 未来规划

### 计划功能
1. **更多工具支持**：文件操作、网络请求、数据库查询等
2. **记忆管理**：对话历史持久化存储
3. **插件系统**：支持第三方插件扩展
4. **Web界面**：提供图形化交互界面
5. **多Agent协作**：支持多个Agent协同工作

### 优化方向
1. **性能优化**：减少API调用延迟
2. **错误处理**：更完善的异常处理机制
3. **配置管理**：支持更灵活的配置方式ß
4. **测试覆盖**：增加单元测试和集成测试
