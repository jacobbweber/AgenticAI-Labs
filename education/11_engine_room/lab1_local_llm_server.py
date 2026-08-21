"""Reference solution. Moved from the old education/labs tree."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
# Local Ollama Host Endpoint (OpenAI-compatible /v1 route)
OLLAMA_OPENAI_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/v1/chat/completions"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

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
