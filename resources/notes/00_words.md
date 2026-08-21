# Understanding the Terminology: Tools, Skills, Agents, and Control Planes

In the AI industry, marketing terms can often make simple software concepts sound mysterious or overly complicated. In reality, each of these buzzwords maps directly to a concrete Python function, file format, or JSON schema.

Here is a quick lookup table translating popular terminology into the actual code objects you build in this course:

| Term You Hear | Concrete Course Object |
|---|---|
| **Tool** | A schema definition in `TOOLS_SCHEMA` paired with a callable function in `TOOL_REGISTRY`. |
| **Skill** | A structured instruction document (`SKILL.md`), or an isolated wrapper tool function. |
| **Agent** | A running Python process with a system prompt, available tools, a ReAct loop, and a session state file. |
| **Independent Agent** | A background worker process that claims records from a job queue and maintains its own session history. |
| **Ephemeral Subagent** | A self-contained wrapper tool that runs a temporary child loop to solve a subtask, returning a single JSON result. |
| **Staff / Department** | An organizational metaphor for a supervisor process managing a host map and specific tools. |
| **Control Plane** | The central backend process managing `jobs.json`, the host configuration map, and handoff protocols. |

For a visual breakdown of how these concepts connect, see the [Shape Tree Guide](./04_shape_tree.md).

---

## 1. Tools

A **tool** ([Chapter 03: Tool Dispatch](../../education/03_the_dispatcher/00_tool_dispatch.md)) is simply a standard Python function registered in your code. 

When you make a request to an LLM provider, your script includes a list of available tool schemas in the `tools` parameter (often stored in a variable like `TOOLS_SCHEMA`). If the model decides a tool is needed, it responds with a `tool_calls` payload. Your script looks up the matching function name in `TOOL_REGISTRY`, executes the Python function with the model's arguments, and appends the result to the conversation as a message with `role: tool`.

To see this in action, review [Chapter 03 Lab 1](../../education/03_the_dispatcher/lab1_tool_dispatch.md).

---

## 2. Skills

The word **skill** is used in three distinct ways across the industry:

1. **Instruction Files (`SKILL.md`)**: A markdown document ([Chapter 15 Lab 2](../../education/15_mcp_and_skills/lab2_skills.md)) containing specialized domain guidelines that are loaded into an agent's prompt when a specific trigger condition is met.
2. **Skill Wrappers**: A Python function ([Chapter 14: Skill vs Two Agents](../../education/14_two_agents/03_skill_vs_two_agents.md)) that runs an internal child loop or script to handle a complex task and returns a single clean JSON response. The parent agent pauses and waits for the result without cluttering its own conversation history.
3. **Marketing Persona**: Fictional character titles (like *"Customer Support Specialist"*). In code, these are simply system prompts paired with specific tool allowlists.

In this course, we reserve the word "skill" for `SKILL.md` documents and wrapper tool patterns.

---

## 3. Agents

An **agent** ([Chapter 13: One Agent](../../education/13_one_agent/00_persona_tools_loop_state.md)) is a single running Python program consisting of four concrete elements:
- A **system prompt** defining its core objective.
- A **tool registry** (`TOOL_REGISTRY`) giving it actionable capabilities.
- An **execution loop** ([Chapter 04: The ReAct Loop](../../education/04_the_loop/00_the_react_loop.md)) that iteratively queries the model, executes tools, and evaluates results.
- A **persistent session file** (such as `state_store/{session_id}.json`) to preserve conversation state across runs.

---

## 4. Supervisors, Staff, and Departments

When marketing materials talk about an "AI staff" or "department," they are usually describing a **supervisor-worker topology** ([Chapter 14 Lab 1](../../education/14_two_agents/lab1_supervisor_worker.md)). 

In practical code, this is simply a coordinator agent that uses a host configuration map ([Note 01: Where, Not Who](./01_where_not_who.md)) to delegate specific tasks to specialized worker processes.

---

## 5. Control Planes

A **control plane** is the central management service that oversees system operations. In our curriculum, the control plane is represented by the central process that manages persistent task queues ([Chapter 18: `jobs.json`](../../education/18_the_job/00_the_job.md)), monitors device maps, and coordinates handoff protocols ([Chapter 14: Handoff Protocol](../../education/14_two_agents/01_handoff_protocol.md)).

---

## What About External Frameworks?

Frameworks like LangChain, LangGraph, and CrewAI provide third-party abstractions around these exact patterns. For instance, LangGraph provides state graphs similar to the deterministic dictionaries and functions built in [Chapter 10](../../education/10_the_workflow/01_graph_workflows.md). 

Because this course teaches the underlying mechanics directly in pure Python, you do not need to install any external frameworks.

