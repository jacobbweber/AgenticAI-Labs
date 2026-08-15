"""Reference solution. Moved from the old education/labs tree."""
import json
import time
import urllib.request
from typing import Dict, Any, List

OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 1. OpenTelemetry (OTel) Trace Collector
class OTelSpanCollector:
    """Simulates OpenTelemetry span collection for multi-step agent serving pipelines."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.spans: List[Dict[str, Any]] = []

    def record_span(self, name: str, duration_ms: float, attributes: Dict[str, Any]):
        span_data = {
            "session_id": self.session_id,
            "span_name": name,
            "duration_ms": duration_ms,
            "attributes": attributes
        }
        self.spans.append(span_data)
        print(f"  [OTel SPAN] '{name}' completed in {duration_ms:.2f}ms | Attrs: {attributes}")

# 2. Load-Balanced Inference Gateway
class InferenceGatewayRouter:
    """Routes LLM requests based on endpoint health and model availability."""
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints

    def dispatch(self, prompt: str) -> Dict[str, Any]:
        target_endpoint = self.endpoints[0]  # In production, uses round-robin / queue depth
        start_time = time.time()

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0}
        }
        json_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            target_endpoint, data=json_bytes, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        duration_ms = (time.time() - start_time) * 1000
        return {
            "response": data.get("response", "").strip(),
            "endpoint_used": target_endpoint,
            "duration_ms": duration_ms,
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0)
        }

# 3. Production Agent Serving Runtime
class ProductionAgentServingRuntime:
    """Manages multi-tenant requests, load-balanced inference, and OTel telemetry."""
    def __init__(self):
        self.gateway = InferenceGatewayRouter([OLLAMA_URL])

    def handle_request(self, session_id: str, prompt: str) -> Dict[str, Any]:
        print(f"\n[SERVING RUNTIME] Handling Session: '{session_id}'")
        tracer = OTelSpanCollector(session_id)

        # Step 1: LLM Inference via Gateway Router
        inf_res = self.gateway.dispatch(prompt)
        tracer.record_span(
            name="llm.inference",
            duration_ms=inf_res["duration_ms"],
            attributes={
                "model": MODEL_NAME,
                "endpoint": inf_res["endpoint_used"],
                "prompt_tokens": inf_res["prompt_tokens"],
                "completion_tokens": inf_res["completion_tokens"]
            }
        )

        # Step 2: Sandboxed Worker Execution Span
        exec_start = time.time()
        time.sleep(0.05)  # Simulate sandboxed execution delay
        exec_duration_ms = (time.time() - exec_start) * 1000

        tracer.record_span(
            name="sandbox.execution",
            duration_ms=exec_duration_ms,
            attributes={
                "isolation_type": "SubprocessSandbox",
                "exit_code": 0,
                "memory_limit_mb": 512
            }
        )

        return {
            "status": "SUCCESS",
            "session_id": session_id,
            "output": inf_res["response"],
            "telemetry_spans": tracer.spans
        }

if __name__ == "__main__":
    print("=== STARTING PRODUCTION AGENT SERVING INFRASTRUCTURE LAB ===")
    runtime = ProductionAgentServingRuntime()
    res = runtime.handle_request("tenant_session_9921", "Summarize 3 production serving best practices.")
    print(f"\nResult Payload: {json.dumps(res, indent=2)}")
