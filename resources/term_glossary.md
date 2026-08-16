# Terms

Optional lookup. Short definitions for words used in the chapters.

For a mapping that matches the labs (hosts and files, not staff names), see [notes/](./notes/).

It demystifies industry marketing jargon into exact computer science and software engineering terms, making it easy to understand what technologies *actually are*, how they differ, and where they fit into real-world software architecture.

---

## 📊 The Autonomy Spectrum: From Copilots to Autonomous OS

To evaluate AI systems objectively, software engineers use the **Autonomy Spectrum**—a 5-level taxonomy measuring control, statefulness, execution authority, and loop persistence.

```
+-----------------------------------------------------------------------------------------------+
| LEVEL 0: Raw LLM          Predicts next tokens given a static prompt context.                 |
| LEVEL 1: Code Assistant   Context-aware auto-complete & single-turn suggestions (Copilot).    |
| LEVEL 2: Agentic AI       Tool-executing state machine with human-in-the-loop oversight.      |
| LEVEL 3: Autonomous Agent Multi-step goal execution with self-correction & sandboxed tools.   |
| LEVEL 4: Agentic OS       Multi-agent platform managing long-horizon lifecycle & background.  |
+-----------------------------------------------------------------------------------------------+
```

### Spectrum Comparison Matrix

| System Level | Example | Primary Mechanism | Execution Authority | Human Role |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0: Raw LLM** | Base `GPT-4` or `Llama-3` API call | Stateless matrix multiplication & next-token probability prediction. | None (Outputs text strings only). | Writes input prompt; reads output tokens. |
| **Level 1: Code Assistant** | GitHub Copilot, IDE auto-complete | Single-turn context assembly (open file tabs + cursor position) sent to LLM for instant inline completion. | Read-only suggestions; inserts text into cursor buffer when accepted. | Driver (Triggers completion, accepts/rejects suggestions inline). |
| **Level 2: Agentic AI** | Custom ReAct Agent, Cursor Composer, Antigravity | Stateful event loop (`while` loop) evaluating LLM tool requests (`read_file`, `exec_cmd`), executing tools, and reading output observations. | Gated execution (Triggers local functions, files, or APIs under human review). | Supervisor (Approves tool calls, gives feedback, sets constraints). |
| **Level 3: Autonomous Agent** | Autonomous Coding Subagent, SWE-bench runner | Goal-driven multi-step graph with state checkpointing, automated unit test verification, and self-correction loops. | High execution authority within isolated sandboxes (Docker/Wasm). | Reviewer (Defines spec & acceptance criteria; reviews final PR/diff). |
| **Level 4: Agentic OS** | Multi-Agent Platform (e.g. Project Lucy) | Distributed supervisor-worker mesh with persistent background queues, event buses (Redis), and domain workspace routing. | Full platform orchestration, background daemon tasks, cron schedules. | Strategic Manager (Monitors dashboards, updates top-level specs). |

---

## 🧠 Core System Classifications

### 1. Artificial Intelligence (AI)
- **Plain English**: Broad umbrella term for any computer system designed to perform tasks that historically required human intelligence (reasoning, perception, learning).
- **Software Primitive**: Algorithms ranging from rule-based decision trees and heuristic search to deep neural network classifiers.

### 2. Large Language Model (LLM)
- **Plain English**: A neural network trained on vast amounts of text to understand and generate human-like natural language and code.
- **Software Primitive**: High-dimensional matrix of parameters (weights) operating as a **stateless mathematical function approximator**:  
  $$\text{Output Tokens} = f(\text{Context Window Prompt})$$

### 3. Small Language Model (SLM)
- **Plain English**: Highly optimized, smaller LLMs (1B to 8B parameters) designed to run efficiently on local edge devices, mobile phones, or laptops.
- **Software Primitive**: Low-latency, low-VRAM model weights compiled for local inference engines (Ollama, llama.cpp, Apple MLX).

### 4. Reasoning Model (CoT Model)
- **Plain English**: An LLM fine-tuned to emit explicit internal "thinking steps" (Chain-of-Thought) before giving its final answer (e.g. DeepSeek-R1, OpenAI o1/o3).
- **Software Primitive**: Model trained via RL/GRPO to output structured XML thinking tags (`<think>...</think>`) that are demuxed from the client-facing output stream.

### 5. Code Assistant (Copilot / Completion Engine)
- **Plain English**: An IDE extension that suggests lines or blocks of code as you type (e.g. GitHub Copilot, Tabnine).
- **Software Primitive**: Passive, single-turn context gatherer listening to editor keystrokes, fetching active file buffers, calling an LLM API, and rendering diff overlays. It does *not* execute code, inspect terminal outputs, or run loops independently.

### 6. Agentic AI (AI Agent)
- **Plain English**: An AI system that doesn't just talk—it takes actions in an environment (reads files, runs tests, calls APIs) to achieve a goal.
- **Software Primitive**: An event-driven state machine (`while` loop) wrapping an LLM with tool schemas, memory buffers, and output parsing.

### 7. Autonomous AI System
- **Plain English**: An advanced AI agent capable of running multi-step complex tasks independently over long periods without stopping for constant human hand-holding.
- **Software Primitive**: Self-correcting state graph with automated verification mechanisms (unit tests, linters), persistent checkpointers, and ephemeral sandboxed runtimes.

---

## 🏗️ Agentic Architecture & Runtime Components

### 8. System Prompt (Instruction Policy)
- **Plain English**: The top-secret initial instructions given to an AI agent defining its identity, rules, boundaries, and available capabilities.
- **Software Primitive**: `Index 0` system-role string prepended to the LLM message array payload (`[{"role": "system", "content": "..."}]`).

### 9. Context Window (Prompt Budget)
- **Plain English**: The maximum amount of text (tokens) an LLM can remember and process at one single time.
- **Software Primitive**: Fixed-capacity sliding memory buffer array. When full, older tokens must be pruned, summarized, or evicted.

### 10. ReAct Loop (Reasoning + Acting)
- **Plain English**: The fundamental 4-step loop that makes an agent work: **Think** $\rightarrow$ **Act** $\rightarrow$ **Observe** $\rightarrow$ **Repeat**.
- **Software Primitive**: Read-Eval-Print Loop (REPL):
  1. Call LLM API with conversation history.
  2. Parse tool call payload from LLM response.
  3. Execute local system function (RPC).
  4. Append tool result string to history and loop back to step 1.

### 11. Agent Harness / Scaffolding
- **Plain English**: The software wrapper surrounding the LLM that handles network connections, file access, safety gates, and error logging.
- **Software Primitive**: Application runtime infrastructure (Python/Node.js host application) managing I/O, subprocesses, and API tokens.

### 12. Skill / Plugin
- **Plain English**: A modular bundle of instructions, documentation, or scripts that equips an agent to perform a specific workflow (e.g., database lookup, PDF parsing).
- **Software Primitive**: On-demand documentation file (`SKILL.md`) or executable helper script loaded into the agent's context window when triggered.

### 13. Model Context Protocol (MCP)
- **Plain English**: An open standard created by Anthropic that lets AI agents securely connect to external tools, databases, and APIs using a universal format.
- **Software Primitive**: Client-Server JSON-RPC 2.0 protocol operating over Stdio or Server-Sent Events (SSE) for dynamic tool and resource discovery.

### 14. Tool Calling / Function Calling
- **Plain English**: The capability of an LLM to output a structured command (like `read_file(path="main.py")`) instead of plain text.
- **Software Primitive**: JSON payload generation conforming to an OpenAPI/JSON Schema function signature definition.

---

## 💾 Memory & Context Engineering

### 15. Short-Term Memory (Turn History)
- **Plain English**: What has been said so far in the current active chat session.
- **Software Primitive**: In-memory Python list or JSON array of turn objects stored in RAM.

### 16. Long-Term Memory (Episodic Memory)
- **Plain English**: Facts, user preferences, and historical decisions stored permanently across chat session restarts.
- **Software Primitive**: External database (SQLite, PostgreSQL, or flat Markdown vault files) queried dynamically at session boot.

### 17. Retrieval-Augmented Generation (RAG) & Vector DB
- **Plain English**: Looking up relevant snippets from large documents or codebases and stuffing them into the prompt so the LLM has exact knowledge.
- **Software Primitive**: High-dimensional vector embedding search over a database (Qdrant, ChromaDB, pgvector) using cosine similarity.

### 18. Context Compaction & KV Cache Eviction
- **Plain English**: Cleaning up and shrinking chat history when it gets too long so the agent doesn't run out of memory or get slow.
- **Software Primitive**: Buffer garbage collection, AST context pruning, and sliding-window text summarization.

---

## 🔄 Orchestration, Workflows & Steering

### 19. Deterministic DAG (Directed Acyclic Graph)
- **Plain English**: A strict, step-by-step workflow where step A *always* leads to step B, with no random AI deviation allowed.
- **Software Primitive**: Standard hard-coded function pipeline / execution graph.

### 20. State Graph (LangGraph)
- **Plain English**: An agentic flowchart where the AI can loop back, retry steps, branch off, or pause for human feedback based on state transitions.
- **Software Primitive**: Finite State Machine (FSM) with persistent checkpointer databases.

### 21. Multi-Agent System (MAS) & Swarm
- **Plain English**: Multiple specialized AI agents working together as a team (e.g., an Architect Agent, a Coder Agent, and a QA Tester Agent).
- **Software Primitive**: Actor Model distributed computing architecture using Pub/Sub message queues or structured JSON handoff schemas.

### 22. Agent-to-Agent (A2A) Handoff Protocol
- **Plain English**: The standardized message format agents use to hand off work to each other cleanly without losing context.
- **Software Primitive**: Strongly-typed inter-process JSON RPC payload schema passing Goal, Logic Chain, State Data, and Verification metrics.

### 23. Human-In-The-Loop (HITL)
- **Plain English**: A safety gate that pauses the AI agent and asks a human for explicit approval before running dangerous commands (like deleting files or deploying code).
- **Software Primitive**: Asynchronous breakpoint / event interrupt waiting for a UI confirmation webhook or CLI input signal.

### 24. Reflection & Self-Correction
- **Plain English**: An agent inspecting its own output or error messages, realizing it made a mistake, and fixing its own code automatically.
- **Software Primitive**: Closed-loop exception handling cycle where stack trace outputs are appended back into the prompt context for a retry turn.

---

## 🛡️ Alignment, Security & Infrastructure

### 25. Guardrails & Red-Teaming
- **Plain English**: Security rules and adversarial testing that prevent an AI agent from leaking sensitive data, going off-topic, or running harmful scripts.
- **Software Primitive**: Web Application Firewall (WAF), input sanitization middleware, and regex/classifier output interceptors.

### 26. Code Sandboxing (Docker / Wasm)
- **Plain English**: Running code generated by an AI agent inside a secure, isolated container so it cannot harm your computer or production server.
- **Software Primitive**: Ephemeral, unprivileged execution container (Wasmtime, Firecracker MicroVM, Docker container) with restricted filesystem permissions.

### 27. Quantization (GGUF, BitNet 1.58b)
- **Plain English**: Compressing heavy AI models so they run fast on consumer computers without needing expensive cloud servers.
- **Software Primitive**: Reducing floating-point precision (e.g. converting 16-bit floats to 4-bit or 1.58-bit ternary integers) to save VRAM and memory bandwidth.

### 28. LoRA / QLoRA Fine-Tuning
- **Plain English**: Training a small, lightweight "adapter plugin" on top of an existing LLM to teach it custom business rules or tool syntax without retraining the whole model.
- **Software Primitive**: Low-Rank Adaptation matrix delta training ($W = W_0 + \Delta W$) attached to model attention layers.

### 29. GRPO (Group Relative Policy Optimization)
- **Plain English**: A modern, efficient reinforcement learning technique (used in DeepSeek-R1) to train AI models to think and reason step-by-step using mathematical rewards.
- **Software Primitive**: RL optimization algorithm calculating relative output rewards within candidate sample groups without needing a separate critic neural network.

---

## 🗂️ Rosetta Stone Summary Matrix

| AI Marketing Buzzword | What It Truly Is Under the Hood | Standard Software Engineering Analog |
| :--- | :--- | :--- |
| **Code Copilot** | Single-turn context builder + inline autocomplete. | Active Cursor Buffer Completion Handler |
| **Agentic AI** | Event-driven loop + tool calling schemas + memory. | Event-Driven State Machine / REPL |
| **Autonomous AI** | Self-correcting state graph + test verification + sandboxes. | Automated Distributed Job Pipeline |
| **Agent Harness** | Python/Node host app managing APIs, files, & logs. | Runtime Container & System Gateway |
| **Model Context Protocol (MCP)** | JSON-RPC 2.0 API over Stdio/SSE for dynamic tool discovery. | Standardized Tool RPC API Protocol |
| **Skill / Plugin** | On-demand documentation or helper script loaded into prompt. | Dynamic Module / Library Import |
| **System Prompt** | Top-level runtime policy rules at index 0 of context. | Root Configuration File / Policy |
| **Context Window** | Sliding memory buffer array of message objects. | Fixed-Capacity Memory Buffer |
| **Guardrails** | Input/output sanitization and jailbreak interceptors. | Web Application Firewall (WAF) |
| **Sandboxing** | Ephemeral container isolation enforcing memory/syscall limits. | Docker Container / Wasm MicroVM |
| **Quantization** | Converting float32 weights to int4 or 1.58-bit ternary integers. | Memory Compression & Precision Reduction |
