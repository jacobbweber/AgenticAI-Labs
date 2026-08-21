# Course Tiers and Feature Directory

The curriculum in this repository follows a step-by-step path from Chapter 00 to Chapter 20 (see [`education/PATH.md`](../../education/PATH.md)).

This guide groups the chapters into logical architectural tiers and provides a quick lookup directory so you can easily map practical application requirements to the exact lab where that capability is built.

> **Note**: If any overview guide conflicts with a specific lab brief, the lab brief is always the primary source of truth.

---

## The 7 Architectural Tiers

| Tier | Chapters & Folders | Core Concepts Covered |
|---|---|---|
| **Tier 1: Wire & Protocol** | [00: Atoms](../../education/00_atoms/)<br>[01: The Call](../../education/01_the_call/)<br>[02: The Contract](../../education/02_the_contract/) | Python scripts, HTTP POST requests, `query_llm` wrappers, token streaming, the `messages` array, and structured JSON schemas. |
| **Tier 2: Core Loop & Kernel** | [03: Dispatcher](../../education/03_the_dispatcher/)<br>[04: The Loop](../../education/04_the_loop/)<br>[05: The Budget](../../education/05_the_budget/)<br>[06: Reliability](../../education/06_the_reliability/) | Tool dispatching, the ReAct loop, execution stop rules and token budgets, Chain-of-Thought (CoT) demuxing, loop cycle detection, and resilient gateways. |
| **Tier 3: Persistence & Memory** | [07: The State](../../education/07_the_state/)<br>[08: Context Compaction](../../education/08_context_compaction/)<br>[09: Memory & RAG](../../education/09_agentic_memory_and_rag/) | JSON and SQLite session checkpointers, context pruning and summarization, episodic facts vs procedural rules, and private local RAG. |
| **Tier 4: Control Flow & Planning** | [10: The Workflow](../../education/10_the_workflow/)<br>[11: Planning & Reflection](../../education/11_planning_and_reflection/)<br>[12: Agent Evals](../../education/12_agent_evals/) | Deterministic DAG pipelines, state graph workflows, async event queues, Plan-and-Solve patterns, Reflexion loops, and automated agent evaluation suites. |
| **Tier 5: Coordination & Standards** | [13: One Agent](../../education/13_one_agent/)<br>[14: Two Agents](../../education/14_two_agents/)<br>[15: MCP & Skills](../../education/15_mcp_and_skills/) | Standalone agent kernels, supervisor-worker topologies, five-key handoff protocols, agent manifests/cards, Model Context Protocol (MCP), and markdown skills. |
| **Tier 6: Security & Runtime** | [16: The Shield](../../education/16_the_shield/)<br>[17: HITL & Park/Resume](../../education/17_hitl_and_park_resume/)<br>[18: The Job](../../education/18_the_job/)<br>[19: The Front Door](../../education/19_the_front_door/) | Subprocess sandboxes, role-based access control (RBAC), Human-In-The-Loop approval gates, parked state machines, background job tables, and FastAPI SSE endpoints. |
| **Tier 7: Full Synthesis** | [20: Synthesis](../../education/20_synthesis/) | End-to-end integration combining all primitives: enterprise harness apps, autonomous SRE agents, and specification-driven test-driven development (TDD). |
| **Auxiliary Training** | [Optional Training](../../education/optional_training/) | Pretraining tiny models, LoRA/QLoRA fine-tuning adapters, 4-bit GGUF quantization, and GRPO reasoning alignment. |

---

## Feature-to-Lab Directory

When you have a specific feature in mind, use this directory to jump directly to the relevant lab:

| What You Want to Build | Where to Look |
|---|---|
| Connect a web frontend or mobile app to your agent | [Chapter 19: FastAPI SSE](../../education/19_the_front_door/00_fastapi_sse.md) paired with [Chapter 13: Kernel](../../education/13_one_agent/00_persona_tools_loop_state.md) |
| Stream generated tokens directly to a browser interface | [Chapter 19 Lab 1](../../education/19_the_front_door/lab1_sse_streaming_api.md) and [Chapter 19 Lab 3](../../education/19_the_front_door/lab3_frontend_client.md) |
| Allow users to interrupt or cancel a running task | [Chapter 19 Lab 2: WebSocket Interrupts](../../education/19_the_front_door/lab2_websocket_interrupt.md) |
| Build an interactive terminal / CLI agent interface | [Chapter 19 Lab 5: CLI Harness](../../education/19_the_front_door/lab5_cli_harness.md) |
| Separate user-facing chat text from internal model metadata | [Chapter 19 Lab 4: Model Experience vs User Experience](../../education/19_the_front_door/lab4_mx_vs_ux.md) |
| Prompt a user for immediate confirmation before executing an action | [Chapter 17 Lab 1: HITL Approval](../../education/17_hitl_and_park_resume/lab1_hitl_approval.md) |
| Pause a task until an administrator approves it asynchronously later | [Chapter 17: Park and Resume](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) |
| Query a remote host or server safely | [Note 02: One Router](../notes/02_one_router.md), [Chapter 14: Wrapper Tools](../../education/14_two_agents/03_skill_vs_two_agents.md), and [Chapter 18: Jobs](../../education/18_the_job/00_the_job.md) |
| Run an automated task (like Ansible or shell commands) via tools | [Chapter 03: Tool Dispatch](../../education/03_the_dispatcher/00_tool_dispatch.md) with guidelines in [Chapter 15: SKILL.md](../../education/15_mcp_and_skills/lab2_skills.md) |
| Run periodic background tasks on a schedule | Use a cron scheduler writing to [Chapter 18: `jobs.json`](../../education/18_the_job/00_the_job.md) |
| Run isolated trial-and-error code execution safely | [Chapter 14: Skill Wrapper](../../education/14_two_agents/03_skill_vs_two_agents.md) with memory saved in [Chapter 09](../../education/09_agentic_memory_and_rag/lab1_episodic_vs_procedural.md) |
| Coordinate multiple worker processes sharing a single task list | [Chapter 18 Lab 2: Two Workers](../../education/18_the_job/lab2_two_workers.md) |
| Prevent infinite loops and control execution costs | [Chapter 05: The Budget](../../education/05_the_budget/00_the_budget.md) |
| Filter out internal `<think>` reasoning tags from output | [Chapter 06 Lab 1: CoT Demuxer](../../education/06_the_reliability/lab1_cot_demuxer.md) |
| Restore conversation state after an app crash or restart | [Chapter 07: Saving State](../../education/07_the_state/00_save_the_messages.md) and [Chapter 13: Kernel](../../education/13_one_agent/00_persona_tools_loop_state.md) |
| Restrict tools based on user roles and permissions | [Chapter 16 Lab 2: Permissions](../../education/16_the_shield/lab2_permissions.md) and [Chapter 16 Lab 3: RBAC](../../education/16_the_shield/lab3_agent_rbac.md) |

---

## Separating User Interface from Agent Logic

In our architecture, the frontend client ([Chapter 19](../../education/19_the_front_door/01_frontend.md)) simply displays streaming tokens and handles user input events. 

The core reasoning loop, state management, background job processing, and security sandboxes reside cleanly inside your backend Python services.

For design decisions on choosing between tools, wrappers, loops, or background workers, refer to [01_when_x_vs_y.md](./01_when_x_vs_y.md).

