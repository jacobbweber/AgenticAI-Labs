"""Lab: one tool_calls dispatch through TOOL_REGISTRY. Chapter 03."""
import json
import os
import sys
import urllib.request


def add_numbers(a, b) -> str:
    return str(a + b)


TOOL_REGISTRY = {"add_numbers": add_numbers}

HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
messages = [{"role": "user", "content": "What is 2 plus 3? Use the tool."}]
tools = [{
    "type": "function",
    "function": {
        "name": "add_numbers",
        "description": "Add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    },
}]


def post(msgs):
    payload = {"model": MODEL, "messages": msgs, "tools": tools, "stream": False}
    req = urllib.request.Request(
        f"{HOST}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


data = post(messages)
calls = data.get("message", {}).get("tool_calls") or []
if not calls:
    print("tool_calls empty; model answered in prose", file=sys.stderr)
    sys.exit(1)
fn = calls[0]["function"]
name, arguments = fn["name"], fn["arguments"]
if isinstance(arguments, str):
    arguments = json.loads(arguments)
if name not in TOOL_REGISTRY:
    print(name, file=sys.stderr)
    sys.exit(1)
result = TOOL_REGISTRY[name](**arguments)
print(name, arguments, result)
messages.append({"role": "tool", "content": result})
