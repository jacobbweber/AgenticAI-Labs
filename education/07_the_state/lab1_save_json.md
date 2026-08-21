# Lab 1: Persisting Messages to Flat JSON Files

In this lab, you will write helper functions `save_messages(messages)` and `load_messages()` to write conversational history to a local JSON file (`messages.json`) and reload it back into memory.

---

## What you touch
- Script to create: `lab1_save_json.py`
- Main Functions: `save_messages(messages)` and `load_messages()`
- Target File: `messages.json` located next to the script
- Data Structures: List of dictionary messages (`[{"role": str, "content": str}, ...]`)

---

## Steps
```mermaid
flowchart LR
    A["In-memory messages list"] -->|"save_messages() / json.dump"| B["messages.json on disk"]
    B -->|"load_messages() / json.load"| C["Restored Python messages list"]
```

1. Set the target file path using `os.path.join(os.path.dirname(__file__), "messages.json")`.
2. Implement `save_messages(messages: list)`:
   - Open `messages.json` in write mode (`"w"`).
   - Use `json.dump(messages, f, indent=2)` to save the list formatted for readability.
   - Print the saved file path.
3. Implement `load_messages() -> list`:
   - Check if `messages.json` exists. If not, return `[]`.
   - Open and read the file with `json.load(f)`.
   - Return the deserialized list.
4. In `__main__`:
   - Construct a test conversation containing `system`, `user`, and `assistant` messages.
   - Call `save_messages(messages)`.
   - Call `load_messages()` and iterate through the restored list, printing each message's `role` and `content`.
   - Verify that the restored data matches the original list exactly.

---

## Data contract

**File Structure: `messages.json`**

```json
[
  { "role": "system", "content": "You add numbers." },
  { "role": "user", "content": "What is 42 plus 58?" },
  { "role": "assistant", "content": "100" }
]
```

---

## Run
From the repository root, run your script:

```bash
python education/07_the_state/lab1_save_json.py
```

```powershell
python education/07_the_state/lab1_save_json.py
```

---

## What you should see
- The absolute file path of `messages.json` upon saving.
- Each message printed line-by-line (`system: You add numbers.`, `user: What is 42 plus 58?`, `assistant: 100`).

---

## Stop here
You now have basic file persistence! In Lab 2, we will create a structured SQLite state checkpointer for multi-step agent workflows.

Next up: [Lab 2: State Checkpointer](./lab2_state_checkpointer.md).

---

## Notes
*(Record your serialized file output here)*

