# Path

Work these folders in order. One chapter per session. A `labN_*.py` on disk means that lab has a reference solution. Delete the `.py` files to start from scratch.

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

To add a chapter, add a numbered folder and one row here. Do not keep a separate roadmap or tracker.
