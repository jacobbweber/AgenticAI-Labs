"""Reference solution: wrap POST /api/generate and print latency. Chapter 01."""
import json
import os
import time
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://192.168.1.29:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b-a3b-65k")

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
