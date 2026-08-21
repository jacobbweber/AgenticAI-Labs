"""Reference solution: Pure Python Agent Capability Manifest validation, discovery, and intent resolution engine."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

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


def validate_agent_manifest(manifest: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates an agent manifest against the Agent Card Data Contract."""
    required_top_level = [
        "agent_id", "name", "version", "description",
        "capabilities", "skills", "transport", "runtime_policy"
    ]
    for key in required_top_level:
        if key not in manifest:
            return False, f"Missing required manifest field: '{key}'"

    if not isinstance(manifest["agent_id"], str) or not manifest["agent_id"].strip():
        return False, "Field 'agent_id' must be a non-empty string"
    if not isinstance(manifest["name"], str) or not manifest["name"].strip():
        return False, "Field 'name' must be a non-empty string"
    if not isinstance(manifest["version"], str) or not manifest["version"].strip():
        return False, "Field 'version' must be a non-empty string"
    if not isinstance(manifest["description"], str) or not manifest["description"].strip():
        return False, "Field 'description' must be a non-empty string"

    if not isinstance(manifest["capabilities"], list) or not manifest["capabilities"]:
        return False, "Field 'capabilities' must be a non-empty list of strings"
    for cap in manifest["capabilities"]:
        if not isinstance(cap, str) or not cap.strip():
            return False, "Each capability item must be a non-empty string"

    if not isinstance(manifest["skills"], list):
        return False, "Field 'skills' must be a list"
    for idx, skill in enumerate(manifest["skills"]):
        if not isinstance(skill, dict):
            return False, f"Skill at index {idx} must be an object"
        for s_key in ["name", "description", "input_schema", "output_schema"]:
            if s_key not in skill:
                return False, f"Skill at index {idx} missing required field '{s_key}'"

    transport = manifest["transport"]
    if not isinstance(transport, dict):
        return False, "Field 'transport' must be an object"
    valid_transports = {"local_process", "http_api", "stdio"}
    if transport.get("type") not in valid_transports:
        return False, f"Transport type '{transport.get('type')}' must be one of {valid_transports}"
    if not isinstance(transport.get("endpoint"), str) or not transport["endpoint"].strip():
        return False, "Transport endpoint must be a non-empty string"

    policy = manifest["runtime_policy"]
    if not isinstance(policy, dict):
        return False, "Field 'runtime_policy' must be an object"
    if not isinstance(policy.get("timeout_seconds"), (int, float)) or policy["timeout_seconds"] <= 0:
        return False, "Field 'timeout_seconds' must be a positive number"
    if not isinstance(policy.get("max_concurrency"), int) or policy["max_concurrency"] < 1:
        return False, "Field 'max_concurrency' must be an integer >= 1"
    if not isinstance(policy.get("requires_human_gate"), bool):
        return False, "Field 'requires_human_gate' must be a boolean"

    return True, "Manifest is valid"


def load_manifests_from_source(source: Union[str, Path, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Loads a list of agent manifests from a directory path, JSON file path, or memory list."""
    if isinstance(source, list):
        return source

    source_path = Path(source)
    manifests = []
    if source_path.is_file():
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    manifests.extend(data)
                elif isinstance(data, dict):
                    manifests.append(data)
        except Exception as e:
            print(f"[WARNING] Failed to load manifest file {source_path}: {e}")
    elif source_path.is_dir():
        for file_p in source_path.glob("*.json"):
            try:
                with open(file_p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        manifests.extend(data)
                    elif isinstance(data, dict) and "agent_id" in data:
                        manifests.append(data)
            except Exception as e:
                print(f"[WARNING] Failed to read {file_p}: {e}")
    return manifests


def discover_agents_by_capability(
    source: Union[str, Path, List[Dict[str, Any]]],
    capability: str
) -> List[Dict[str, Any]]:
    """Discovers all valid agent manifests offering a specific capability."""
    all_manifests = load_manifests_from_source(source)
    matching_agents = []
    target = capability.strip().lower()

    for manifest in all_manifests:
        valid, msg = validate_agent_manifest(manifest)
        if not valid:
            print(f"[DISCOVERY WARNING] Skipping invalid manifest ({msg}): {manifest.get('agent_id', 'unknown')}")
            continue

        caps = [c.strip().lower() for c in manifest.get("capabilities", [])]
        skill_names = [s.get("name", "").strip().lower() for s in manifest.get("skills", [])]

        if target in caps or target in skill_names or any(target in c for c in caps):
            matching_agents.append(manifest)

    return matching_agents


def resolve_agent_for_intent(
    source: Union[str, Path, List[Dict[str, Any]]],
    intent_description: str
) -> Optional[Dict[str, Any]]:
    """Resolves the best matching agent for a natural language intent description."""
    all_manifests = load_manifests_from_source(source)
    valid_agents = []
    for m in all_manifests:
        valid, _ = validate_agent_manifest(m)
        if valid:
            valid_agents.append(m)

    if not valid_agents:
        return None

    # 1. Attempt LLM router if local LLM is available
    agent_summaries = [
        {
            "agent_id": a["agent_id"],
            "name": a["name"],
            "description": a["description"],
            "capabilities": a["capabilities"]
        }
        for a in valid_agents
    ]
    prompt = f"""You are an Agent Dispatch Router.
Given the user intent and the available agent capability manifests, select the best agent_id.
Intent: "{intent_description}"
Available Agents: {json.dumps(agent_summaries)}

Return ONLY JSON:
{{"selected_agent_id": "agent-id-here", "confidence": 0.95}}
"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw = data.get("response", "").strip()
            if raw.startswith("```json"):
                raw = raw.replace("```json", "").replace("```", "").strip()
            elif raw.startswith("```"):
                raw = raw.replace("```", "").strip()
            parsed = json.loads(raw)
            selected_id = parsed.get("selected_agent_id")
            for a in valid_agents:
                if a["agent_id"] == selected_id:
                    return a
    except Exception:
        pass

    # 2. Deterministic keyword and capability matching fallback
    intent_words = set(intent_description.lower().replace(",", " ").replace(".", " ").split())
    scored_agents = []

    for a in valid_agents:
        score = 0
        # Check capability matches
        for cap in a.get("capabilities", []):
            cap_words = set(cap.lower().replace("_", " ").replace("-", " ").split())
            if cap_words.intersection(intent_words):
                score += 3

        # Check skill matches
        for skill in a.get("skills", []):
            skill_words = set(skill.get("name", "").lower().replace("_", " ").split())
            if skill_words.intersection(intent_words):
                score += 2
            desc_words = set(skill.get("description", "").lower().split())
            score += len(desc_words.intersection(intent_words))

        # Check description matches
        desc_words = set(a.get("description", "").lower().split())
        score += len(desc_words.intersection(intent_words))

        scored_agents.append((score, a))

    scored_agents.sort(key=lambda x: x[0], reverse=True)
    if scored_agents and scored_agents[0][0] > 0:
        return scored_agents[0][1]

    return valid_agents[0]


if __name__ == "__main__":
    print("=== STARTING AGENT CAPABILITY MANIFEST ENGINE ===")

    # Define catalog of specialist agent cards
    sample_catalog = [
        {
            "agent_id": "agent-sec-01",
            "name": "Security Auditor Agent",
            "version": "1.0.0",
            "description": "Specialized agent for detecting security vulnerabilities, SQL injection, and secrets.",
            "capabilities": ["security_audit", "vulnerability_scan", "code_review"],
            "skills": [
                {
                    "name": "audit_sql_injection",
                    "description": "Analyzes SQL query parameterization defects.",
                    "input_schema": {"type": "object", "properties": {"code_snippet": {"type": "string"}}},
                    "output_schema": {"type": "object", "properties": {"flaws": {"type": "array"}}}
                }
            ],
            "transport": {"type": "http_api", "endpoint": "http://127.0.0.1:8001/a2a/v1/invoke"},
            "runtime_policy": {"timeout_seconds": 60, "max_concurrency": 2, "requires_human_gate": False}
        },
        {
            "agent_id": "agent-doc-02",
            "name": "Tech Writer Agent",
            "version": "1.2.0",
            "description": "Generates API reference documentation, guides, and docstrings from source code.",
            "capabilities": ["documentation", "docstring_generation", "api_reference"],
            "skills": [
                {
                    "name": "generate_module_docs",
                    "description": "Generates markdown documentation for Python modules.",
                    "input_schema": {"type": "object", "properties": {"module_path": {"type": "string"}}},
                    "output_schema": {"type": "object", "properties": {"markdown": {"type": "string"}}}
                }
            ],
            "transport": {"type": "local_process", "endpoint": "python -m agents.writer"},
            "runtime_policy": {"timeout_seconds": 30, "max_concurrency": 4, "requires_human_gate": False}
        },
        {
            "agent_id": "agent-db-03",
            "name": "Database Optimizer Agent",
            "version": "0.9.1",
            "description": "Analyzes query execution plans, indexes, and database migration safety.",
            "capabilities": ["query_optimization", "sql_indexing", "migration_planning"],
            "skills": [
                {
                    "name": "analyze_explain_plan",
                    "description": "Identifies sequential table scans and missing indexes.",
                    "input_schema": {"type": "object", "properties": {"explain_json": {"type": "string"}}},
                    "output_schema": {"type": "object", "properties": {"recommendations": {"type": "array"}}}
                }
            ],
            "transport": {"type": "stdio", "endpoint": "bin/db_optimizer"},
            "runtime_policy": {"timeout_seconds": 45, "max_concurrency": 1, "requires_human_gate": True}
        }
    ]

    print("\n--- 1. SCHEMA VALIDATION ---")
    for agent in sample_catalog:
        valid, msg = validate_agent_manifest(agent)
        print(f"Agent [{agent['agent_id']}] '{agent['name']}': Valid={valid} ({msg})")

    # Test invalid schema handling
    invalid_agent = {"agent_id": "bad-01", "name": "Broken Agent"}
    valid, msg = validate_agent_manifest(invalid_agent)
    print(f"Invalid Agent Test: Valid={valid} (Caught: {msg})")

    print("\n--- 2. CAPABILITY DISCOVERY ---")
    target_cap = "security_audit"
    discovered = discover_agents_by_capability(sample_catalog, target_cap)
    print(f"Found {len(discovered)} agent(s) offering '{target_cap}':")
    for a in discovered:
        print(f"  -> {a['agent_id']}: {a['name']} (Transport: {a['transport']['type']} @ {a['transport']['endpoint']})")

    print("\n--- 3. INTENT-BASED AGENT RESOLUTION ---")
    queries = [
        "Scan SQL queries for injection vulnerabilities and security defects",
        "Generate developer API reference documentation for the auth module",
        "Analyze database execution plan for missing index recommendations"
    ]

    for q in queries:
        resolved = resolve_agent_for_intent(sample_catalog, q)
        if resolved:
            print(f"Query : '{q}'")
            print(f"Resolved Agent : [{resolved['agent_id']}] {resolved['name']}")
            print(f"Capabilities   : {resolved['capabilities']}")
            print(f"Endpoint       : {resolved['transport']['endpoint']}\n")

    print("--- 4. DISK MANIFEST FILE RESOLUTION ---")
    current_dir = Path(__file__).resolve().parent
    disk_discovered = discover_agents_by_capability(current_dir, "security_audit")
    print(f"Loaded from disk ({current_dir / 'agent_card.json'}): Found {len(disk_discovered)} agent(s):")
    for a in disk_discovered:
        print(f"  -> [{a['agent_id']}] {a['name']} v{a['version']} (Transport: {a['transport']['type']})")
