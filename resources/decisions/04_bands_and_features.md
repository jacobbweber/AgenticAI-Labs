# Bands and features

The walk is still [PATH.md](../../education/PATH.md) 00 through 20. This page does not move folders. It groups the numbered chapters and maps a sentence or a button to the lab.

If a page disagrees with a lab brief, the brief wins. For tool vs wrapper vs two loops vs a job row, fill [01_when_x_vs_y.md](./01_when_x_vs_y.md) first.

## Bands

These names are groupings. They are not a second path.

| Band | Folders | What sits here |
|---|---|---|
| Tier 1: The Wire & Protocol | [00](../../education/00_atoms/) [01](../../education/01_the_call/) [02](../../education/02_the_contract/) | Script, POST, `query_llm`, streaming, `messages[]`, structured JSON schemas |
| Tier 2: The Core Loop & Kernel | [03](../../education/03_the_dispatcher/) [04](../../education/04_the_loop/) [05](../../education/05_the_budget/) [06](../../education/06_the_reliability/) | Dispatcher, ReAct loop, stop rules & budgets, CoT demuxing, loop detection, resilient gateways |
| Tier 3: Persistence & Memory | [07](../../education/07_the_state/) [08](../../education/08_context_compaction/) [09](../../education/09_agentic_memory_and_rag/) | JSON / SQLite checkpointers, context pruning, episodic facts vs procedural rules, private RAG |
| Tier 4: Control Flows & Reasoning | [10](../../education/10_the_workflow/) [11](../../education/11_planning_and_reflection/) [12](../../education/12_agent_evals/) | Linear DAGs, state graph workflows, async event queues, plan-and-solve, reflexion, evals |
| Tier 5: Coordination & Protocols | [13](../../education/13_one_agent/) [14](../../education/14_two_agents/) [15](../../education/15_mcp_and_skills/) | Standalone agent kernel, supervisor-worker topologies, 5-key handoffs, agent cards, MCP, skills |
| Tier 6: Security, Governance & Runtime | [16](../../education/16_the_shield/) [17](../../education/17_hitl_and_park_resume/) [18](../../education/18_the_job/) [19](../../education/19_the_front_door/) | Subprocess sandboxes, RBAC allowlists, HITL approval, parked states, jobs table, FastAPI SSE |
| Tier 7: Synthesis | [20](../../education/20_synthesis/) | One host that composes all primitives: enterprise harnesses, SRE agents, spec TDD |
| Auxiliary Training | [optional_training](../../education/optional_training/) | Pretrain tiny, LoRA/QLoRA adapters, 4-bit GGUF quantization, GRPO reasoning alignment |
| Judgment | [this folder](./), [notes](../notes/) | When/Why and jargon. No new primitive |

## Feature map

Start from the sentence or the control. Then open the lab.

| I want | Open |
|---|---|
| Chat from a phone or browser | [19](../../education/19_the_front_door/00_fastapi_sse.md) plus the [13](../../education/13_one_agent/00_persona_tools_loop_state.md) kernel |
| Stream tokens on a page | [19 lab1](../../education/19_the_front_door/lab1_sse_streaming_api.md), [19 lab3](../../education/19_the_front_door/lab3_frontend_client.md) |
| Stop a running job from the page | [19 lab2](../../education/19_the_front_door/lab2_websocket_interrupt.md) `{ "type": "interrupt" }` |
| A CLI instead of a page | [19 lab5](../../education/19_the_front_door/lab5_cli_harness.md) |
| Hide person-facing vs model-facing text | [19 lab4](../../education/19_the_front_door/lab4_mx_vs_ux.md) |
| A button mapped to a path and a JSON key | [notes 07](../notes/07_surface_map.md) |
| Approve now, at this stdin | [17 lab1](../../education/17_hitl_and_park_resume/lab1_hitl_approval.md) |
| Approve later, same row continues | [17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) `park_job` |
| "Any alerts on jarvis?" | [notes 02](../notes/02_one_router.md), [14 wrapper](../../education/14_two_agents/03_skill_vs_two_agents.md), [18](../../education/18_the_job/00_the_job.md). `jarvis` is `host_id` |
| Run `ansible-playbook` | [03](../../education/03_the_dispatcher/00_tool_dispatch.md) tool `run_playbook`. Rules go in [15 `SKILL.md`](../../education/15_mcp_and_skills/lab2_skills.md) |
| Watch logs on a schedule | Cron writes a [18](../../education/18_the_job/00_the_job.md) row, or a regex tool if no model is needed |
| Messy coding without wrecking this chat | [14 wrapper](../../education/14_two_agents/03_skill_vs_two_agents.md). Past fixes in [09](../../education/09_agentic_memory_and_rag/lab1_episodic_vs_procedural.md) facts or files |
| Two workers, one job list | [18 lab2](../../education/18_the_job/lab2_two_workers.md) `claimed_by` |
| Stop a long loop with a reason | [05](../../education/05_the_budget/00_the_budget.md) |
| Hide `<think>` tokens | [06](../../education/06_the_reliability/lab1_cot_demuxer.md) |
| Survive a crash | [07](../../education/07_the_state/00_save_the_messages.md) / [13](../../education/13_one_agent/00_persona_tools_loop_state.md) session file |
| Different allowlists (read logs vs run a playbook) | [16](../../education/16_the_shield/lab2_permissions.md), [lab3](../../education/16_the_shield/lab3_agent_rbac.md) |
| Tool vs wrapper vs two loops vs a job row | [01_when_x_vs_y.md](./01_when_x_vs_y.md) |
| Where the API sits vs the weight file | [00_script_server_weights.md](./00_script_server_weights.md) |

## Surface

The page does not run ReAct. [19](../../education/19_the_front_door/01_frontend.md) holds `tokens` and `job_id` and can send interrupt. The loop, the job row, and the allowlist stay in the script.

If you are adding a button, name the key it sends or shows, then find that key in [notes 07](../notes/07_surface_map.md). Do not add a second tree of folders for UI.
