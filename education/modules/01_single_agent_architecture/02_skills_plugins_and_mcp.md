# 02: Skills, Plugins & Model Context Protocol (MCP)

## 1. Macro Concept & Industry Need

As AI agents scale from simple scripts into enterprise assistants, hardcoding every tool schema and system prompt directly into a monolithic codebase creates severe architectural bottlenecks. Loading hundreds of static tool definitions into an LLM context window pollutes attention, increases latency, inflates API token costs, and violates modular software design.

**Skills**, **Plugins**, and the **Model Context Protocol (MCP)** provide standard mechanisms for modular agent capability extension. 

MCP—an open standard initiated by Anthropic—establishes a universal JSON-RPC 2.0 protocol enabling agents to connect seamlessly to external tools, data resources, and workflow templates. Combined with dynamic instruction loading (**Skills**), agents can dynamically discover and consume specialized capabilities on demand without recompiling or redeploying host harnesses.

---

## 2. Architectural Component Mapping

To demystify agentic concepts into standard software engineering primitives, the table below maps skills and MCP terminology to established software components:

| AI Buzzword / Paradigm | Standard Software Engineering Primitive | System Description & Mechanics |
| :--- | :--- | :--- |
| **MCP Server** | Microservice RPC Endpoint Host | Background process exposing standardized JSON-RPC endpoints for tools and data. |
| **MCP Transport (Stdio)** | Subprocess Standard I/O IPC Pipe | Low-latency local IPC communicating via process standard input and output streams. |
| **MCP Transport (SSE)** | Server-Sent Events HTTP + POST Stream | Remote HTTP streaming transport for distributed multi-client service architectures. |
| **MCP Resource** | URI-Addressable Data Provider | Read-only state endpoint (e.g., `file:///logs/app.log`) providing context data. |
| **MCP Tool** | Executable RPC Function Signature | Executable function schema with JSON Schema argument validation. |
| **Skill (`SKILL.md`)** | Dynamic Policy Instruction Module | Modular Markdown document containing workflow playbooks and domain instructions. |
| **Progressive Disclosure** | Lazy-Loaded Module Import Pattern | Exposing lightweight frontmatter indices initially, loading full instructions on demand. |

---

## 3. Key Technical Aspects & Dig-In Topics

### 1. Model Context Protocol (MCP) Deep-Dive
MCP standardizes agent-to-environment integration using JSON-RPC 2.0 message framing over formal handshake lifecycles:
- **Capability Negotiation**: Handshake protocol (`initialize` request -> `initialized` notification) where client and server exchange supported features (logging, prompts, resources, tools).
- **Core Primitives**:
  - **Tools**: Executable functions invoked by the model via `tools/call`.
  - **Resources**: URI-addressable contextual data (e.g., database schemas, log files) fetched via `resources/read`.
  - **Prompts**: Parameterized workflow templates exposed to users or agents via `prompts/get`.
- **Subscriptions & Notifications**: Real-time notifications (e.g., `notifications/resources/updated`) allowing agents to react to external state changes.

### 2. Stdio vs SSE Transport Architecture
MCP decouples protocol logic from underlying network transport mechanisms:
- **Stdio Transport**: Launches local background subprocesses. Low-latency, highly secure (bound to local process boundary), ideal for desktop IDE agents (Claude Code, AGY, Cursor).
- **SSE (Server-Sent Events) Transport**: Operates over HTTP streaming. Uses SSE for server-to-client event channels and HTTP POST requests for client-to-server messages. Enables remote microservices, multi-tenant agent platforms, and cloud integrations with OAuth2 bearer token authentication.

### 3. Progressive Disclosure Pattern (`SKILL.md`)
To avoid context window overload, agents utilize progressive disclosure for domain playbooks:
- **Skill Manifests**: Skills are packaged as folders containing a `SKILL.md` file with structured YAML frontmatter (name, description, required tools).
- **Tier 1 (Discovery Index)**: The harness injects only high-level skill names and descriptions into the system prompt index (consuming minimal tokens).
- **Tier 2 (Full Loading)**: When user intent matches a skill's domain, the harness lazily loads the full `SKILL.md` instruction body, reference documentation, and auxiliary scripts into active context.

### 4. Multi-Server Routing & Security Boundaries
Production harnesses route tool requests across heterogeneous MCP environments:
- **Multi-Server Routers**: Aggregating multiple MCP clients into a unified namespace router.
- **Dynamic Tool Discovery (Vector RAG)**: When scaling to 100+ tools, embedding tool schemas into a vector index to dynamically fetch top-$K$ relevant schemas per turn.
- **URI Root Path Security**: Enforcing strict path validation on `file://` resources to restrict file access to designated workspace directories.

```json
// Example MCP JSON-RPC 2.0 Tool Call Request Payload
{
  "jsonrpc": "2.0",
  "id": "turn-42",
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT id, status FROM deployments WHERE env = 'prod';",
      "timeout_ms": 5000
    }
  }
}
```

---

## 4. Future Lab Blueprint

High-level directional prompts for subsequent hands-on lab creation:

- **Lab 1: Baseline Architecture** — Construct a local Stdio JSON-RPC MCP server exposing custom tools and resources, along with an MCP client integrated into an agent harness.
- **Lab 2: Intermediate Capability Integration** — Implement the Progressive Disclosure pattern using `SKILL.md` instruction manifests with lazy context loading, and deploy an SSE-based remote MCP transport.
- **Lab 3: Enterprise Resilience & Advanced Edge Cases** — Build a multi-server MCP router with dynamic vector tool schema discovery, automatic server reconnection, and URI root path authorization.
- **Stretch Goal: Production Hardening** — Develop an enterprise MCP gateway featuring OAuth2 authentication over SSE streams, request rate limiting, JSON schema validation middleware, and distributed trace propagation.
