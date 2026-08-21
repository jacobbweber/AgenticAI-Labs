"""Lab: structured JSON from POST /api/chat. Chapter 02."""
import json
import os
import sys
import urllib.request
from pathlib import Path

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

messages = [
    {
        "role": "system",
        "content": "Reply with JSON only. Keys: intent (string), confidence (number 0-1).",
    },
    {"role": "user", "content": "Classify: reset my password"},
]
payload = {"model": MODEL, "messages": messages, "stream": False, "format": "json"}
req = urllib.request.Request(
    f"{HOST}/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)

try:
    with urllib.request.urlopen(req, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

text = data["message"]["content"].strip()
if text.startswith("```"):
    lines = text.splitlines()
    end = -1 if lines[-1].strip().startswith("```") else None
    text = "\n".join(lines[1:end])

try:
    obj = json.loads(text)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}", file=sys.stderr)
    sys.exit(1)

intent, confidence = obj.get("intent"), obj.get("confidence")
if not isinstance(intent, str) or not intent:
    print("intent must be a non-empty string", file=sys.stderr)
    sys.exit(1)
if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
    print("confidence must be a number", file=sys.stderr)
    sys.exit(1)
print(obj)
