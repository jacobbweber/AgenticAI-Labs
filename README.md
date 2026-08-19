# Script to Agent

Hands-on course for building AI agents from ordinary scripts. Open the repo root in an AI IDE (Cursor, Claude Code, Antigravity) and work one chapter at a time.

The markdown is the course. The Python is what you and the IDE write.

New here? Start at [`getting_started/`](./getting_started/). You can do these labs on a tiny laptop model. Answers will vary. The concepts do not.

## How to use it

1. Read [`getting_started/README.md`](./getting_started/README.md). Install Python, pick a model, start Ollama or set a cloud key.
2. Clone the repo (or download the ZIP). Open the repo root so the IDE reads `AGENTS.md`.
3. Copy the env template. Uncomment one provider and fill it in:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

4. Start at `education/00_atoms/`.
5. Read the module `.md`. Then open the `labN_*.md` brief.
6. Write the `labN_*.py` with the IDE, or write it yourself and have the IDE check it.
7. Run the script. Put real output under **Notes** in the lab brief.
8. Go to the next numbered folder.

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
.env.example              # copy to .env; do not commit .env
load_env.py               # stdlib loader used by the labs
getting_started/          # Python, models, Ollama, cloud keys, first run
education/
  PATH.md                 # the numbered path, plus "when you want X"
  00_atoms/ ... 18_park_and_resume/
  optional_training/      # LoRA / GGUF / GRPO, not on the main path
resources/
  term_glossary.md        # optional lookup
  notes/                   # jargon to lab objects (optional)
  decisions/              # when X vs Y (optional)
  templates/              # MODULE.md and LAB.md for new chapters
```

## Provider settings

Labs read the repo-root `.env` (see `.env.example`). Copy it, uncomment one block, fill the URL, key, and model.

Local Ollama defaults if those vars are unset:

- `OLLAMA_HOST` = `http://127.0.0.1:11434`
- `OLLAMA_MODEL` = `llama3.2:1b`

Do not commit `.env`. It can hold a key.

See [`getting_started/01_pick_a_model.md`](./getting_started/01_pick_a_model.md) and [`getting_started/03_cloud_apis.md`](./getting_started/03_cloud_apis.md).

## Share it

Clone and use as-is. To add a chapter, add a numbered folder and a row in `education/PATH.md`.
