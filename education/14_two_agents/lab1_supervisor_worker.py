"""Reference solution. Moved from the old education/labs tree."""
import asyncio
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

raw_host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").strip()
if not raw_host.startswith("http://") and not raw_host.startswith("https://"):
    raw_host = f"http://{raw_host}"
if ":" not in raw_host.split("://", 1)[1]:
    raw_host = f"{raw_host}:11434"

OLLAMA_URL = f"{raw_host.rstrip('/')}/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

# Helper for async LLM calls
async def async_llm_call(system_prompt: str, user_prompt: str) -> str:
    loop = asyncio.get_running_loop()
    full_prompt = f"{system_prompt}\n\nUser Task: {user_prompt}"
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(
            OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
        )
        response_bytes = await loop.run_in_executor(
            None, lambda: urllib.request.urlopen(req, timeout=3).read()
        )
        result = json.loads(response_bytes.decode("utf-8"))
        return result.get("response", "").strip()
    except Exception:
        # Fallback specialist responses when offline
        if "Security Auditor" in system_prompt:
            return "- Critical vulnerability: SQL query uses direct string interpolation allowing SQL injection.\n- Remediation: Refactor to parameterized queries using placeholder parameters."
        else:
            return "- The login function executes an authentication query against a SQL database using user credentials.\n- It accepts user and password strings and queries the 'users' table."

# --- SPECIALIST WORKERS (Isolated Scoped Context) ---
async def worker_security_auditor(code_snippet: str) -> Dict[str, str]:
    print("[WORKER: SECURITY AUDITOR] Analyzing code for vulnerabilities...")
    sys_prompt = "You are a Security Auditor. Analyze code and list security flaws in 2 bullet points."
    result = await async_llm_call(sys_prompt, code_snippet)
    print("  [WORKER: SECURITY AUDITOR] Finished audit.")
    return {"role": "Security Auditor", "output": result}

async def worker_doc_generator(code_snippet: str) -> Dict[str, str]:
    print("[WORKER: DOC GENERATOR] Drafting technical documentation...")
    sys_prompt = "You are a Tech Writer. Write 2 bullet points explaining what this code does."
    result = await async_llm_call(sys_prompt, code_snippet)
    print("  [WORKER: DOC GENERATOR] Finished documentation.")
    return {"role": "Doc Generator", "output": result}

# --- SUPERVISOR ORCHESTRATOR (Hub-and-Spoke Dispatcher) ---
async def supervisor_orchestrator(code_snippet: str):
    print("=== STARTING SUPERVISOR-WORKER MULTI-AGENT SWARM ===")
    print(f"Target Code:\n{code_snippet}\n")
    
    start_time = time.time()
    print("[SUPERVISOR] Dispatching sub-tasks to Specialist Workers in parallel (Fan-Out)...")

    # Parallel Execution (Fan-Out) via asyncio.gather
    results = await asyncio.gather(
        worker_security_auditor(code_snippet),
        worker_doc_generator(code_snippet)
    )

    print("\n[SUPERVISOR] All worker responses received. Synthesizing final report (Fan-In)...")
    
    # Synthesis Phase
    print("\n==============================================")
    print("           CONSOLIDATED AGENT REPORT          ")
    print("==============================================")
    for res in results:
        print(f"\n--- {res['role']} Report ---")
        print(res['output'])

    print(f"\nTotal Multi-Agent Execution Duration: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    sample_code = "def login(user, password):\n    query = f'SELECT * FROM users WHERE user={user} AND pass={password}'\n    db.execute(query)"
    asyncio.run(supervisor_orchestrator(sample_code))
