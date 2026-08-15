# Stub: lab numbering in 15_synthesis

This folder has two files named lab2 (resilient executor, enterprise SQL agent) and three files named lab3 (spec TDD loop, autonomous SRE agent, enterprise harness app). They kept the `labN` prefix they had in the old tree (`modules/11`, `modules/09`, `modules/04`). The ideas are different. The numbers are not. This page is not a lab. There is no script to run.

Read them in this order:

- `00_harness_overview` then `lab2_resilient_executor` then `lab3_enterprise_harness_app` — snap hydrate, route, sandbox, cycle, HITL, trace.
- `01_project_blueprints` then `lab1_multi_agent_workbench` then `lab2_enterprise_sql_agent` then `lab3_autonomous_sre_agent` then `lab4_agent_serving_infra` — optional vertical slices.
- `02_spec_tdd` then `lab3_spec_tdd_loop` — spec, red, green.
- `03_self_evolution` — read only. No lab.

Why the numbers collide:

- Each file kept the name it had when it was moved in.
- This pass does not rename files, even when names collide.

What a later cleanup would do:

- Renumber only (for example lab2 resilient executor, lab3 enterprise harness app, lab4 workbench, lab5 SQL agent, lab6 SRE agent, lab7 spec TDD, lab8 serving infra).
- Not rewrite the ideas.
- Not edit the `.py` files unless a path string must change.
- Not edit `PATH.md` in this pass.

What not to add:

- Runnable steps, a new `.py` file, or another lab2 / lab3.
- A rename of the colliding files in this pass. The duplicate numbering stays until that later cleanup.
