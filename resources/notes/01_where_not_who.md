# Where, not who

The useful key is where or what, not who.

Example host map (JSON only, not a lab):

```json
{
  "jarvis": { "kind": "windows", "role": "desktop" },
  "nimo": { "kind": "linux", "role": "desktop" },
  "core": { "kind": "server", "role": "jobs_and_router" },
  "net": { "kind": "server", "role": "ssh_to_switches", "same_host_as": "core" }
}
```

`jarvis` and `nimo` are machine names (`host_id`), not staff. "Department" in marketing is this map. "Talk to the Windows intern" is the wrong sentence. "Ask jarvis for alerts" is a `host_id` on a tool call.

Memory is keyed by `host_id` or `session_id` ([chapters 05](../../education/05_the_state/00_save_the_messages.md), [07](../../education/07_one_agent/00_persona_tools_loop_state.md), [13](../../education/13_memory/01_agentic_memory.md)), not by a person name. The lab keys are `session_id` ([07](../../education/07_one_agent/00_persona_tools_loop_state.md) `state_store/{session_id}.json`), `thread_id` ([05](../../education/05_the_state/00_save_the_messages.md) `checkpoints.db`), and a fact `key` ([13](../../education/13_memory/01_agentic_memory.md) `facts.json`). If you keep a file per machine, use `host_id` from the map.

If two loops must stay up on one machine, that is still [chapter 08](../../education/08_two_agents/03_skill_vs_two_agents.md) (two agents or a skill wrapper), not two employees.
