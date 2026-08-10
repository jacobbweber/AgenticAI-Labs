# 01: Agent Harness & Control Flow

## 1. Macro Concept & Industry Need

Large Language Models are stateless, non-deterministic text prediction engines. On their own, they possess no intrinsic ability to read files, execute code, access networks, or enforce safety boundaries. To function as enterprise agents (e.g., in modern IDE assistants like Claude Code, Cursor, or AGY), models must run inside an application runtime environment—the **Agent Harness**.

The Agent Harness provides the control flow architecture, surrounding context, security isolation, and operational middleware necessary to host an LLM execution loop safely. 

Without a robust harness, autonomous loops risk executing destructive shell commands, leaking workspace data, failing ungracefully on network exceptions, or running without audit trails. The harness acts as the application container that bridges stateless model reasoning with deterministic software systems.

---

## 2. Architectural Component Mapping

To demystify agentic concepts into standard software engineering primitives, the table below maps agent harness terminology to established software components:

| AI Buzzword / Paradigm | Standard Software Engineering Primitive | System Description & Mechanics |
| :--- | :--- | :--- |
| **Agent Harness** | Application Runtime Host Process | Encapsulating host process managing process lifecycle, state, and API routing. |
| **Scaffolding** | Framework Middleware Infrastructure | Config loaders, event interceptors, error handlers, and state management stack. |
| **Context Injection** | Dynamic Metadata Interpolator | Assembling OS details, git status, user session, and workspace paths into prompts. |
| **Lifecycle Hooks** | Interceptor Middleware Pipeline | Event hooks (`pre_turn`, `post_tool`, `on_thought`, `on_error`, `on_compact`) intercepting state. |
| **Tool Sandbox** | Containerized / Isolated Execution Boundary | Docker, gVisor, or WebAssembly (Wasm) runtime isolating system tool execution. |
| **Permission Policy** | Access Control List (ACL) Engine | Rule-based evaluator enforcing human-in-the-loop approvals for sensitive calls. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 1. Pluggable Middleware Pipeline Architecture
Production harnesses employ interceptor pipeline patterns to manage execution lifecycles cleanly:
- **`pre_turn` Hook**: Ingests fresh environment state, checks context token budgets, and formats dynamic system prompts prior to LLM inference.
- **`post_tool` Hook**: Validates tool return schemas, strips verbose logs, and inspects tool outputs for security anomalies.
- **`on_thought` Hook**: Logs internal reasoning tokens to telemetry collectors.
- **`on_error` Hook**: Intercepts tool execution exceptions, network timeouts, or schema errors, transforming raw stack traces into actionable context feedback for model self-correction.
- **`on_compact` Hook**: Triggers AST-aware context compaction when token limits approach configured watermarks.

### 2. Secure Execution Sandboxing
Executing LLM-generated shell commands or code scripts directly on host environments presents severe security risks:
- **Containerized Isolation**: Running tool executions inside ephemeral Docker containers, gVisor micro-kernels, or Firecracker microVMs.
- **WebAssembly Runtimes (Wasm)**: Executing lightweight code snippets inside isolated Wasm sandboxes with strict memory and CPU caps.
- **Network & File Controls**: Restricting outbound network interfaces and mounting workspace directories as read-only except for explicitly designated target paths.

### 3. Granular Policy Engines & Human-in-the-Loop (HITL) Approval
Enterprise harnesses enforce strict governance rules over agent tool execution:
- **Rule-Based ACLs**: Categorizing tools into permission tiers (e.g., Read-Only, Safe Modification, Destructive Execution).
- **Interactive Approval Gates**: Automatically granting approval for read operations (`list_dir`, `view_file`) while interrupting execution to prompt human operators for write operations (`write_to_file`, `run_command`).
- **Workspace Root Isolation**: Enforcing strict path canonicalization to prevent directory traversal attacks (`../`) outside designated project boundaries.

### 4. Workspace State Snapshotting & Rollback
To recover from faulty agent modifications, advanced harnesses track state changes across turns:
- **Git Tree Checkpointing**: Taking transient git commits or filesystem snapshots prior to executing file-modification tools.
- **Transactional Rollback**: Reverting workspace state to prior checkpoints if test suites fail or the agent enters an unrecoverable state trajectory.

```python
# Conceptual Agent Harness Middleware Pipeline
class AgentHarness:
    def __init__(self, sandbox: ContainerSandbox, policy: PolicyEngine):
        self.sandbox = sandbox
        self.policy = policy
        self.middlewares = []

    def register_middleware(self, mw: HarnessMiddleware):
        self.middlewares.append(mw)

    def dispatch_tool(self, tool_call: ToolCall) -> ToolResult:
        for mw in self.middlewares:
            mw.pre_tool(tool_call)
        
        if not self.policy.authorize(tool_call):
            return ToolResult(error="Execution rejected by policy engine")
            
        result = self.sandbox.execute(tool_call)
        
        for mw in reversed(self.middlewares):
            result = mw.post_tool(result)
        return result
```

---

## 4. Future Lab Blueprint

High-level directional prompts for subsequent hands-on lab creation:

- **Lab 1: Baseline Architecture** — Build a foundational agent harness runtime class in Python featuring workspace context assembly, tool invocation routing, and basic error recovery handlers.
- **Lab 2: Intermediate Capability Integration** — Implement a pluggable middleware interceptor pipeline (`pre_turn`, `post_tool`, `on_error`) and an interactive human permission policy engine for sensitive tools.
- **Lab 3: Enterprise Resilience & Advanced Edge Cases** — Integrate containerized execution sandboxing (Docker/gVisor) for shell commands with strict root path isolation and git state snapshotting/rollback.
- **Stretch Goal: Production Hardening** — Construct an enterprise multi-tenant agent harness featuring multi-tenant sandbox pooling, automated permission delegation rules, and full OpenTelemetry trace logging.
