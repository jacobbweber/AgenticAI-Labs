"""Lab 1: POST JSON to a provider. Print the text. No wrapper."""
import json
import os
import urllib.error
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://192.168.1.29:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b-a3b-65k")
URL = f"{HOST}/api/generate"

payload = {
    "model": MODEL,
    "prompt": "In 2 sentences, explain what an HTTP POST request is.",
    "stream": False,
}

print(f"POST {URL}")
print(f"model={MODEL}")

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

text = (body.get("response") or "").strip()
if not text:
    raise SystemExit("Response JSON had an empty 'response' field. Check the route and model.")
print(text)
