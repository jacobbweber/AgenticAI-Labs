# Stub: load a skill file

Chapter 01 says a skill is a `SKILL.md` (or a helper script) loaded when a trigger matches, then appended to system or user `content`. This folder only has lab 1, which is a JSON-RPC brief with no file read. A reader is told not to merge skill and MCP, then they have nothing to run for the file path. The missing lab is: detect a trigger, read one markdown file, POST with that string in `content`.

A real lab 2 would cover:
- A script such as `lab2_skills.py` next to this file
- A `SKILL.md` in the same folder (a short markdown string, one workflow)
- A trigger (a keyword in the user text, or an explicit name)
- `open("SKILL.md").read()` only when the trigger matches
- Append the body to `role: "system"` `content` (or to the user message)
- POST to `{OLLAMA_HOST}/api/generate` or `/v1/chat/completions` (defaults `http://192.168.1.29:11434`, `qwen3.6:35b-a3b-65k`)
- Print the trigger, the path, and the first line of the body so the load is visible

Do not add `tools/list`, `tools/call`, a second model, or a 200-line MCP server. Those are lab 1 and chapter 03. This stub is not a full lab. Do not treat it as steps to run.
