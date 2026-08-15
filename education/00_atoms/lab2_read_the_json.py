"""Lab 2: same POST as lab 1. Print the data contract keys."""
import json
import os
import urllib.error
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://192.168.1.29:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b-a3b-65k")
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
