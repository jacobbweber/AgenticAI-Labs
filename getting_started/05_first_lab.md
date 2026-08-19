# Run the first lab

This page is one script. If it prints text from a model, your setup works.

## 1. Confirm Python

```text
python --version
```

If that fails, try `python3 --version`. Use whichever command works in the steps below.

## 2. Confirm the model is reachable

Copy the env template if you have not yet:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

Uncomment one provider in `.env`.

**Ollama**

```text
ollama list
```

You should see the model name you pulled. The Ollama lines in `.env` should match it.

**LM Studio**

Start the local server in the app. Use its port (often `1234`) and the model name it shows in `.env`.

**Cloud**

Uncomment that provider in `.env` from [cloud APIs](./03_cloud_apis.md). You will write the chat-style JSON from chapter 00, not the Ollama `prompt` field.

## 3. Run the reference script (optional)

This repo already has a finished `lab1_script_posts_json.py`. You may run it once to test the connection. Then delete it if you want to write it yourself. Deleting `.py` files is how you start from scratch. Keep every `.md`.

From the repo root:

```text
python education/00_atoms/lab1_script_posts_json.py
```

The script loads `.env` from the repo root.

## What you should see

A short paragraph about HTTP POST. That is success.

| What you see | What it means |
|---|---|
| A few sentences of text | Setup works. Read the chapter 00 module next. |
| `URLError` or connection refused | Nothing is listening at `OLLAMA_HOST`. Start Ollama or LM Studio, or fix the URL in `.env`. |
| HTTP 404 | The model name is wrong or not pulled. Run `ollama list`. |
| Empty `response` | The model returned no visible text. Try a larger model, or a shorter prompt. The script still taught you the keys. |

## 4. Write it yourself

Open [`education/00_atoms/lab1_script_posts_json.md`](../education/00_atoms/lab1_script_posts_json.md). That file is the whole assignment.

Read the module [education/00_atoms/00_script_provider_weights.md](../education/00_atoms/00_script_provider_weights.md) first. Then write lab1 from the brief, or keep the reference and go to lab2. [education/PATH.md](../education/PATH.md) is the rest of the course.

## If the answers look bad

Keep going. A 1B model on a laptop with no GPU will sound worse than Claude. The course is still the same POST, the same keys, and the same loop. Write what you saw under **Notes** in the lab brief.
