# Path canvas

One flowchart of the course. Not an enterprise product canvas. Objects below are files, JSON keys, and functions already in the labs.

```mermaid
flowchart TD
    subgraph dec02_call [Script and call]
        dec02_00["00 script"]
        dec02_01["01 query_llm"]
        dec02_02["02 messages"]
    end
    subgraph dec02_loop [Loop and tools]
        dec02_03["03 dispatcher"]
        dec02_04["04 while loop"]
        dec02_07["07 kernel"]
    end
    subgraph dec02_state [State and memory]
        dec02_05["05 messages.json"]
        dec02_13["13 facts and files"]
    end
    subgraph dec02_graph [Graph]
        dec02_06["06 dict through functions"]
    end
    subgraph dec02_split [Split work]
        dec02_08w["08 wrapper"]
        dec02_08h["08 handoff five keys"]
        dec02_16["16 jobs.json"]
    end
    subgraph dec02_shield [Shield]
        dec02_09["09 evaluate_action"]
        dec02_17["17 budget"]
        dec02_18["18 park_job"]
    end
    subgraph dec02_door [Front door]
        dec02_10["10 EventSource"]
    end
    subgraph dec02_prov [Provider]
        dec02_11["11 provider"]
        dec02_w["weights"]
    end
    subgraph dec02_rel [Reliability]
        dec02_12["12 cycle / CoT / evals"]
    end
    subgraph dec02_else [Dispatcher elsewhere]
        dec02_14["14 SKILL.md / MCP"]
    end
    dec02_10 -->|"POST prompt or EventSource token"| dec02_07
    dec02_00 -->|"POST /api/chat"| dec02_11
    dec02_01 -->|"POST /api/chat"| dec02_11
    dec02_07 -->|"POST /api/chat"| dec02_11
    dec02_11 -->|"matrix math"| dec02_w
    dec02_11 -->|"JSON with tool_calls"| dec02_03
    dec02_02 -->|"messages"| dec02_04
    dec02_03 -->|"role tool"| dec02_04
    dec02_04 --> dec02_07
    dec02_07 -->|"messages"| dec02_05
    dec02_07 --> dec02_13
    dec02_07 -->|"ask_host wrapper"| dec02_08w
    dec02_08w -->|"handoff five keys"| dec02_08h
    dec02_08w -->|"jobs.json status"| dec02_16
    dec02_16 -->|"claimed_by"| dec02_04
    dec02_07 --> dec02_09
    dec02_09 -->|"needs_hitl now"| dec02_09
    dec02_09 -->|"needs_hitl later"| dec02_18
    dec02_07 --> dec02_17
    dec02_07 --> dec02_12
    dec02_07 -->|"load SKILL.md"| dec02_14
    dec02_06 -->|"no model required"| dec02_06
```

HITL is evaluate_action ([09](../../education/09_the_shield/01_security_overview.md) `lookup_permission` / `execute_action_with_hitl_gate`) or `park_job` ([18](../../education/18_park_and_resume/00_park_and_resume.md)). Do not invent a product name for the pause.

Chapter files for the boxes: [00](../../education/00_atoms/00_script_provider_weights.md), [01](../../education/01_the_call/00_the_wrapper_and_the_stream.md), [02](../../education/02_the_contract/00_messages_and_json.md), [03](../../education/03_the_dispatcher/00_tool_dispatch.md), [04](../../education/04_the_loop/00_the_react_loop.md), [05](../../education/05_the_state/00_save_the_messages.md), [06](../../education/06_the_workflow/01_graph_workflows.md), [07](../../education/07_one_agent/00_persona_tools_loop_state.md), [08 wrapper](../../education/08_two_agents/03_skill_vs_two_agents.md), [08 handoff](../../education/08_two_agents/01_handoff_protocol.md), [09](../../education/09_the_shield/01_security_overview.md), [10](../../education/10_the_front_door/00_fastapi_sse.md), [11](../../education/11_engine_room/00_local_servers.md), [12](../../education/12_reliability/01_cycle_and_steering.md), [13](../../education/13_memory/01_agentic_memory.md), [14](../../education/14_mcp/00_mcp_overview.md), [16](../../education/16_the_job/00_the_job.md), [17](../../education/17_the_budget/00_the_budget.md), [18](../../education/18_park_and_resume/00_park_and_resume.md).

## Guided walk: "any alerts on jarvis?"

One request.

1. The [chapter 10](../../education/10_the_front_door/00_fastapi_sse.md) client POSTs the prompt (or you type into the [07](../../education/07_one_agent/00_persona_tools_loop_state.md) kernel).
2. The core loop ([07](../../education/07_one_agent/00_persona_tools_loop_state.md)) may load a `SKILL.md` ([14 lab2](../../education/14_mcp/lab2_skills.md)) that says: when the user names a host, call `ask_host`.
3. `ask_host` is an [08](../../education/08_two_agents/03_skill_vs_two_agents.md) wrapper: enqueue a job with `host_id` `jarvis` ([16](../../education/16_the_job/00_the_job.md)) or send handoff JSON ([08 01](../../education/08_two_agents/01_handoff_protocol.md)). `jarvis` is a `host_id` ([notes 01](../notes/01_where_not_who.md), [notes 02](../notes/02_one_router.md)).
4. The jarvis worker claims the row (`claimed_by` in [16 lab2](../../education/16_the_job/lab2_two_workers.md)), runs its own [04](../../education/04_the_loop/00_the_react_loop.md) loop, own tools (read logs). The [09](../../education/09_the_shield/lab3_agent_rbac.md) allowlist is read-only.
5. Result JSON returns. Core `messages` get one `role: tool` result ([03](../../education/03_the_dispatcher/00_tool_dispatch.md)), not jarvis trial tokens.
6. If a mutative fix is next, [09](../../education/09_the_shield/lab4_hitl_generative_ui.md) or [18](../../education/18_park_and_resume/00_park_and_resume.md), not a silent root command.
7. The provider ([11](../../education/11_engine_room/00_local_servers.md)) is only the POST for tokens. Weights do not run Ansible. See [00](./00_script_server_weights.md).

Fill [01_when_x_vs_y.md](./01_when_x_vs_y.md) before you add a second process.

## Outside chats vs this course

If a canvas requires Redis, OpenTelemetry, or Docker to exist, it is a product sketch. Those products are optional and not in this course. The labs already have the objects. Add those products only when a lab object is not enough ([08](../../education/08_two_agents/03_skill_vs_two_agents.md) wisdom: no bus until a wrapper fails).
