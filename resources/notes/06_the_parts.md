# Brain, memory, plan, tools

An agent in this course is one process ([13](../../education/13_one_agent/00_persona_tools_loop_state.md)): system prompt, tools, the [04](../../education/04_the_loop/00_the_react_loop.md) loop, a session file. The words below are marketing for those pieces. If this page disagrees with a lab brief, the brief wins.

| Word you hear | Course object |
|---|---|
| Brain / foundation model | The provider plus the weight file ([00](../../education/00_atoms/00_script_provider_weights.md), [01](../../education/01_the_call/00_the_wrapper_and_the_stream.md)). It emits `messages` and `tool_calls`. It does not run bash. |
| Short-term memory | The `messages` list in this turn ([02](../../education/02_the_contract/00_messages_and_json.md), [07](../../education/07_the_state/00_save_the_messages.md)). That is the context window. |
| Long-term memory | Session file, `facts.json`, other files ([07](../../education/07_the_state/00_save_the_messages.md), [09](../../education/09_agentic_memory_and_rag/01_agentic_memory.md) / [lab1](../../education/09_agentic_memory_and_rag/lab1_episodic_vs_procedural.md)). RAG is optional. Not required to be a vector database. |
| Planning / task decomposition | The [04](../../education/04_the_loop/00_the_react_loop.md) loop, [11](../../education/11_planning_and_reflection/00_planning_and_reflection.md) plan-and-solve, or a [10](../../education/10_the_workflow/01_graph_workflows.md) graph if the phases are fixed. |
| Self-reflection | [11](../../education/11_planning_and_reflection/lab2_reflexion_loop.md) reflexion. Read the last tool result or error traceback, then retry. |
| Prompting frameworks (CoT, ReAct) | CoT is think tokens ([06](../../education/06_the_reliability/lab1_cot_demuxer.md) demux). ReAct is the [04](../../education/04_the_loop/00_the_react_loop.md) `while` loop. |
| Tools / actuators | [03](../../education/03_the_dispatcher/00_tool_dispatch.md) `TOOLS_SCHEMA` plus `TOOL_REGISTRY`. The script runs the function. |

Shape of the work (tool vs job vs wrapper vs this loop): [04_shape_tree.md](./04_shape_tree.md). Fill [decisions 01](../decisions/01_when_x_vs_y.md) before you add a second process.
