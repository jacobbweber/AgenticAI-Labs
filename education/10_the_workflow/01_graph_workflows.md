# 10: Graph workflows

After this page a state dict can loop: draft, then test, then refactor, then test again. Edges are functions that return the next node name. Checkpoints are chapter 07. This page does not require SQLite.

## Data
The last page was a DAG: arrows go forward only. This page adds a **back edge**. A back edge is an arrow from a later node to an earlier one. Draft to test is forward. Test to refactor to test is a cycle.

**Graph state** is a shared dict. The example keys are the same as chapter 07: `code` (string), `attempts` (int), `test_passed` (bool).

**Nodes** are functions `dict -> dict`. They update keys and return the dict. They do not choose the next node. Lab 2 names them `draft`, `run_tests`, and `refactor`.

A **conditional edge** is a function that reads the dict and returns a string node name, for example `"refactor"` or `"finish"`. Lab 2 calls this `edge_after_tests`. The runner `run_graph` calls that function after `run_tests` and jumps to the named node.

A **cycle** is allowed here. A DAG forbids it. Cap the loop with `max_retries` (chapter 07 uses 3) so `attempts` cannot grow forever.

The checkpointer script in chapter 07 (`lab2_state_checkpointer.py`) is this graph plus SQLite. This page is the edge and loop, not the INSERT.

## Information
A DAG has no back edge. A graph does. After `run_tests`, Python reads `test_passed` and `attempts`. If the test failed and retries remain, the next name is `refactor`. If the test passed or `attempts` hit the cap, the next name is `finish`.

LangGraph and XState are libraries around this same picture: a dict, node functions, and edge functions that return a name. Human-in-the-loop interrupts and time-travel forks are later chapters. Do not add them here.

The model is optional. The chapter 07 nodes never POST. A later graph can put a model call inside one node. The new idea on this page is the named edge, not the POST.

## Knowledge
1. Define nodes that update a dict (`draft`, `run_tests`, `refactor`).
2. After `run_tests`, call `edge_after_tests`. It returns a string: `"refactor"` or `"finish"`.
3. Loop in `run_graph` until the edge returns `"finish"` or `attempts` reaches `max_retries`. Print each node name and each edge return.
4. Optionally call `save_checkpoint` after each node (chapter 07). That is not required to understand the edge.
5. Do not add Temporal, Postgres locking, or a second process.

## Wisdom
A graph is for retry and repair. A DAG is for one-pass pipelines. If the steps never need to run again, stay on the last page. Temporal, Redis locks, and human approval gates are not this page. Adding them now hides whether the edge function or the lock is what broke the loop.

## The When and Why
- **When:** a step must run again after a failure (test, then refactor, then test).
- **Why:** an acyclic list cannot express that loop without a second script. The edge return value is how the runner knows to go back.

## How it works

```mermaid
flowchart TD
    subgraph graph_nodes [Node functions]
        DRAFT["draft"]
        TEST["run_tests"]
        REF["refactor"]
        DONE["finish"]
    end
    subgraph graph_edge [Conditional edge]
        EDGE["reads test_passed and attempts"]
    end
    DRAFT --> TEST
    TEST --> EDGE
    EDGE -->|"fail and retries left"| REF
    REF --> TEST
    EDGE -->|"pass or max retries"| DONE
```

Walkthrough of lab 2 (same dict as chapter 07, no SQLite):

1. `draft` writes a one-line `calculate_total` into `code` and sets `test_passed` to false.
2. `run_tests` increments `attempts`. On attempt 1 it sets `test_passed` false.
3. `edge_after_tests` reads those keys and returns `"refactor"`.
4. `refactor` replaces `code` with a version that checks `price < 0`.
5. `run_tests` runs again. Attempt 2 sets `test_passed` true.
6. The edge returns `"finish"`. `run_graph` stops.

The new control is the string the edge returns. The dict is the same object the whole time.

## Data contract

**State dict**

```json
{ "code": "string", "attempts": 0, "test_passed": false }
```

**Edge return:** a string node name, for example `"refactor"` or `"finish"`. Not a URL. Not a JSON object.

**Node signature:** `def node(state: dict) -> dict`.

## Lab
Done when the runner prints each node name and the edge return, then stops on `"finish"`.

- Module: [this file](./01_graph_workflows.md)
- Lab 2: [lab2_graph_workflow.md](./lab2_graph_workflow.md) — write `lab2_graph_workflow.py`. Nodes `draft`, `run_tests`, `refactor`. `edge_after_tests` returns `"refactor"` or `"finish"`. Done when the print shows the cycle then `"finish"`.
- Previous page: [00_deterministic_dags.md](./00_deterministic_dags.md) / [lab1_dag_pipeline.md](./lab1_dag_pipeline.md) (no back edge).
- Chapter 07 checkpointer: [../07_the_state/lab2_state_checkpointer.py](../07_the_state/lab2_state_checkpointer.py) is this graph plus SQLite. This page is the edge, not the INSERT.

## Related
- **State graph workflows:** nodes, reducers, checkpointers as classes. Same dict plus edge names.
- **XState:** same finite-state job in JavaScript.
- **Chapter 07 checkpointer:** this loop with an INSERT after each node.

## Notes
- There is no reference `lab2_graph_workflow.py` yet. Write it from the brief.
- HITL interrupts and time-travel forks are later. Do not add them here.
