# Pick a model

A model is a file of numbers. Bigger files usually give smarter answers and need more memory. Smaller files run on almost anything.

You can do every lab with a small model. Expect slower replies and weaker wording. The JSON still comes back. That is what the labs check.

Ollama and LM Studio store models in a compressed form (often called Q4). The table below assumes that. If a download fails with "out of memory", pick the row above it.

## A simple rule

Leave a few GB free for the operating system. If the model file is 3 GB, you want about 6 GB of free RAM or VRAM so the prompt has room.

- **RAM** is the memory your laptop already has. Models can run on the CPU using RAM. They will be slow. They still work.
- **VRAM** is memory on a video card. If you have a GPU, the model runs much faster there.
- **Unified memory** (Apple Silicon, some other machines) is one pool the CPU and GPU share. A 128 GB Mac can hold a large model.

## What to pick

| Your machine | Try this first (Ollama name) | About how much memory | What to expect |
|---|---|---|---|
| 8 GB laptop, no GPU | `llama3.2:1b` or `qwen2.5:0.5b` | 1 to 2 GB | Slow. Short answers. Fine for chapters 00 to 04. |
| 16 GB laptop, no GPU | `llama3.2:3b` or `qwen2.5:3b` | 2 to 4 GB | Usable. Still weak on tools and long JSON. |
| 8 to 12 GB video card (RTX 3060 / 4060 class) | `qwen2.5:7b` or `llama3.1:8b` | 5 to 8 GB VRAM | Fast enough to feel like chat. Good through most chapters. |
| 16 to 24 GB video card | `qwen2.5:14b` or `qwen2.5:32b` | 10 to 24 GB VRAM | Stronger JSON and tool calls. |
| 64 GB unified memory | `qwen2.5:32b` or a 70B Q4 | 20 to 48 GB | Comfortable for the whole path. |
| 128 GB unified memory | `qwen3.6:35b-a3b-65k` (course default) or a 70B Q4/Q5 | 35 to 50 GB | This is the machine the course notes were written on. |

Those Ollama names are starting points. In LM Studio, search the same family and pick a **Q4** file that is smaller than your free memory.

## Set the name so labs use it

Labs read two environment variables. They do not care how famous the model is.

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="llama3.2:1b"
```

```bash
export OLLAMA_HOST="http://127.0.0.1:11434"
export OLLAMA_MODEL="llama3.2:1b"
```

If you skip this, some reference scripts fall back to `qwen3.6:35b-a3b-65k` on a LAN host. That will fail on your laptop. Set both values.

## If the model is "dumb"

Keep going. A 1B model can still:

- Return a string in `response`
- Return keys you can print
- Call a simple tool if you keep the prompt tiny (`What is 2 plus 3? Use the tool.`)

It may fail at long JSON or multi-step plans. Write that under **Notes** in the lab. Do not switch chapters. Do not add a smarter API to "fix" a small model. The concept is the same.

Next: [install Ollama or LM Studio](./02_ollama_and_lmstudio.md), or [use a cloud key](./03_cloud_apis.md).
