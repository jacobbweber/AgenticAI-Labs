# One router

You talk to one process. That process is the [chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md) kernel plus [chapter 14](../../education/14_two_agents/00_topologies.md) routing plus [chapter 19](../../education/19_the_front_door/00_fastapi_sse.md) as the front door.

User says: "any alerts on jarvis?"
Router does not SSH itself unless that is a local tool. It calls a tool, for example `ask_host(host_id, prompt)`.

`ask_host` is a skill wrapper ([14](../../education/14_two_agents/03_skill_vs_two_agents.md)): it builds the five-key handoff ([01_handoff_protocol.md](../../education/14_two_agents/01_handoff_protocol.md)) or a job row in [18](../../education/18_the_job/00_the_job.md) and waits for one JSON result. The model on core never needs the child tokens.

When to use a skill wrapper vs two live loops, quote the [14 rule](../../education/14_two_agents/03_skill_vs_two_agents.md):

- If the child can finish alone, wrap it as a tool.
- If you need mid-run inspection, two agents.
- If many pending rows, [chapter 18 lab2](../../education/18_the_job/lab2_two_workers.md) workers.

SSH network admin on the same server as the router: that is a tool ([03](../../education/03_the_dispatcher/00_tool_dispatch.md)) with [chapter 17 HITL](../../education/17_hitl_and_park_resume/lab1_hitl_approval.md) for mutative commands, or [chapter 17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) park if the yes comes later. It is not a "network person." Same host as core is fine (`same_host_as` in the map).

```mermaid
flowchart LR
    notes02_user["user"]
    notes02_door["front door"]
    notes02_core["core router"]
    notes02_ask["ask_host tool"]
    notes02_jarvis["jarvis worker"]
    notes02_user --> notes02_door
    notes02_door --> notes02_core
    notes02_core --> notes02_ask
    notes02_ask --> notes02_jarvis
```

The jarvis worker has its own loop, its own `messages` list, and its own tools.
