# What is an Agent Harness?

In developer discussions, the term **"agent harness"** refers to the surrounding Python application that manages the AI model's inputs and outputs. 

The AI model itself only does two things: it generates text tokens and suggests tool calls. The **harness** is everything else: dispatching functions, maintaining conversation history, enforcing security policies, managing token budgets, and saving state to disk.

In [Chapter 20: Synthesis](../../education/20_synthesis/00_harness_overview.md), you bring all these capabilities together into a complete enterprise harness.

---

## Harness Terminology Translated to Code

| Concept You Hear | Concrete Course Implementation |
|---|---|
| **Execution Sandbox** | An isolated environment (such as a restricted subprocess) where untrusted tool code runs safely ([Chapter 16](../../education/16_the_shield/01_security_overview.md)). |
| **Deterministic Policy Gates** | Explicit security and approval checks before running a tool, such as `lookup_permission` ([Chapter 16 Lab 2](../../education/16_the_shield/lab2_permissions.md)) or Human-In-The-Loop approval ([Chapter 17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md)). |
| **Tool Orchestration** | The combination of the tool dispatcher ([Chapter 03](../../education/03_the_dispatcher/00_tool_dispatch.md)) and the ReAct execution loop ([Chapter 04](../../education/04_the_loop/00_the_react_loop.md)). |
| **State & Persistence** | Storing conversation data outside the model's context window using session files ([Chapter 07](../../education/07_the_state/00_save_the_messages.md)), facts databases ([Chapter 09](../../education/09_agentic_memory_and_rag/01_agentic_memory.md)), and job records ([Chapter 18](../../education/18_the_job/00_the_job.md)). |
| **Subagent Delegation** | Isolating subtasks using skill wrappers ([Chapter 14](../../education/14_two_agents/03_skill_vs_two_agents.md)) or coordinating multiple agent loops. |
| **Observability & Safety** | Tracking execution budgets ([Chapter 05](../../education/05_the_budget/00_the_budget.md)), detecting repetitive reasoning loops ([Chapter 06](../../education/06_the_reliability/)), and running automated benchmark evaluations ([Chapter 12](../../education/12_agent_evals/00_agent_evals.md)). |

You do not need heavy third-party enterprise platforms or complex telemetry servers to build a powerful agent harness. The standard Python patterns built across these labs give you complete control and reliability.

