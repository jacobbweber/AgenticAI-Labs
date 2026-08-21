# The Architecture Shape Tree: Mapping Concepts to Code

This visual decision tree maps common industry terms directly to the concrete building blocks you create in this course.

Use this tree alongside [Architectural Decisions: When X vs Y](../decisions/01_when_x_vs_y.md) whenever you start designing a new capability.

---

## The Decision Tree

```mermaid
flowchart TD
    classDef startNode fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#000
    classDef question fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000
    classDef tool fill:#eceff1,stroke:#455a64,stroke-width:2px,color:#000
    classDef agent fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#000
    classDef subagent fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000

    notes04_task(["New Task"]):::startNode --> notes04_q1

    notes04_q1{"1. Does this step require an AI model?"}:::question
    notes04_q1 -- "No (Deterministic Logic)" --> notes04_tool["STANDARD TOOL<br/>Python function in Chapter 03"]:::tool
    notes04_q1 -- "Yes" --> notes04_q2

    notes04_q2{"2. Must it run on a schedule<br/>or outlive this chat?"}:::question
    notes04_q2 -- "Yes" --> notes04_ind["INDEPENDENT AGENT / WORKER<br/>Background job row in Chapter 18"]:::agent
    notes04_q2 -- "No (Current Interactive Chat)" --> notes04_q3

    notes04_q3{"3. Would trial-and-error<br/>clutter the main messages list?"}:::question
    notes04_q3 -- "Yes (e.g. Iterative Coding)" --> notes04_sub["EPHEMERAL SUBAGENT<br/>Isolated skill wrapper in Chapter 14"]:::subagent
    notes04_q3 -- "No (Clean Discussion)" --> notes04_loop["MAIN AGENT LOOP<br/>Single ReAct process in Chapter 04 / 13"]:::agent

    notes04_ind -.-> notes04_q4
    notes04_sub -.-> notes04_q4
    notes04_loop -.-> notes04_q4

    notes04_q4{"4. Does it need written domain guidelines?"}:::question
    notes04_q4 -- "Yes" --> notes04_skill["SKILL DOCUMENT<br/>Load SKILL.md on trigger"]:::tool
    notes04_q4 -- "No" --> notes04_done(["Ready to Build"]):::startNode
```

---

## Glossary of Architectural Leaves

| Term You Hear | Concrete Course Implementation |
|---|---|
| **Standard Tool** | A callable Python function registered in `TOOL_REGISTRY` and described in `TOOLS_SCHEMA` ([Chapter 03](../../education/03_the_dispatcher/00_tool_dispatch.md)). |
| **Independent Agent / Worker** | A background worker process that claims records from `jobs.json` ([Chapter 18](../../education/18_the_job/00_the_job.md)) and manages its own session state ([Chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md)). |
| **Ephemeral Subagent** | A skill wrapper function ([Chapter 14](../../education/14_two_agents/03_skill_vs_two_agents.md)) that spins up a temporary child reasoning loop to complete a subtask and returns a single JSON result. |
| **Main Agent Loop** | The primary interactive ReAct control loop executing in your current process ([Chapter 04](../../education/04_the_loop/00_the_react_loop.md) and [Chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md)). |
| **Skill** | A structured instruction file ([`SKILL.md`](../../education/15_mcp_and_skills/lab2_skills.md)) loaded dynamically into the model's context when needed. |

---

## Additional Considerations

Once you have selected the structural leaf for your task, review [When X vs Y](../decisions/01_when_x_vs_y.md) to determine:
- Permission allowlists and RBAC security policies (Question 5).
- Human-In-The-Loop approval gates (Question 7).
- Target host locations and uptime requirements (Question 8).

