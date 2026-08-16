# Tool, skill, agent, staff, department, control plane

Marketing words are not extra types. Each one maps to a file, a JSON key, or a function already in the course.

| Word | Course object |
|---|---|
| Tool | A name in `TOOLS_SCHEMA`, a function in `TOOL_REGISTRY` |
| Skill | A `SKILL.md` file, or a wrapper tool. Not a process. |
| Agent | One process: system prompt, tools, the chapter 04 loop, a session file |
| Staff / department | Not an object. A supervisor process plus a host map plus tools |
| Control plane | Not a new primitive. The process that owns `jobs.json`, the host map, and handoff tools |

## Tool

**Tool** ([chapter 03](../../education/03_the_dispatcher/00_tool_dispatch.md)): a name in `TOOLS_SCHEMA`, a function in a registry. Chapter 03 sends the list as the `tools` key and looks the name up in `TOOL_REGISTRY`. [Chapter 04](../../education/04_the_loop/00_the_react_loop.md) names that list `TOOLS_SCHEMA`. The model emits `tool_calls`. The dispatcher runs the function and sends `role: tool` back.

See [lab1_tool_dispatch.md](../../education/03_the_dispatcher/lab1_tool_dispatch.md).

## Skill

**Skill** is three different things. Do not collapse them.

1. `SKILL.md` ([chapter 14 lab2](../../education/14_mcp/lab2_skills.md)): a text file loaded when a trigger matches. It is not a process. It is not a person. See also [01_skills_and_plugins.md](../../education/14_mcp/01_skills_and_plugins.md).
2. Skill wrapper ([chapter 08 03_skill_vs_two_agents](../../education/08_two_agents/03_skill_vs_two_agents.md)): a tool whose body runs a longer script or a child loop, then returns one JSON. The parent blocks.
3. Marketing "skill": any of the above, plus a fake staff member. Ignore the staff part.

The reader who wants to call "skills" "tools" is half right: the thing the model calls is a tool. Keep "skill" for the markdown file and for the wrapper pattern. Do not name a running process a skill.

## Agent

**Agent** ([chapter 07](../../education/07_one_agent/00_persona_tools_loop_state.md)): one process with a system prompt, tools, the [chapter 04](../../education/04_the_loop/00_the_react_loop.md) loop, and a session file. Not a personality. The kernel is `CoreAgentKernel`. State is `state_store/{session_id}.json`.

See [lab1_core_harness_kernel.md](../../education/07_one_agent/lab1_core_harness_kernel.md).

## Staff / department

**Staff / Chief of Staff / department** (marketing): an org chart of named people. In this course that is a supervisor process ([08](../../education/08_two_agents/00_topologies.md) `supervisor_orchestrator`) plus a host map plus tools. There is no staff object.

See [lab1_supervisor_worker.md](../../education/08_two_agents/lab1_supervisor_worker.md) and [01_where_not_who.md](./01_where_not_who.md).

## Control plane

**Control plane** (marketing): often Kubernetes or a product. In this course: the process that owns the job list ([chapter 16](../../education/16_the_job/00_the_job.md) `jobs.json`), the host map, and the tools that send handoff JSON ([chapter 08](../../education/08_two_agents/01_handoff_protocol.md)). Not a new primitive.

## LangChain / LangGraph / LangFlow

**LangChain / LangGraph / LangFlow**: Related only. LangGraph is one library for the dict-and-edge you wrote in [chapter 06](../../education/06_the_workflow/01_graph_workflows.md). LangChain wraps `tool_calls` and the loop ([03](../../education/03_the_dispatcher/00_tool_dispatch.md) / [04](../../education/04_the_loop/00_the_react_loop.md)). LangFlow is a canvas for that graph. None of them are required. Do not pip install them for these notes.
