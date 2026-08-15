# 05: The State

After this chapter you can save and load the message list (or a state dict) so a restart does not start from zero. JSON first, then SQLite. This chapter does not POST to the model.

## Data
Chapter 04 keeps `messages` in a Python list. When the process exits, that list is gone. This chapter adds a file (or a SQLite row) that holds the same data.

**In-memory state** is a JSON-serializable `dict` or the `messages` list. JSON-serializable means `json.dumps` can encode it: strings, numbers, booleans, lists, and dicts. No live function objects.

A **JSON file** is the first form. `json.dump(state, f)` writes the dict. `json.load(f)` reads it back. One process, one file, no SQL.

A **checkpoint** is one saved snapshot. The lab stores checkpoints in SQLite. The file is `checkpoints.db` next to `lab2_state_checkpointer.py` (or the path in `CHECKPOINT_DB`). The table is `checkpoints` with columns `thread_id`, `step_name`, `checkpoint_id`, `state_data`, `timestamp`.

A **thread_id** is a string that names one run, such as `task_session_101`. Several rows can share a thread. Load returns the newest row for that id.

The functions are `save_checkpoint(thread_id, step_name, state)` (INSERT after `json.dumps`) and `load_latest_checkpoint(thread_id)` (SELECT latest, then `json.loads`). `init_sqlite_checkpointer` creates the table if it is missing.

The lab state keys are `code` (string), `attempts` (int), and `test_passed` (bool). Compaction (sliding window, summarization, AST prune) and vector long-term memory are chapter 13.

## Information
Working memory is the payload you would send this turn: the `messages` list, or a dict the next node will read. A checkpointer writes that payload to disk after a step. On resume you load by `thread_id` and continue from that dict.

Without a write, a crash drops the conversation. You re-run from the first message. The write is the new fact. The model is not involved. `lab2_state_checkpointer.py` never opens port `11434`.

JSON is enough to prove save and load. SQLite is the same bytes in a table so you can keep more than one snapshot and pick the latest by `checkpoint_id`.

## Knowledge
1. Keep state as a JSON-serializable dict. The lab starts with `{ "code": "", "attempts": 0, "test_passed": false }`.
2. After each step, call `save_checkpoint`. It runs `json.dumps(state)` and INSERTs `thread_id`, `step_name`, `state_data`, and `time.time()`.
3. On resume, call `load_latest_checkpoint(thread_id)`. It SELECTs `step_name, state_data` for that thread, `ORDER BY checkpoint_id DESC LIMIT 1`, then `json.loads`.
4. If you are not using SQL yet, `json.dump` / `json.load` on one file is the same contract with one snapshot.
5. Do not build a 4-tier memory taxonomy or a vector store here.

## Wisdom
A JSON file is enough for one process. SQLite is enough for pause and resume on one machine. Postgres or Redis checkpointers are the same INSERT/SELECT on a server. Compaction and RAG are chapter 13. If you add a vector store now, you will not know whether a bad resume came from the checkpoint row or from retrieval.

## The When and Why
- **When:** a task has more than one step and the process might stop.
- **Why:** without a checkpoint, you re-run from the first message. The save is how the next process sees the last dict.

## How it works

```mermaid
flowchart TD
    subgraph state_script [lab2_state_checkpointer.py]
        ST["state dict"]
        SAVE["save_checkpoint"]
        LOAD["load_latest_checkpoint"]
    end
    subgraph state_file [checkpoints.db]
        TBL["table checkpoints"]
    end
    ST -->|"json.dumps INSERT"| SAVE
    SAVE --> TBL
    TBL -->|"SELECT latest"| LOAD
    LOAD -->|"json.loads"| ST
```

Walkthrough of the lab thread `task_session_101`:

1. `init_sqlite_checkpointer` creates `checkpoints` if the table is missing.
2. `node_draft_code` sets `code` to a one-line `calculate_total`. `save_checkpoint` writes step `draft_code`.
3. `node_run_tests` sets `attempts` to 1 and `test_passed` to false. The script prints `[FAIL]`. Step `run_tests_attempt_1` is saved.
4. `node_refactor_code` replaces `code` with a version that checks `price < 0`. Step `refactor_attempt_1` is saved.
5. `node_run_tests` sets `attempts` to 2 and `test_passed` to true. The script prints `[PASS]`. Step `run_tests_attempt_2` is saved.
6. After the run, `load_latest_checkpoint("task_session_101")` SELECTs that last row and prints `Restored Code` plus the refactored function.

Nothing in that walkthrough calls Ollama. The nodes are ordinary Python functions. The new behavior is the INSERT and the SELECT.

## Data contract

**Table**

```sql
CREATE TABLE checkpoints (
    thread_id TEXT,
    step_name TEXT,
    checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_data TEXT,
    timestamp REAL
)
```

**state_data example** (what `json.dumps` writes into the TEXT column)

```json
{ "code": "string", "attempts": 0, "test_passed": false }
```

**save** INSERTs `thread_id`, `step_name`, `state_data`, `timestamp`. SQLite fills `checkpoint_id`.

**load** SELECTs `step_name, state_data WHERE thread_id = ? ORDER BY checkpoint_id DESC LIMIT 1`.

**JSON-file form** (no lab script in this folder yet): one object on disk, same keys, `json.dump` / `json.load`.

## Lab
Done when a reload prints the last saved `code`.

- Module: [this file](./00_save_the_messages.md)
- Lab 1 (missing): save and load `messages` as a JSON file. See [STUB_lab1_save_json.md](./STUB_lab1_save_json.md) after it is added.
- Lab 2: [lab2_state_checkpointer.py](./lab2_state_checkpointer.py) / [lab2_state_checkpointer.md](./lab2_state_checkpointer.md) — SQLite INSERT/SELECT. Done when `load_latest_checkpoint` prints the refactored `code`.

## Related
- **JSON file:** `json.dump` / `json.load` if you do not need more than one snapshot.
- **LangGraph checkpointer:** same INSERT/SELECT behind a framework class.
- **SQLite:** one file, no server. What the lab uses.

## Notes
- Windows console: use `[FAIL]` / `[PASS]` instead of emoji (cp1252).
- `checkpoints.db` sits next to the script and is gitignored. Override the path with `CHECKPOINT_DB`.
- The lab does not send `OLLAMA_HOST` or `OLLAMA_MODEL`. There is no HTTP call.
