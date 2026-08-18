# Brain, memory, plan, tools

An agent in this course is one process ([07](../../education/07_one_agent/00_persona_tools_loop_state.md)): system prompt, tools, the [04](../../education/04_the_loop/00_the_react_loop.md) loop, a session file. The words below are marketing for those pieces. If this page disagrees with a lab brief, the brief wins.

| Word you hear | Course object |
|---|---|
| Brain / foundation model | The provider plus the weight file ([00](../../education/00_atoms/00_script_provider_weights.md), [11](../../education/11_engine_room/)). It emits `messages` and `tool_calls`. It does not run bash. |
| Short-term memory | The `messages` list in this turn ([02](../../education/02_the_contract/00_messages_and_json.md), [05](../../education/05_the_state/00_save_the_messages.md)). That is the context window. |
| Long-term memory | Session file, `facts.json`, other files ([05](../../education/05_the_state/00_save_the_messages.md), [13](../../education/13_memory/01_agentic_memory.md) / [lab2](../../education/13_memory/lab2_episodic_vs_procedural.md)). RAG is optional. Not required to be a vector database. |
| Planning / task decomposition | The [04](../../education/04_the_loop/00_the_react_loop.md) loop, or a [06](../../education/06_the_workflow/01_graph_workflows.md) graph if the phases are fixed. Not a separate planning module. |
| Self-reflection | [12](../../education/12_reliability/) reflexion. Read the last tool result, then continue. |
| Prompting frameworks (CoT, ReAct) | CoT is think tokens ([12](../../education/12_reliability/lab1_cot_demuxer.md) demux). ReAct is the [04](../../education/04_the_loop/00_the_react_loop.md) `while` loop. |
| Tools / actuators | [03](../../education/03_the_dispatcher/00_tool_dispatch.md) `TOOLS_SCHEMA` plus `TOOL_REGISTRY`. The script runs the function. |

Shape of the work (tool vs job vs wrapper vs this loop): [04_shape_tree.md](./04_shape_tree.md). Fill [decisions 01](../decisions/01_when_x_vs_y.md) before you add a second process.
