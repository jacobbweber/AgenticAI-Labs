# Stub: save and load messages as JSON

Chapter 05 says JSON first, then SQLite, but this folder only has lab 2 (`lab2_state_checkpointer.py`), which writes a state dict to `checkpoints.db`. A reader coming from chapter 04 has a `messages` list in RAM and no file. They are told to persist that list, then they land on CREATE TABLE. The missing lab is the smaller step: write the list to a `.json` file and read it back.

A real lab 1 would cover:
- A script such as `lab1_save_json.py` next to this file
- `json.dump` of a `messages` list (or a small state dict) to a path beside the script, for example `messages.json`
- `json.load` of that same path in a second function or a second run
- Print the loaded `role` and `content` keys so you can see the list survived the process
- No SQLite, no `thread_id`, no HTTP, no compaction

Do not add a vector store, a sliding window, or a checkpointer class. Those are lab 2 and chapter 13. This stub is not a full lab. Do not treat it as steps to run.
