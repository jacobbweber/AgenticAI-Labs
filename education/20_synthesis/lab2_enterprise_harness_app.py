"""Reference solution. Moved from the old education/labs tree."""
import json
import os
import sys
import time
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
DEEP_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
FAST_MODEL = os.environ.get("OLLAMA_FAST_MODEL", os.environ.get("OLLAMA_MODEL", "llama3.2:1b"))

# 1. Multi-Model Gateway Router (Module 07 Lab 2 Primitive)
class MultiModelGatewayRouter:
    """Routes prompts based on task complexity keyword heuristics."""
    def select_tier(self, prompt: str) -> Tuple[str, str]:
        complex_keywords = ["refactor", "analyze", "debug", "architect", "synthesis"]
        if any(k in prompt.lower() for k in complex_keywords):
            return "DEEP_TIER", DEEP_MODEL
        return "FAST_TIER", FAST_MODEL

# 2. SDUI HITL Approval Gate (Module 05 Lab 3 Primitive)
class SDUIHITLApprovalGate:
    """Evaluates proposed commands and emits HITL modal payloads for mutative actions."""
    def __init__(self):
        self.forbidden_keywords = ["rm -rf /", "drop database"]
        self.mutative_keywords = ["rollout restart", "delete", "drop", "update", "write"]

    def evaluate_action(self, action_cmd: str) -> Dict[str, Any]:
        cmd_lower = action_cmd.lower()
        if any(k in cmd_lower for k in self.forbidden_keywords):
            return {"status": "FORBIDDEN", "reason": "Destructive command blocked by policy."}
        if any(k in cmd_lower for k in self.mutative_keywords):
            return {
                "status": "PAUSED_FOR_HITL_APPROVAL",
                "approval_modal": {
                    "type": "HITLApprovalModal",
                    "proposed_command": action_cmd,
                    "risk_level": "HIGH",
                    "requires_token": True
                }
            }
        return {"status": "APPROVED", "reason": "Read-only command automatically approved."}

# 3. OpenTelemetry Eval Tracer (Module 04 Lab 2 Primitive)
class OTelEvalTracer:
    """Captures hierarchical OpenTelemetry trace spans for operational auditing."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.spans: List[Dict[str, Any]] = []

    def record_span(self, name: str, duration_ms: float, attributes: Dict[str, Any]):
        self.spans.append({
            "session_id": self.session_id,
            "span_name": name,
            "duration_ms": round(duration_ms, 2),
            "attributes": attributes
        })

# 4. Enterprise Agent Application Harness (Integrated Subsystem)
class EnterpriseAgentAppHarness:
    """Combines Multi-Model Gateway, SDUI HITL Gate, and OTel Telemetry into a production app."""
    def __init__(self):
        self.router = MultiModelGatewayRouter()
        self.hitl_gate = SDUIHITLApprovalGate()

    def process_request(self, session_id: str, prompt: str, proposed_action: str) -> Dict[str, Any]:
        print(f"\n=== STARTING ENTERPRISE AGENT APP HARNESS: '{session_id}' ===")
        tracer = OTelEvalTracer(session_id)
        start_time = time.time()

        # Step 1: Model Gateway Routing
        tier, model_name = self.router.select_tier(prompt)
        print(f"[ROUTER] Prompt Triage -> Selected Tier: {tier} ({model_name})")

        # Step 2: Local Model Inference Call
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        }
        json_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"})

        inf_start = time.time()
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            llm_text = data.get("response", "").strip()
        inf_duration = (time.time() - inf_start) * 1000

        tracer.record_span(
            name="llm.inference",
            duration_ms=inf_duration,
            attributes={
                "tier": tier,
                "model": model_name,
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0)
            }
        )

        # Step 3: SDUI HITL Safety Evaluation
        hitl_res = self.hitl_gate.evaluate_action(proposed_action)
        print(f"[SAFETY GATE] Proposed Action: '{proposed_action}' -> Status: {hitl_res['status']}")

        tracer.record_span(
            name="hitl.safety_gate",
            duration_ms=5.0,
            attributes={"action": proposed_action, "status": hitl_res["status"]}
        )

        total_duration = (time.time() - start_time) * 1000

        return {
            "status": hitl_res["status"],
            "session_id": session_id,
            "selected_tier": tier,
            "llm_response": llm_text[:120] + "...",
            "safety_eval": hitl_res,
            "total_duration_ms": round(total_duration, 2),
            "telemetry_spans": tracer.spans
        }

if __name__ == "__main__":
    app = EnterpriseAgentAppHarness()
    res = app.process_request(
        session_id="ent_session_701",
        prompt="Analyze system logs and refactor database connection pool.",
        proposed_action="kubectl rollout restart deployment/api-gateway"
    )
    print(f"\nFinal Enterprise App Harness Result:\n{json.dumps(res, indent=2)}")
