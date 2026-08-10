import json
import sys
import time
import urllib.request

# 1. Configuration (Local Ollama LAN Endpoint & Model)
OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 2. Data Contract with `"stream": True` enabled
payload = {
    "model": MODEL_NAME,
    "prompt": "Write a 3-step technical summary of why streaming HTTP responses reduces perceived latency.",
    "stream": True,  # Enable real-time streaming chunks
    "options": {
        "temperature": 0.0
    }
}

print(f"Connecting to Ollama stream at {OLLAMA_URL}...")
print("Sending HTTP POST request (stream=True)...\n")

start_time = time.time()
ttft = None          # Time To First Token (seconds)
token_count = 0      # Generated chunk counter
first_token_time = 0

json_bytes = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    OLLAMA_URL, 
    data=json_bytes, 
    headers={"Content-Type": "application/json"}
)

print("=== REAL-TIME STREAMING OUTPUT ===")
try:
    with urllib.request.urlopen(req) as response:
        # Read the HTTP stream line by line as Ollama emits JSON chunks
        for line in response:
            if not line:
                continue
            
            # Record Time to First Token (TTFT) on the very first received line
            if ttft is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time
            
            token_count += 1
            
            # Parse the JSON chunk
            chunk = json.loads(line.decode("utf-8"))
            token_text = chunk.get("response", "")
            
            # Print token to console immediately without newline buffering
            sys.stdout.write(token_text)
            sys.stdout.flush()

            # If chunk flags done=True, grab final execution metrics if present
            if chunk.get("done", False):
                eval_count = chunk.get("eval_count", token_count)
                eval_duration = chunk.get("eval_duration", 1)

    total_duration = time.time() - start_time
    decode_duration = total_duration - ttft
    tps = eval_count / (eval_duration / 1e9) if eval_duration > 0 else 0

    print("\n\n=== STREAMING PERFORMANCE METRICS ===")
    print(f"Time to First Token (TTFT)   : {ttft:.2f} seconds")
    print(f"Total Response Duration     : {total_duration:.2f} seconds")
    print(f"Generated Tokens            : {eval_count} tokens")
    print(f"Generation Speed (TPS)      : {tps:.2f} tokens/sec")

except Exception as e:
    print(f"\nError reading stream: {e}")
