# Stub: compact the context window

Chapter 00 teaches three compaction moves (window, summary, prune) so a long `messages` list still fits the next POST. This folder only has lab 3 (`lab3_local_private_rag.py`), which redacts strings and searches an in-memory store. A reader coming from chapter 05 has a saved list and no shrink step. They are told the list can overflow, then they land on RAG. The missing lab is the smaller step: count size, keep system + last N, POST the shorter list.

A real lab 1 would cover:
- A script such as `lab1_context_window.py` next to this file
- A long `messages` list in RAM (or loaded from a JSON file)
- A size check (`len(json.dumps(messages))` or a token count)
- Keep the first `role: "system"` item and the last N turns; drop the middle
- Optional: one summary POST of the dropped turns, insert one message in the gap
- Optional: slice a long tool `content` string to a character cap
- POST the smaller list to `{OLLAMA_HOST}/api/generate` (defaults `http://192.168.1.29:11434`, `qwen3.6:35b-a3b-65k`) and print `response`
- Print character counts before and after so the shrink is visible

Do not add a vector store, PII tokens, a fact table, or a repo walk. Those are lab 3 and the other stubs in this folder. This stub is not a full lab. Do not treat it as steps to run.
