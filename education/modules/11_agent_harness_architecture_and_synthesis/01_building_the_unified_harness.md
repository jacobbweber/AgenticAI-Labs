# 01: Building the Unified Agent Harness Architecture

## 1. Macro Concept & Industry Need

Building a production AI agent platform (such as Claude Code, Kiro, OpenClaw, or enterprise autonomous workbenches) requires assembling decoupled software primitives into a **Unified Agent Harness**.

While early prototypes execute linear Python loops, enterprise applications demand a multi-layered harness architecture that solves four fundamental production challenges:
1. **Crash Resilience & Conversational Continuity**: Long-running multi-turn agent turns must survive server restarts, pod auto-scaling, and network drops by checkpointing state before and after every turn.
2. **Infinite Loop & Resource Runaways**: Agents can easily get trapped in infinite fix-break-fix cycles. A production harness enforces strict cycle detection, MD5 error hash tracking, and sandboxed subprocess execution limits.
3. **Safety & Compliance Boundaries**: Mutative commands (e.g. modifying production files, restarting pods, dropping tables) require real-time interceptors that emit Human-in-the-Loop (HITL) approval gates before execution.
4. **End-to-End Operational Telemetry**: Distributed tracing must record hierarchical OpenTelemetry spans across model inference, tool execution, self-healing retries, and token cost attribution.

---

## 2. Architectural Component Mapping

| Harness Component | Mastered Primitives Combined | Software Engineering Role |
| :--- | :--- | :--- |
| **Agent Kernel Subsystem** | ReAct Loop + State Checkpointer + CoT Demuxer | Manages conversation state, streams tokens, and executes decision cycles. |
| **Execution Control Subsystem** | Cycle Detector + Sandboxed Worker + Reflexion Engine | Runs untrusted code safely, detects infinite loops, and auto-corrects runtime errors. |
| **Gateway & Safety Subsystem** | Multi-Model Router + SDUI HITL Gate + OTel Evals | Handles model triage, enforces human token approval on mutative commands, and logs traces. |

---

## 3. Step-by-Step Module 11 Lab Specifications

The following specs guide the hands-on code labs in `labs/11_harness_architecture/`:

### Lab 1: Core Harness Execution Loop & Session State Hydrator
- **Objective**: Create `lab1_core_harness_kernel.py` and `lab1_core_harness_kernel.md`.
- **System Spec**:
  - Implement `SessionStateHydrator`: Loads and saves conversation turn history from a JSON state store.
  - Implement `CoTStreamDemuxer`: Demultiplexes reasoning `<think>` tokens from response text.
  - Implement `CoreAgentKernel`: Runs a ReAct decision loop using local Ollama (`qwen3.6:35b-a3b-65k`).

### Lab 2: Resilient Execution & Safety Control Subsystem
- **Objective**: Create `lab2_resilient_executor.py` and `lab2_resilient_executor.md`.
- **System Spec**:
  - Implement `CycleOscillationDetector`: Tracks recent tool calls and MD5 error signatures to abort looping behavior.
  - Implement `SandboxedSubprocessWorker`: Runs Python code inside isolated subprocess sandboxes with 500MB memory limits and 5-second timeouts.
  - Implement `ReflexionSelfHealingEngine`: Intercepts `stderr` tracebacks, formatting bug fixes for the kernel.

### Lab 3: End-to-End Enterprise Agent App with Observability & UI Surfacing
- **Objective**: Create `lab3_enterprise_harness_app.py` and `lab3_enterprise_harness_app.md`.
- **System Spec**:
  - Implement `MultiModelGateway`: Routes routine queries to 7B models and complex tasks to 35B models.
  - Implement `SDUIHITLApprovalGate`: Emits `HITLApprovalModal` JSON payloads for mutative actions (`rollout restart`, `file_delete`), pausing execution.
  - Implement `OTelEvalTracer`: Generates hierarchical OpenTelemetry JSON traces (`agent.turn` $\rightarrow$ `llm.inference` $\rightarrow$ `tool.sandbox`).
