import json
import math
import random
import subprocess
import sys
import tempfile
from typing import Dict, Any, List, Tuple

# 1. Deterministic Program Verifier (RLVR Engine)
def verify_python_code(code: str, expected_output: str) -> float:
    """Executes code in a sandbox and returns 1.0 (Pass) or 0.0 (Fail)."""
    with tempfile.TemporaryDirectory(prefix="grpo_") as temp_dir:
        file_path = f"{temp_dir}/script.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        try:
            proc = subprocess.Popen(
                [sys.executable, file_path],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(timeout=3)
            if proc.returncode == 0 and expected_output in stdout.strip():
                return 1.0
            return 0.0
        except Exception:
            return 0.0

# 2. GRPO Group Advantage Normalizer
def calculate_grpo_group_advantages(rewards: List[float]) -> List[float]:
    """Calculates A_i = (R_i - mean(R)) / (std(R) + eps) across a candidate group."""
    n = len(rewards)
    mean_r = sum(rewards) / n
    variance = sum((r - mean_r) ** 2 for r in rewards) / n
    std_r = math.sqrt(variance)
    eps = 1e-8

    if std_r == 0:
        return [0.0 for _ in rewards]

    return [round((r - mean_r) / (std_r + eps), 4) for r in rewards]

# 3. GRPO Alignment Engine Simulation
class GRPOAlignmentEngine:
    """Orchestrates candidate group sampling, RLVR verification, and advantage computation."""
    def run_alignment_step(self, prompt: str, candidate_outputs: List[str], expected_output: str) -> Dict[str, Any]:
        print("=== STARTING GRPO PREFERENCE ALIGNMENT LAB ===")
        print(f"[PROMPT]: '{prompt}'")
        print(f"[GROUP SIZE]: G = {len(candidate_outputs)}")

        rewards = []
        print("\n--- STEP 1: VERIFIABLE REWARD EVALUATION (RLVR) ---")
        for idx, code in enumerate(candidate_outputs, start=1):
            r = verify_python_code(code, expected_output)
            rewards.append(r)
            status = "PASSED" if r == 1.0 else "FAILED"
            print(f"  Candidate {idx}: [{status}] -> Reward R_{idx} = {r}")

        print("\n--- STEP 2: GROUP RELATIVE ADVANTAGE NORMALIZATION ---")
        advantages = calculate_grpo_group_advantages(rewards)
        for idx, (r, a) in enumerate(zip(rewards, advantages), start=1):
            direction = "POLICY INCREASE (+)" if a > 0 else ("POLICY DECREASE (-)" if a < 0 else "NEUTRAL (0)")
            print(f"  Candidate {idx}: Reward = {r:.1f} | Advantage A_{idx} = {a:+.4f} | Action: {direction}")

        return {
            "status": "SUCCESS",
            "group_rewards": rewards,
            "group_advantages": advantages
        }

if __name__ == "__main__":
    candidates = [
        "def is_even(n):\n    return n % 2 == 0\nprint(is_even(4))",          # Pass -> True
        "def is_even(n):\n    return n % 2 != 0\nprint(is_even(4))",          # Fail -> False
        "def is_even(n):\n    return True if n == 4 else False\nprint(is_even(4))", # Pass -> True
        "syntax error line 1"                                                # Fail -> Crash
    ]
    prompt = "Write a python function is_even(n) returning True for even numbers."
    
    engine = GRPOAlignmentEngine()
    res = engine.run_alignment_step(prompt, candidates, expected_output="True")
    print(f"\nFinal GRPO Result Payload:\n{json.dumps(res, indent=2)}")
