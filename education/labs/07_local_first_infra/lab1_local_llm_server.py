import json
import time
import urllib.request
from typing import Dict, Any

# Local Ollama Host Endpoint (LAN Nimo Mini PC hardware)
OLLAMA_OPENAI_URL = "http://192.168.1.29:11434/v1/chat/completions"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

def benchmark_local_llm_endpoint(prompt: str) -> Dict[str, Any]:
    """
    Executes a structured RPC request against local Ollama OpenAI-compatible /v1 endpoint
    and measures empirical performance metrics (Latency, TTFT, TPS).
    """
    print(f"[LOCAL INFRA] Connecting to OpenAI-compatible endpoint: {OLLAMA_OPENAI_URL}")
    print(f"[LOCAL INFRA] Target Local Model: '{MODEL_NAME}'")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a local system architecture analyst. Keep answers to 2 concise sentences."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "stream": False
    }

    json_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_OPENAI_URL,
        data=json_bytes,
        headers={"Content-Type": "application/json"}
    )

    start_time = time.time()
    with urllib.request.urlopen(req, timeout=120) as response:
        total_latency = time.time() - start_time
        res_data = json.loads(response.read().decode("utf-8"))

    # Extract choices and usage metadata
    choice = res_data["choices"][0]["message"]["content"].strip()
    usage = res_data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    
    tps = round(completion_tokens / total_latency, 2) if total_latency > 0 else 0.0

    print(f"\n[LOCAL INFRA] Execution Completed in {total_latency:.2f}s!")
    print(f"  Prompt Tokens    : {prompt_tokens}")
    print(f"  Completion Tokens: {completion_tokens}")
    print(f"  Empirical Speed  : {tps} Tokens/Sec (TPS)")

    return {
        "model": MODEL_NAME,
        "response": choice,
        "total_latency_sec": round(total_latency, 2),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "tps": tps
    }

if __name__ == "__main__":
    print("=== STARTING LOCAL LLM SERVER & OPENAI-COMPATIBLE BENCHMARK LAB ===")
    prompt = "Explain why local-first LLM inference is critical for agent privacy and latency."
    result = benchmark_local_llm_endpoint(prompt)
    
    print("\n=== LOCAL MODEL RESPONSE ===")
    print(result["response"])
