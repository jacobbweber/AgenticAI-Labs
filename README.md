# AgenticAI-Labs

Hands-on course for building AI agents from ordinary scripts. Open the repo root in an AI IDE (Cursor, Claude Code, Antigravity) and work one chapter at a time.

The markdown is the course. The Python is what you and the IDE write.

## How to use it

1. Clone the repo. Open the repo root so the IDE reads `AGENTS.md`.
2. Start at `education/00_atoms/`.
3. Read the module `.md`. Then open the `labN_*.md` brief.
4. Write the `labN_*.py` with the IDE, or write it yourself and have the IDE check it.
5. Run the script. Put real output under **Notes** in the lab brief.
6. Go to the next numbered folder.

That is the whole workflow. There is no separate tracker to keep in sync.

## Start from scratch

Delete the lab scripts. Keep the markdown.

```powershell
Get-ChildItem -Path education -Recurse -Filter lab*.py | Remove-Item
```

Worked solutions, if present, live under `reference/` and are optional.

## What lives where

```
education/
  PATH.md             # numbered chapter list
  templates/          # MODULE.md and LAB.md — copy these headers
  00_atoms/           # first chapter
  01_the_call/        # then this, then the next number
  ...
  optional_training/  # LoRA, GGUF, GRPO — side folder, not on the path
demos/                # optional apps you build after the path
AGENTS.md             # rules for the AI IDE
```

The folder numbers are the path. If a folder is missing, it is not on the course yet.

## Local model

Labs default to a local Ollama server.

- `OLLAMA_HOST` (default `http://192.168.1.29:11434`)
- `OLLAMA_MODEL` (default `qwen3.6:35b-a3b-65k`)

Any OpenAI-compatible server works if you point those variables at it.

## Share it

This repo is meant to be cloned and used as-is. You should not need to edit the README, a roadmap, or a progress file to add a chapter. Add a numbered folder with a module, a lab brief, and (later) a script.
