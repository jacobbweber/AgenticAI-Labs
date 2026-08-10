import json
import time
import urllib.request

# 1. Configuration (Local Ollama LAN Endpoint & Model)
OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 2. Data Contract: JSON Payload required by Ollama API
payload = {
    "model": MODEL_NAME,
    "prompt": "In 2 sentences, explain what an HTTP POST request is.",
    "stream": False,  # Non-streaming call for baseline lab
    "options": {
        "temperature": 0.0  # Deterministic decoding
    }
}

print(f"Connecting to Ollama at {OLLAMA_URL}...")
print(f"Model: {MODEL_NAME}")
print("Sending HTTP POST request...\n")

# 3. Record start time for latency measurement
start_time = time.time()

# 4. Prepare and execute the raw HTTP POST request
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
        
        # 5. Parse the JSON response
        result = json.loads(response_bytes.decode("utf-8"))
        
        # 6. Extract response text and metrics from Ollama response schema
        response_text = result.get("response", "").strip()
        eval_count = result.get("eval_count", 0)         # Total generated tokens
        eval_duration = result.get("eval_duration", 1)  # Duration in nanoseconds
        
        # Calculate Tokens Per Second (TPS)
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
