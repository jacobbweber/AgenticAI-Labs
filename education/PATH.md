# Path

Work these folders in order. One chapter per session. Open the repo root so the IDE reads `AGENTS.md`.

A `labN_*.py` on disk is a reference solution. Delete the `.py` files to start from scratch.

| Folder | What you can do after it |
|---|---|
| [00_atoms](./00_atoms/) | Point at the script, the provider API, and the weight file as three separate things. POST JSON and name the keys. |
| [01_the_call](./01_the_call/) | Wrap the POST in `query_llm(prompt) -> str`. Stream tokens. |
| [02_the_contract](./02_the_contract/) | Use `messages[]` and roles. Ask for JSON and validate it. |
| [03_the_dispatcher](./03_the_dispatcher/) | Read `tool_calls`, run a local function from a registry, send `role: tool` back. |
| [04_the_loop](./04_the_loop/) | Run a `while` loop over that dispatcher. That is ReAct. |
| [05_the_state](./05_the_state/) | Save and load the message list. JSON first, then SQLite. |
| [06_the_workflow](./06_the_workflow/) | Pass a dict through functions. That is a graph. |
| [07_one_agent](./07_one_agent/) | Persona + tools + loop + state. First time the word agent is earned. |
| [08_two_agents](./08_two_agents/) | Handoff JSON, a queue, isolated permissions. |
| [09_the_shield](./09_the_shield/) | Sandbox, RBAC, HITL. |
| [10_the_front_door](./10_the_front_door/) | FastAPI / SSE. The UI is a client of the script. |
| [11_engine_room](./11_engine_room/) | Ollama vs vLLM vs llama.cpp. Multi-model routing. Gateway retries. |
| [12_reliability](./12_reliability/) | Cycle detect, CoT demux, reflexion, evals. |
| [13_memory](./13_memory/) | Compaction, RAG, episodic vs procedural. |
| [14_mcp](./14_mcp/) | The dispatcher, extracted into its own process. |
| [15_synthesis](./15_synthesis/) | Snap the pieces into one harness. |

Side folder, not on this line: [optional_training](./optional_training/) (LoRA, GGUF, GRPO).

Terms: [../resources/term_glossary.md](../resources/term_glossary.md).

## When you want X

Stay on the current chapter until you finish it. Use this only to find the chapter, not to skip ahead.

| When you want | Go to |
|---|---|
| A script that talks to a model | [00_atoms](./00_atoms/), then [01_the_call](./01_the_call/) |
| JSON that always parses | [02_the_contract](./02_the_contract/) |
| The model to run a local function | [03_the_dispatcher](./03_the_dispatcher/) |
| Multi-step tool use | [04_the_loop](./04_the_loop/) |
| Survive a crash / reload | [05_the_state](./05_the_state/) |
| Fixed phases (recon, then diagnose, then fix) | [06_the_workflow](./06_the_workflow/) |
| One agent with a persona | [07_one_agent](./07_one_agent/) |
| Two agents, or a skill vs a second agent | [08_two_agents](./08_two_agents/) |
| Approval before a dangerous command | [09_the_shield](./09_the_shield/) |
| A browser or Discord talking to the script | [10_the_front_door](./10_the_front_door/) |
| Small model vs large model | [11_engine_room](./11_engine_room/) |
| Stop loops, hide `<think>`, auto-retry on traceback | [12_reliability](./12_reliability/) |
| Compact history or private RAG | [13_memory](./13_memory/) |
| Tools in a separate process | [14_mcp](./14_mcp/) |
| Put the pieces together | [15_synthesis](./15_synthesis/) |

To add a chapter, add a numbered folder and one row in both tables.

## Open gaps

Missing labs and colliding names found on this branch. One line each. Not a tracker.

- [05_the_state/STUB_lab1_save_json.md](./05_the_state/STUB_lab1_save_json.md): write and read a `messages` list as JSON before SQLite.
- [06_the_workflow/STUB_lab2_graph_workflow.md](./06_the_workflow/STUB_lab2_graph_workflow.md): a named-edge loop between the one-pass DAG and the async queue.
- [09_the_shield/STUB_lab2_permissions.md](./09_the_shield/STUB_lab2_permissions.md): a tool-name allowlist after the sandbox and before HITL.
- [10_the_front_door/STUB_cli_harness.md](./10_the_front_door/STUB_cli_harness.md): stdin and stdout as a client of `run_turn`.
- [10_the_front_door/STUB_frontend_client.md](./10_the_front_door/STUB_frontend_client.md): a page that holds tokens, `job_id`, and an interrupt control.
- [10_the_front_door/STUB_mx_vs_ux.md](./10_the_front_door/STUB_mx_vs_ux.md): split person-facing frames from model-facing frames.
- [12_reliability/STUB_lab_numbering.md](./12_reliability/STUB_lab_numbering.md): three different labs share the `lab2_` prefix.
- [13_memory/STUB_lab1_context_window.md](./13_memory/STUB_lab1_context_window.md): shrink a long `messages` list before RAG.
- [13_memory/STUB_lab2_episodic_vs_procedural.md](./13_memory/STUB_lab2_episodic_vs_procedural.md): one fact row versus how-to text in system `content`.
- [13_memory/STUB_lab4_codebase_index.md](./13_memory/STUB_lab4_codebase_index.md): walk a repo and print hits with `path` and `span`.
- [14_mcp/STUB_lab2_skills.md](./14_mcp/STUB_lab2_skills.md): load a `SKILL.md` when a trigger matches.
- [15_synthesis/STUB_lab_numbering.md](./15_synthesis/STUB_lab_numbering.md): two `lab2_` files and three `lab3_` files share numbers.
- [optional_training/STUB_lab0_pretrain_tiny.md](./optional_training/STUB_lab0_pretrain_tiny.md): no `lab0_pretrain_tiny.py` for next-token train and a `loss` float.
