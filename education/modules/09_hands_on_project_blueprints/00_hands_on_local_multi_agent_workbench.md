# 00: Local Multi-Agent Software Engineering Workbench Blueprint

## 1. Macro Concept & Industry Need

An **air-gapped local multi-agent software engineering workbench** is an offline-first development platform that executes autonomous multi-agent software engineering loops entirely on consumer or workstation hardware (e.g., 64GB or 128GB unified memory systems, or local multi-GPU workstations). 

In enterprise environments, relying exclusively on public cloud LLM APIs introduces four severe structural challenges:
1. **Intellectual Property & Security Risk**: Streaming proprietary source code repositories to external third-party API endpoints creates data egress vulnerabilities and potential compliance violations.
2. **Unpredictable Operational Costs**: Iterative multi-agent loops—where agents continuously read, edit, execute, and debug code—can generate millions of input/output tokens per session, leading to exponential API bill spikes.
3. **Network Latency & Rate Limit Starvation**: High-frequency inter-agent RPC calls across public internet connections suffer from variable network jitter and cloud provider rate-limiting (HTTP 429).
4. **Non-Deterministic Execution & Model Drift**: Closed-source API models are frequently updated or swapped by cloud vendors, breaking brittle agent prompts and causing execution regressions across software development lifecycles.

To solve these industry challenges, the Local Multi-Agent Workbench deploys a specialized **tri-agent hierarchical topology** running on local model servers:
- **Supervisor Agent (Fast Tier - `qwen2.5:14b`)**: Responsible for high-level user prompt analysis, task decomposition, sub-goal planning, turn arbitration, and execution state management.
- **Coder Agent (Deep Reasoning Tier - `llama3.3:70b` / `deepseek-r1:70b`)**: Responsible for deep repository context inspection, architectural modification design, code generation, and file editing.
- **QA Reviewer Agent (Fast Audit Tier - `qwen2.5:14b`)**: Responsible for isolated test suite execution, static code auditing, stack trace analysis, and returning structured critique vectors back to the Coder Agent.

---

## 2. Architectural Component Mapping

The following table demystifies key AI and agentic concepts by mapping them directly to standard software engineering primitives:

| AI / Agentic Concept | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **Multi-Agent Topology** | Hierarchical Finite State Machine (FSM) | Directs execution control flow between Supervisor, Coder, and QA roles based on state transitions. |
| **VRAM Allocation Plan** | Dual-Process HTTP Server Binding | Dedicated local model server instances (e.g., Ollama/llama.cpp ports 11434 & 11435) with fixed GPU KV-cache budgets. |
| **Turn Arbitration** | Token Bucket & Lock Controller | Prevents concurrent model execution deadlocks and enforces strict single-writer file modifications. |
| **Local SSE Event Stream** | Server-Sent Events (HTTP Chunked Response) | Pushes real-time agent state transitions, `<think>` reasoning traces, and tool execution logs to the web UI. |
| **Local RAG & File Context** | Embedded Vector Store & File System Reader | BGE-M3 embeddings + Chroma vector DB for AST code chunk indexing, keyword search, and repository context injection. |
| **Reflection / Self-Correction** | Standard Error Capture & Context Re-injection | Captures `pytest` stdout/stderr, formats stack traces, and appends them to context window memory for iterative retry turns. |

---

## 3. Key Technical Aspects & Dig-In Topics

### VRAM Budgeting & Local Model Server Isolation
Running multiple large language models concurrently on a single local system requires strict VRAM memory budgeting and process isolation to prevent Out-Of-Memory (OOM) crashes. On a 128GB unified memory system (or dual 48GB GPU workstation), VRAM allocation is divided into dedicated server instances with explicit context window caps:

- **Instance 1 (Port 11434 - Deep Reasoning Tier)**: `llama3.3:70b-instruct-q4_K_M` (or `deepseek-r1:70b-q4_K_M`).
  - Model Weights Footprint: ~42 GB VRAM.
  - Context Window Allocation (32k context): ~6 GB VRAM KV-cache.
  - Total Allocated VRAM: ~48 GB.
- **Instance 2 (Port 11435 - Fast Supervisor & Audit Tier)**: `qwen2.5:14b-instruct-q4_K_M`.
  - Model Weights Footprint: ~9 GB VRAM.
  - Context Window Allocation (16k context): ~2 GB VRAM KV-cache.
  - Total Allocated VRAM: ~11 GB.
- **System Overhead & Vector Store**: OS kernel, PyTorch runtime, embedded ChromaDB + BGE-M3 model, FastAPI server, and Next.js frontend consumer ~10 GB RAM.
- **Total System Allocation**: ~69 GB out of 128 GB (leaving ~59 GB headroom for system cache and context scaling).

### Turn Arbitration & FSM State Machine Mechanics
To prevent agent race conditions and infinite execution loops, the workbench implements a deterministic turn-arbitration state machine. Agents do not communicate asynchronously in an unstructured mesh; instead, execution passes sequentially through validated handshakes:

```
                  +--------------------------+
                  |    User Task Request     |
                  +------------+-------------+
                               |
                               v
                  +--------------------------+
                  |     Supervisor Agent     |
                  |     (qwen2.5:14b)        |
                  +------------+-------------+
                               | (Sub-Goal Assignment)
                               v
                  +--------------------------+
                  |       Coder Agent        |
                  |     (llama3.3:70b)       |
                  +------------+-------------+
                               | (Code Edit Completed)
                               v
                  +--------------------------+
                  |    QA Reviewer Agent     |
                  |     (qwen2.5:14b)        |
                  +------------+-------------+
                               |
            +------------------+------------------+
            | (Tests Fail: Stack Trace)           | (Tests Pass)
            v                                     v
+-----------------------+             +-----------------------+
|  Iterative Reflection |             |   Task Completed &    |
|   (Max Retries = 3)   |             |   Code Committed      |
+-----------------------+             +-----------------------+
```

1. **Supervisor Dispatch**: Decomposes user request into concrete sub-goals and assigns Task 1 to Coder Agent.
2. **Coder Execution**: Inspects repo via `view_file`, makes code edits via `edit_file`, and yields control upon edit completion.
3. **QA Verification**: Triggers local `run_test_suite` tool. If tests pass, control returns to Supervisor for next task. If tests fail, the stderr stack trace is formatted into a reflection vector and routed back to Coder Agent.
4. **Oscillation Guard**: A hard constraint (`max_retries = 3`) halts execution if QA fails 3 consecutive turns on the same sub-goal, triggering human-in-the-loop escalation.

### Local Server-Sent Events (SSE) Streaming Architecture
To provide a responsive user experience without cloud dependencies, the FastAPI backend streams agent execution deltas to the web UI using HTTP chunked Server-Sent Events (`text/event-stream`). Custom event frames isolate agent thought processes from tool operations:

```python
# Conceptual FastAPI SSE Stream Generator (< 50 lines)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json, asyncio

app = FastAPI()

async def agent_event_generator(task_id: str):
    # Event 1: Supervisor Thought Trace
    yield f"event: supervisor_thought\ndata: {json.dumps({'thought': 'Deposing task into sub-goals...'})}\n\n"
    await asyncio.sleep(0.5)
    
    # Event 2: Coder Tool Invocation
    yield f"event: coder_tool\ndata: {json.dumps({'tool': 'edit_file', 'path': 'src/main.py'})}\n\n"
    await asyncio.sleep(0.5)
    
    # Event 3: QA Test Execution Result
    yield f"event: qa_result\ndata: {json.dumps({'status': 'PASSED', 'passed': 12, 'failed': 0})}\n\n"

@app.get("/api/workbench/stream/{task_id}")
async def stream_workbench(task_id: str):
    return StreamingResponse(agent_event_generator(task_id), media_type="text/event-stream")
```

### Air-Gapped Tool Harness & File System Security
All tool operations executed by local agents pass through a strict security harness to enforce repository isolation:
- **Path Canonicalization Guard**: Resolves target paths using `os.path.realpath()` and verifies that resolved paths reside strictly within the project root directory, preventing directory traversal attacks (`../`).
- **Subprocess Timeout Isolation**: `run_test_suite` calls run inside `subprocess.run(..., timeout=30, capture_output=True)` with explicit memory limits, preventing rogue tests from locking host resources.

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this blueprint module:

### Lab 1: Baseline Architecture (Dual Local Model Server Binding & Basic Tool Harness)
Configure two isolated local model server instances on custom ports (Port 11434 for 70B Coder model, Port 11435 for 14B Supervisor/QA model). Construct a Python agent harness equipped with safe file system tools (`list_dir`, `view_file`, `edit_file`) enforcing strict path canonicalization within a target sandbox directory.

### Lab 2: Intermediate Capability Integration (Tri-Agent Turn Arbitration & Automated Test Reflection Loop)
Implement the 3-agent Finite State Machine turn arbitrator. Build a local `pytest` execution tool that captures standard output and error streams. Integrate an automated reflection loop that formats failed stack traces and reinjects them into the Coder Agent's context window upon QA test failure, enforcing a 3-retry limit.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Real-Time SSE Streaming & Local Vector RAG Context Pruning)
Develop a FastAPI backend providing an SSE endpoint (`text/event-stream`) that streams live agent reasoning deltas (`<think>`), tool calls, and test results. Integrate a local vector store (ChromaDB + BGE-M3 embeddings) to index repository code files and perform dynamic AST chunk retrieval, preventing context window bloat during large project modifications.

### Stretch Goal: Production Hardening (Full Next.js Multi-Agent IDE Dashboard & Zero-Egress Security Suite)
Build a production-grade Next.js frontend web interface featuring real-time agent state visualization, expandable reasoning trace cards, visual code diff inspection components, real-time VRAM allocation monitors, and a complete zero-network-egress validation audit suite.
