"""Reference solution: stream NDJSON tokens and print TTFT. Chapter 01."""
import json
import os
import sys
import time
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://192.168.1.29:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b-a3b-65k")

payload = {
    "model": MODEL_NAME,
    "prompt": "Write a 3-step technical summary of why streaming HTTP responses reduces perceived latency.",
    "stream": True,
    "options": {
        "temperature": 0.0
    }
}

print(f"Connecting to Ollama stream at {OLLAMA_URL}...")
print("Sending HTTP POST request (stream=True)...\n")

start_time = time.time()
ttft = None
token_count = 0
first_token_time = 0
eval_count = 0
eval_duration = 1

json_bytes = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    OLLAMA_URL,
    data=json_bytes,
    headers={"Content-Type": "application/json"}
)

print("=== REAL-TIME STREAMING OUTPUT ===")
try:
    with urllib.request.urlopen(req) as response:
        for line in response:
            if not line:
                continue

            if ttft is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time

            token_count += 1

            chunk = json.loads(line.decode("utf-8"))
            token_text = chunk.get("response", "")

            sys.stdout.write(token_text)
            sys.stdout.flush()

            if chunk.get("done", False):
                eval_count = chunk.get("eval_count", token_count)
                eval_duration = chunk.get("eval_duration", 1)

    total_duration = time.time() - start_time
    tps = eval_count / (eval_duration / 1e9) if eval_duration > 0 else 0

    print("\n\n=== STREAMING PERFORMANCE METRICS ===")
    print(f"Time to First Token (TTFT)   : {ttft:.2f} seconds")
    print(f"Total Response Duration     : {total_duration:.2f} seconds")
    print(f"Generated Tokens            : {eval_count} tokens")
    print(f"Generation Speed (TPS)      : {tps:.2f} tokens/sec")

except Exception as e:
    print(f"\nError reading stream: {e}")
