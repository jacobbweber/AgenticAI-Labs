# Agentic & Autonomous AI Labs: Master Learning Tracker

This living tracker records all completed labs, runtime metrics, review counts, self-assessed understanding scores, and key discussion notes. Any future session with Antigravity will automatically inspect this tracker to resume work seamlessly.

---

## 📍 Current Resume Pointer

- **Current Completed Milestone**: **Pillar V — Module 11: Production Agent Harness Architecture & System Synthesis** (Completed all 3 labs).
- **Curriculum Status**: **🏆 ALL 11 MODULES & ALL 5 PILLARS 100% MASTERED!**.
- **Next Steps**: Review living lab documentation files or build end-to-end custom production agent applications!

---

## 📊 Summary Progress Dashboard

| Pillar | Module | Completed Labs | Total Labs | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Pillar I** | `00_foundations_and_primitives` | 3 | 3 | **100% Complete** |
| **Pillar I** | `01_single_agent_architecture` | 3 | 3 | **100% Complete** |
| **Pillar II** | `02_orchestration_and_workflows` | 3 | 3 | **100% Complete** |
| **Pillar II** | `03_multi_agent_systems` | 3 | 3 | **100% Complete** |
| **Pillar II** | `04_autonomous_platforms` | 3 | 3 | **100% Complete** |
| **Pillar II** | `05_ui_ux_surfacing` | 3 | 3 | **100% Complete** |
| **Pillar II** | `06_jargon_dictionary` | 0 | 1 | Reference |
| **Pillar III** | `07_local_first_infra` | 3 | 3 | **100% Complete** |
| **Pillar III** | `08_advanced_reasoning` | 3 | 3 | **100% Complete** |
| **Pillar IV** | `09_project_blueprints` | 4 | 4 | **100% Complete** |
| **Pillar IV** | `10_llm_training_finetuning` | 3 | 3 | **100% Complete** |
| **Pillar V** | `11_harness_architecture` | 3 | 3 | **100% Complete** |






























---

## 📓 Detailed Lab Execution & Review History

### Module 00: LLM API Basics

#### Lab 1: Stateless HTTP API Basics & Latency Profiling
- **Script**: [`education/labs/00_foundations/lab1_llm_api_basics.py`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab1_llm_api_basics.py)
- **Doc & Q&A**: [`education/labs/00_foundations/lab1_llm_api_basics.md`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab1_llm_api_basics.md)
- **Last Executed**: `2026-08-08 17:54`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Raw HTTP `POST` to local Ollama (`qwen3.6:35b-a3b-65k` at `192.168.1.29:11434`).
  - Empirical metrics: TPS = 61.29 tokens/sec, Total Latency = 13.01s.
  - High token count (766 tokens) explained by internal reasoning/thinking tokens.

#### Lab 2: Streaming Token Reader & Latency Profiling (SSE)
- **Script**: [`education/labs/00_foundations/lab2_streaming_tokens.py`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab2_streaming_tokens.py)
- **Doc & Q&A**: [`education/labs/00_foundations/lab2_streaming_tokens.md`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab2_streaming_tokens.md)
- **Last Executed**: `2026-08-08 18:17`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - SSE line-by-line streaming (`stream=True`).
  - Reduced initial wait (TTFT) from **13.01s down to 0.44s** (96.6% improvement).

#### Lab 3: Resilient LLM Gateway (Timeouts, Retries & Fallbacks)
- **Script**: [`education/labs/00_foundations/lab3_resilient_gateway.py`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab3_resilient_gateway.py)
- **Doc & Q&A**: [`education/labs/00_foundations/lab3_resilient_gateway.md`](file:///d:/Google/AgenticAI-Labs/education/labs/00_foundations/lab3_resilient_gateway.md)
- **Last Executed**: `2026-08-08 18:26`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Timeout enforcement, exponential backoff retries ($2^{\text{attempt}}$ seconds), and backup model fallbacks.

---

### Module 01: Single Agent Architecture (The ReAct Loop)

#### Lab 1: The ReAct Process Control Loop
- **Script**: [`education/labs/01_single_agent/lab1_react_loop.py`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab1_react_loop.py)
- **Doc & Q&A**: [`education/labs/01_single_agent/lab1_react_loop.md`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab1_react_loop.md)
- **Last Executed**: `2026-08-08 18:51`
- **Review Count**: 2 (In-depth Q&A discussion on ReAct definition)
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - **ReAct Definition**: Clarified that ReAct is a **Software Design Pattern** (published in 2022 by Princeton/Google), NOT a programming language or commercial product.
  - Python `while` loop orchestrating `Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation`.
  - Multi-turn execution completed cleanly in 3 turns.

#### Lab 2: Trajectory Hashing & Infinite Loop Protection
- **Script**: [`education/labs/01_single_agent/lab2_cycle_detection.py`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab2_cycle_detection.py)
- **Doc & Q&A**: [`education/labs/01_single_agent/lab2_cycle_detection.md`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab2_cycle_detection.md)
- **Last Executed**: `2026-08-08 19:09`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - SHA-256 digital fingerprinting of `tool_name + args + output`.
  - Caught duplicate failing call on Turn 2 and halted execution safely to save compute/tokens.

#### Lab 3: Reasoning Token Demuxing (CoT Stream Separation)
- **Script**: [`education/labs/01_single_agent/lab3_reasoning_demux.py`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab3_reasoning_demux.py)
- **Doc & Q&A**: [`education/labs/01_single_agent/lab3_reasoning_demux.md`](file:///d:/Google/AgenticAI-Labs/education/labs/01_single_agent/lab3_reasoning_demux.md)
- **Last Executed**: `2026-08-08 19:17`
- **Review Count**: 2 (In-depth discussion on WHEN and WHY takeaway)
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Demultiplexing incoming token streams: Channel 1 (Thinking Telemetry Log) vs Channel 2 (Action / UI Stream).
  - **WHEN & WHY Takeaway**: Essential for reasoning models (Qwen 3.6, DeepSeek-R1) to prevent JSON syntax crashes in tool calls, keep user UI clean, and maintain developer log observability.

---

### Module 02: Orchestration & Workflows

#### Lab 1: Deterministic DAG Pipelines & LLM Router Nodes
- **Script**: [`education/labs/02_orchestration/lab1_dag_pipeline.py`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab1_dag_pipeline.py)
- **Doc & Q&A**: [`education/labs/02_orchestration/lab1_dag_pipeline.md`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab1_dag_pipeline.md)
- **Last Executed**: `2026-08-08 19:26`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - 4-node topological DAG execution ($Node_1 \rightarrow Node_2 \rightarrow Node_3 \rightarrow Node_4$).
  - LLM restricted to Node 2 for structured JSON classification (`intent == "code_fix"` with 0.98 confidence).
  - Boundary schema validation fallback protecting downstream nodes from invalid JSON format.

#### Lab 2: Stateful Graph Workflows & SQLite Checkpointing
- **Script**: [`education/labs/02_orchestration/lab2_state_checkpointer.py`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab2_state_checkpointer.py)
- **Doc & Q&A**: [`education/labs/02_orchestration/lab2_state_checkpointer.md`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab2_state_checkpointer.md)
- **Last Executed**: `2026-08-08 19:33`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - State Graph with cyclic transitions (Draft $\rightarrow$ Test $\rightarrow$ Conditional Edge $\rightarrow$ Refactor & Retry Loop).
  - Built zero-magic SQLite checkpointer saving state JSON snapshots to `checkpoints.db` after every step.
  - Demonstrated fault-tolerance by restoring historical state snapshot from SQLite database.
  - Windows terminal encoding fix (`cp1252` compatibility using standard text tags).

#### Lab 3: Async Event-Driven Agent Architecture & Task Queues
- **Script**: [`education/labs/02_orchestration/lab3_async_event_queue.py`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab3_async_event_queue.py)
- **Doc & Q&A**: [`education/labs/02_orchestration/lab3_async_event_queue.md`](file:///d:/Google/AgenticAI-Labs/education/labs/02_orchestration/lab3_async_event_queue.md)
- **Last Executed**: `2026-08-08 20:08`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Non-blocking `asyncio` task producer returning `HTTP 202 Accepted` immediately (0.00s latency).
  - Background async worker process consuming tasks off queue and executing LLM inference.
  - Pub/Sub Event Stream emitting typed JSON frames (`job.started`, `agent.thought`, `agent.completed`) to subscribers in real-time.

---

### Module 03: Multi-Agent Systems

#### Lab 1: Supervisor-Worker (Hub-and-Spoke) Topology
- **Script**: [`education/labs/03_multi_agent/lab1_supervisor_worker.py`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab1_supervisor_worker.py)
- **Doc & Q&A**: [`education/labs/03_multi_agent/lab1_supervisor_worker.md`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab1_supervisor_worker.md)
- **Last Executed**: `2026-08-08 20:30`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Supervisor Orchestrator dispatching sub-tasks to specialist workers in parallel via `asyncio.gather` (Fan-Out).
  - Context isolation: `Security Auditor` worker and `Doc Generator` worker execute in isolated, focused prompts without context window bloating.
  - Supervisor synthesizes worker reports into a single consolidated audit document (Fan-In).
  - Increased HTTP timeout to 120s to allow local 35B model (`qwen3.6:35b-a3b-65k`) inference queues to process cleanly.

#### Lab 2: The 5-Component Agent-to-Agent (A2A) Handoff Protocol
- **Script**: [`education/labs/03_multi_agent/lab2_agent_handoff.py`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab2_agent_handoff.py)
- **Doc & Q&A**: [`education/labs/03_multi_agent/lab2_agent_handoff.md`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab2_agent_handoff.md)
- **Last Executed**: `2026-08-08 20:46`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Structured 5-component JSON handoff contract (`context`, `content`, `action`, `state_dump`, `verification`).
  - Correlation ID header (`trace-1786236351996`) for W3C / OpenTelemetry distributed tracing lineage.
  - Schema middleware validation blocking malformed JSON before invoking LLM inference.
  - Developer agent executed refactoring and ran automated verification test (`pytest tests/test_sql_security.py` -> PASSED).

#### Lab 3: Agent Role-Based Access Control (RBAC) & Tool Whitelisting
- **Script**: [`education/labs/03_multi_agent/lab3_agent_rbac.py`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab3_agent_rbac.py)
- **Doc & Q&A**: [`education/labs/03_multi_agent/lab3_agent_rbac.md`](file:///d:/Google/AgenticAI-Labs/education/labs/03_multi_agent/lab3_agent_rbac.md)
- **Last Executed**: `2026-08-08 21:04`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Persona & Role design with explicit tool whitelists (`ROLE_TOOL_PERMISSIONS`).
  - RBAC Interceptor Middleware (`rbac_tool_interceptor`) blocking unauthorized tool execution attempts (`HTTP 403 Forbidden`).
  - Successfully demonstrated authorized access (Architect reading files, Developer writing files) vs unauthorized access (Architect running bash commands, Developer running unit tests).

---

### Module 04: Autonomous Platforms & Engineering

#### Lab 1: Isolated Subprocess Code Execution Sandboxing
- **Script**: [`education/labs/04_autonomous_platforms/lab1_code_sandbox.py`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab1_code_sandbox.py)
- **Doc & Q&A**: [`education/labs/04_autonomous_platforms/lab1_code_sandbox.md`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab1_code_sandbox.md)
- **Last Executed**: `2026-08-08 21:41`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Isolated subprocess execution runner with 4 POSIX resource boundaries: temporary workspace directory (`tempfile.TemporaryDirectory`), hard timeout enforcement (5.0s), `stdout`/`stderr` capture, and exit code extraction.
  - Successfully demonstrated 3 test scenarios: Valid code (`exit_code = 0`), Runtime error traceback capture (`exit_code = 1`), and Infinite loop process termination (`TIMEOUT_EXCEEDED`).
  - Windows terminal encoding fix (`cp1252` compatibility using `[TIMEOUT]` tag).

#### Lab 2: OpenTelemetry (OTel) Tracing & LLM-as-a-Judge Evals
- **Script**: [`education/labs/04_autonomous_platforms/lab2_agent_evals.py`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab2_agent_evals.py)
- **Doc & Q&A**: [`education/labs/04_autonomous_platforms/lab2_agent_evals.md`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab2_agent_evals.md)
- **Last Executed**: `2026-08-08 22:13`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - OTel-compliant `AgentTracer` generating hierarchical JSON trace spans (`agent.session` $\rightarrow$ `llm.inference` $\rightarrow$ `tool.execution`).
  - Captured token consumption (`1702 completion tokens`) and execution latencies (`28943ms LLM duration`, `51ms tool duration`).
  - Automated LLM-as-a-Judge evaluator scoring agent output against JSON rubric (`Score: 100`, `Verdict: PASSED`).

#### Lab 3: Spec-Driven Development (SDD) & Autonomous TDD Loops
- **Script**: [`education/labs/04_autonomous_platforms/lab3_spec_tdd_loop.py`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab3_spec_tdd_loop.py)
- **Doc & Q&A**: [`education/labs/04_autonomous_platforms/lab3_spec_tdd_loop.md`](file:///d:/Google/AgenticAI-Labs/education/labs/04_autonomous_platforms/lab3_spec_tdd_loop.md)
- **Last Executed**: `2026-08-08 22:31`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Spec-Driven SDLC pipeline with Phase 1 EARS requirement compilation (`WHEN [trigger], the system SHALL [action]`).
  - Phase 2 TDD Red Step: Writes unit test suite and verifies test failure (`Exit Code: 1`).
  - Phase 3 TDD Green Step: Generates python code implementation and verifies test pass (`Exit Code: 0`).
  - Subprocess exit code forcing function blocking feature completion until binary exit code `0` is achieved.

---

### Module 05: UI/UX Surfacing & App Integration

#### Lab 1: Server-Sent Events (SSE) & Real-Time Agent Streaming APIs
- **Script**: [`education/labs/05_ui_ux_surfacing/lab1_sse_streaming_api.py`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab1_sse_streaming_api.py)
- **Doc & Q&A**: [`education/labs/05_ui_ux_surfacing/lab1_sse_streaming_api.md`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab1_sse_streaming_api.md)
- **Last Executed**: `2026-08-08 22:41`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `generate_agent_sse_stream` async generator yielding formatted SSE text frames (`data: {...}\n\n`).
  - Streamed 5 typed frame categories: `session_started`, `token_delta`, `tool_call_start`, `tool_call_result`, `turn_complete`.
  - Solved HTTP timeout issues by delivering real-time tokens to clients without blocking the main event loop.

#### Lab 2: Full-Duplex WebSockets & Mid-Turn Interruption Harness
- **Script**: [`education/labs/05_ui_ux_surfacing/lab2_websocket_interrupt.py`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab2_websocket_interrupt.py)
- **Doc & Q&A**: [`education/labs/05_ui_ux_surfacing/lab2_websocket_interrupt.md`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab2_websocket_interrupt.md)
- **Last Executed**: `2026-08-08 22:48`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Multi-step graph runner with node boundary interrupt checkpoints (`interrupt_event.is_set()`).
  - Simulated WebSocket inbound control receiver pushing `INTERRUPT_TURN` frame mid-turn.
  - Successfully demonstrated uninterrupted completion (3 nodes completed) vs mid-turn interrupt trapping (`status: INTERRUPTED` at Node 3).

#### Lab 3: Generative UI & Human-in-the-Loop (HITL) Approval Engine
- **Script**: [`education/labs/05_ui_ux_surfacing/lab3_hitl_generative_ui.py`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab3_hitl_generative_ui.py)
- **Doc & Q&A**: [`education/labs/05_ui_ux_surfacing/lab3_hitl_generative_ui.md`](file:///d:/Google/AgenticAI-Labs/education/labs/05_ui_ux_surfacing/lab3_hitl_generative_ui.md)
- **Last Executed**: `2026-08-08 23:22`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `AgentHITLEngine` managing automatic low-risk action execution vs high-risk stateful pause gates.
  - Server-Driven UI (SDUI) component frame emission (`HITLApprovalModal` with proposed SQL parameters).
  - Human clearance RPC resume postback (`resume_agent_execution`) reloading checkpoint state and completing execution cleanly.

---

### Module 07: Local-First & Multi-Model Infrastructure

#### Lab 1: Local LLM Serving & OpenAI-Compatible Middleware
- **Script**: [`education/labs/07_local_first_infra/lab1_local_llm_server.py`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab1_local_llm_server.py)
- **Doc & Q&A**: [`education/labs/07_local_first_infra/lab1_local_llm_server.md`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab1_local_llm_server.md)
- **Last Executed**: `2026-08-08 23:27`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Connected to local LAN Ollama host at `http://192.168.1.29:11434/v1/chat/completions` using standard OpenAI-compatible API payloads.
  - Target model: `qwen3.6:35b-a3b-65k`.
  - Empirical metrics recorded: 47 prompt tokens, 570 completion tokens, total latency 9.75s, empirical speed of **58.44 Tokens/Sec (TPS)**.
  - Zero-code shift enabling agent harnesses to talk to local models with 100% data privacy and $0 API token bills.

#### Lab 2: Multi-Model Routing & Fallback Cascades
- **Script**: [`education/labs/07_local_first_infra/lab2_multi_model_router.py`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab2_multi_model_router.py)
- **Doc & Q&A**: [`education/labs/07_local_first_infra/lab2_multi_model_router.md`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab2_multi_model_router.md)
- **Last Executed**: `2026-08-08 23:40`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Semantic Triage Router evaluating prompt feature keywords to dispatch queries between `FAST_TIER` (Fast SLM 7B) and `DEEP_TIER` (Deep LLM 35B/70B).
  - Context-preserving Fallback Cascade catching schema validation errors on `FAST_TIER` and escalating execution to `DEEP_TIER` with error context.
  - Successfully demonstrated routine task routing (150ms latency), complex architecture routing (1200ms latency), and automated fallback escalation (`fallback_occurred: True`).

#### Lab 3: Air-Gapped Private Vector Databases & Local RAG
- **Script**: [`education/labs/07_local_first_infra/lab3_local_private_rag.py`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab3_local_private_rag.py)
- **Doc & Q&A**: [`education/labs/07_local_first_infra/lab3_local_private_rag.md`](file:///d:/Google/AgenticAI-Labs/education/labs/07_local_first_infra/lab3_local_private_rag.md)
- **Last Executed**: `2026-08-08 23:57`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `LocalPIIRedactor` string substitution middleware masking names and emails (`John Doe` $\to$ `[PERSON_2]`, `john@acme.com` $\to$ `[EMAIL_1]`).
  - Local in-memory vector store performing document ingestion and cosine relevance matching.
  - Local LLM generation via LAN Ollama host (`qwen3.6:35b-a3b-65k`).
  - Ephemeral memory vault de-anonymization restoring original text tokens before presenting final output to user.

---

### Module 08: Advanced Reasoning, Steering & Reliability

#### Lab 1: Reasoning Models & Chain-of-Thought (CoT) Stream Demuxing
- **Script**: [`education/labs/08_advanced_reasoning/lab1_cot_demuxer.py`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab1_cot_demuxer.py)
- **Doc & Q&A**: [`education/labs/08_advanced_reasoning/lab1_cot_demuxer.md`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab1_cot_demuxer.md)
- **Last Executed**: `2026-08-09 00:18`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - State machine `CoTStreamDemuxer` demultiplexing streamed tokens into Channel 1 (`[THINKING LOG]`) and Channel 2 (`[RESPONSE PAYLOAD]`).
  - Protected JSON tool execution parsers and frontends from `<think>` syntax token pollution.

#### Lab 2: Inference-Time Steering & Guardrail Interceptors
- **Script**: [`education/labs/08_advanced_reasoning/lab2_logit_steering.py`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab2_logit_steering.py)
- **Doc & Q&A**: [`education/labs/08_advanced_reasoning/lab2_logit_steering.md`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab2_logit_steering.md)
- **Last Executed**: `2026-08-09 00:19`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Logit bias steering engine applying scalar offsets ($\delta = -100$) to force 0% sampling probability on prohibited tokens (`apologize`, `cannot`).
  - Pre-inference guardrail interceptor catching prompt injections (`ignore prior instructions`).
  - Post-inference format guardrail enforcing JSON structural compliance.

#### Lab 3: Reflection & Self-Correction Loops (Reflexion Engine)
- **Script**: [`education/labs/08_advanced_reasoning/lab3_reflexion_loop.py`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab3_reflexion_loop.py)
- **Doc & Q&A**: [`education/labs/08_advanced_reasoning/lab3_reflexion_loop.md`](file:///d:/Google/AgenticAI-Labs/education/labs/08_advanced_reasoning/lab3_reflexion_loop.md)
- **Last Executed**: `2026-08-09 00:24`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `ReflexionEngine` state machine managing multi-turn generation, sandboxed execution, and traceback ingestion.
  - MD5 hash fingerprinting of `stderr` error signatures to detect error oscillations and trigger strategy pivots.
  - Successfully verified self-healing python code generation returning `exit_code: 0`.

---

### Module 09: Production Project Blueprints

#### Lab 1: Local Multi-Agent Software Engineering Workbench
- **Script**: [`education/labs/09_project_blueprints/lab1_multi_agent_workbench.py`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab1_multi_agent_workbench.py)
- **Doc & Q&A**: [`education/labs/09_project_blueprints/lab1_multi_agent_workbench.md`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab1_multi_agent_workbench.md)
- **Last Executed**: `2026-08-09 00:30`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Tri-agent hierarchical topology (Supervisor, Coder, QA Reviewer) orchestrating software engineering tasks.
  - Coder Agent writing modules (`calculator.py`) and test suites (`test_calculator.py`) to an isolated temporary sandbox.
  - QA Reviewer Agent executing tests in a subprocess sandbox, returning clean execution traces (`exit_code: 0`).

#### Lab 2: Enterprise Data & SQL Synthesis Agent
- **Script**: [`education/labs/09_project_blueprints/lab2_enterprise_sql_agent.py`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab2_enterprise_sql_agent.py)
- **Doc & Q&A**: [`education/labs/09_project_blueprints/lab2_enterprise_sql_agent.md`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab2_enterprise_sql_agent.md)
- **Last Executed**: `2026-08-09 00:40`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - Text-to-SQL transpilation engine translating business queries into SQLite statements via local Ollama (`qwen3.6:35b-a3b-65k`).
  - AST & Security Guardrail interceptor blocking mutation commands (`DELETE`) and enforcing row limits (`LIMIT 1000`).
  - Dynamic SQL healing loop intercepting database runtime exceptions and self-correcting queries.

#### Lab 3: Autonomous DevOps & SRE Incident Remediation Agent
- **Script**: [`education/labs/09_project_blueprints/lab3_autonomous_sre_agent.py`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab3_autonomous_sre_agent.py)
- **Doc & Q&A**: [`education/labs/09_project_blueprints/lab3_autonomous_sre_agent.md`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab3_autonomous_sre_agent.md)
- **Last Executed**: `2026-08-09 00:43`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `LogTriageEngine` filtering log streams for `ERROR`/`CRITICAL` log signatures (`ConnectionPoolExhausted`) to reduce context overhead.
  - SRE Agent root-cause analysis diagnosing database pool exhaustion causing HTTP 502 Bad Gateway.
  - `SRECommandSafetyGuard` automatically approving read-only commands (`kubectl get pods`), blocking destructive actions (`delete namespace`), and emitting `HITLApprovalModal` for mutative commands (`kubectl rollout restart`).

#### Lab 4: Production Agent Serving Infrastructure
- **Script**: [`education/labs/09_project_blueprints/lab4_agent_serving_infra.py`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab4_agent_serving_infra.py)
- **Doc & Q&A**: [`education/labs/09_project_blueprints/lab4_agent_serving_infra.md`](file:///d:/Google/AgenticAI-Labs/education/labs/09_project_blueprints/lab4_agent_serving_infra.md)
- **Last Executed**: `2026-08-09 00:45`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `InferenceGatewayRouter` load-balancing prompts across model endpoints (`http://192.168.1.29:11434`), tracking prompt tokens and completion tokens.
  - Subprocess sandboxed worker pool enforcing execution time and memory limits.
  - `OTelSpanCollector` emitting OpenTelemetry spans (`llm.inference` & `sandbox.execution`) to profile multi-tenant latencies.

---

### Module 10: LLM Fine-Tuning, Quantization & Domain Adaptation

#### Lab 1: Parameter-Efficient Fine-Tuning (LoRA / QLoRA)
- **Script**: [`education/labs/10_llm_training_finetuning/lab1_lora_qlora.py`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab1_lora_qlora.py)
- **Doc & Q&A**: [`education/labs/10_llm_training_finetuning/lab1_lora_qlora.md`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab1_lora_qlora.md)
- **Last Executed**: `2026-08-09 00:48`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `PurePythonLoRALayer` matrix decomposition engine wrapping frozen base weights ($W_0$) with trainable low-rank adapters ($A \cdot B$).
  - Demonstrated 99.61% reduction in trainable parameters (65,536 adapter params vs 16.7M base params).
  - Executed zero-dependency forward pass calculation: $y = W_0 \cdot x + \frac{\alpha}{r} (B \cdot A \cdot x)$.

#### Lab 2: Quantization, GGUF Export & Model Compression
- **Script**: [`education/labs/10_llm_training_finetuning/lab2_gguf_quantization.py`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab2_gguf_quantization.py)
- **Doc & Q&A**: [`education/labs/10_llm_training_finetuning/lab2_gguf_quantization.md`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab2_gguf_quantization.md)
- **Last Executed**: `2026-08-09 00:52`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `Uniform4BitQuantizer` engine compressing 16-bit float weights to 4-bit unsigned integers ($q \in 0..15$) with Scale ($S$) and Zero-Point ($Z$) mapping.
  - Demonstrated 4.0x VRAM compression ratio (75% VRAM memory reduction) with ultra-low reconstruction MSE loss (0.02203).
  - Generated Ollama `Modelfile` configuration manifest for custom GGUF model registration.

#### Lab 3: Preference Optimization & GRPO Alignment
- **Script**: [`education/labs/10_llm_training_finetuning/lab3_grpo_preference_alignment.py`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab3_grpo_preference_alignment.py)
- **Doc & Q&A**: [`education/labs/10_llm_training_finetuning/lab3_grpo_preference_alignment.md`](file:///d:/Google/AgenticAI-Labs/education/labs/10_llm_training_finetuning/lab3_grpo_preference_alignment.md)
- **Last Executed**: `2026-08-09 00:53`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `GRPOAlignmentEngine` implementing Critic-free policy gradient updates (DeepSeek-R1 pattern).
  - `verify_python_code` deterministic program verifier (RLVR) evaluating candidate outputs in a sandbox environment.
  - Calculated group-relative advantage normalization $A_i = \frac{R_i - \mu_R}{\sigma_R + \epsilon}$, penalizing below-average outputs ($A_i = -1.0$) and rewarding above-average outputs ($A_i = +1.0$) with zero Critic VRAM memory overhead.

---

### Pillar V — Module 11: Production Agent Harness Architecture & System Synthesis

#### Overview & Q&A
- **Q&A Notes**: [`education/labs/11_harness_architecture/00_combining_primitives_qa.md`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/00_combining_primitives_qa.md)
- **Module Specs**: [`11_agent_harness_architecture_and_synthesis/00_harness_architecture_overview.md`](file:///d:/Google/AgenticAI-Labs/11_agent_harness_architecture_and_synthesis/00_harness_architecture_overview.md) & [`01_building_the_unified_harness.md`](file:///d:/Google/AgenticAI-Labs/11_agent_harness_architecture_and_synthesis/01_building_the_unified_harness.md)

#### Lab 1: Core Harness Execution Loop & Session State Hydrator
- **Script**: [`education/labs/11_harness_architecture/lab1_core_harness_kernel.py`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab1_core_harness_kernel.py)
- **Doc & Q&A**: [`education/labs/11_harness_architecture/lab1_core_harness_kernel.md`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab1_core_harness_kernel.md)
- **Last Executed**: `2026-08-09 10:51`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `SessionStateHydrator` managing multi-turn conversation graph state persistence (`state_store/session_9001.json`).
  - `CoTStreamDemuxer` demultiplexing internal `<think>` reasoning traces from clean user response payloads.
  - `CoreAgentKernel` coordinating the multi-turn ReAct decision loop, verifying context preservation across sequential turns ("What is my name?" $\rightarrow$ "Your name is Jacob!").

#### Lab 2: Resilient Execution & Safety Control Subsystem
- **Script**: [`education/labs/11_harness_architecture/lab2_resilient_executor.py`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab2_resilient_executor.py)
- **Doc & Q&A**: [`education/labs/11_harness_architecture/lab2_resilient_executor.md`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab2_resilient_executor.md)
- **Last Executed**: `2026-08-09 10:53`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `SandboxedSubprocessWorker` running untrusted Python code inside isolated subprocesses with 3.0s execution timeout caps.
  - `CycleOscillationDetector` tracking call signatures and MD5 error tracebacks (`hashlib.md5(stderr.encode())`) to break infinite loop token burns.
  - `ResilientExecutionController` executing self-healing reflexion loops, capturing `ZeroDivisionError` tracebacks and auto-correcting code (`10 / 0` $\rightarrow$ `10 / 2`) to achieve `exit_code: 0`.

#### Lab 3: Enterprise Agent App with Observability & UI Surfacing
- **Script**: [`education/labs/11_harness_architecture/lab3_enterprise_harness_app.py`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab3_enterprise_harness_app.py)
- **Doc & Q&A**: [`education/labs/11_harness_architecture/lab3_enterprise_harness_app.md`](file:///d:/Google/AgenticAI-Labs/education/labs/11_harness_architecture/lab3_enterprise_harness_app.md)
- **Last Executed**: `2026-08-09 10:55`
- **Review Count**: 1
- **Score**: 5/5
- **Key Takeaways & Discussions**:
  - `MultiModelGatewayRouter` evaluating prompt complexity heuristics to route queries between `FAST_TIER` (7B) and `DEEP_TIER` (`qwen3.6:35b-a3b-65k`).
  - `SDUIHITLApprovalGate` intercepting mutative commands (`kubectl rollout restart`), emitting `HITLApprovalModal` JSON components and pausing execution.
  - `OTelEvalTracer` recording hierarchical OpenTelemetry JSON trace spans (`llm.inference` & `hitl.safety_gate`) to audit latencies, model tiers, and token counts.





























