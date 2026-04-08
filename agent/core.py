from memory.memory_manager import MemoryManager
from skill.skill_loader import load_skill
from skill.skill_manager import SkillManager

class Agent:

    def __init__(self, llm, adapter, tool_map, tools):
        self.llm = llm
        self.tool_map = tool_map
        self.tools = tools
        self.memory = MemoryManager()
        self.adapter = adapter
        self.skill_manager = SkillManager()

    def run(self, session_id, user_input: str, skill_name=None):
        self.memory.add_user_message(session_id, user_input)

        while True:
            # 取出会话中之前的消息
            messages = self.memory.get_messages(session_id)

            # 加载技能
            if skill_name:
                skill_metadata = self.skill_manager.get(name=skill_name)
                skill = load_skill(skill_metadata.path)
                # 将技能前插到会话信息
                messages = [
                               {"role": "system", "content": skill.prompt}
                           ] + messages

            response = self.llm.chat(messages, tools= self.tools)

            content = response.get("content", "")

            if content:
                self.memory.add_assistant_message(session_id, content)

            handled = self.adapter.handle(response, self.memory, session_id)
            if not handled:
                return content
