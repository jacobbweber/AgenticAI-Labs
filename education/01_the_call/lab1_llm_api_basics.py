"""Reference solution: wrap POST /api/generate and print latency. Chapter 01."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

payload = {
    "model": MODEL_NAME,
    "prompt": "In 2 sentences, explain what an HTTP POST request is.",
    "stream": False,
    "options": {
        "temperature": 0.0
    }
}

print(f"Connecting to Ollama at {OLLAMA_URL}...")
print(f"Model: {MODEL_NAME}")
print("Sending HTTP POST request...\n")

start_time = time.time()

json_data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    OLLAMA_URL,
    data=json_data,
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        response_bytes = response.read()
        end_time = time.time()

        result = json.loads(response_bytes.decode("utf-8"))

        response_text = result.get("response", "").strip()
        eval_count = result.get("eval_count", 0)
        eval_duration = result.get("eval_duration", 1)

        tps = (eval_count / (eval_duration / 1e9)) if eval_duration > 0 else 0
        total_latency = end_time - start_time

        print("=== RESPONSE FROM MODEL ===")
        print(response_text)
        print("\n=== PERFORMANCE METRICS ===")
        print(f"Total Wall-Clock Latency : {total_latency:.2f} seconds")
        print(f"Generated Tokens          : {eval_count} tokens")
        print(f"Generation Throughput (TPS): {tps:.2f} tokens/sec")

except Exception as e:
    print(f"Error connecting to Ollama: {e}")
