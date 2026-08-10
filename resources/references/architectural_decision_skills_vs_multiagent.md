# Architectural Reference: Skill / Tool Wrapper vs. Multi-Agent (A2A) System Boundaries

## 1. Executive Summary & Core Question

When constructing complex agentic software platforms (e.g., an orchestrator agent `Lucy` managing a specialized `Blogger Agent`), software architects must decide how to structure the communication boundary between agents:

1. **Option A (Tool / Skill Wrapper)**: Wrap the specialized agent (`Blogger Agent`) into a single executable tool script (`python main.py` or `BloggerOrchestrator.run()`) surfaced to the orchestrator (`Lucy`) as a discrete function call.
2. **Option B (Multi-Agent A2A System)**: Deploy both `Lucy` and the `Blogger Agent` as independent concurrent actor kernels communicating across an asynchronous RPC or WebSocket message transport bus.

---

## 2. Technical Comparison Matrix

```mermaid
flowchart TD
    subgraph Pattern A: Skill / Tool Wrapper (Blocking Call / Facade)
        L1["Lucy Orchestrator Agent"] --> |"Tool Call: run_blogger_skill(topic)"| S1["Blogger Script (Subprocess Execution)"]
        S1 --> |"Returns Final JSON Output Payload"| L1
    end

    subgraph Pattern B: Multi-Agent System (A2A Asynchronous Message Transport)
        L2["Lucy Orchestrator Agent"] <--> |"Async JSON-RPC / WebSocket Bus"| B2["Blogger Agent Kernel"]
        B2 <--> |"Streams Intermediate Status & Real-time Progress"| L2
    end
```

| Architectural Dimension | Pattern A: Skill / Tool Wrapper | Pattern B: Multi-Agent (A2A Transport) |
| :--- | :--- | :--- |
| **Software Primitive** | Subprocess Execution (`subprocess.run`) or In-Process Function Facade (`BloggerOrchestrator.run()`) | Asynchronous Event Bus / Actor Transport (JSON-RPC, WebSockets, MCP stdio/SSE) |
| **Context Window Isolation** | **Complete**: Lucy's context window only stores the single-line tool call and final JSON result. | **Complete**: Both agents run separate event loops with isolated state stores (`lucy_session.json` vs `blogger_session.json`). |
| **Control Flow** | **Synchronous / Blocking**: Lucy pauses while the blogger script runs its internal execution turns. | **Asynchronous / Concurrent**: Both agents run concurrent event loops and can message each other mid-run. |
| **Intermediate Inspection** | Low: Lucy does not inspect or edit intermediate draft text during execution. | High: Lucy receives real-time progress events (*"Skeptic score 4/10"*) and can send mid-run corrections. |
| **System Overhead & Latency** | **Minimal**: In-process function execution, zero transport serialization, simple debugging. | **Moderate**: Requires message routing, event handlers, and protocol serialization logic. |

---

## 3. Pattern Breakdown: Tool / Skill Wrapper (Pattern A)

### Mechanics & Data Flow
1. Orchestrator agent (`Lucy`) decides a blog post is required.
2. `Lucy` invokes a declared tool function: `run_blogger_skill(topic="ReAct Loops")`.
3. The underlying harness executes the blogger pipeline to completion inside an isolated process or function scope.
4. The blogger script returns a structured JSON payload: `{"status": "published", "url": "https://..."}`.

### WHEN to Choose
- The specialized task is self-contained and handles its own internal retries, file scanning, git commits, and quality validation.
- `Lucy` does not need to intervene or edit intermediate text while the task is running.
- You want minimal system complexity, low execution latency, and clean stack trace debugging.

### WHY Choose
- **Single Responsibility Principle**: Decouples the orchestrator from sub-task implementation. `Lucy` stays focused on high-level planning.
- **Context Window Protection**: Prevents `Lucy`'s prompt context from filling up with thousands of intermediate draft tokens and error logs.

---

## 4. Pattern Breakdown: Multi-Agent System / A2A Transport (Pattern B)

### Mechanics & Data Flow
1. Orchestrator agent (`Lucy`) sends an asynchronous event message across a transport bus: `{"event": "START_DRAFT", "task_id": 101}`.
2. Specialized `Blogger Agent` runs its own event loop, emitting progress updates: `{"event": "STEP_UPDATE", "status": "skeptic_eval_failed"}`.
3. `Lucy` monitors event streams and can issue real-time feedback or change directives mid-execution.

### WHEN to Choose
- `Lucy` must actively monitor, critique, or approve intermediate sub-task artifacts before completion.
- Multiple specialized agents (e.g. *Researcher Agent* $\rightarrow$ *Orchestrator* $\rightarrow$ *Blogger Agent* $\rightarrow$ *Social Agent*) must collaborate interactively.

### WHY Choose
- **Interactive Governance**: Enables real-time collaboration between independent agents without merging their implementations into a monolithic script.

---

## 5. The Industry Standard: The Subsystem Facade Pattern

In production enterprise software architectures, system engineers combine both patterns using the **Facade Pattern**:

1. **Outer Boundary (Orchestrator Interface)**: Surfaced to `Lucy`'s system prompt as a single clean **Skill** (`post_to_blog`).
2. **Inner Implementation (Execution Engine)**: The skill function delegates execution to an **Autonomous Agent Harness** (`SessionStateHydrator`, `ReflexionEngine`, `SandboxedWorker`, `OTelTracer`).

This provides complete separation of concerns: **`Lucy` stays light and focused on planning**, while **the `Blogger Agent` executes safely inside its own isolated harness**.

---

## 6. Architectural Takeaway & SDLC Notes

> *"Btw, this is WHEN and WHY we need this framing concept (System Boundaries & Tool Facades vs. Multi-Agent Transports):"*  
> **WHEN**: Designing interaction interfaces between high-level orchestrator agents and specialized sub-task execution modules.  
> **WHY**: Wrapping self-contained agentic pipelines as tool skills keeps orchestrator prompts lightweight and predictable. Reserving multi-agent (A2A) message buses for tasks requiring real-time inter-agent negotiation eliminates unnecessary message transport overhead and keeps system debugging simple.
