# The harness

Marketing "harness" is not a new primitive. It is the script around the POST: dispatcher, loop, session, allowlist, job row. [Chapter 20](../../education/20_synthesis/00_harness_overview.md) is the compose step. If this page disagrees with a lab brief, the brief wins.

The model only emits text and `tool_calls`. The script runs the function, saves state, and stops or parks.

| Word you hear | Course object |
|---|---|
| Sandbox / execution environment | Isolated place a tool runs ([16](../../education/16_the_shield/01_security_overview.md)). Not the model. |
| Hooks / deterministic gates | A check before the function runs: [16](../../education/16_the_shield/lab2_permissions.md) `lookup_permission`, HITL, or [17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) park. Not a second model. |
| Tool orchestration | [03](../../education/03_the_dispatcher/00_tool_dispatch.md) dispatcher plus the [04](../../education/04_the_loop/00_the_react_loop.md) loop. The model emits `tool_calls`. The script runs `TOOL_REGISTRY`. That is ReAct. |
| State / persistence / memory | [07](../../education/07_the_state/00_save_the_messages.md) session file, [09](../../education/09_agentic_memory_and_rag/01_agentic_memory.md) facts and files, [18](../../education/18_the_job/00_the_job.md) `jobs.json`, [17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) park. Outside the context window. |
| Subagents / delegation | [14 wrapper](../../education/14_two_agents/03_skill_vs_two_agents.md) or two loops. See [04_shape_tree.md](./04_shape_tree.md). Isolated `messages`, then one JSON or a handoff. |
| Observability / evaluation | [06](../../education/06_the_reliability/) cycle hash, reflexion, evals ([12](../../education/12_agent_evals/00_agent_evals.md)). Print the [05](../../education/05_the_budget/00_the_budget.md) stop reason. Not a required telemetry stack. |

Do not add Redis, OpenTelemetry, or a sandbox product because this page lists the words. The lab objects above are enough.
