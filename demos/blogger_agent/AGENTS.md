## 1. Primary Mandate & Coaching Protocol

- **User Context**: The user is building an agentic AI software project and describing desired features in plain, non-technical English (e.g., *"I want the agent to remember past turns and ask me for approval before posting to my blog"*).
- **Active Intent Translation & Guidance**: The AI assistant MUST NOT blindly write simple 1-off scripts. Instead, the AI assistant MUST:
  1. Work with the user and help establish, create and maintain a `./user_vision.md` file. The intent of this file is to establish the following:
     - Summary
     - Problem Statement
     - Goal
  2. Inspect `intent_to_primitive_catalog.md`.
  3. Ask simple, targeted clarifying questions whenever the user's intent is ambiguous.
  4. Map the user's plain English intent to exact production software primitives (`SessionStateHydrator`, `CycleOscillationDetector`, `ReflexionEngine`, `SandboxedSubprocessWorker`, `SDUIHITLApprovalGate`, `MultiModelGatewayRouter`, `OTelEvalTracer`).
  5. Read back in laymans simplest terms the process flow in what you think the users intent is, clarify the user intent idea or action to systems mapping in a process flow explanation.
  6. If the user confirms the process looks correct, show a visual Mermaid flowchart explaining **HOW** those primitives fit together into a unified control flow before writing code.

---

## 2. Technical Directives & Architecture

- **Decoupled System Architecture**: Always assemble primitives into clean, decoupled software layers (`core/`, `api/`, `tools/`, `evals/`).
- **No Metaphors or Analogies**: Explain software decisions using direct, simple, literal terms.
- **"WHEN & WHY" Focus**: Highlight *when* to choose a specific primitive and *why* (practical trade-offs).

---

## 3. Local Infrastructure Defaults

- **Local Ollama Host**: `http://127.0.0.1:11434`
- **Default Model**: `llama3.2:1b` (or configured model in `.env`)
