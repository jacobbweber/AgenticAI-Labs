# Ollama and LM Studio

Both of these run a model on your machine and listen on a port. The labs talk to that port with HTTP. You do not need both. Pick one.

**Ollama** matches this course with the least extra work. The first labs POST to `/api/generate`. That is Ollama's native route.

**LM Studio** is a window you click. It can serve an OpenAI-style route (`/v1/chat/completions`). Use it if you want a GUI, or if you already have models there.

## Ollama (recommended first)

1. Install from [https://ollama.com/download](https://ollama.com/download).
2. Open a terminal and pull the model you picked:

```text
ollama pull llama3.2:1b
```

3. Leave Ollama running. On Windows and Mac the app stays in the tray. On Linux, `ollama serve`.
4. Check that it answers:

```text
ollama run llama3.2:1b "Say hello in one sentence."
```

5. Point the labs at your machine:

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="llama3.2:1b"
```

`127.0.0.1` means this computer. Port `11434` is Ollama's default.

If `ollama pull` says there is not enough memory, go back to [pick a model](./01_pick_a_model.md) and choose a smaller name.

## LM Studio

1. Install from [https://lmstudio.ai](https://lmstudio.ai).
2. In the app, download a **Q4** model that fits your RAM or VRAM.
3. Open the **Developer** / local server page. Start the server. Note the port (often `1234`).
4. Point the labs at that server. LM Studio speaks OpenAI-style JSON (`messages`), not Ollama's `prompt` field.

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:1234"
$env:OLLAMA_MODEL="the-name-shown-in-lm-studio"
```

Chapter 00 shows both JSON shapes. If you use LM Studio on day one, write the lab against `/v1/chat/completions` and read `choices[0].message.content`. Do not pretend the `/api/generate` keys exist.

## Which one should I use?

| You want | Use |
|---|---|
| The labs as written, least typing | Ollama |
| A window to try models before you write code | LM Studio |
| Both | Fine. One port at a time. Set `OLLAMA_HOST` to the one you are using. |

You do not need a cloud account for this page.

Next: [run the first lab](./05_first_lab.md), or [use a cloud API](./03_cloud_apis.md) if you do not want a local model.
