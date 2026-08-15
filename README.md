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

That is the whole workflow.

## Start from scratch

Delete the lab scripts. Keep the markdown.

```powershell
Get-ChildItem -Path education -Recurse -Filter lab*.py | Remove-Item
```

Existing `.py` files in the chapter folders are optional reference solutions.

## What lives where

```
AGENTS.md                 # rules for the AI IDE
README.md
education/
  PATH.md                 # the numbered path, plus "when you want X"
  00_atoms/ ... 15_synthesis/
  optional_training/      # LoRA / GGUF / GRPO — not on the main path
resources/
  term_glossary.md        # optional lookup
  templates/              # MODULE.md and LAB.md for new chapters
```

## Local model

- `OLLAMA_HOST` (default `http://192.168.1.29:11434`)
- `OLLAMA_MODEL` (default `qwen3.6:35b-a3b-65k`)

## Share it

Clone and use as-is. To add a chapter, add a numbered folder and a row in `education/PATH.md`.
