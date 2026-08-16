# Script to Agent

Hands-on course for building AI agents from ordinary scripts. Open the repo root in an AI IDE (Cursor, Claude Code, Antigravity) and work one chapter at a time.

The markdown is the course. The Python is what you and the IDE write.

New here? Start at [`getting_started/`](./getting_started/). You can do these labs on a tiny laptop model. Answers will vary. The concepts do not.

## How to use it

1. Read [`getting_started/README.md`](./getting_started/README.md). Install Python, pick a model, start Ollama or set a cloud key.
2. Clone the repo (or download the ZIP). Open the repo root so the IDE reads `AGENTS.md`.
3. Start at `education/00_atoms/`.
4. Read the module `.md`. Then open the `labN_*.md` brief.
5. Write the `labN_*.py` with the IDE, or write it yourself and have the IDE check it.
6. Run the script. Put real output under **Notes** in the lab brief.
7. Go to the next numbered folder.

That is the whole workflow.

## Start from scratch

Delete the lab scripts. Keep the markdown.

```powershell
Get-ChildItem -Path education -Recurse -Filter lab*.py | Remove-Item
```

```bash
find education -name 'lab*.py' -delete
```

Existing `.py` files in the chapter folders are optional reference solutions.

## What lives where

```
AGENTS.md                 # rules for the AI IDE
README.md
getting_started/          # Python, models, Ollama, cloud keys, first run
education/
  PATH.md                 # the numbered path, plus "when you want X"
  00_atoms/ ... 18_park_and_resume/
  optional_training/      # LoRA / GGUF / GRPO, not on the main path
resources/
  term_glossary.md        # optional lookup
  notes/                   # jargon to lab objects (optional)
  templates/              # MODULE.md and LAB.md for new chapters
```

## Local model

Set these on your machine. The numbers below are course defaults, not a requirement.

- `OLLAMA_HOST` (your machine: `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` (example: `llama3.2:1b` on a small laptop)

See [`getting_started/01_pick_a_model.md`](./getting_started/01_pick_a_model.md).

## Share it

Clone and use as-is. To add a chapter, add a numbered folder and a row in `education/PATH.md`.
