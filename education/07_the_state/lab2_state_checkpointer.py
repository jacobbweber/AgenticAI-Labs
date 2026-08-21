"""Reference solution: SQLite checkpoint save/load. Chapter 05."""
import json
import os
import sqlite3
import time

DB_PATH = os.environ.get(
    "CHECKPOINT_DB",
    os.path.join(os.path.dirname(__file__), "checkpoints.db"),
)

def init_sqlite_checkpointer():
    """Initializes SQLite database table for state snapshot persistence."""
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            thread_id TEXT,
            step_name TEXT,
            checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_data TEXT,
            timestamp REAL
        )
    """)
    conn.commit()
    conn.close()

def save_checkpoint(thread_id: str, step_name: str, state: dict):
    """Commits a JSON state snapshot to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO checkpoints (thread_id, step_name, state_data, timestamp) VALUES (?, ?, ?, ?)",
        (thread_id, step_name, json.dumps(state), time.time())
    )
    conn.commit()
    conn.close()
    print(f"  [CHECKPOINT SAVED] Thread '{thread_id}' | Step '{step_name}' committed to SQLite.")

def load_latest_checkpoint(thread_id: str) -> dict:
    """Loads the most recent state snapshot from SQLite for a given thread_id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT step_name, state_data FROM checkpoints WHERE thread_id = ? ORDER BY checkpoint_id DESC LIMIT 1",
        (thread_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        step_name, state_data = row
        print(f"  [CHECKPOINT LOADED] Resuming Thread '{thread_id}' from Step '{step_name}'.")
        return json.loads(state_data)
    return {}

def node_draft_code(state: dict) -> dict:
    print("\n[NODE: DRAFT CODE] Writing initial code implementation...")
    state["code"] = "def calculate_total(price, tax): return price + tax"
    state["test_passed"] = False
    return state

def node_run_tests(state: dict) -> dict:
    print("[NODE: RUN TESTS] Executing unit tests against code...")
    state["attempts"] = state.get("attempts", 0) + 1

    if state["attempts"] < 2:
        print("  [FAIL] Tests Failed: Missing parameter validation.")
        state["test_passed"] = False
    else:
        print("  [PASS] Tests Passed: Code meets requirements!")
        state["test_passed"] = True
    return state

def node_refactor_code(state: dict) -> dict:
    print("[NODE: REFACTOR CODE] Refactoring code based on test failure feedback...")
    state["code"] = "def calculate_total(price, tax):\n    if price < 0: raise ValueError()\n    return price + tax"
    return state

def run_stateful_graph(thread_id: str, max_retries: int = 3):
    print(f"=== STARTING STATEFUL GRAPH WORKFLOW (Thread: {thread_id}) ===")
    init_sqlite_checkpointer()

    state = {"code": "", "attempts": 0, "test_passed": False}
    state = node_draft_code(state)
    save_checkpoint(thread_id, "draft_code", state)

    while state["attempts"] < max_retries:
        state = node_run_tests(state)
        save_checkpoint(thread_id, f"run_tests_attempt_{state['attempts']}", state)

        if state["test_passed"]:
            print("\n[CONDITIONAL EDGE] Tests Passed! Transitioning to Publish Node.")
            break
        else:
            print("[CONDITIONAL EDGE] Tests Failed! Transitioning to Refactor Node (Looping Back).\n")
            state = node_refactor_code(state)
            save_checkpoint(thread_id, f"refactor_attempt_{state['attempts']}", state)

    print("\n=== FINAL PERSISTED WORKFLOW STATE ===")
    print(json.dumps(state, indent=2))
    return state

if __name__ == "__main__":
    thread = "task_session_101"
    run_stateful_graph(thread)

    print("\n--- FAULT-TOLERANCE DEMO: RESTORING FROM SQLITE CHECKPOINT ---")
    restored_state = load_latest_checkpoint(thread)
    print(f"Restored Code:\n{restored_state.get('code')}")
