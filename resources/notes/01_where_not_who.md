# System Architecture: Designing by Location (`host_id`), Not Personas

When building real-world automation systems, it is much more effective to organize tasks by *where* execution happens (target hosts and network ports) and *what* permissions are required, rather than assigning fictional job titles to agents.

Here is an example host configuration map (stored cleanly as JSON):

```json
{
  "jarvis": { "kind": "windows", "role": "desktop" },
  "nimo": { "kind": "linux", "role": "desktop" },
  "core": { "kind": "server", "role": "jobs_and_router" },
  "net": { "kind": "server", "role": "ssh_to_switches", "same_host_as": "core" }
}
```

In this architecture:
- `jarvis` and `nimo` are physical machine names (`host_id`), not fictional workers.
- Instead of saying *"ask the Windows specialist,"* your code calls an explicit tool like `ask_host(host_id="jarvis", prompt="Check active alerts")`.

---

## Organizing Memory and State

System state and memory should always be indexed by concrete identifiers rather than personal names:
- **`session_id`**: Identifies a specific interactive conversation ([Chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md), stored in `state_store/{session_id}.json`).
- **`thread_id`**: Identifies persistent database checkpoints ([Chapter 07](../../education/07_the_state/00_save_the_messages.md), stored in `checkpoints.db`).
- **`key` / `host_id`**: Identifies specific system facts or machine profiles ([Chapter 09](../../education/09_agentic_memory_and_rag/01_agentic_memory.md), stored in `facts.json`).

If you need to run two separate reasoning loops on a single server, structure them as a coordinator and a skill wrapper ([Chapter 14](../../education/14_two_agents/03_skill_vs_two_agents.md)) with clear security boundaries.

