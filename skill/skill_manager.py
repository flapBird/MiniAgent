import os

class SkillMeta:
    def __init__(self, name, path):
        self.name = name
        self.path = path


class SkillManager:


    def __init__(self):
        base_dir = os.getcwd()
        self.skills_path = os.path.join(base_dir, "skillDir")
        self.skill_index = {}  # 👈 只存元信息

        self._build_index()

    def _build_index(self):

        if not os.path.exists(self.skills_path):
            return

        for name in os.listdir(self.skills_path):
            skill_dir = os.path.join(self.skills_path, name)

            if os.path.isdir(skill_dir):
                self.skill_index[name] = SkillMeta(name, skill_dir)

    def list(self):
        return list(self.skill_index.keys())

    def get(self, name):
        return self.skill_index.get(name)