# Getting started

You do not need a powerful computer. You do not need to be a programmer.

This course is ordinary Python scripts that send JSON to a model. A tiny model on a cheap laptop is enough to learn every idea. The answers will be shorter and sometimes wrong. That is fine. The lesson is the script, the JSON keys, and the loop, not a perfect reply.

The course default model (`qwen3.6:35b-a3b-65k`) is for a strong local machine. It is not required.

## Do these six things

1. Install [Python 3](https://www.python.org/downloads/). On the installer, check **Add python.exe to PATH**.
2. [Pick a model that fits your machine](./01_pick_a_model.md).
3. Run it locally with [Ollama or LM Studio](./02_ollama_and_lmstudio.md), or send the same JSON to [OpenAI, Gemini, or Claude](./03_cloud_apis.md).
4. From the repo root, copy the env template and uncomment one provider:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

5. Open this repo in [Cursor, VS Code, Claude Code, Antigravity, or a terminal](./04_editors_and_terminal.md).
6. [Run the first lab](./05_first_lab.md).
7. Start the course at [`education/00_atoms/`](../education/00_atoms/).

If a step fails, stay on that page. Do not skip ahead.

## What "done" looks like

You can open a terminal in this repo and run:

```bash
cp .env.example .env
```

Edit `.env`. Uncomment the Ollama lines (or another provider). Then:

```text
python education/00_atoms/lab1_script_posts_json.py
```

You see a few sentences of text. Then you are ready for chapter 00.

Do not commit `.env`. It can hold a key.

## Files in this folder

| File | Read it when |
|---|---|
| [01_pick_a_model.md](./01_pick_a_model.md) | You are choosing a size |
| [02_ollama_and_lmstudio.md](./02_ollama_and_lmstudio.md) | You want the model on your machine |
| [03_cloud_apis.md](./03_cloud_apis.md) | You want OpenAI, Gemini, or Claude |
| [04_editors_and_terminal.md](./04_editors_and_terminal.md) | You need a place to write and run Python |
| [05_first_lab.md](./05_first_lab.md) | You are ready to run one script |
