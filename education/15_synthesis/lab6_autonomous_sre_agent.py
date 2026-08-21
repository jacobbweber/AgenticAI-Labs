"""Reference solution. Moved from the old education/labs tree."""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Tuple

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/generate"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

def llm_call(prompt: str) -> str:
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
        return data.get("response", "").strip()

# 1. Log Triage Engine (Filter & Compression)
class LogTriageEngine:
    """Filters log streams for ERROR/CRITICAL signatures to reduce context bloat."""
    def extract_error_signatures(self, log_stream: List[str]) -> List[str]:
        error_logs = []
        for line in log_stream:
            if any(level in line for level in ["ERROR", "CRITICAL", "FATAL"]):
                error_logs.append(line)
        return error_logs

# 2. SRE Command Safety Guard & HITL Gate
class SRECommandSafetyGuard:
    """Evaluates proposed commands against safety policies."""
    MUTATIVE_WHITELIST = [
        r"^kubectl rollout restart deployment/[a-z0-9-]+ -n [a-z0-9-]+$",
        r"^kubectl scale deployment/[a-z0-9-]+ --replicas=\d+ -n [a-z0-9-]+$"
    ]
    FORBIDDEN_PATTERNS = [r"delete namespace", r"rm -rf", r"drop database"]

    def evaluate_command(self, command: str) -> Tuple[str, str]:
        cmd_clean = command.strip().lower()
        if any(re.search(pat, cmd_clean) for pat in self.FORBIDDEN_PATTERNS):
            return "FORBIDDEN", "Destructive command strictly prohibited by security policy."

        if any(re.match(pat, cmd_clean) for pat in self.MUTATIVE_WHITELIST):
            return "REQUIRES_HITL_APPROVAL", "Mutative infrastructure command requires human SRE token clearance."

        return "READ_ONLY", "Diagnostic command approved for automatic execution."

# 3. Autonomous SRE Remediation Agent
class AutonomousSREAgent:
    """Manages incident triage, root cause analysis, and HITL remediation gates."""
    def __init__(self):
        self.triage = LogTriageEngine()
        self.guard = SRECommandSafetyGuard()

    def investigate_and_remediate(self, raw_logs: List[str]) -> Dict[str, Any]:
        print("=== STARTING AUTONOMOUS DEVOPS & SRE AGENT LAB ===")
        print(f"[SRE AGENT] Ingesting {len(raw_logs)} raw log lines...")

        # Step 1: Log Triage & Filtering
        filtered_logs = self.triage.extract_error_signatures(raw_logs)
        print(f"  Extracted {len(filtered_logs)} ERROR log signatures.")

        # Step 2: Root Cause Analysis (RCA) via Ollama
        prompt = f"System Log Errors:\n" + "\n".join(filtered_logs) + "\n\nProvide 1-sentence Root Cause Analysis:"
        rca = llm_call(prompt)
        print(f"\n[ROOT CAUSE ANALYSIS]: {rca}")

        # Step 3: Propose Remediation Commands
        proposed_cmd1 = "kubectl get pods -n production"
        proposed_cmd2 = "kubectl rollout restart deployment/api-gateway -n production"
        proposed_cmd3 = "kubectl delete namespace production"

        print("\n[SAFETY GUARD EVALUATION]:")
        for cmd in [proposed_cmd1, proposed_cmd2, proposed_cmd3]:
            status, reason = self.guard.evaluate_command(cmd)
            print(f"  Command: '{cmd}'")
            print(f"  Status : [{status}] -> {reason}\n")

        return {
            "status": "SUCCESS",
            "rca": rca,
            "remediation_status": "PAUSED_FOR_HITL_APPROVAL",
            "approval_modal": {
                "type": "HITLApprovalModal",
                "proposed_command": proposed_cmd2,
                "risk_level": "MEDIUM"
            }
        }

if __name__ == "__main__":
    sample_logs = [
        "2026-08-09T00:43:00Z INFO [api-gateway] Processing GET /api/v1/checkout",
        "2026-08-09T00:43:01Z ERROR [api-gateway] ConnectionPoolExhausted: DB pool maxed at 100/100",
        "2026-08-09T00:43:02Z CRITICAL [api-gateway] HTTP 502 Bad Gateway emitted to client",
        "2026-08-09T00:43:03Z INFO [frontend] Retrying connection to api-gateway"
    ]
    agent = AutonomousSREAgent()
    res = agent.investigate_and_remediate(sample_logs)
    print(f"Result Payload: {json.dumps(res, indent=2)}")
