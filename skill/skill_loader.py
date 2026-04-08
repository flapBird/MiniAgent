import os
import yaml
from skill.skill_model import Skill

def load_skill(skill_dir):

    md_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(md_path):
        return None

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 分离 YAML + Prompt
    if content.startswith("---"):
        parts = content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        prompt = parts[2].strip()
    else:
        meta = {}
        prompt = content

    return Skill(
        name=meta.get("name"),
        description=meta.get("description"),
        tools=meta.get("tools", []),
        prompt=prompt
    )