# Lab 1: Script posts JSON

A Python file on disk has received text from a model. No wrapper function. No streaming. No tools.

## What you touch
- Script: `lab1_script_posts_json.py`
- URL / path: `{OLLAMA_HOST}/api/generate` (default `http://127.0.0.1:11434/api/generate`)
- Keys sent: `model`, `prompt`, `stream` (`false`)
- Keys read: `response`

## Steps
```mermaid
flowchart LR
    A["lab1_script_posts_json.py"] -->|"POST /api/generate"| B["Ollama :11434"]
    B -->|"JSON.response"| A
```

1. Read `OLLAMA_HOST` and `OLLAMA_MODEL` from the environment. If they are unset, use `http://127.0.0.1:11434` and `llama3.2:1b`.
2. Build one JSON body: `model`, `prompt` ("In 2 sentences, explain what an HTTP POST request is."), `stream: false`. Do not send `options`.
3. POST it to `{host}/api/generate` with header `Content-Type: application/json`.
4. Decode the response JSON.
5. Print `result["response"]`. If that field is missing or empty, exit with an error. If the host is unreachable, exit with the URL and the connection error.

## Data contract
Only the keys this script sends and reads.

**Request**

```json
{
  "model": "llama3.2:1b",
  "prompt": "In 2 sentences, explain what an HTTP POST request is.",
  "stream": false
}
```

**Response**

```json
{
  "response": "string"
}
```

## Run
From the repo root:

```bash
OLLAMA_HOST=http://127.0.0.1:11434 OLLAMA_MODEL=llama3.2:1b python education/00_atoms/lab1_script_posts_json.py
```

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="llama3.2:1b"
python education/00_atoms/lab1_script_posts_json.py
```

## What you should see
Two sentences about HTTP POST. If you see `URLError` or `Connection refused`, the provider process is not reachable at that host. If you see HTTP 404, the model name is wrong or not pulled. If you see `empty 'response' field`, you hit the wrong route or the model returned no visible text.

## Stop here
This is not a client library. Do not add `def query_llm(prompt) -> str`. That is chapter 01. Do not stream. Do not add tools. Next: [lab2_read_the_json.md](./lab2_read_the_json.md).

## Notes
Leave this empty until you run it. Paste the printed text from your machine here.
