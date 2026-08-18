"""Lab: load SKILL.md when pr-review matches. Chapter 14."""
import os


def load_skill(user_text, skill_path):
    if "pr-review" not in user_text:
        return {"loaded": False}
    with open(skill_path, encoding="utf-8") as f:
        return {"loaded": True, "path": skill_path, "body": f.read()}


if __name__ == "__main__":
    skill_path = os.path.join(os.path.dirname(__file__), "SKILL.md")
    hit = load_skill("Please do a pr-review on this branch", skill_path)
    print("trigger", "pr-review")
    print("path", hit["path"])
    print("body", hit["body"])
    miss = load_skill("What is 2+2?", skill_path)
    print("skipped")
    assert miss == {"loaded": False}
