"""Lab 2: same POST as lab 1. Print the data contract keys."""
import json
import os
import sys
import urllib.error
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
URL = f"{HOST}/api/generate"

payload = {
    "model": MODEL,
    "prompt": "Reply with one sentence: what is JSON?",
    "stream": False,
    "options": {"temperature": 0.0},
}

print("REQUEST KEYS")
print(json.dumps(payload, indent=2))

req = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode("utf-8"))
except urllib.error.URLError as exc:
    raise SystemExit(f"Provider not reachable at {URL}: {exc}") from exc

print("\nRESPONSE KEYS")
print(sorted(body.keys()))

print("\nFIELDS WE WILL KEEP USING")
print(f"done={body.get('done')}")
print(f"eval_count={body.get('eval_count')}")
print(f"response={((body.get('response') or '').strip())}")
