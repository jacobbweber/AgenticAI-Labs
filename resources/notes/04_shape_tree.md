# The shape tree

Same walk as [decisions 01](../decisions/01_when_x_vs_y.md). Each leaf has two names: the word you hear, then the course object. If this page disagrees with the form, the form wins. If the form disagrees with a lab brief, the brief wins.

Read after [00_words.md](./00_words.md).

## The tree

```mermaid
flowchart TD
    classDef startNode fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000
    classDef question fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
    classDef tool fill:#eceff1,stroke:#455a64,stroke-width:2px,color:#000
    classDef agent fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000
    classDef subagent fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000

    notes04_task(["New task"]):::startNode --> notes04_q1

    notes04_q1{"1. Does this need a model?"}:::question
    notes04_q1 -- "NO (predictable)" --> notes04_tool["TOOL<br/>chapter 03 function"]:::tool
    notes04_q1 -- "YES" --> notes04_q2

    notes04_q2{"2. Must it run on its own schedule<br/>or outlive this chat?"}:::question
    notes04_q2 -- "YES" --> notes04_ind["INDEPENDENT AGENT<br/>job row + own session"]:::agent
    notes04_q2 -- "NO (this chat)" --> notes04_q3

    notes04_q3{"3. Will trial-and-error<br/>wreck this messages list?"}:::question
    notes04_q3 -- "YES (messy, like coding)" --> notes04_sub["EPHEMERAL SUBAGENT<br/>isolated loop that dies after"]:::subagent
    notes04_q3 -- "NO (clean)" --> notes04_loop["MAIN LOOP<br/>this process, add tools"]:::agent

    notes04_ind -.-> notes04_q4
    notes04_sub -.-> notes04_q4
    notes04_loop -.-> notes04_q4

    notes04_q4{"4. Need domain rules in a file?"}:::question
    notes04_q4 -- "YES" --> notes04_skill["SKILL<br/>SKILL.md on a trigger"]:::tool
    notes04_q4 -- "NO" --> notes04_done(["Done"])
```

## The leaves

| Word you hear | Course object |
|---|---|
| Tool | A function in `TOOL_REGISTRY`. [03](../../education/03_the_dispatcher/00_tool_dispatch.md) |
| Independent agent | A [18](../../education/18_the_job/00_the_job.md) job row plus its own session file ([13](../../education/13_one_agent/00_persona_tools_loop_state.md)). "Own queue" is `jobs.json`. Not a person. |
| Ephemeral subagent | An [14 wrapper](../../education/14_two_agents/03_skill_vs_two_agents.md): a child loop that returns one JSON and dies. Parent blocks. |
| Main loop | This [04](../../education/04_the_loop/00_the_react_loop.md) / [13](../../education/13_one_agent/00_persona_tools_loop_state.md) process. Add tools. |
| Skill | A [`SKILL.md`](../../education/15_mcp_and_skills/lab2_skills.md) loaded when a trigger matches. Still not a loop. |

## Not on this tree

Blast radius (Q5), park (Q7), and which host runs the loop (Q8) stay on [the form](../decisions/01_when_x_vs_y.md). Fill those after you pick a leaf.

More trees like this belong in this folder when a word still floats. Do not add one to a chapter unless that chapter already decides the split.
