"""Reference solution. Moved from the old education/labs tree."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from typing import Dict, Any, List, Tuple

OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

def llm_generate(prompt: str) -> str:
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
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        res = data.get("response", "").strip()
        if res.startswith("```python"):
            res = res.replace("```python", "").replace("```", "").strip()
        return res

# 1. Sandboxed Critic Node (Execution Verification)
def run_sandboxed_critic(temp_dir: str) -> Tuple[int, str]:
    script_path = os.path.join(temp_dir, "solution.py")
    proc = subprocess.Popen(
        [sys.executable, script_path],
        cwd=temp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(timeout=5)
    return proc.returncode, stderr.strip()

# 2. Reflexion & Self-Correction Engine
class ReflexionEngine:
    """Manages multi-turn reflection, traceback context feedback, and oscillation detection."""
    def __init__(self, max_turns: int = 3):
        self.max_turns = max_turns
        self.seen_signatures = set()

    def run_reflexion_loop(self, task_goal: str) -> Dict[str, Any]:
        print("=== STARTING REFLEXION & SELF-CORRECTION LOOP LAB ===")
        print(f"[TASK GOAL]: {task_goal}")

        with tempfile.TemporaryDirectory(prefix="reflexion_") as temp_dir:
            solution_path = os.path.join(temp_dir, "solution.py")
            current_prompt = f"Write a Python script for: {task_goal}. Provide ONLY runnable code."

            for turn in range(1, self.max_turns + 1):
                print(f"\n[TURN {turn}] Generator Node generating code...")
                code = llm_generate(current_prompt)
                
                # Write generated code to sandbox
                with open(solution_path, "w", encoding="utf-8") as f:
                    f.write(code)

                # Critic Node executes code
                exit_code, stderr = run_sandboxed_critic(temp_dir)

                if exit_code == 0:
                    print(f"  [PASSED] Execution Succeeded on Turn {turn}! (Exit Code: 0)")
                    return {"status": "SUCCESS", "turns": turn, "verified_code": code}

                print(f"  [FAILED] Execution Failed (Exit Code: {exit_code})")
                print(f"  [CRITIC TRACEBACK]:\n{stderr}")

                # Oscillation Detection via MD5 Hash
                sig_hash = hashlib.md5(stderr.encode("utf-8")).hexdigest()
                if sig_hash in self.seen_signatures:
                    print("  [CASCADE] [OSCILLATION ALERT] Repeated error signature detected!")
                    current_prompt = f"CRITICAL: Oscillation detected. Strategy Pivot Required!\nTask: {task_goal}\nPrior Error: {stderr}\nRewrite solution using a completely different strategy."
                else:
                    self.seen_signatures.add(sig_hash)
                    current_prompt = f"Fix defects in prior code.\nTask: {task_goal}\nTraceback Error:\n{stderr}\nCode:\n{code}"

            print("\n[REFLEXION ENGINE] Reached Max Turns without resolution.")
            return {"status": "FAILED_MAX_TURNS", "turns": self.max_turns}

if __name__ == "__main__":
    goal = "Create a function safe_divide(a, b) that divides a by b, handling ZeroDivisionError gracefully, and print safe_divide(10, 0)."
    engine = ReflexionEngine(max_turns=3)
    result = engine.run_reflexion_loop(goal)
    print(f"\nFinal Result: {result}")
