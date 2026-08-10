# 02: Generative UI & Human-in-the-Loop (HITL) Interfaces

## 1. Macro Concept & Industry Need

Unstructured conversational text is an inadequate interface for complex agentic workflows. Presenting multi-file code modifications, complex database queries, or financial transactions as raw Markdown text creates cognitive overload and increases human operational error. **Generative UI** and **Human-in-the-Loop (HITL)** architectures break free from static text chat by dynamically rendering rich, interactive frontend components directly from structured tool execution streams and backend graph interrupts.

Key industry primitives for Generative UI & HITL interfaces include:
- **Server-Driven UI (SDUI) & Dynamic Registries**: Mapping backend tool outputs to registered React components (`WeatherCard`, `DataTable`, `DiffEditor`).
- **Streaming JSON Patch Schemas (RFC 6902)**: Incrementally rendering component props via RFC 6902 JSON patch updates while model generation is actively in progress.
- **Code Diff Inspection Cards**: Interactive cards visualizing proposed file changes side-by-side with inline approve/reject controls.
- **Human Approval Pause/Resume RPC Payloads**: Stateful interrupt handling that pauses backend state graph execution at sensitive nodes, surfaces interactive confirmation modals in the UI, and resumes execution upon human approval.

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Generative UI Engine** | Component lookup registry mapping tool names to interactive React components. |
| **Streaming JSON Patch Schema** | Incremental JSON Patch (RFC 6902) stream parser updating component props during generation. |
| **Server-Driven UI (SDUI)** | Typed component schema protocol (`{ component: "DiffCard", props: {...} }`) driving UI layout. |
| **Code Diff Inspection Card** | Specialized frontend component (Monaco Diff Editor) rendering side-by-side code diffs. |
| **HITL Approval RPC Payload** | Stateful interrupt event (`approval_id`, `tool_name`) paired with a resume RPC postback endpoint. |

## 3. Key Technical Aspects & Dig-In Topics

### 1. Next.js Streaming Generative UI & JSON Patch Schemas
- **RFC 6902 JSON Patch Protocol**: Emitting atomic JSON patch operations (`add`, `replace`, `remove`) over SSE to update React component props progressively during LLM output generation.
- **Lenient Partial JSON Parsing**: Utilizing incremental parsers (e.g. `best-effort-json-parser`) to safely extract and render partial object structures without triggering React runtime render exceptions.

### 2. Server-Driven UI (SDUI) Component Registry Architecture
- **Dynamic Component Lookup**: Maintaining a component registry `ComponentRegistry.get(tool_name)` mapping backend tool names to React components.
- **Fallback Boundaries**: Wrapping generative UI blocks in React Error Boundaries and rendering clean Markdown fallbacks if an unmapped tool name or malformed schema is received.

### 3. Human Approval Pause/Resume RPC Payload Lifecycle
1. **Interrupt Signal**: Agent graph reaches a sensitive node (`execute_deployment`) and pauses execution, persisting graph state to a durable checkpoint (`thread_id`).
2. **Event Emission**: Backend emits a `HITL_INTERRUPT_RAISED` event carrying the `approval_id`, tool name, and proposed parameters.
3. **UI Render**: Frontend renders an interactive `<ApprovalModal />` or Code Diff Inspection Card with "Approve", "Reject", and "Modify" actions.
4. **RPC Resume**: User action posts to `/api/agent/resume` with `{ approval_id, decision: "APPROVED", modified_params: null }`.
5. **Graph Continuation**: Backend reloads checkpoint and resumes graph execution.

```
+-----------------------------------------------------------------------------------+
|                     HUMAN-IN-THE-LOOP (HITL) RPC LIFECYCLE                        |
+-----------------------------------------------------------------------------------+
|  [Agent Execution Node] ---> Reaches Sensitive Tool (e.g., execute_payment)       |
|                                         |                                         |
|                                         v                                         |
|                         [Pause Graph & Save Checkpoint]                           |
|                                         |                                         |
|                                         v                                         |
|            [Stream HITL_INTERRUPT Event] (carrying approval_id & params)         |
|                                         |                                         |
|                                         v                                         |
|            [Frontend Renders <ApprovalModal /> or <DiffCard />]                   |
|                                         |                                         |
|            [User Clicks "Approve"] -----+                                         |
|                                         |                                         |
|                                         v                                         |
|            [POST /api/agent/resume] ---> [Reload Checkpoint & Resume Execution]  |
+-----------------------------------------------------------------------------------+
```

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
Build a React Generative UI renderer using a static component mapping table that converts backend agent tool execution events into rich visual cards (`WeatherCard`, `DataTableCard`) within the chat feed.

### Lab 2: Intermediate Capability Integration
Construct a Next.js streaming generative UI pipeline utilizing RFC 6902 JSON patch stream parsing to progressively render props into interactive React components as the model generates tool arguments.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
Architect an interactive Human-in-the-Loop governance interface featuring Code Diff Inspection Cards for file modifications and stateful Pause/Resume RPC payloads for human authorization gates.

### Stretch Goal: Production Hardening
Build an enterprise SDUI component system with schema validation gates, automatic UI fallback error boundaries for malformed model outputs, cryptographically signed human approval RPC payloads, and audit logs for compliance tracking.
