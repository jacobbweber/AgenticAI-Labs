# Distributing Tasks Across Hosts with Background Jobs

In a distributed environment with multiple computers, you can coordinate tasks cleanly using standard job records in `jobs.json` without needing complex orchestration frameworks.

Here is how responsibilities are divided across machines:

- **Central Server (`core`)**:
  - Maintains the primary task queue in `jobs.json` ([Chapter 18](../../education/18_the_job/00_the_job.md)).
  - Enforces cost and execution limits using `check_budget` ([Chapter 05](../../education/05_the_budget/00_the_budget.md)).
  - Handles approval gates and parked states ([Chapter 17](../../education/17_hitl_and_park_resume/00_hitl_and_park_resume.md)).
  - Exposes router tools like `ask_host` and `ssh_net`.
- **Target Host Worker (e.g., `jarvis`)**:
  - Runs a standalone agent kernel ([Chapter 13](../../education/13_one_agent/00_persona_tools_loop_state.md)).
  - Claims jobs where `claimed_by` or `host_id` matches `"jarvis"` ([Chapter 18 Lab 2](../../education/18_the_job/lab2_two_workers.md)), or accepts handoffs ([Chapter 14](../../education/14_two_agents/01_handoff_protocol.md)).
  - Maintains its own local `messages` history and restricted tool allowlist ([Chapter 16 Lab 3](../../education/16_the_shield/lab3_agent_rbac.md)).
- **Secondary Host Worker (e.g., `nimo`)**:
  - Follows the identical worker pattern, claiming rows where `claimed_by == "nimo"`.
- **Network / Appliance Host (`net`)**:
  - Executes SSH tools directly from `core` or runs its own lightweight loop if it needs dedicated uptime.

By attaching a simple `host_id` field to each job row in `jobs.json`, workers automatically process the exact tasks intended for them without needing external message brokers or complex framework classes.

