# Script to Agent: Learn to Build AI Agents from First Principles

Welcome to **Script to Agent**! This is a hands-on, learn-by-building curriculum that guides you through creating robust AI agents starting from simple, standard Python scripts. 

Open this repository in your preferred AI IDE (such as Cursor, Claude Code, Antigravity, or VS Code) and work through one chapter at a time. The markdown files provide the concepts and assignments, while you and your assistant write and test the Python code.

If you are new to Python or local AI models, start with our [Getting Started Guide](./getting_started/). You can complete every lab using a small model on an everyday laptop!

---

## How a Learning Session Works

1. **Set Up Your Environment**: Follow [`getting_started/README.md`](./getting_started/README.md) to install Python, choose a model, and start Ollama or configure a cloud API key.
2. **Open the Repository**: Open the repository root folder in your IDE so that project instructions (`AGENTS.md`) are automatically recognized.
3. **Configure Your Settings**: Copy `.env.example` to `.env` and uncomment the settings for your chosen provider:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

4. **Navigate to Chapter 00**: Start at [`education/00_atoms/`](./education/00_atoms/).
5. **Read the Concept Module**: Read the module file (`00_*.md`) first to understand the *When*, the *Why*, and the data contract.
6. **Review the Lab Brief**: Open the lab brief (`labN_*.md`). This document is your complete assignment.
7. **Write and Test Your Code**: Write `labN_*.py` alongside the brief and run it from your terminal. Record real output or observations under the **Notes** section of the brief.
8. **Move Forward**: Once your script runs successfully, proceed to the next chapter!

---

## The 20-Stage Progressive Curriculum (7 Tiers)

The curriculum takes you on a structured progression from raw network sockets to autonomous enterprise systems:

1. **Tier 1: The Wire & Protocol** (`00_atoms`, `01_the_call`, `02_the_contract`): Making raw HTTP POST calls, building wrappers, streaming tokens, and validating structured JSON.
2. **Tier 2: The Core Loop & Kernel** (`03_the_dispatcher`, `04_the_loop`, `05_the_budget`, `06_the_reliability`): Dispatching tools, running ReAct loops, managing execution budgets, and building resilient gateways.
3. **Tier 3: Persistence & Memory** (`07_the_state`, `08_context_compaction`, `09_agentic_memory_and_rag`): Persisting state to SQLite/JSON, compacting context windows, and implementing private local RAG.
4. **Tier 4: Control Flows & Reasoning** (`10_the_workflow`, `11_planning_and_reflection`, `12_agent_evals`): Deterministic DAG pipelines, Plan-and-Solve patterns, Reflexion retry loops, and automated evaluations.
5. **Tier 5: Coordination & Standards** (`13_one_agent`, `14_two_agents`, `15_mcp_and_skills`): Standalone agent kernels, multi-agent supervisor topologies, 5-key handoffs, MCP, and dynamic markdown skills.
6. **Tier 6: Security, Governance & Production Runtime** (`16_the_shield`, `17_hitl_and_park_resume`, `18_the_job`, `19_the_front_door`): Subprocess sandboxes, RBAC permissions, Human-In-The-Loop gates, background job tables, and FastAPI SSE streaming.
7. **Tier 7: Full System Synthesis** (`20_synthesis`): Composing all primitives into full enterprise autonomous harnesses, SRE agents, and spec-driven TDD loops.

**Auxiliary Training Path**: Explore [`optional_training/`](./education/optional_training/) to learn model pretraining, LoRA fine-tuning, 4-bit GGUF quantization, and GRPO alignment.

For full course navigation, see the [Curriculum Path Map](./education/PATH.md).

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
