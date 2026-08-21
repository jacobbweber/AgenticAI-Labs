# Path

Work these folders in order. One chapter per session. Open the repo root so the IDE reads AGENTS.md.

If you have not run a script yet, start at [../getting_started/](../getting_started/).

A labN_*.py on disk is a reference solution. Delete the .py files to start from scratch.

## The 20-Stage Progressive Curriculum (7 Tiers)

### Tier 1: The Wire & Protocol
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [00_atoms](./00_atoms/) | [00_script_provider_weights.md](./00_atoms/00_script_provider_weights.md) | [lab1_script_posts_json.md](./00_atoms/lab1_script_posts_json.md), [lab2_read_the_json.md](./00_atoms/lab2_read_the_json.md) | Point at the script, the provider API, and the weight file as three separate things. POST JSON and parse keys. |
| [01_the_call](./01_the_call/) | [00_the_wrapper_and_the_stream.md](./01_the_call/00_the_wrapper_and_the_stream.md) | [lab1_llm_api_basics.md](./01_the_call/lab1_llm_api_basics.md), [lab2_streaming_tokens.md](./01_the_call/lab2_streaming_tokens.md) | Wrap the POST in query_llm(prompt) -> str. Stream tokens incrementally. |
| [02_the_contract](./02_the_contract/) | [00_messages_and_json.md](./02_the_contract/00_messages_and_json.md) | [lab1_structured_json.md](./02_the_contract/lab1_structured_json.md) | Use messages[] arrays and roles. Ask for structured JSON schemas and validate keys. |

### Tier 2: The Core Loop & Kernel
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [03_the_dispatcher](./03_the_dispatcher/) | [00_tool_dispatch.md](./03_the_dispatcher/00_tool_dispatch.md) | [lab1_tool_dispatch.md](./03_the_dispatcher/lab1_tool_dispatch.md) | Read 	ool_calls, run a local function from a registry, and send 
ole: tool results back. |
| [04_the_loop](./04_the_loop/) | [00_the_react_loop.md](./04_the_loop/00_the_react_loop.md) | [lab1_react_loop.md](./04_the_loop/lab1_react_loop.md) | Run a while loop over that dispatcher. That is the foundational ReAct loop. |
| [05_the_budget](./05_the_budget/) | [00_the_budget.md](./05_the_budget/00_the_budget.md) | [lab1_stop_rules.md](./05_the_budget/lab1_stop_rules.md) | Stop an agent loop deterministically with stop rules (max turns, token budgets, explicit stop reasons). |
| [06_the_reliability](./06_the_reliability/) | [00_cot_and_reasoning.md](./06_the_reliability/00_cot_and_reasoning.md), [01_cycle_and_steering.md](./06_the_reliability/01_cycle_and_steering.md), [02_resilient_gateway.md](./06_the_reliability/02_resilient_gateway.md) | [lab1_cot_demuxer.md](./06_the_reliability/lab1_cot_demuxer.md), [lab2_cycle_detection.md](./06_the_reliability/lab2_cycle_detection.md), [lab3_logit_steering.md](./06_the_reliability/lab3_logit_steering.md), [lab4_resilient_gateway.md](./06_the_reliability/lab4_resilient_gateway.md) | Demux <think> CoT tokens, detect cyclic oscillation loops, steer logit schemas, and route multi-model gateways with retries. |

### Tier 3: Persistence & Memory
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [07_the_state](./07_the_state/) | [00_save_the_messages.md](./07_the_state/00_save_the_messages.md) | [lab1_save_json.md](./07_the_state/lab1_save_json.md), [lab2_state_checkpointer.md](./07_the_state/lab2_state_checkpointer.md) | Persist and reload conversation message histories and agent states with JSON and SQLite checkpointers. |
| [08_context_compaction](./08_context_compaction/) | [00_context_compaction.md](./08_context_compaction/00_context_compaction.md) | [lab1_context_window.md](./08_context_compaction/lab1_context_window.md) | Compact sliding context windows, prune token histories, and summarize old conversation turns. |
| [09_agentic_memory_and_rag](./09_agentic_memory_and_rag/) | [01_agentic_memory.md](./09_agentic_memory_and_rag/01_agentic_memory.md), [02_private_rag.md](./09_agentic_memory_and_rag/02_private_rag.md), [03_codebase_indexing.md](./09_agentic_memory_and_rag/03_codebase_indexing.md) | [lab1_episodic_vs_procedural.md](./09_agentic_memory_and_rag/lab1_episodic_vs_procedural.md), [lab2_local_private_rag.md](./09_agentic_memory_and_rag/lab2_local_private_rag.md), [lab3_codebase_index.md](./09_agentic_memory_and_rag/lab3_codebase_index.md) | Distinguish episodic facts from procedural rules, perform private local RAG, and index codebases with BM25/vector search. |

### Tier 4: Control Flows & Reasoning
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [10_the_workflow](./10_the_workflow/) | [00_deterministic_dags.md](./10_the_workflow/00_deterministic_dags.md), [01_graph_workflows.md](./10_the_workflow/01_graph_workflows.md), [02_event_driven.md](./10_the_workflow/02_event_driven.md) | [lab1_dag_pipeline.md](./10_the_workflow/lab1_dag_pipeline.md), [lab2_graph_workflow.md](./10_the_workflow/lab2_graph_workflow.md), [lab3_async_event_queue.md](./10_the_workflow/lab3_async_event_queue.md) | Pass dicts through deterministic linear DAGs, state graph workflows with cycles, and async event queues. |
| [11_planning_and_reflection](./11_planning_and_reflection/) | [00_planning_and_reflection.md](./11_planning_and_reflection/00_planning_and_reflection.md) | [lab1_plan_and_solve.md](./11_planning_and_reflection/lab1_plan_and_solve.md), [lab2_reflexion_loop.md](./11_planning_and_reflection/lab2_reflexion_loop.md) | Decompose complex goals into step plans with replanning on failure, and execute self-correcting reflexion loops. |
| [12_agent_evals](./12_agent_evals/) | [00_agent_evals.md](./12_agent_evals/00_agent_evals.md) | [lab1_agent_evals.md](./12_agent_evals/lab1_agent_evals.md) | Benchmark agent trajectories, trace latency and token costs via OpenTelemetry JSONL, and assert pass/fail criteria. |

### Tier 5: Coordination & Protocols
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [13_one_agent](./13_one_agent/) | [00_persona_tools_loop_state.md](./13_one_agent/00_persona_tools_loop_state.md) | [lab1_core_harness_kernel.md](./13_one_agent/lab1_core_harness_kernel.md) | Assemble a single standalone agent kernel unifying system persona, tool registry, ReAct loop, and session state. |
| [14_two_agents](./14_two_agents/) | [00_topologies.md](./14_two_agents/00_topologies.md), [01_handoff_protocol.md](./14_two_agents/01_handoff_protocol.md), [02_specialized_roles.md](./14_two_agents/02_specialized_roles.md), [03_skill_vs_two_agents.md](./14_two_agents/03_skill_vs_two_agents.md) | [lab1_supervisor_worker.md](./14_two_agents/lab1_supervisor_worker.md), [lab2_agent_handoff.md](./14_two_agents/lab2_agent_handoff.md), [lab3_agent_card_manifest.md](./14_two_agents/lab3_agent_card_manifest.md) | Coordinate supervisor-worker topologies, execute strongly-typed 5-key handoffs, and discover agents via gent_card.json manifests. |
| [15_mcp_and_skills](./15_mcp_and_skills/) | [00_mcp_overview.md](./15_mcp_and_skills/00_mcp_overview.md), [01_skills_and_plugins.md](./15_mcp_and_skills/01_skills_and_plugins.md) | [lab1_mcp_client.md](./15_mcp_and_skills/lab1_mcp_client.md), [lab2_skills.md](./15_mcp_and_skills/lab2_skills.md) | Connect to tool servers over Model Context Protocol (JSON-RPC) and load dynamic on-demand SKILL.md instruction files. |

### Tier 6: Security, Governance & Production Runtime
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [16_the_shield](./16_the_shield/) | [00_sandbox.md](./16_the_shield/00_sandbox.md), [01_security_overview.md](./16_the_shield/01_security_overview.md) | [lab1_code_sandbox.md](./16_the_shield/lab1_code_sandbox.md), [lab2_permissions.md](./16_the_shield/lab2_permissions.md), [lab3_agent_rbac.md](./16_the_shield/lab3_agent_rbac.md) | Execute untrusted code safely in subprocess sandboxes, check tool permissions, and enforce agent role-based access control (RBAC). |
| [17_hitl_and_park_resume](./17_hitl_and_park_resume/) | [00_hitl_and_park_resume.md](./17_hitl_and_park_resume/00_hitl_and_park_resume.md) | [lab1_hitl_approval.md](./17_hitl_and_park_resume/lab1_hitl_approval.md), [lab2_park_and_resume.md](./17_hitl_and_park_resume/lab2_park_and_resume.md) | Require human approval tokens before mutative operations and park long-running agent jobs for asynchronous resumption. |
| [18_the_job](./18_the_job/) | [00_the_job.md](./18_the_job/00_the_job.md) | [lab1_jobs_table.md](./18_the_job/lab1_jobs_table.md), [lab2_two_workers.md](./18_the_job/lab2_two_workers.md) | Maintain persistent job rows in jobs.json that outlive the terminal session, with concurrent worker claiming. |
| [19_the_front_door](./19_the_front_door/) | [00_fastapi_sse.md](./19_the_front_door/00_fastapi_sse.md), [01_frontend.md](./19_the_front_door/01_frontend.md), [02_mx_vs_ux.md](./19_the_front_door/02_mx_vs_ux.md), [03_cli_harness.md](./19_the_front_door/03_cli_harness.md) | [lab1_sse_streaming_api.md](./19_the_front_door/lab1_sse_streaming_api.md), [lab2_websocket_interrupt.md](./19_the_front_door/lab2_websocket_interrupt.md), [lab3_frontend_client.md](./19_the_front_door/lab3_frontend_client.md), [lab4_mx_vs_ux.md](./19_the_front_door/lab4_mx_vs_ux.md), [lab5_cli_harness.md](./19_the_front_door/lab5_cli_harness.md) | Expose FastAPI SSE streaming endpoints, handle WebSocket user interrupts, bridge model-facing (MX) and user-facing (UX) text, and build web/CLI clients. |

### Tier 7: Full System Synthesis
| Folder | Concept Module | Labs | What you can do after it |
|---|---|---|---|
| [20_synthesis](./20_synthesis/) | [00_harness_overview.md](./20_synthesis/00_harness_overview.md), [01_project_blueprints.md](./20_synthesis/01_project_blueprints.md), [02_spec_tdd.md](./20_synthesis/02_spec_tdd.md), [03_self_evolution.md](./20_synthesis/03_self_evolution.md) | [lab1_resilient_executor.md](./20_synthesis/lab1_resilient_executor.md), [lab2_enterprise_harness_app.md](./20_synthesis/lab2_enterprise_harness_app.md), [lab3_multi_agent_workbench.md](./20_synthesis/lab3_multi_agent_workbench.md), [lab4_enterprise_sql_agent.md](./20_synthesis/lab4_enterprise_sql_agent.md), [lab5_autonomous_sre_agent.md](./20_synthesis/lab5_autonomous_sre_agent.md), [lab6_spec_tdd_loop.md](./20_synthesis/lab6_spec_tdd_loop.md), [lab7_agent_serving_infra.md](./20_synthesis/lab7_agent_serving_infra.md) | Compose all primitives into full enterprise autonomous harnesses, multi-agent workbenches, SQL agents, SRE agents, and spec-driven TDD loops. |

---

## Auxiliary Training Path

Side folder, not on the main linear path: [optional_training](./optional_training/)

| Module | Labs | Description |
|---|---|---|
| [00_pretrain_tiny.md](./optional_training/00_pretrain_tiny.md) | [lab0_pretrain_tiny.md](./optional_training/lab0_pretrain_tiny.md) | Pretrain a tiny character/byte-level transformer model from scratch in pure Python. |
| [01_lora_qlora.md](./optional_training/01_lora_qlora.md) | [lab1_lora_qlora.md](./optional_training/lab1_lora_qlora.md) | Fine-tune local models using low-rank adapter (LoRA) matrices with forward/backward passes. |
| [02_gguf.md](./optional_training/02_gguf.md) | [lab2_gguf_quantization.md](./optional_training/lab2_gguf_quantization.md) | Quantize FP16 model weights into 4-bit integer formats to minimize VRAM footprint. |
| [03_grpo.md](./optional_training/03_grpo.md) | [lab3_grpo_preference_alignment.md](./optional_training/lab3_grpo_preference_alignment.md) | Align reasoning models using Group Relative Policy Optimization (GRPO) rule-based rewards. |

---

## Reference & Conceptual Guides

- Terms & Rosetta Stone: [../resources/term_glossary.md](../resources/term_glossary.md)
- Conceptual Notes (Jargon to Software Primitives): [../resources/notes/](../resources/notes/)
  - [08_what_is_an_agent.md](../resources/notes/08_what_is_an_agent.md): Literal anatomy of an AI agent
  - [09_tools_skills_agents.md](../resources/notes/09_tools_skills_agents.md): Clean boundaries between tools, skills, and agents
  - [10_planning_and_reflection.md](../resources/notes/10_planning_and_reflection.md): Deconstruct Plan-and-Solve, ReAct, and Reflexion
  - [11_memory_architectures.md](../resources/notes/11_memory_architectures.md): Short-term, episodic facts, procedural rules, and vector retrieval
  - [12_framework_translations.md](../resources/notes/12_framework_translations.md): Translating high-level framework wrappers to standard Python primitives
- Architectural Decisions (When X vs Y): [../resources/decisions/](../resources/decisions/)
  - [00_script_server_weights.md](../resources/decisions/00_script_server_weights.md): Where the API sits vs the weight file
  - [01_when_x_vs_y.md](../resources/decisions/01_when_x_vs_y.md): Tool vs wrapper vs two loops vs job row
  - [02_path_canvas.md](../resources/decisions/02_path_canvas.md): Visual flowchart map of the entire curriculum
  - [04_bands_and_features.md](../resources/decisions/04_bands_and_features.md): Grouping numbered folders and mapping features to labs

---

## When you want X

Stay on the current chapter until you finish it. Use this only to find the chapter, not to skip ahead.

| When you want | Go to |
|---|---|
| A script that talks to a model | [00_atoms](./00_atoms/), then [01_the_call](./01_the_call/) |
| JSON that always parses | [02_the_contract](./02_the_contract/) |
| The model to run a local function | [03_the_dispatcher](./03_the_dispatcher/) |
| Multi-step tool use (ReAct loop) | [04_the_loop](./04_the_loop/) |
| A stop reason / token budget for a long loop | [05_the_budget](./05_the_budget/) |
| Hide <think> tags, detect loops, steer schemas, retry gateways | [06_the_reliability](./06_the_reliability/) |
| Save and reload message history / checkpointer | [07_the_state](./07_the_state/) |
| Compact sliding context windows and prune tokens | [08_context_compaction](./08_context_compaction/) |
| Episodic facts vs procedural rules, private RAG, codebase index | [09_agentic_memory_and_rag](./09_agentic_memory_and_rag/) |
| Deterministic linear DAGs, state graph workflows, async event queues | [10_the_workflow](./10_the_workflow/) |
| Plan-and-solve task decomposition and reflexion auto-correction | [11_planning_and_reflection](./11_planning_and_reflection/) |
| Benchmark agent trajectories, trace token costs, and evaluate accuracy | [12_agent_evals](./12_agent_evals/) |
| One agent with persona, tools, loop, and state | [13_one_agent](./13_one_agent/) |
| Two agents, supervisor-worker topologies, agent cards | [14_two_agents](./14_two_agents/) |
| Dynamic tool protocols (MCP) and on-demand markdown skills | [15_mcp_and_skills](./15_mcp_and_skills/) |
| Sandbox code execution, permissions, and agent RBAC | [16_the_shield](./16_the_shield/) |
| Ask human approval before running dangerous commands, park/resume | [17_hitl_and_park_resume](./17_hitl_and_park_resume/) |
| Jobs table outliving the terminal, multiple background workers | [18_the_job](./18_the_job/) |
| FastAPI SSE streaming server, WebSockets, web UI / CLI client | [19_the_front_door](./19_the_front_door/) |
| Full enterprise multi-agent harness synthesis | [20_synthesis](./20_synthesis/) |
| Pretrain tiny models, LoRA fine-tuning, GGUF quantization, GRPO | [optional_training](./optional_training/) |
| Tool vs wrapper vs two loops vs a job row | [decisions 01](../resources/decisions/01_when_x_vs_y.md) |
| Where the provider sits vs the weight file | [decisions 00](../resources/decisions/00_script_server_weights.md) |
| A sentence or button mapped to a lab | [decisions 04](../resources/decisions/04_bands_and_features.md) |
| What an agent is (anatomy & process loop) | [notes 08](../resources/notes/08_what_is_an_agent.md) |
| Tools vs Skills vs Agents distinction | [notes 09](../resources/notes/09_tools_skills_agents.md) |
| Planning & reflection architectures | [notes 10](../resources/notes/10_planning_and_reflection.md) |
| Short-term, episodic, procedural, vector memory | [notes 11](../resources/notes/11_memory_architectures.md) |
| Framework wrappers mapped to standard Python primitives | [notes 12](../resources/notes/12_framework_translations.md) |

To add a chapter, add a numbered folder and one row in both tables.
