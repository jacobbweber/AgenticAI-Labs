"""Reference solution: Pure Python Plan-and-Solve task decomposition and dynamic replanning primitive."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

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


def llm_generate(prompt: str) -> Optional[str]:
    """Generates text from local LLM or returns None on connection/timeout error."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(
            OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw = data.get("response", "").strip()
            if raw.startswith("```json"):
                raw = raw.replace("```json", "").replace("```", "").strip()
            elif raw.startswith("```"):
                raw = raw.replace("```", "").strip()
            return raw
    except Exception:
        return None


def generate_initial_plan(goal: str, tool_schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Decomposes a user goal into an ExecutionPlan JSON structure."""
    tool_names = [t.get("name", t.get("function", {}).get("name", "unknown")) for t in tool_schemas]
    prompt = f"""You are a Plan-and-Solve decomposition planner.
Goal: {goal}
Available Tools: {json.dumps(tool_schemas)}

Output ONLY valid JSON adhering to this schema:
{{
  "plan_id": "plan-001",
  "goal": "{goal}",
  "steps": [
    {{
      "step_id": 1,
      "description": "step description",
      "tool_name": "tool_name",
      "tool_args": {{}}
    }}
  ]
}}
"""
    raw_response = llm_generate(prompt)
    if raw_response:
        try:
            parsed = json.loads(raw_response)
            if "steps" in parsed and isinstance(parsed["steps"], list):
                steps = []
                for i, s in enumerate(parsed["steps"], start=1):
                    steps.append({
                        "step_id": s.get("step_id", i),
                        "description": s.get("description", f"Step {i}"),
                        "tool_name": s.get("tool_name", tool_names[0] if tool_names else "default_tool"),
                        "tool_args": s.get("tool_args", {}),
                        "status": "pending",
                        "result": None,
                        "error": None
                    })
                return {
                    "plan_id": parsed.get("plan_id", f"plan-{int(time.time() * 1000)}"),
                    "goal": goal,
                    "steps": steps,
                    "status": "pending",
                    "replan_count": 0
                }
        except Exception:
            pass

    # Deterministic decomposition fallback when LLM is offline or non-JSON
    steps = [
        {
            "step_id": 1,
            "description": "Fetch user account record from primary database",
            "tool_name": "primary_db_query",
            "tool_args": {"user_id": 42},
            "status": "pending",
            "result": None,
            "error": None
        },
        {
            "step_id": 2,
            "description": "Format and summarize user account profile",
            "tool_name": "format_user_report",
            "tool_args": {"user_data": "$step_1_result"},
            "status": "pending",
            "result": None,
            "error": None
        }
    ]
    return {
        "plan_id": f"plan-{int(time.time() * 1000)}",
        "goal": goal,
        "steps": steps,
        "status": "pending",
        "replan_count": 0
    }


def replan_on_failure(
    plan: Dict[str, Any],
    failed_step_idx: int,
    error_msg: str,
    tool_schemas: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Dynamically adapts remaining plan steps upon execution failure."""
    plan["replan_count"] += 1
    failed_step = plan["steps"][failed_step_idx]
    print(f"\n[REPLANNER TRIGGERED] Step {failed_step['step_id']} failed with error: '{error_msg}'")
    print(f"[REPLANNER] Attempting dynamic recovery plan (Replan count: {plan['replan_count']})...")

    # Prompt LLM for alternate step if online
    prompt = f"""Plan step failed during execution:
Failed Step: {json.dumps(failed_step)}
Error: {error_msg}
Remaining Goal: {plan['goal']}
Tools: {json.dumps(tool_schemas or [])}

Provide a replacement step JSON:
{{"step_id": {failed_step['step_id']}, "description": "alternate step", "tool_name": "fallback_cache_query", "tool_args": {{"user_id": 42}}}}
"""
    raw_response = llm_generate(prompt)
    if raw_response:
        try:
            replacement = json.loads(raw_response)
            if "tool_name" in replacement:
                plan["steps"][failed_step_idx] = {
                    "step_id": failed_step["step_id"],
                    "description": replacement.get("description", "Fallback execution step"),
                    "tool_name": replacement["tool_name"],
                    "tool_args": replacement.get("tool_args", failed_step.get("tool_args", {})),
                    "status": "pending",
                    "result": None,
                    "error": None
                }
                plan["status"] = "replanned"
                return plan
        except Exception:
            pass

    # Deterministic recovery: pivot to fallback replica cache
    plan["steps"][failed_step_idx] = {
        "step_id": failed_step["step_id"],
        "description": "Fetch user account record from fallback replica cache",
        "tool_name": "fallback_cache_query",
        "tool_args": failed_step.get("tool_args", {"user_id": 42}),
        "status": "pending",
        "result": None,
        "error": None
    }
    plan["status"] = "replanned"
    return plan


def execute_plan(
    plan: Dict[str, Any],
    tool_registry: Dict[str, Any],
    tool_schemas: Optional[List[Dict[str, Any]]] = None,
    max_replans: int = 2
) -> Dict[str, Any]:
    """Executes plan steps sequentially, resolving dependencies and triggering replanning on failure."""
    plan["status"] = "executing"
    idx = 0

    while idx < len(plan["steps"]):
        step = plan["steps"][idx]
        step["status"] = "in_progress"
        tool_name = step.get("tool_name")
        tool_args = dict(step.get("tool_args", {}))

        # Resolve inter-step variable references (e.g. $step_1_result)
        for k, v in tool_args.items():
            if isinstance(v, str) and v.startswith("$step_") and "_result" in v:
                ref_step_id = int(v.split("$step_")[1].split("_result")[0])
                for prior_step in plan["steps"]:
                    if prior_step["step_id"] == ref_step_id and prior_step["result"] is not None:
                        tool_args[k] = prior_step["result"]

        print(f"\n[EXECUTOR] Running Step {step['step_id']}: '{step['description']}' -> {tool_name}({tool_args})")

        if tool_name not in tool_registry:
            step["status"] = "failed"
            step["error"] = f"Tool '{tool_name}' not found in tool registry."
            if plan["replan_count"] < max_replans:
                plan = replan_on_failure(plan, idx, step["error"], tool_schemas)
                continue
            else:
                plan["status"] = "failed"
                return plan

        try:
            tool_fn = tool_registry[tool_name]
            result = tool_fn(**tool_args)

            # Check for simulated or explicit error return
            if isinstance(result, str) and result.startswith("ERROR:"):
                step["status"] = "failed"
                step["error"] = result
                if plan["replan_count"] < max_replans:
                    plan = replan_on_failure(plan, idx, result, tool_schemas)
                    continue
                else:
                    plan["status"] = "failed"
                    return plan

            step["status"] = "completed"
            step["result"] = result
            step["error"] = None
            print(f"  [STEP {step['step_id']} COMPLETED] Output: {result}")
            idx += 1

        except Exception as exc:
            step["status"] = "failed"
            step["error"] = str(exc)
            if plan["replan_count"] < max_replans:
                plan = replan_on_failure(plan, idx, str(exc), tool_schemas)
                continue
            else:
                plan["status"] = "failed"
                return plan

    plan["status"] = "completed"
    return plan


# --- DEMO TOOL IMPLEMENTATIONS ---
def primary_db_query(user_id: int) -> str:
    """Primary database tool: fails intentionally on user_id=42 to exercise replanning."""
    if user_id == 42:
        return "ERROR: Connection timeout on primary_db_query (replica host unreachable)."
    return f"User #{user_id}: Name='Alice Smith', Role='Engineer', Status='Active'"


def fallback_cache_query(user_id: int) -> str:
    """Fallback cache tool: successfully resolves user data."""
    return f"User #{user_id}: Name='Alice Smith', Role='Engineer', Source='Replica Cache'"


def format_user_report(user_data: str) -> str:
    """Summarizes user profile information."""
    return f"AUDIT REPORT -> Profile: [{user_data}] | Verified: True | Timestamp: {int(time.time())}"


if __name__ == "__main__":
    print("=== STARTING PLAN-AND-SOLVE TASK DECOMPOSITION LAB ===")

    tools_schema = [
        {"name": "primary_db_query", "description": "Query user from primary relational database."},
        {"name": "fallback_cache_query", "description": "Query user from high-availability cache."},
        {"name": "format_user_report", "description": "Format user details into an audit report."}
    ]

    registry = {
        "primary_db_query": primary_db_query,
        "fallback_cache_query": fallback_cache_query,
        "format_user_report": format_user_report
    }

    user_goal = "Fetch account data for user 42 and generate an audit report."
    print(f"User Goal: '{user_goal}'\n")

    initial_plan = generate_initial_plan(user_goal, tools_schema)
    print("--- INITIAL GENERATED PLAN ---")
    print(json.dumps(initial_plan, indent=2))

    print("\n--- EXECUTING PLAN WITH DYNAMIC REPLANNING ---")
    final_plan = execute_plan(initial_plan, registry, tools_schema)

    print("\n=== FINAL EXECUTION PLAN RESULT ===")
    print(json.dumps(final_plan, indent=2))
