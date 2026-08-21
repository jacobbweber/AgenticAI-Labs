# How to Pick a Model That Fits Your Computer

An AI model is simply a file of numbers stored on your computer. As a general rule, larger model files produce more detailed or intelligent answers, but they also require more memory to run. Smaller model files can run smoothly on almost any computer.

You can complete every lab in this course using a small model. While smaller models might give shorter answers or generate text a little more slowly, they will still return valid JSON responses. Testing how your code handles those responses is what these labs are all about.

Tools like Ollama and LM Studio store models in a compressed format (often labeled as **Q4**). The recommendations below are based on those standard compressed sizes. If a download ever fails with an "out of memory" error, simply choose a model from a row higher up in the table.

## A Simple Memory Rule

Always leave a few gigabytes (GB) of memory free for your operating system and open apps. For example, if a model file is 3 GB in size, you will want around 6 GB of available RAM or VRAM so there is plenty of room to process text prompts.

Here is a quick refresher on computer memory types:
- **System RAM**: This is the regular memory built into your laptop or desktop. Models can run directly on your CPU using system RAM. They will run a bit slower, but they work just fine for learning.
- **VRAM (Video RAM)**: This is dedicated memory on a graphics card (GPU). If your computer has a dedicated GPU, models will run much faster.
- **Unified Memory**: Found on modern Macs (Apple Silicon) and some newer PCs, unified memory is shared between the CPU and GPU. A Mac with plenty of unified memory can run large models with ease.

## Recommended Starting Models

| Your Computer Setup | Recommended First Model (Ollama Name) | Approximate Memory Needed | What to Expect |
|---|---|---|---|
| 8 GB laptop (no dedicated GPU) | `llama3.2:1b` or `qwen2.5:0.5b` | 1 to 2 GB | Slower speeds and brief answers, but works well for Chapters 00 through 04. |
| 16 GB laptop (no dedicated GPU) | `llama3.2:3b` or `qwen2.5:3b` | 2 to 4 GB | Comfortable speed for learning; may occasionally struggle with complex JSON. |
| 8 to 12 GB dedicated GPU (RTX 3060 / 4060 class) | `qwen2.5:7b` or `llama3.1:8b` | 5 to 8 GB VRAM | Fast, interactive speeds. Great for working through almost all chapters. |
| 16 to 24 GB dedicated GPU | `qwen2.5:14b` or `qwen2.5:32b` | 10 to 24 GB VRAM | Excellent quality for structured JSON output and tool calling. |
| 64 GB unified memory (Mac / PC) | `qwen2.5:32b` or a 70B Q4 | 20 to 48 GB | Very smooth performance across the entire curriculum. |
| 128 GB unified memory | `qwen3.6:35b-a3b-65k` (Course Default) or 70B Q4/Q5 | 35 to 50 GB | High performance with extended context capacity. |

These names are convenient starting points for Ollama. If you prefer LM Studio, search for the same model family and select a **Q4** quantized file that comfortably fits your available memory.

## Configuring the Model in Your Environment

To let the lab scripts know which model to use, copy the environment template from the repository root and uncomment your chosen provider:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

Set the `OLLAMA_MODEL` variable (or your cloud model variable) to your chosen model name. The lab scripts read this configuration automatically. If `.env` is not found, the labs default to `http://127.0.0.1:11434` with `llama3.2:1b`.

> **Reminder**: Keep `.env` on your local machine and do not commit it to git.

## What if My Small Model Makes Mistakes?

Don't worry—keep going! Even a compact 1B model is fully capable of:
- Returning text inside the `response` field.
- Formatting JSON keys that your script can read and print.
- Calling a straightforward tool when given a simple instruction (like *"What is 2 plus 3? Use the calculator tool."*).

Small models might occasionally struggle with complicated multi-step reasoning or large JSON schemas. When that happens, simply note the behavior under the **Notes** section of your lab brief. You do not need to switch chapters or buy expensive cloud credits—the underlying code and architectural concepts remain identical!

---

**Next Steps**: [Install Ollama or LM Studio](./02_ollama_and_lmstudio.md), or [configure a cloud API key](./03_cloud_apis.md).
