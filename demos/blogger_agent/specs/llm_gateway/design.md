# LLM Gateway Design Specification

## 1. Overview & Architecture
The LLM Gateway module (`api/llm_gateway.py`), centered around `MultiModelGatewayRouter`, serves as the unified interface between core pipeline primitives and local/remote Ollama inference servers.

It guarantees request execution stability against transient network stalls, long generation latencies, and server load spikes through strict request timeouts, backoff retries, and terminal diagnostic reporting.

---

## 2. Component Responsibilities
- **HTTP Routing**: Sends payload requests to the Ollama host `/api/generate` endpoint with configured model names and prompts.
- **Timeout Management**: Sets an explicit per-request socket timeout of >= 300 seconds to support complex multi-token reasoning models.
- **Exponential Backoff Retry**: Implements up to 5 retry attempts with exponential delays (`5 * (3 ** (attempt - 1))` seconds: 5s, 15s, 45s, 135s, 405s).
- **Hard Failure Termination**: Raises a explicit `RuntimeError` on attempt exhaustion rather than returning partial outputs or falling back silently.
- **Terminal Diagnostics**: Outputs clear terminal messages for retry counts, backoff wait durations, and response status codes.

---

## 3. Interfaces & Key Functions
- `generate(prompt: str, system_prompt: str | None = None) -> str`: Sends generation request to Ollama and returns response string.
- Environment variables: `OLLAMA_HOST` (default: `http://192.168.1.29:11434`), `DEFAULT_MODEL` (default: `qwen3.6:35b-a3b-65k`).

---

## 4. Error Handling & Resilience
- **HTTP 5xx / 429 / Connection Timeout**: Retries with exponential backoff delay.
- **Max Retries Exhausted**: Logs error and raises `RuntimeError("LLM Gateway request failed after 5 retries: <details>")`.
