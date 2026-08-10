# Agentic & Autonomous AI Engineering Workspace

Welcome to the **Agentic & Autonomous AI Engineering Workspace**. This repository is a comprehensive, hands-on software engineering workspace designed to master AI agent architecture **under the hood**—from single LLM API calls and ReAct control loops to state checkpointers, POSIX sandboxing, fine-tuning (LoRA/QLoRA/GRPO), local-first infrastructure, and production agent application harnesses.

---

## 1. Macro Concept & Industry Need

The artificial intelligence landscape is shifting from passive single-turn prompt wrappers to autonomous, stateful agentic systems. Enterprise production AI requires deterministic software engineering primitives: persistent finite state machines, structured RPC protocols, memory compaction algorithms, local-first inference infrastructure, and automated post-training optimization.

This repository decouples complex agentic systems into clear, low-abstraction building blocks so developers can understand exact RPC payloads, token streams, state transitions, and memory mechanics without magic framework abstractions.

---

## 2. Workspace Directory Structure

The repository is organized into three primary operational domains:

```
AgenticAI-Labs/
├── AGENTS.md                            # Persona, rules, and intent translation protocol
├── README.md                            # Main repository documentation
│
├── education/                           # Curriculum Modules & Hands-on Code Labs
│   ├── modules/                         # Architectural concept specifications
│   └── labs/                            # Low-abstraction Python implementations & co-located docs
│
├── demos/                               # Production Application Harnesses & Demo Projects
│   └── 01_learner_blog_poster_agent/    # Real-world agent projects built from primitives
│
└── resources/                           # Master Reference Guides, Trackers & Bridges
    ├── LAB_TRACKER.md                   # Live lab execution & score tracker
    ├── ROADMAP.md                       # Master strategic phase roadmap
    ├── term_glossary.md                 # Master AI engineering glossary
    ├── tracker_reset_template.md        # Prompt directive to reset lab progress tracker
    └── human_to_ai_bridge/              # Plain-English Intent-to-Primitive Translation Catalog
```

---

## 3. How to Use This Workspace: Step-by-Step Human Procedure

The workspace follows a strict 3-Phase workflow moving from concept research to lab experimentation and real-world application construction:

| 1. Research & Module Specs (`/education/modules`) | 2. Hands-On Lab Code (`/education/labs`) | 3. Demo Application Projects (`/demos/<project>`) |
| :--- | :--- | :--- |
| **IDE Scope**: Open AI IDE (Antigravity, Claude Code, Cursor) at root directory (`AgenticAI-Labs/`). | **IDE Scope**: Open AI IDE at root directory (`AgenticAI-Labs/`). | **IDE Scope**: Open AI IDE directly in target demo folder (`demos/01_learner_blog_poster_agent/`). |
| **Action**: Read architectural concept specifications (`education/modules/01_single_agent_architecture/00_the_react_loop.md`). | **Action**: Execute low-abstraction Python scripts (`python education/labs/01_single_agent/lab1_react_loop.py`), capture TTFT/TPS metrics, and inspect outputs. | **Action**: Copy `AGENTS_TEMPLATE.md` (as `AGENTS.md`) and `intent_to_primitive_catalog.md` from `resources/human_to_ai_bridge/` into the demo root. |
| **Goal**: Understand problem statements, Rosetta Stone jargon mappings, and system design trade-offs. | **Goal**: See raw RPC calls, state transitions, and memory mechanics under the hood without magic framework abstractions. | **Goal**: Describe business features in plain English; AI maps intent to lab primitives, presents a Mermaid architecture flowchart, and builds decoupled code (`core/`, `api/`, `tools/`). |
| **Maintenance**: Review concepts before writing code. | **Maintenance**: Auto-update `resources/LAB_TRACKER.md`. To restart labs from scratch, prompt AI using [`resources/tracker_reset_template.md`](file:///d:/Google/AgenticAI-Labs/resources/tracker_reset_template.md). | **Maintenance**: Report edge cases or new primitive needs back to root workspace. |

---

### Step-by-Step Execution Guidelines for Humans

#### Phase 1: Module Concept Research
1. Open your AI IDE (Antigravity, Claude Code, Cursor) at the root directory (`d:\Google\AgenticAI-Labs`).
2. Navigate to `/education/modules/` to review architectural specifications and Rosetta Stone jargon mappings.
3. Prompt your AI assistant to explain **WHEN** and **WHY** specific architectural patterns apply.

#### Phase 2: Hands-On Lab Experimentation
1. Keep your AI IDE open at the root directory so it automatically reads `AGENTS.md` and `resources/LAB_TRACKER.md`.
2. Work through python scripts in `/education/labs/`. Run scripts via terminal and inspect co-located `.md` docs.
3. The AI assistant automatically updates `resources/LAB_TRACKER.md` after every run.
4. *Resetting Labs*: If you ever want to re-learn or restart the labs from scratch, copy the prompt from [`resources/tracker_reset_template.md`](file:///d:/Google/AgenticAI-Labs/resources/tracker_reset_template.md) into your chat.

#### Phase 3: Building Real-World Applications
1. Open a new AI IDE window pointing **directly** to your target demo project folder (e.g. `d:\Google\AgenticAI-Labs\demos\01_learner_blog_poster_agent`).
2. Copy `AGENTS_TEMPLATE.md` (renamed as `AGENTS.md`) and `intent_to_primitive_catalog.md` from `resources/human_to_ai_bridge/` into your demo folder.
3. Prompt the AI assistant with your desired feature in plain English. The local `AGENTS.md` will force the AI assistant to ask clarifying questions, map your intent to lab primitives, display a Mermaid architecture flowchart, and write production-grade decoupled code (`core/`, `api/`, `tools/`).

---

## 4. Core Operational Pillars

The curriculum and codebase are organized across five fundamental engineering pillars:

### 🏛️ Pillar I: Foundations & Single-Agent Core
- **Focus**: Low-level LLM API calls, token streaming, constrained JSON schema decoding, and single-agent ReAct control loops with short-term/long-term memory compaction.

### 🏛️ Pillar II: Orchestration, Multi-Agent Systems & UI Surfacing
- **Focus**: Deterministic finite state machines (FSMs), multi-agent topologies (supervisor-worker, peer-to-peer), agent handoffs with correlation tracing, POSIX code sandboxing, Server-Sent Events (SSE), and Server-Driven UI (SDUI) Human-in-the-Loop approval gates.

### 🏛️ Pillar III: Local-First Infrastructure & Advanced Reasoning
- **Focus**: On-premise local model serving (Ollama/vLLM), multi-model triage routing, air-gapped private RAG with PII redaction, Chain-of-Thought (CoT) stream demuxing, logit bias steering, and self-healing reflexion loops.

### 🏛️ Pillar IV: Production Project Blueprints & Post-Training
- **Focus**: Software engineering workbenches, Text-to-SQL synthesis, autonomous SRE incident remediation bots, production agent serving runtimes, Parameter-Efficient Fine-Tuning (LoRA/QLoRA), 4-bit GGUF quantization, and DeepSeek-R1 style GRPO preference alignment.

### 🏛️ Pillar V: Agent Harness Architecture & System Synthesis
- **Focus**: Integrating state hydration, model routing, sandboxed execution, cycle detection, human-in-the-loop gates, and OpenTelemetry tracing into an enterprise-grade agent application harness.

---

## 5. Rosetta Stone: AI Buzzwords vs. Software Primitives

| AI Buzzword | Standard Software Engineering Primitive | System Function / Role |
| :--- | :--- | :--- |
| **Inference Call** | Stateless RPC Call | Sends prompt payload to neural network endpoint and returns completion tokens. |
| **ReAct Loop** | Process Feedback Control Loop | Iteratively executes reasoning turns, generates tool calls, and ingests tool outputs. |
| **State Checkpointer** | Finite State Machine (FSM) Hydrator | Persists and restores conversation graph state to Redis, PostgreSQL, or JSON stores. |
| **Model Context Protocol (MCP)** | JSON-RPC 2.0 Transport Protocol | Standardizes inter-process communication between agent kernels and external tool servers. |
| **Execution Sandbox** | Subprocess / Micro-Container | Runs untrusted LLM code inside isolated sub-processes with cgroup memory/CPU caps. |
| **Generative UI Stream** | Asynchronous State Patch Feed | Streams WebSocket/SSE JSON frames rendering interactive frontend components. |
| **Local Inference Engine** | Low-Latency Daemon Service | Serves open-weight LLMs locally on LAN hardware via OpenAI-compatible endpoints. |
| **CoT Stream Demuxer** | Token State Machine Parser | Demultiplexes internal `<think>` reasoning traces from clean user-facing payloads. |
| **LoRA / QLoRA** | Low-Rank Weight Matrix Insertion | Updates trainable adapter matrices ($A \cdot B$) over frozen 4-bit quantized base weights. |
| **GRPO Reinforcement Learning** | Critic-Free Policy Gradient Engine | Optimizes model responses using intra-group relative reward normalization and unit tests. |

---

## 6. Living Workspace Assets

- [`AGENTS.md`](file:///d:/Google/AgenticAI-Labs/AGENTS.md): Defines coaching persona rules, environment setup, and the **Intent-to-Primitive Translation Protocol**.
- [`resources/LAB_TRACKER.md`](file:///d:/Google/AgenticAI-Labs/resources/LAB_TRACKER.md): Live tracker recording completed labs, execution metrics, review counts, and resume pointers.
- [`resources/ROADMAP.md`](file:///d:/Google/AgenticAI-Labs/resources/ROADMAP.md): Tracks active strategic phases from reference catalog setup to production demo projects.
- [`resources/term_glossary.md`](file:///d:/Google/AgenticAI-Labs/resources/term_glossary.md): Master AI engineering and autonomy glossary.
- [`resources/tracker_reset_template.md`](file:///d:/Google/AgenticAI-Labs/resources/tracker_reset_template.md): Prompt directive for resetting lab tracker history to restart learning.
- [`resources/human_to_ai_bridge/intent_to_primitive_catalog.md`](file:///d:/Google/AgenticAI-Labs/resources/human_to_ai_bridge/intent_to_primitive_catalog.md): Plain-English catalog translating non-technical requirements into production lab primitives.
