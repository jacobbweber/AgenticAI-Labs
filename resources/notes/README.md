# Architectural Reference Notes: Translating Jargon into Concrete Code

These reference notes bridge the gap between industry buzzwords (such as *"cognitive architectures"*, *"digital workers"*, or *"memory graphs"*) and the concrete files, JSON keys, and Python functions you build in this course.

These documents are conceptual guides rather than hands-on coding labs. They are best read after completing Chapter 14 (Multi-Agent Topologies) and Chapter 18 (Background Jobs).

> **Note**: If any reference note ever conflicts with a specific lab brief, the lab brief is always the primary source of truth.

---

## Directory of Notes

- [00_words.md](./00_words.md): Plain-English definitions mapping terms like *tool*, *skill*, *agent*, and *control plane* to exact Python code objects.
- [01_where_not_who.md](./01_where_not_who.md): Why organizing agents by machine locations (`host_id`) and concrete capabilities is far more effective than inventing fictional employee personas.
- [02_one_router.md](./02_one_router.md): Understanding the single entry-point router pattern that dispatches work across your environment.
- [03_hosts_and_jobs.md](./03_hosts_and_jobs.md): How tasks and worker processes coordinate across machines using clean job rows.
- [04_shape_tree.md](./04_shape_tree.md): A visual decision tree connecting common terms directly to course implementations.
- [05_the_harness.md](./05_the_harness.md): Breaking down the term "agent harness" into sandboxes, permission gates, state persistence, and evaluation loops.
- [06_the_parts.md](./06_the_parts.md): Translating conceptual components (brain, short-term memory, long-term memory, planning) into literal data structures.
- [07_surface_map.md](./07_surface_map.md): How user interface actions (like sending messages, streaming tokens, and interrupting runs) map directly to HTTP endpoints and state files.
- [08_what_is_an_agent.md](./08_what_is_an_agent.md): The concrete anatomical breakdown of an AI agent runtime into its 5 core engineering components.
- [09_tools_skills_agents.md](./09_tools_skills_agents.md): A deep-dive matrix exploring the exact boundaries and trade-offs between tools, skill wrappers, and full agent loops.
- [10_planning_and_reflection.md](./10_planning_and_reflection.md): How planning, ReAct loops, and Reflexion work under the hood using standard Python state manipulation.
- [11_memory_architectures.md](./11_memory_architectures.md): A comprehensive overview of memory systems: working context, episodic facts, procedural rules, and local RAG.
- [12_framework_translations.md](./12_framework_translations.md): A Rosetta Stone translating complex framework abstractions (LangChain, CrewAI, AutoGen, LangGraph) into pure, understandable Python.

For practical decision trees on selecting architecture patterns, visit [Architectural Decisions](../decisions/) and the [Feature Directory](../decisions/04_bands_and_features.md).

