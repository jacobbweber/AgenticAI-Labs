# Hosts and jobs

How the pieces sit on machines, using only existing objects.

- **core:** [jobs.json](../../education/18_the_job/00_the_job.md) (18), [check_budget](../../education/05_the_budget/00_the_budget.md) (05), [park/resume](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md) (17), host map, `ask_host` / `ssh_net` tools.
- **jarvis process:** [chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md) kernel, claims jobs with `claimed_by` `"jarvis"` ([18 lab2](../../education/18_the_job/lab2_two_workers.md)) or accepts a handoff ([14](../../education/14_two_agents/01_handoff_protocol.md)). Own `messages` list. Own tool allowlist ([16](../../education/16_the_shield/lab3_agent_rbac.md) `ROLE_TOOL_PERMISSIONS`).
- **nimo:** same, `claimed_by` `"nimo"`.
- **net:** tool on core, or its own loop if it must stay up. SSH is the tool body, not an agent name.

A job row can carry `host_id` so a worker only claims matching rows. That is a field on the [chapter 18](../../education/18_the_job/00_the_job.md) object, not a new store.

Do not add a department class. Do not add a staff class. Do not add LangGraph.
