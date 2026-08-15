# Cloud APIs (OpenAI, Gemini, Claude)

A cloud API is the same idea as Ollama: you send JSON, you get JSON back. The host is on the internet. You pay with an API key. You do not download a weight file.

Use this if you cannot run a local model, or if you want a stronger model than your laptop can hold. The labs still teach the same keys. The answers will just be better.

These labs default to Ollama's `/api/generate` and the `prompt` key. Cloud APIs usually want `/v1/chat/completions` and a `messages` list. Chapter 00 shows both. If you start on a cloud host, use the chat shape from the first day.

Never paste a key into a file you will commit. Use an environment variable.

## OpenAI

1. Create a key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Set the values:

```powershell
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_MODEL="gpt-4o-mini"
```

3. The request looks like this:

```text
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer <OPENAI_API_KEY>
Content-Type: application/json
```

```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "user", "content": "In 2 sentences, explain what an HTTP POST request is." }]
}
```

The text you print is `choices[0].message.content`.

`gpt-4o-mini` is a cheap starter. Any current chat model name from the OpenAI dashboard works. Swap the string.

## Gemini (Google)

1. Create a key in [Google AI Studio](https://aistudio.google.com/apikey).
2. Set the values:

```powershell
$env:GEMINI_API_KEY="..."
$env:GEMINI_MODEL="gemini-2.5-flash"
```

3. Google also accepts OpenAI-style JSON at this host:

```text
POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
Authorization: Bearer <GEMINI_API_KEY>
Content-Type: application/json
```

```json
{
  "model": "gemini-2.5-flash",
  "messages": [{ "role": "user", "content": "In 2 sentences, explain what an HTTP POST request is." }]
}
```

The text you print is again `choices[0].message.content`.

Use the model name shown in AI Studio if `gemini-2.5-flash` is not listed on your account.

## Claude (Anthropic)

1. Create a key at [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys).
2. Set the values:

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:ANTHROPIC_MODEL="claude-sonnet-4-5"
```

3. Anthropic's native route is not the OpenAI URL. The header name is different:

```text
POST https://api.anthropic.com/v1/messages
x-api-key: <ANTHROPIC_API_KEY>
anthropic-version: 2023-06-01
Content-Type: application/json
```

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 256,
  "messages": [{ "role": "user", "content": "In 2 sentences, explain what an HTTP POST request is." }]
}
```

The text you print is `content[0].text`.

Use the model name from the Anthropic console if that string has changed.

## How this maps to the labs

| Lab default (Ollama) | Cloud chat APIs |
|---|---|
| `OLLAMA_HOST` + `/api/generate` | Provider URL above |
| key `prompt` | key `messages` |
| read `response` | read `choices[0].message.content` (or Claude's `content[0].text`) |
| no auth header | `Authorization` or `x-api-key` |

A tiny local model and a frontier API both count. The script still POSTs JSON. If you can name the URL, the keys you send, and the key you read, the lab is doing its job.

Do not put the key in `AGENTS.md`, in a lab file, or in a git commit.

Next: [open an editor](./04_editors_and_terminal.md).
