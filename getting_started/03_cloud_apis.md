# Using Cloud APIs (OpenAI, Gemini, Claude)

Using a cloud API follows the exact same pattern as running a model locally: your script sends a JSON request over HTTP and receives a JSON response back. The main differences are that the server is hosted over the internet, you authenticate using an API key, and you do not need to download model weight files to your computer.

Cloud APIs are a great option if your computer cannot run local models, or if you want to test with larger frontier models. The labs teach the exact same concepts regardless of whether you use a local or cloud provider.

> **Note on Endpoints**: The early labs default to Ollama's `/api/generate` endpoint with a single `prompt` key. Most cloud providers use the `/v1/chat/completions` endpoint with a `messages` list. Chapter 00 details both formats so you can easily follow along regardless of the backend you choose.

## Setting Up Your `.env` File

To configure a cloud provider, create your local `.env` file by copying the template from the repository root:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

Open `.env`, uncomment the section for your chosen provider, and add your API key.

> **Important**: Never commit your `.env` file or share your API keys publicly. The `.env` file is already listed in `.gitignore` to keep your credentials safe.

| Provider | POST Endpoint URL | API Key Variable | Example Model |
|---|---|---|---|
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| **Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `GEMINI_API_KEY` | `gemini-2.5-flash` |
| **Claude** | `https://api.anthropic.com/v1/messages` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5` |

---

## 1. OpenAI Setup

1. Generate an API key at [OpenAI Platform](https://platform.openai.com/api-keys).
2. In your `.env` file, uncomment and configure:

```text
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

3. An HTTP request to OpenAI looks like this:

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

To extract the generated text from the response, read `choices[0].message.content`.

---

## 2. Google Gemini Setup

1. Create a free API key in [Google AI Studio](https://aistudio.google.com/apikey).
2. In your `.env` file, uncomment and configure:

```text
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash
```

3. Gemini supports the standard OpenAI-compatible endpoint:

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

Just like with OpenAI, you extract the generated text from `choices[0].message.content`.

---

## 3. Anthropic Claude Setup

1. Create an API key at [Anthropic Console](https://console.anthropic.com/settings/keys).
2. In your `.env` file, uncomment and configure:

```text
ANTHROPIC_API_URL=https://api.anthropic.com/v1/messages
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-5
```

3. Claude uses its own dedicated Messages API format and headers:

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

To extract the text from Claude's response, read `content[0].text`.

---

## How Cloud Providers Compare to the Local Default

| Feature | Local Default (Ollama) | Cloud Providers (OpenAI, Gemini, Claude) |
|---|---|---|
| **Base URL** | `OLLAMA_HOST` + `/api/generate` | `OPENAI_API_URL` / `GEMINI_API_URL` / `ANTHROPIC_API_URL` |
| **Prompt Payload** | `prompt: "..."` | `messages: [...]` |
| **Reading the Reply** | Read `response` field | Read `choices[0].message.content` (or Claude's `content[0].text`) |
| **Authentication** | None needed (runs locally) | `Authorization: Bearer <KEY>` or `x-api-key: <KEY>` |

Whether you use a small local model or a cloud service, the core workflow remains identical: your script builds JSON, sends it over HTTP, and parses the response.

---

**Next Steps**: [Set up your editor and terminal](./04_editors_and_terminal.md).
