# Stub: graph workflow with a named edge

Page 01 (`01_graph_workflows.md`) is a separate idea from the DAG: a state dict can loop because an edge function returns the next node name (`"refactor"` or `"finish"`). This folder has lab 1 (one-pass DAG) and lab 3 (async queue) and no lab 2. A reader who just learned that a DAG cannot go back has no script that returns a node name. Chapter 05 `lab2_state_checkpointer.py` has the same draft/test/refactor loop, but the branch is a `while` plus `if`, not an edge function, and the lesson there is SQLite.

A real lab 2 would cover:
- A script such as `lab2_graph_workflow.py` next to this file
- Nodes `draft`, `run_tests`, `refactor` as `dict -> dict` on keys `code`, `attempts`, `test_passed`
- One edge function that returns a string node name after `run_tests`
- A runner that calls the named node until the edge returns `"finish"` or `attempts` hits `max_retries`
- Print each node name and the edge return so the cycle is visible
- No SQLite, no HTTP, no queue, no Temporal

Do not add a checkpointer class, a human-approval gate, or time-travel forks. Those are chapter 05 and later pages. This stub is not a full lab. Do not treat it as steps to run.
