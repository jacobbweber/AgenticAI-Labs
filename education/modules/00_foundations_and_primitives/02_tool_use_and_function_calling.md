# 02: Tool Use & Function Calling

## 1. Macro Concept & Industry Need

Large Language Models in isolation are static, closed-world reasoning engines limited by training cutoffs and unable to perform external side-effects. **Tool Use** (or **Function Calling**) is the architectural mechanism that connects an LLM to external software systems, allowing the model to request the execution of local functions, database queries, web searches, and API endpoints.

In enterprise software engineering, function calling transforms LLMs from passive conversational text predictors into active, goal-directed autonomous agents. Rather than executing code directly, the LLM emits a structured tool call request specifying a target function name and argument dictionary. The host application intercepts this request, validates and dispatches the execution, and returns the result back to the model context.

Key enterprise applications include natural-language enterprise database querying, automated ticket triage, multi-step cloud infrastructure provisioning, and transactional workflow automation.

---

## 2. Architectural Component Mapping

The following table translates tool use and function calling concepts to standard software engineering primitives:

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Tool / Function Spec** | JSON Schema Remote Method Signature (`name`, `description`, `parameters`) |
| **Tool Call Request** | Serialized Remote Procedure Call (RPC) Invocation Payload |
| **Tool Execution Dispatcher** | Polymorphic Method Router / Switch Handler mapping strings to callables |
| **Tool Result Feedback** | Context Frame appended to Message History (`role: "tool"`, `tool_call_id`) |
| **Dynamic Tool Discovery** | Vector Index Tool Schema Retriever (RAG for Function Signatures) |
| **MCP Tool Provider** | Standardized JSON-RPC 2.0 Microservice Transport (stdio / SSE) |

---

## 3. Key Technical Aspects & Dig-In Topics

### Model Context Protocol (MCP) Tool Standard
Anthropic's **Model Context Protocol (MCP)** standardizes how applications provide tools, resources, and prompts to LLM agents over JSON-RPC 2.0 transports (stdio or HTTP with SSE). MCP decouples tool implementation from model wrappers, enabling reusable tool microservices.

```
Client Agent                     MCP Host Daemon                   Local/Remote Tool
     |                                  |                                  |
     |--- tools/list (JSON-RPC) ------->|                                  |
     |<-- Return Tool Schemas ----------|                                  |
     |                                  |                                  |
     |--- tools/call ("query_db") ----->|--- Execute Local Handler ------->|
     |<-- Return JSON Result -----------|<-- Return Result Data -----------|
```

### Dynamic Tool Discovery (RAG for Tools)
When an enterprise environment defines 100+ potential tools, passing every tool schema in every API request causes severe context window saturation and inflates prompt costs. **Dynamic Tool Discovery** solves this by storing function signatures in a vector database. At each conversation turn, a semantic search retrieves only the top-$K$ relevant tool schemas based on the user's current goal, dynamically injecting them into the request payload.

### Parallel Execution & Fan-Out/Fan-In Concurrency
Modern LLMs can emit multiple tool call requests within a single generation step (e.g., fetching weather for three cities simultaneously). The client execution dispatcher must parse the tool call array, spawn asynchronous parallel tasks (fan-out), execute the local functions concurrently, and aggregate all result objects into corresponding `tool` role messages (fan-in) before re-invoking the model.

### Error Feedback Protocols & Self-Correction Loops
Tool execution can fail due to invalid parameters, database timeouts, or permission errors. Rather than crashing the agent loop, execution exceptions are formatted as structured error payloads (e.g., `{"status": "error", "error_type": "ValidationError", "details": "Field 'age' must be positive"}`) and returned to the LLM. The model interprets the error feedback frame and generates a corrected tool call on the subsequent turn.

### Security Sandboxing & Least-Privilege Scoping
Executing external code requested by a probabilistic model introduces significant security risks. Security primitives include:
- **Permission Scoping**: Restricting available tools per turn based on user RBAC roles.
- **Side-Effect Isolation**: Enforcing read-only execution modes by default.
- **Human-in-the-Loop (HITL) Triggers**: Requiring explicit user confirmation for destructive write operations (e.g., `delete_database`, `transfer_funds`).

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (Polymorphic Tool Execution Engine)
Build a local tool dispatching engine that registers function signatures, compiles them to JSON Schema definitions, intercepts model tool call requests, validates argument types, executes local functions, and appends formatted `tool` role result messages back into conversation state.

### Lab 2: Intermediate Capability Integration (Parallel Dispatch & Self-Correction)
Construct an asynchronous parallel tool dispatcher using `asyncio.gather` or Promise fan-out. Implement a self-correcting error handling protocol that catches runtime exceptions during tool execution, formats error stack traces into structured JSON feedback frames, and demonstrates model self-correction over subsequent turns.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Vector RAG Dynamic Tool Discovery)
Develop a dynamic tool discovery system that indexes 100+ tool schemas in a local vector store. Implement semantic retrieval that selects the top-3 relevant function signatures based on user intent and dynamically injects them into the API request context, preventing context window bloat.

### Stretch Goal: Production Hardening (MCP-Compliant Multi-Transport Gateway)
Implement a production-grade Model Context Protocol (MCP) server supporting stdio and SSE transports. Integrate fine-grained role-based permission scoping, execution sandboxing, interactive human-in-the-loop approval triggers for state-modifying tools, and comprehensive request auditing.
