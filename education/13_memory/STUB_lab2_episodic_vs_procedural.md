# Stub: episodic vs procedural memory

Chapter 01 names four stores and splits long-term facts (episodic) from how-to text (procedural). This folder has no lab for that split. Lab 3 indexes sanitized document strings. It does not write a fact row or load a `SKILL.md`. A reader is told the session file is not long-term memory, then they land on RAG. The missing lab is: write one `{ "key", "value" }` fact, start a new list, inject the fact, keep job instructions in the system `content`.

A real lab 2 would cover:
- A script such as `lab2_episodic_vs_procedural.py` next to this file
- A facts file or a SQLite table of rows `{ "key": "string", "value": "string" }`
- INSERT one fact in "session A" (for example `preferred_name` / `Ada`)
- A new `messages` list for "session B" that SELECTs that row and prepends it
- A system message whose `content` is the job instructions (procedural). Do not INSERT that string as a fact
- POST the injected list to `{OLLAMA_HOST}/api/generate` (defaults `http://192.168.1.29:11434`, `qwen3.6:35b-a3b-65k`) and print `response`
- Print the fact row and the system `content` as two separate objects so the stores stay visible

Do not add a vector store, PII tokens, a sliding window, or a repo walk. Those are lab 3, lab 1, and lab 4. This stub is not a full lab. Do not treat it as steps to run.
