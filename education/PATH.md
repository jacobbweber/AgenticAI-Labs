# Curriculum Learning Path

Follow these chapters in numerical order. We recommend completing one chapter per learning session. 

Open the repository root folder in your IDE so that repository settings (`AGENTS.md`) are automatically applied.

If you have not tested a model connection yet, start with our [Getting Started Guide](../getting_started/).

> **Tip**: Any `labN_*.py` files currently on disk serve as reference solutions. To build from scratch, delete the `.py` files and implement them using the `.md` lab briefs.

---

## The 20-Stage Progressive Curriculum (7 Tiers)

### Tier 1: The Wire & Protocol
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [00_atoms](./00_atoms/) | [00_script_provider_weights.md](./00_atoms/00_script_provider_weights.md) | [lab1_script_posts_json.md](./00_atoms/lab1_script_posts_json.md)<br>[lab2_read_the_json.md](./00_atoms/lab2_read_the_json.md) | Point at the script, the provider API, and the weight file as three distinct components. Send an HTTP POST request and parse JSON keys. |
| [01_the_call](./01_the_call/) | [00_the_wrapper_and_the_stream.md](./01_the_call/00_the_wrapper_and_the_stream.md) | [lab1_llm_api_basics.md](./01_the_call/lab1_llm_api_basics.md)<br>[lab2_streaming_tokens.md](./01_the_call/lab2_streaming_tokens.md) | Wrap HTTP calls into a clean `query_llm(prompt) -> str` function and stream tokens incrementally in real time. |
| [02_the_contract](./02_the_contract/) | [00_messages_and_json.md](./02_the_contract/00_messages_and_json.md) | [lab1_structured_json.md](./02_the_contract/lab1_structured_json.md) | Format conversation history using the `messages` array and roles (`system`, `user`, `assistant`), and enforce strict JSON schemas. |

### Tier 2: The Core Loop & Kernel
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [03_the_dispatcher](./03_the_dispatcher/) | [00_tool_dispatch.md](./03_the_dispatcher/00_tool_dispatch.md) | [lab1_tool_dispatch.md](./03_the_dispatcher/lab1_tool_dispatch.md) | Inspect `tool_calls` in model responses, execute matching Python functions from a registry, and return `role: tool` results. |
| [04_the_loop](./04_the_loop/) | [00_the_react_loop.md](./04_the_loop/00_the_react_loop.md) | [lab1_react_loop.md](./04_the_loop/lab1_react_loop.md) | Run an iterative `while` loop that allows models to call multiple tools in sequence—the foundation of the ReAct pattern. |
| [05_the_budget](./05_the_budget/) | [00_the_budget.md](./05_the_budget/00_the_budget.md) | [lab1_stop_rules.md](./05_the_budget/lab1_stop_rules.md) | Prevent runaway execution by enforcing turn limits, token budgets, and explicit stop conditions. |
| [06_the_reliability](./06_the_reliability/) | [00_cot_and_reasoning.md](./06_the_reliability/00_cot_and_reasoning.md)<br>[01_cycle_and_steering.md](./06_the_reliability/01_cycle_and_steering.md)<br>[02_resilient_gateway.md](./06_the_reliability/02_resilient_gateway.md) | [lab1_cot_demuxer.md](./06_the_reliability/lab1_cot_demuxer.md)<br>[lab2_cycle_detection.md](./06_the_reliability/lab2_cycle_detection.md)<br>[lab3_logit_steering.md](./06_the_reliability/lab3_logit_steering.md)<br>[lab4_resilient_gateway.md](./06_the_reliability/lab4_resilient_gateway.md) | Filter `<think>` reasoning tags, detect repetitive infinite loops, guide output schemas, and build resilient multi-model failover gateways. |
### Tier 3: Persistence & Memory
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [07_the_state](./07_the_state/) | [00_save_the_messages.md](./07_the_state/00_save_the_messages.md) | [lab1_save_json.md](./07_the_state/lab1_save_json.md)<br>[lab2_state_checkpointer.md](./07_the_state/lab2_state_checkpointer.md) | Persist and reload conversation message histories and agent states using JSON files and SQLite checkpointers. |
| [08_context_compaction](./08_context_compaction/) | [00_context_compaction.md](./08_context_compaction/00_context_compaction.md) | [lab1_context_window.md](./08_context_compaction/lab1_context_window.md) | Compact sliding context windows, prune token histories, and summarize older conversation turns. |
| [09_agentic_memory_and_rag](./09_agentic_memory_and_rag/) | [01_agentic_memory.md](./09_agentic_memory_and_rag/01_agentic_memory.md)<br>[02_private_rag.md](./09_agentic_memory_and_rag/02_private_rag.md)<br>[03_codebase_indexing.md](./09_agentic_memory_and_rag/03_codebase_indexing.md) | [lab1_episodic_vs_procedural.md](./09_agentic_memory_and_rag/lab1_episodic_vs_procedural.md)<br>[lab2_local_private_rag.md](./09_agentic_memory_and_rag/lab2_local_private_rag.md)<br>[lab3_codebase_index.md](./09_agentic_memory_and_rag/lab3_codebase_index.md) | Distinguish episodic facts from procedural rules, perform private local RAG, and index codebases using BM25 and vector search. |

### Tier 4: Control Flows & Reasoning
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [10_the_workflow](./10_the_workflow/) | [00_deterministic_dags.md](./10_the_workflow/00_deterministic_dags.md)<br>[01_graph_workflows.md](./10_the_workflow/01_graph_workflows.md)<br>[02_event_driven.md](./10_the_workflow/02_event_driven.md) | [lab1_dag_pipeline.md](./10_the_workflow/lab1_dag_pipeline.md)<br>[lab2_graph_workflow.md](./10_the_workflow/lab2_graph_workflow.md)<br>[lab3_async_event_queue.md](./10_the_workflow/lab3_async_event_queue.md) | Pass state dictionaries through deterministic linear DAGs, cyclical state graph workflows, and asynchronous event queues. |
| [11_planning_and_reflection](./11_planning_and_reflection/) | [00_planning_and_reflection.md](./11_planning_and_reflection/00_planning_and_reflection.md) | [lab1_plan_and_solve.md](./11_planning_and_reflection/lab1_plan_and_solve.md)<br>[lab2_reflexion_loop.md](./11_planning_and_reflection/lab2_reflexion_loop.md) | Decompose complex goals into step-by-step plans with dynamic replanning on errors, and execute self-correcting reflexion loops. |
| [12_agent_evals](./12_agent_evals/) | [00_agent_evals.md](./12_agent_evals/00_agent_evals.md) | [lab1_agent_evals.md](./12_agent_evals/lab1_agent_evals.md) | Benchmark agent trajectories, trace latency and token costs via OpenTelemetry JSONL, and assert automated pass/fail criteria. |

### Tier 5: Coordination & Protocols
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [13_one_agent](./13_one_agent/) | [00_persona_tools_loop_state.md](./13_one_agent/00_persona_tools_loop_state.md) | [lab1_core_harness_kernel.md](./13_one_agent/lab1_core_harness_kernel.md) | Assemble a single standalone agent kernel unifying system personas, tool registries, ReAct loops, and session persistence. |
| [14_two_agents](./14_two_agents/) | [00_topologies.md](./14_two_agents/00_topologies.md)<br>[01_handoff_protocol.md](./14_two_agents/01_handoff_protocol.md)<br>[02_specialized_roles.md](./14_two_agents/02_specialized_roles.md)<br>[03_skill_vs_two_agents.md](./14_two_agents/03_skill_vs_two_agents.md) | [lab1_supervisor_worker.md](./14_two_agents/lab1_supervisor_worker.md)<br>[lab2_agent_handoff.md](./14_two_agents/lab2_agent_handoff.md)<br>[lab3_agent_card_manifest.md](./14_two_agents/lab3_agent_card_manifest.md) | Coordinate supervisor-worker topologies, execute strongly-typed 5-key handoffs, and discover agents via `agent_card.json` manifests. |
| [15_mcp_and_skills](./15_mcp_and_skills/) | [00_mcp_overview.md](./15_mcp_and_skills/00_mcp_overview.md)<br>[01_skills_and_plugins.md](./15_mcp_and_skills/01_skills_and_plugins.md) | [lab1_mcp_client.md](./15_mcp_and_skills/lab1_mcp_client.md)<br>[lab2_skills.md](./15_mcp_and_skills/lab2_skills.md) | Connect to tool servers over Model Context Protocol (JSON-RPC) and load dynamic on-demand `SKILL.md` instruction documents. |

### Tier 6: Security, Governance & Production Runtime
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [16_the_shield](./16_the_shield/) | [00_sandbox.md](./16_the_shield/00_sandbox.md)<br>[01_security_overview.md](./16_the_shield/01_security_overview.md) | [lab1_code_sandbox.md](./16_the_shield/lab1_code_sandbox.md)<br>[lab2_permissions.md](./16_the_shield/lab2_permissions.md)<br>[lab3_agent_rbac.md](./16_the_shield/lab3_agent_rbac.md) | Execute untrusted code safely inside subprocess sandboxes, check tool permissions, and enforce agent role-based access control (RBAC). |
| [17_hitl_and_park_resume](./17_hitl_and_park_resume/) | [00_hitl_and_park_resume.md](./17_hitl_and_park_resume/00_hitl_and_park_resume.md) | [lab1_hitl_approval.md](./17_hitl_and_park_resume/lab1_hitl_approval.md)<br>[lab2_park_and_resume.md](./17_hitl_and_park_resume/lab2_park_and_resume.md) | Require human approval tokens before mutative operations and park long-running agent jobs for asynchronous resumption. |
| [18_the_job](./18_the_job/) | [00_the_job.md](./18_the_job/00_the_job.md) | [lab1_jobs_table.md](./18_the_job/lab1_jobs_table.md)<br>[lab2_two_workers.md](./18_the_job/lab2_two_workers.md) | Maintain persistent job records in `jobs.json` that outlive the terminal session, with concurrent worker claiming. |
| [19_the_front_door](./19_the_front_door/) | [00_fastapi_sse.md](./19_the_front_door/00_fastapi_sse.md)<br>[01_frontend.md](./19_the_front_door/01_frontend.md)<br>[02_mx_vs_ux.md](./19_the_front_door/02_mx_vs_ux.md)<br>[03_cli_harness.md](./19_the_front_door/03_cli_harness.md) | [lab1_sse_streaming_api.md](./19_the_front_door/lab1_sse_streaming_api.md)<br>[lab2_websocket_interrupt.md](./19_the_front_door/lab2_websocket_interrupt.md)<br>[lab3_frontend_client.md](./19_the_front_door/lab3_frontend_client.md)<br>[lab4_mx_vs_ux.md](./19_the_front_door/lab4_mx_vs_ux.md)<br>[lab5_cli_harness.md](./19_the_front_door/lab5_cli_harness.md) | Expose FastAPI SSE streaming endpoints, handle WebSocket user interrupts, bridge model-facing (MX) and user-facing (UX) text, and build web/CLI clients. |

### Tier 7: Full System Synthesis
| Folder | Concept Module | Labs | What You Can Do After It |
|---|---|---|---|
| [20_synthesis](./20_synthesis/) | [00_harness_overview.md](./20_synthesis/00_harness_overview.md)<br>[01_project_blueprints.md](./20_synthesis/01_project_blueprints.md)<br>[02_spec_tdd.md](./20_synthesis/02_spec_tdd.md)<br>[03_self_evolution.md](./20_synthesis/03_self_evolution.md) | [lab1_resilient_executor.md](./20_synthesis/lab1_resilient_executor.md)<br>[lab2_enterprise_harness_app.md](./20_synthesis/lab2_enterprise_harness_app.md)<br>[lab3_multi_agent_workbench.md](./20_synthesis/lab3_multi_agent_workbench.md)<br>[lab4_enterprise_sql_agent.md](./20_synthesis/lab4_enterprise_sql_agent.md)<br>[lab5_autonomous_sre_agent.md](./20_synthesis/lab5_autonomous_sre_agent.md)<br>[lab6_spec_tdd_loop.md](./20_synthesis/lab6_spec_tdd_loop.md)<br>[lab7_agent_serving_infra.md](./20_synthesis/lab7_agent_serving_infra.md) | Compose all primitives into full enterprise autonomous harnesses, multi-agent workbenches, SQL agents, SRE agents, and spec-driven TDD loops. |

---

## Auxiliary Training Path

Side modules focusing on model training, fine-tuning, and quantization: [optional_training](./optional_training/)

| Module | Labs | Description |
|---|---|---|
| [00_pretrain_tiny.md](./optional_training/00_pretrain_tiny.md) | [lab0_pretrain_tiny.md](./optional_training/lab0_pretrain_tiny.md) | Pretrain a tiny character/byte-level transformer model from scratch in pure Python. |
| [01_lora_qlora.md](./optional_training/01_lora_qlora.md) | [lab1_lora_qlora.md](./optional_training/lab1_lora_qlora.md) | Fine-tune local models using low-rank adapter (LoRA) matrices with forward/backward passes. |
| [02_gguf.md](./optional_training/02_gguf.md) | [lab2_gguf_quantization.md](./optional_training/lab2_gguf_quantization.md) | Quantize FP16 model weights into 4-bit integer formats to minimize memory footprint. |
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

## Quick Navigation: Finding What You Want

Stay focused on your current chapter until you complete it. Use this index when you need to locate a specific technique:

| When You Want to Build | Where to Go |
|---|---|
| A basic script that sends a prompt to a model | [00_atoms](./00_atoms/), then [01_the_call](./01_the_call/) |
| Reliable JSON output conforming to a schema | [02_the_contract](./02_the_contract/) |
| An AI model that triggers local Python functions | [03_the_dispatcher](./03_the_dispatcher/) |
| Multi-step tool execution in an iterative loop (ReAct) | [04_the_loop](./04_the_loop/) |
| Bounded execution with turn and token limits | [05_the_budget](./05_the_budget/) |
| Filtering thinking tags, loop detection, and failovers | [06_the_reliability](./06_the_reliability/) |
| Saving and restoring conversation history | [07_the_state](./07_the_state/) |
| Compacting large context windows | [08_context_compaction](./08_context_compaction/) |
| Storing structured facts and private local RAG | [09_agentic_memory_and_rag](./09_agentic_memory_and_rag/) |
| Deterministic DAGs and state graph workflows | [10_the_workflow](./10_the_workflow/) |
| Plan-and-solve task planning and auto-correction | [11_planning_and_reflection](./11_planning_and_reflection/) |
| Benchmarking agent accuracy and performance | [12_agent_evals](./12_agent_evals/) |
| A complete single-agent kernel class | [13_one_agent](./13_one_agent/) |
| Multi-agent supervisor-worker teams | [14_two_agents](./14_two_agents/) |
| Dynamic tool discovery (MCP) and markdown skills | [15_mcp_and_skills](./15_mcp_and_skills/) |
| Secure subprocess sandboxing and role-based permissions | [16_the_shield](./16_the_shield/) |
| Interactive human approval gates and parked jobs | [17_hitl_and_park_resume](./17_hitl_and_park_resume/) |
| Background job tables and asynchronous workers | [18_the_job](./18_the_job/) |
| FastAPI streaming backend and frontend clients | [19_the_front_door](./19_the_front_door/) |
| Full enterprise autonomous agent harnesses | [20_synthesis](./20_synthesis/) |
| Pretraining, LoRA fine-tuning, and quantization | [optional_training](./optional_training/) |

