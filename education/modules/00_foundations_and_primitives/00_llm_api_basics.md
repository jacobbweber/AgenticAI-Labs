# 00: LLM API Basics

## 1. Macro Concept & Industry Need

At the foundation of agentic AI systems, an **LLM API call** is a stateless Remote Procedure Call (RPC) sent to a neural network inference engine (e.g., Anthropic Claude, OpenAI GPT-4o, Google Gemini, or local models running via Ollama and vLLM). Unlike traditional deterministic REST APIs that accept structured parameters and return static computed fields, an inference API accepts an array of past conversational messages and computes next-token probability distributions autoregressively.

Enterprise production systems require moving past basic single-prompt wrappers toward robust API infrastructure. AI software engineers must master low-level API mechanics, streaming protocols, token economics, latency profiling, and gateway resilience patterns to build high-throughput, low-latency, and fault-tolerant agentic platforms.

Common enterprise applications include multi-provider failover gateways, real-time document summarization streams, and low-latency intent classification microservices.

---

## 2. Architectural Component Mapping

The following table translates common AI API terminology into standard software engineering primitives:

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Inference Call** | Stateless HTTP POST Remote Procedure Call (RPC) to a backend neural engine |
| **Token** | Integer vocabulary ID mapped via BPE / SentencePiece tokenizer algorithms |
| **Context Window** | Fixed-size input/output memory buffer array processed by self-attention layers |
| **System Prompt** | Runtime policy configuration string placed at array index 0 (`role: "system"`) |
| **Temperature** | Softmax division scalar adjusting next-token logit probability distribution |
| **Time to First Token (TTFT)** | HTTP Time-to-First-Byte (TTFB) plus initial prompt processing (prefill) latency |
| **Tokens Per Second (TPS)** | Autoregressive decoding generation throughput rate (generated tokens / decode duration) |

---

## 3. Key Technical Aspects & Dig-In Topics

### Streaming Transport Protocols (SSE vs WebSockets vs HTTP/2)
Streaming responses are delivered via Server-Sent Events (SSE) over standard HTTP connections, WebSockets, or HTTP/2 chunked transfer encoding. In SSE streams, the inference server emits text deltas as MIME type `text/event-stream` chunks formatted as `data: {"choices": [{"delta": {"content": "token"}}]}\n\n`, terminating with `data: [DONE]`. Client applications must implement stream demuxers to assemble incoming token deltas into complete context frames without blocking the main event loop.

```
Client (App)                     Gateway Proxy                   Inference Engine
     |                                 |                                 |
     |--- HTTP POST /v1/chat---------->|--- Prefill Phase (Prompt)------>|
     |<-- 200 OK (text/event-stream)---|                                 |
     |<-- SSE Chunk: "data: token1"----|<-- Decode Phase (TTFT)----------|
     |<-- SSE Chunk: "data: token2"----|<-- Token 2 (ITL Latency)--------|
     |<-- SSE Chunk: "data: [DONE]"----|<-- Generation Complete----------|
```

### Latency Profiling & Token Mechanics
Inference latency is split into two distinct compute phases:
1. **Prefill Phase (Prompt Ingestion)**: Parallel matrix multiplication processing all input tokens simultaneously. Governs **Time to First Token (TTFT)**.
2. **Decode Phase (Autoregressive Token Generation)**: Sequential token generation where each step requires loading full model weights. Governs **Tokens Per Second (TPS)** and **Inter-Token Latency (ITL)**.

Tokenization relies on Byte-Pair Encoding (BPE) or SentencePiece algorithms, converting raw UTF-8 text into numerical integer IDs. On average, 1 token equates to approximately 4 characters or 0.75 English words. Enterprise cost budgeting and rate limiting require precise pre-request token estimation.

### Unified Multi-Provider Gateway & Resiliency Architecture
To eliminate vendor lock-in and handle rate limits, modern systems deploy a unified API gateway (e.g., LiteLLM, OpenRouter, or custom proxy) that standardizes request/response schemas across OpenAI, Anthropic, and local vLLM endpoints. Resiliency strategies include:
- **Rate Limit Management**: Token bucket algorithms tracking requests-per-minute (RPM) and tokens-per-minute (TPM).
- **Exponential Backoff with Full Jitter**: Randomizing backoff delays on HTTP 429/5xx errors to prevent thundering herd problems.
- **Circuit Breakers**: Tripping failed provider routes and automatically routing fallback requests to local vLLM or secondary cloud endpoints.

---

## 4. Future Lab Blueprint

The following directional prompts guide the construction of hands-on technical labs for this module:

### Lab 1: Baseline Architecture (Stateless Multi-Provider LLM Client & Gateway)
Construct a unified Python/TypeScript HTTP client wrapper that normalizes request payloads across OpenAI, Anthropic, and local Ollama/vLLM endpoints. Implement standardized sampling parameter configuration (`temperature`, `max_tokens`, `top_p`) and parse standard JSON completions without relying on third-party framework abstractions.

### Lab 2: Intermediate Capability Integration (Streaming Token Demuxer & Latency Profiler)
Develop an asynchronous SSE streaming token reader using raw HTTP clients (`httpx` or `fetch`). Implement a real-time latency profiler that calculates and logs exact TTFT (milliseconds to initial chunk), TPS (generation rate during decode), ITL (variance between chunks), and total E2E execution duration.

### Lab 3: Enterprise Resilience & Advanced Edge Cases (Circuit Breaker & Rate Limiter)
Build a resilient proxy gateway wrapper featuring a token-bucket rate limiter, exponential backoff with randomized full jitter, and an automated circuit breaker. Demonstrate automatic failover from a primary cloud provider to a secondary local vLLM instance upon encountering HTTP 429 rate limit or 503 service unavailable errors.

### Stretch Goal: Production Hardening (Multi-Region Load-Balanced LLM Gateway)
Design a high-throughput enterprise proxy gateway featuring connection pooling, HTTP/2 multiplexing, per-tenant token usage tracking, request cost attribution telemetry, and zero-downtime health-checked provider failover.
