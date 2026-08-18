"""Lab: save and load messages.json. Chapter 05."""
import json
import os

PATH = os.path.join(os.path.dirname(__file__), "messages.json")


def save_messages(messages):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)
    print(PATH)


def load_messages():
    if not os.path.exists(PATH):
        return []
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You add numbers."},
        {"role": "user", "content": "What is 42 plus 58?"},
        {"role": "assistant", "content": "100"},
    ]
    save_messages(messages)
    loaded = load_messages()
    for item in loaded:
        print(item["role"], item["content"])
