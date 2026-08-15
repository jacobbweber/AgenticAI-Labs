# AgenticAI-Labs — AI IDE instructions

Open this repository at the repo root in Cursor, Claude Code, Antigravity, or any AI IDE that reads `AGENTS.md`.

This is a learn-by-building course. The markdown is the course. The Python is the work.

## Pairing

Each chapter folder under `education/` has:

| File | Who writes it | Role |
|---|---|
| `NN_*.md` (the module) | Course author | The concept. Read first. |
| `labN_*.md` | Course author | The brief. This is the whole assignment. |
| `labN_*.py` | Learner or AI, during the session | The artifact. Proof the chapter is done. |

If a `.py` is already on disk, treat it as a reference solution. Ask the user whether to read it, rewrite it with them, or delete it and start from the brief.

Do not invent extra labs. Do not skip to a later chapter. The `labN_*.md` in the current folder is the only assignment.

## How a session works

1. User names a chapter, or you start at the lowest numbered chapter that has no `.py` yet.
2. Read the module `.md` with the user. Stay on When, Why, the data contract, and Related.
3. Read the lab `.md`. Implement only what it asks for.
4. Write or rewrite `labN_*.py` next to that brief. Keep it 30–50 lines. If it wants to grow, stop and split the brief.
5. Run it. Put real output and questions under **Notes** in the lab `.md`.
6. Stop. The next chapter is a new session.

## Start from scratch

Delete the `labN_*.py` files. Leave every `.md`. That is a full reset.

```text
# PowerShell, from the repo root
Get-ChildItem -Path education -Recurse -Filter lab*.py | Remove-Item
```

Do not delete modules, lab briefs, or `education/templates/`.

## What you must not do

- Do not update `README.md` after a lab.
- Do not maintain a global lab tracker or roadmap file as part of normal work. The chapter folders are the path. A `.py` on disk is progress.
- Do not add "Btw" asides. **The When and Why** is a header in the template.
- Do not use metaphors. Name the file, the port, the JSON key, the function.
- Do not pull in LangGraph, MCP, FastAPI, or a second model until the current brief says so.
- Do not open a second instruction file. This file and `education/PATH.md` are the whole map.

## Templates

New modules and lab briefs copy the headers in:

- `education/templates/MODULE.md`
- `education/templates/LAB.md`

Required headers: Data, Information, Knowledge, Wisdom, The When and Why, How it works, Data contract, Lab or Run, Related, Notes.

Related is 1–2 sentences per sibling tool (example: Ollama, LM Studio, vLLM). If there are no siblings, omit the header.

## Environment

When a lab talks to a model, default to the local provider unless the user says otherwise.

- Host: `OLLAMA_HOST` or `http://192.168.1.29:11434`
- Model: `OLLAMA_MODEL` or `qwen3.6:35b-a3b-65k`
- Read those from the environment in every script. Do not hardcode the URL in new labs.

## Intent to code

If the user describes a feature in plain English, stay inside the current chapter. Map it to the lab brief. If they need a different chapter, point at `education/PATH.md` and stop. Do not assemble a full harness until chapter 15.
