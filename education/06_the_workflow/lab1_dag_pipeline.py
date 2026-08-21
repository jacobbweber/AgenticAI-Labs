"""Reference solution: dict-through-functions DAG with an LLM router. Chapter 06."""
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
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

def node_ingest_request(raw_user_input: str) -> Dict[str, Any]:
    print("[NODE 1: INGESTION] Normalizing input payload...")
    return {
        "raw_input": raw_user_input,
        "timestamp": time.time(),
        "status": "INGESTED"
    }

def node_route_intent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("[NODE 2: LLM ROUTER] Classifying user intent via Ollama...")
    prompt = f"""You are a strict JSON classifier.
Analyze the following user input and return ONLY a raw JSON object (no markdown formatting, no extra text):
{{"intent": "code_fix" OR "general_qa", "confidence": 0.0 to 1.0}}

User Input: "{state['raw_input']}"
"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = data.get("response", "").strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(raw_text)
            intent = parsed.get("intent", "general_qa")
            confidence = parsed.get("confidence", 0.5)
            print(f"[NODE 2: LLM ROUTER] Classified Intent: '{intent}' (Confidence: {confidence:.2f})")
            state["intent"] = intent
            state["confidence"] = confidence
            return state
    except Exception as err:
        print(f"[NODE 2: FALLBACK CASCADE] Routing failed ({err}). Falling back to 'general_qa'")
        state["intent"] = "general_qa"
        state["confidence"] = 0.0
        return state

def node_worker_code_fix(state: Dict[str, Any]) -> Dict[str, Any]:
    print("[NODE 3A: CODE WORKER] Executing specialized code-repair pipeline...")
    state["worker_output"] = f"Generated code patch stub for query: '{state['raw_input']}'"
    return state

def node_worker_general_qa(state: Dict[str, Any]) -> Dict[str, Any]:
    print("[NODE 3B: QA WORKER] Executing general Q&A pipeline...")
    state["worker_output"] = f"Retrieved answer response for query: '{state['raw_input']}'"
    return state

def node_format_output(state: Dict[str, Any]) -> Dict[str, Any]:
    print("[NODE 4: FORMATTER] Compiling final pipeline summary payload...")
    state["final_payload"] = {
        "status": "COMPLETED",
        "processed_intent": state["intent"],
        "result": state["worker_output"],
        "pipeline_duration_seconds": round(time.time() - state["timestamp"], 2)
    }
    return state

def run_dag_pipeline(user_prompt: str):
    print("=== STARTING DETERMINISTIC DAG PIPELINE ENGINE ===")
    print(f"User Request: '{user_prompt}'\n")
    state = node_ingest_request(user_prompt)
    state = node_route_intent(state)
    if state["intent"] == "code_fix":
        state = node_worker_code_fix(state)
    else:
        state = node_worker_general_qa(state)
    state = node_format_output(state)
    print("\n=== PIPELINE EXECUTION SUCCESSFUL ===")
    print(json.dumps(state["final_payload"], indent=2))
    return state

if __name__ == "__main__":
    test_prompt = "Fix the syntax error on line 42 in main.py where a closing parenthesis is missing."
    run_dag_pipeline(test_prompt)
