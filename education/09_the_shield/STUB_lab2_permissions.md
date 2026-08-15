# Stub: permissions / allowlist before HITL

This folder has lab1 (sandbox) then two files both named lab3 (`lab3_agent_rbac` and `lab3_hitl_generative_ui`) and no lab2. RBAC and HITL are two different ideas. The missing middle step is a permissions allowlist: which tool names are high-risk and must pause, before a human gate runs. This page is not a lab. There is no script to run.

A real lab2 would cover:

- A dict from tool name to a flag, for example `{"read_file": false, "write_file": true, "run_command": true, "apply_db_migration": true}`.
- One function that looks up the name and returns `{ "allowed": true }` or `{ "needs_hitl": true, "tool": "string" }` without calling the tool and without opening a UI.
- How this list sits after the sandbox (lab1) and before `rbac_tool_interceptor` (lab3 RBAC) and `execute_action_with_hitl_gate` (lab3 HITL).

What not to add:

- Runnable steps, a `.py` file, Docker, a React modal, or a WebSocket.
- A second copy of `ROLE_TOOL_PERMISSIONS` or of `AgentHITLEngine`.
- A PATH.md edit. That list is a later pass.
- A rename of the two lab3 files in this pass. The duplicate numbering stays until a later cleanup.
