"""Reference solution. Moved from the old education/labs tree."""
import json
from typing import Dict, Any, List

# 1. Role-Based Access Control (RBAC) Whitelist Matrix
ROLE_TOOL_PERMISSIONS: Dict[str, List[str]] = {
    "ARCHITECT": ["read_file", "list_dir"],
    "DEVELOPER": ["read_file", "write_file"],
    "AUDITOR":   ["read_file", "run_tests"]
}

# 2. Mock Capabilities
def mock_read_file(path: str) -> str:
    return f"Content of file '{path}'"

def mock_write_file(path: str, content: str) -> str:
    return f"Wrote content to '{path}'"

def mock_run_tests(test_suite: str) -> str:
    return f"Executed '{test_suite}' -> 100% Tests Passed"

def mock_run_command(cmd: str) -> str:
    return f"Executed bash command: '{cmd}'"

TOOL_EXECUTORS = {
    "read_file": mock_read_file,
    "write_file": mock_write_file,
    "run_tests": mock_run_tests,
    "run_command": mock_run_command
}

# 3. RBAC Guardrail Interceptor Middleware
def rbac_tool_interceptor(agent_role: str, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """Intercepts and validates tool calls against the agent role's RBAC whitelist."""
    print(f"\n[RBAC INTERCEPTOR] Role: '{agent_role}' -> Attempting Tool: '{tool_name}'")
    
    allowed_tools = ROLE_TOOL_PERMISSIONS.get(agent_role, [])
    
    # PERMISSION CHECK
    if tool_name not in allowed_tools:
        print(f"  [DENIED] PERMISSION DENIED (HTTP 403 Forbidden)")
        print(f"  Reason: Role '{agent_role}' is not granted access to tool '{tool_name}'. Allowed: {allowed_tools}")
        return {
            "status": 403,
            "error": f"Permission Denied: Role '{agent_role}' cannot execute tool '{tool_name}'."
        }
    
    print(f"  [GRANTED] PERMISSION GRANTED")

    executor = TOOL_EXECUTORS.get(tool_name)
    result = executor(**tool_args)
    return {
        "status": 200,
        "result": result
    }

if __name__ == "__main__":
    print("=== STARTING AGENT ROLE-BASED ACCESS CONTROL (RBAC) LAB ===")

    # Scenario 1: Architect Agent attempts authorized read_file call
    res1 = rbac_tool_interceptor("ARCHITECT", "read_file", {"path": "architecture.md"})
    print(f"Result: {res1}")

    # Scenario 2: Architect Agent attempts unauthorized run_command call (Privilege Violation)
    res2 = rbac_tool_interceptor("ARCHITECT", "run_command", {"cmd": "rm -rf /"})
    print(f"Result: {res2}")

    # Scenario 3: Developer Agent attempts authorized write_file call
    res3 = rbac_tool_interceptor("DEVELOPER", "write_file", {"path": "main.py", "content": "print('hello')"})
    print(f"Result: {res3}")

    # Scenario 4: Developer Agent attempts unauthorized run_tests call
    res4 = rbac_tool_interceptor("DEVELOPER", "run_tests", {"test_suite": "pytest"})
    print(f"Result: {res4}")
