# Bands and features

The walk is still [PATH.md](../../education/PATH.md) 00 through 18. This page does not move folders. It groups the numbered chapters and maps a sentence or a button to the lab.

If a page disagrees with a lab brief, the brief wins. For tool vs wrapper vs two loops vs a job row, fill [01_when_x_vs_y.md](./01_when_x_vs_y.md) first.

## Bands

These names are groupings. They are not a second path.

| Band | Folders | What sits here |
|---|---|---|
| One process | [00](../../education/00_atoms/) [01](../../education/01_the_call/) [02](../../education/02_the_contract/) [03](../../education/03_the_dispatcher/) [04](../../education/04_the_loop/) [05](../../education/05_the_state/) [06](../../education/06_the_workflow/) [07](../../education/07_one_agent/) | Script, POST, `messages`, dispatcher, loop, session file, one kernel |
| Provider | [11](../../education/11_engine_room/), [optional_training](../../education/optional_training/) | Port, router, weight file. See [00_script_server_weights.md](./00_script_server_weights.md) |
| Reliability | [12](../../education/12_reliability/) | Cycle hash, CoT split, evals, reflexion |
| Split work and gates | [08](../../education/08_two_agents/) [09](../../education/09_the_shield/) [16](../../education/16_the_job/) [17](../../education/17_the_budget/) [18](../../education/18_park_and_resume/) | Wrapper, handoff, allowlist, job row, stop reason, park |
| Memory and tools elsewhere | [13](../../education/13_memory/) [14](../../education/14_mcp/) | Facts and files, `SKILL.md`, MCP |
| Compose | [15](../../education/15_synthesis/) | One host that calls pieces you already have. Blueprints are optional |
| Surface | [10](../../education/10_the_front_door/) | The page or CLI is a client. It does not own the loop |
| Judgment | [this folder](./), [notes](../notes/) | When/Why and jargon. No new primitive |

## Feature map

Start from the sentence or the control. Then open the lab.

| I want | Open |
|---|---|
| Chat from a phone or browser | [10](../../education/10_the_front_door/00_fastapi_sse.md) plus the [07](../../education/07_one_agent/00_persona_tools_loop_state.md) kernel |
| Stream tokens on a page | [10 lab1](../../education/10_the_front_door/lab1_sse_streaming_api.md), [10 lab3](../../education/10_the_front_door/lab3_frontend_client.md) |
| Stop a running job from the page | [10 lab2](../../education/10_the_front_door/lab2_websocket_interrupt.md) `{ "type": "interrupt" }` |
| A CLI instead of a page | [10 lab5](../../education/10_the_front_door/lab5_cli_harness.md) |
| Hide person-facing vs model-facing text | [10 lab4](../../education/10_the_front_door/lab4_mx_vs_ux.md) |
| Approve now, at this stdin | [09](../../education/09_the_shield/lab4_hitl_generative_ui.md) |
| Approve later, same row continues | [18](../../education/18_park_and_resume/00_park_and_resume.md) `park_job` |
| "Any alerts on jarvis?" | [notes 02](../notes/02_one_router.md), [08 wrapper](../../education/08_two_agents/03_skill_vs_two_agents.md), [16](../../education/16_the_job/00_the_job.md). `jarvis` is `host_id` |
| Run `ansible-playbook` | [03](../../education/03_the_dispatcher/00_tool_dispatch.md) tool `run_playbook`. Rules go in [14 `SKILL.md`](../../education/14_mcp/lab2_skills.md) |
| Watch logs on a schedule | Cron writes a [16](../../education/16_the_job/00_the_job.md) row, or a regex tool if no model is needed |
| Messy coding without wrecking this chat | [08 wrapper](../../education/08_two_agents/03_skill_vs_two_agents.md). Past fixes in [13](../../education/13_memory/lab2_episodic_vs_procedural.md) facts or files |
| Two workers, one job list | [16 lab2](../../education/16_the_job/lab2_two_workers.md) `claimed_by` |
| Stop a long loop with a reason | [17](../../education/17_the_budget/00_the_budget.md) |
| Hide `<think>` tokens | [12](../../education/12_reliability/lab1_cot_demuxer.md) |
| Survive a crash | [05](../../education/05_the_state/00_save_the_messages.md) / [07](../../education/07_one_agent/00_persona_tools_loop_state.md) session file |
| Different allowlists (read logs vs run a playbook) | [09](../../education/09_the_shield/lab2_permissions.md), [lab3](../../education/09_the_shield/lab3_agent_rbac.md) |
| Tool vs wrapper vs two loops vs a job row | [01_when_x_vs_y.md](./01_when_x_vs_y.md) |
| Where the API sits vs the weight file | [00_script_server_weights.md](./00_script_server_weights.md) |

## Surface

The page does not run ReAct. [10](../../education/10_the_front_door/01_frontend.md) holds `tokens` and `job_id` and can send interrupt. The loop, the job row, and the allowlist stay in the script.

If you are adding a button, name the key it sends or shows, then find that key in the table. Do not add a second tree of folders for UI.
