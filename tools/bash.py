import shlex
import subprocess
from tools.base import BaseTool
import re,json

class BashTool(BaseTool):
    name = "bash"
    description = """
                    Execute safe bash commands on local machine. 
                    Allowed commands:
                    - ls: list directory contents, allowed flags: -l, -a, -la
                    - pwd: print current directory
                    - echo: print text
                    - cat: print file content
                    Do NOT use any other commands or destructive operations.
                   """

    # LLM 调用时可用命令和允许参数
    ALLOWED_COMMANDS = {
        "ls": ["-l", "-a", "-la"],
        "pwd": [],
        "echo": [],
        "cat": []
    }

    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The bash command to execute (must be allowed command)"
            }
        },
        "required": ["command"]
    }

    def run(self, command: str):
        # 1️⃣ 修复 JSON 格式
        fixed_args = re.sub(r'([{,]\s*)(\w+)\s*:', r'\1"\2":', command)
        args_dict = json.loads(fixed_args)

        # 2️⃣ 获取命令字符串
        command_str = args_dict["command"]

        # 3️⃣ 用 shlex 拆分成合法列表
        try:
            cmd_parts = shlex.split(command_str)
        except Exception as e:
            return f"Failed to parse command: {e}"

        if not cmd_parts:
            return "Empty command"

        cmd = cmd_parts[0]
        args = cmd_parts[1:]

        # 检查命令是否在白名单
        if cmd not in self.ALLOWED_COMMANDS:
            return f"Command '{cmd}' not allowed"

        # 检查参数是否在白名单
        allowed_args = self.ALLOWED_COMMANDS[cmd]
        for arg in args:
            if arg not in allowed_args:
                return f"Argument '{arg}' not allowed for command '{cmd}'"

        # 执行命令
        try:
            result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=5)
            return result.stdout or result.stderr
        except Exception as e:
            return str(e)