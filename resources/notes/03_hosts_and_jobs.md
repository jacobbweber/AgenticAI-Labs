# Hosts and jobs

How the pieces sit on machines, using only existing objects.

- **core:** [jobs.json](../../education/16_the_job/00_the_job.md) (16), [check_budget](../../education/17_the_budget/00_the_budget.md) (17), [park/resume](../../education/18_park_and_resume/00_park_and_resume.md) (18), host map, `ask_host` / `ssh_net` tools.
- **jarvis process:** [chapter 07](../../education/07_one_agent/00_persona_tools_loop_state.md) kernel, claims jobs with `claimed_by` `"jarvis"` ([16 lab2](../../education/16_the_job/lab2_two_workers.md)) or accepts a handoff ([08](../../education/08_two_agents/01_handoff_protocol.md)). Own `messages` list. Own tool allowlist ([09](../../education/09_the_shield/lab3_agent_rbac.md) `ROLE_TOOL_PERMISSIONS`).
- **nimo:** same, `claimed_by` `"nimo"`.
- **net:** tool on core, or its own loop if it must stay up. SSH is the tool body, not an agent name.

A job row can carry `host_id` so a worker only claims matching rows. That is a field on the [chapter 16](../../education/16_the_job/00_the_job.md) object, not a new store.

Do not add a department class. Do not add a staff class. Do not add LangGraph.
