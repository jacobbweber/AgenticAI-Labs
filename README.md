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

## The 20-Stage Progressive Hierarchy (7 Tiers)

The curriculum is organized into a 20-stage cognitive progression across 7 tiers, taking you from raw network calls to full multi-agent enterprise synthesis:

1. **Tier 1: The Wire & Protocol** (`00_atoms`, `01_the_call`, `02_the_contract`)
2. **Tier 2: The Core Loop & Kernel** (`03_the_dispatcher`, `04_the_loop`, `05_the_budget`, `06_the_reliability`)
3. **Tier 3: Persistence & Memory** (`07_the_state`, `08_context_compaction`, `09_agentic_memory_and_rag`)
4. **Tier 4: Control Flows & Reasoning** (`10_the_workflow`, `11_planning_and_reflection`, `12_agent_evals`)
5. **Tier 5: Coordination & Protocols** (`13_one_agent`, `14_two_agents`, `15_mcp_and_skills`)
6. **Tier 6: Security, Governance & Production Runtime** (`16_the_shield`, `17_hitl_and_park_resume`, `18_the_job`, `19_the_front_door`)
7. **Tier 7: Full System Synthesis** (`20_synthesis`)

Auxiliary Training Path: [`optional_training/`](./education/optional_training/) (Pretraining, LoRA/QLoRA fine-tune, GGUF quantization, GRPO preference alignment).

For full navigation, see [`education/PATH.md`](./education/PATH.md).

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
  PATH.md                 # 20-stage progressive hierarchy across 7 tiers
  00_atoms/ ... 20_synthesis/ # 21 numbered chapters
  optional_training/      # LoRA / GGUF / GRPO, auxiliary training path
resources/
  term_glossary.md        # architectural terminology & Rosetta Stone
  notes/                  # deep conceptual notes 00-12 (pedagogical models)
  decisions/              # architectural decision guides (when X vs Y)
  templates/              # MODULE.md and LAB.md templates
demos/
  blogger_agent/          # end-to-end multi-stage blogging agent
  ciscoengineeragent/     # multi-agent networking demo
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
