# 02: Specialized Roles, Persona Design & Agent RBAC

## 1. Macro Concept & Industry Need

Assigning broad, unconstrained system prompts and unrestricted tool grants to autonomous agents creates severe operational and security risks in enterprise environments. When an agent is granted access to all available functions simultaneously, issues such as role bleeding, prompt leakage, tool confusion, and over-permissioned execution (e.g., a documentation agent executing shell commands) become common failure modes.

To build secure multi-agent systems, organizations must adopt standard software engineering principles: **Role-Based Access Control (RBAC)**, **Least-Privilege Tool Allocation**, **Strict Output Contracts**, and **Formal Escalation Gates**. By decoupling systemic responsibilities into specialized agent personas with scoped tool access and schema-enforced output boundaries, autonomous workflows achieve operational predictability, auditability, and privilege isolation.

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Persona / Role Design** | System Prompt Configuration specifying domain boundaries and negative behavioral constraints. |
| **Tool Grant / Whitelist** | Role-Based Access Control (RBAC) Array / Function Pointer Whitelist. |
| **Guardrail Interceptor** | Middleware Request Filter validating input/output schemas and regex pattern rules. |
| **Output Contract** | JSON Schema Validation Gate or Markdown Template Specification enforcing output structures. |
| **Privilege Escalation** | Stateful Approval Handler requesting temporary tool elevation or Human-in-the-Loop (HITL) clearance. |

## 3. Key Technical Aspects & Dig-In Topics

### 1. Agent Role Taxonomy & RBAC Matrix
Production multi-agent platforms classify agents into four standardized operational tiers, each bound to a explicit tool grant matrix:

| Specialized Agent Role | Primary Function | Granted Tool Set | Prohibited Actions / Tools |
| :--- | :--- | :--- | :--- |
| **System Architect** | Requirements breakdown, spec drafting, task planning. | `view_file`, `list_dir`, `write_spec` | Code execution, database writes, git commit. |
| **Software Engineer** | Implementation of code components based on specs. | `view_file`, `replace_file_content`, `write_to_file` | Terminal execution, package deployment, root DB access. |
| **QA / Security Auditor** | Static analysis, vulnerability scanning, test verification. | `run_command` (scoped to `pytest`/`eslint`), `view_file` | File creation/modification, exfiltration, network calls. |
| **Sub-Orchestrator** | Delegating tasks to sub-agents, aggregate results. | `invoke_subagent`, `send_message`, `manage_task` | Direct file edits, raw shell command execution. |

### 2. Output Contract Enforcement
- **JSON Schema Validation Gates**: Every specialized agent role returns data matching a pre-defined JSON schema. If an agent output fails validation, the harness intercepts the response and re-prompts the model with explicit schema error feedback.
- **Structured Markdown Templates**: Enforcing standardized section headers and bullet structures for human-facing reports (e.g., mandatory `# Observation`, `# Logic Chain`, `# Conclusion` sections).

### 3. Hard Guardrail Interceptors & System Prompt Isolation
- **System Prompt Isolation**: System prompts must explicitly state negative constraints (*"You must NEVER run terminal commands or modify source files directly"*).
- **Runtime Middleware Interceptors**: Independent wrapper functions intercepting LLM tool invocation calls before execution. Even if an agent hallucinates a tool call outside its whitelist, the middleware rejects the invocation at the RPC boundary.

### 4. Dynamic Role Escalation & Human-in-the-Loop (HITL) Gates
- **Privilege Elevation Requests**: When a specialized agent encounters a task requiring elevated permissions (e.g., a Developer agent needing to install a new npm dependency), it emits a `REQUEST_PRIVILEGE_ELEVATION` event.
- **HITL Verification Approval**: The request pauses the agent execution thread, persisting graph state, and notifies a human operator or security auditor agent for authorization.

```
+-----------------------------------------------------------------------------------+
|                        AGENT ROLE-BASED ACCESS CONTROL (RBAC)                     |
+-----------------------------------------------------------------------------------+
| [Incoming Task] ---> [RBAC Gateway Middleware]                                   |
|                             |                                                     |
|      +----------------------+----------------------+                              |
|      | (Architect Scope)    | (Developer Scope)    | (Auditor Scope)              |
|      v                      v                      v                              |
| [Architect Agent]    [Developer Agent]      [Auditor Agent]                       |
| Tools: view, plan    Tools: view, edit      Tools: test runner                    |
| Deny: edit, exec     Deny: shell exec       Deny: write files                     |
+-----------------------------------------------------------------------------------+
```

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
Define system prompts and restricted tool grants for three distinct agent roles (Architect, Coder, Auditor). Implement an RBAC wrapper in Python that inspects attempted tool calls against static role whitelist arrays, blocking unauthorized actions.

### Lab 2: Intermediate Capability Integration
Implement Output Contract Enforcement using Pydantic schemas and JSON Schema validators for each agent role. Build an automated re-prompting handler that catches malformed model outputs and feeds schema validation errors back to the model for self-correction.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
Construct a multi-role SDLC pipeline (Architect -> Coder -> QA Auditor) with automated role-boundary middleware enforcement. Prevent role leakage and enforce explicit sub-agent context isolation during inter-role handoffs.

### Stretch Goal: Production Hardening
Architect a dynamic RBAC Agent Gateway featuring cryptographically tokenized tool grants, real-time command sanitization, automated security auditing of executed tools, and a Human-in-the-Loop (HITL) privilege escalation workflow with state persistence and audit logging.
