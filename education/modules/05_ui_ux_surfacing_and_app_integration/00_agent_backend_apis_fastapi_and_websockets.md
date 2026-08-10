# 00: Agent Backend APIs: FastAPI, WebSockets & Real-Time Streaming Protocols

## 1. Macro Concept & Industry Need

Surfacing autonomous agents through traditional synchronous REST HTTP endpoints causes severe architectural failures. Because agentic turns involve multi-step reasoning, tool execution, and graph state transitions that can take anywhere from seconds to several minutes, synchronous HTTP request-response patterns result in client timeouts, blank loading screens, and unresponsive user interfaces.

Surfacing agentic backends requires event-driven, real-time streaming architectures:
- **Server-Sent Events (SSE)**: HTTP/2 unidirectional streaming (`text/event-stream`) providing lightweight, fire-and-forget push of LLM token streams, tool invocation logs, and node status updates.
- **WebSockets (`ws://`)**: Full-duplex TCP framing required for interactive agent control, multiplexing inbound user control signals (`INTERRUPT_TURN`, prompt steering) to backend execution event loops.
- **Session Graph Stream Chunking**: Structuring graph state deltas into ordered, strongly-typed SSE frame payloads linked to persistent state checkpoints (`thread_id`).
- **Stream Backpressure & Disconnect Handling**: Detecting client disconnects in real time to immediately cancel upstream model calls and prevent runaway GPU token usage.

## 2. Architectural Component Mapping

| AI Jargon / Buzzword | Actual Software Component / Standard Primitive |
| :--- | :--- |
| **Agent API Endpoint** | FastAPI `@app.post("/api/agent/run")` route returning a `StreamingResponse` wrapping an async generator. |
| **Token Streaming** | Async generator function emitting SSE lines (`data: {"type": "token", "delta": "..."}\n\n`). |
| **Bidirectional Interrupt / Steering** | WebSocket connection multiplexing inbound control signals to backend `asyncio.Event` flags. |
| **Session Graph Stream Chunking** | JSON serialization pipeline partitioning graph state updates (`node_start`, `tool_call`) into stream frames. |
| **Async Job Polling Fallback** | HTTP 202 Accepted returning a `job_id`, paired with `GET /api/jobs/{job_id}/events` polling endpoint. |

## 3. Key Technical Aspects & Dig-In Topics

### 1. Protocol Selection Architecture (SSE vs. WebSockets vs. HTTP 202)
- **Server-Sent Events (SSE)**: Unidirectional HTTP stream (`text/event-stream`). Native browser `EventSource` support. Low overhead, automatic HTTP/2 multiplexing, ideal for chat interfaces with live token generation.
- **WebSockets (`ws://` / `wss://`)**: Full-duplex framing. Mandatory when clients push real-time interruptions, mid-turn prompt steering, or live approval signals directly into active agent loops.
- **Async HTTP 202 Polling**: Decoupled background queue pattern (FastAPI + Redis + Celery/Temporal) used for long-horizon multi-minute autonomous tasks where client socket connections are unreliable.

### 2. Session Graph Stream Chunking & Event Schema
Standardized JSON SSE Frame Structure:
- `event_id`: Monotonically increasing sequence index (`uint64`).
- `thread_id`: Unique identifier linking stream frame to backend state graph checkpoint.
- `event_type`: Categorized payload type (`token_delta`, `tool_call_start`, `tool_call_result`, `node_transition`, `interrupt_raised`).
- `data`: Typed JSON payload.

```json
{
  "event_id": 1042,
  "thread_id": "th_98a72f",
  "event_type": "tool_call_start",
  "data": {
    "tool_name": "execute_sql_query",
    "arguments": {"query": "SELECT COUNT(*) FROM users WHERE status = 'active'"}
  }
}
```

### 3. Bidirectional Interrupt & Steering State Machine
- **Inbound Control Frames**: Client pushes `INTERRUPT` frame via WebSocket.
- **Asyncio Event Trapping**: The WebSocket receiver sets an `asyncio.Event` flag bound to the agent graph runner, gracefully pausing graph execution at the next node boundary.
- **Mid-Turn Context Steering**: Client pushes `STEER` frame with updated prompt constraints, which the runner injects into context before clearing the event flag and resuming execution.

### 4. Stream Backpressure & Disconnect Handling
- **Client Disconnect Trapping**: Monitoring `request.is_disconnected()` inside FastAPI async generator loops. Upon client disconnect, the generator raises `asyncio.CancelledError`, immediately cancelling upstream LLM API calls and releasing server resources.

```
+-----------------------------------------------------------------------------------+
|                     STREAMING BACKEND PROTOCOL ARCHITECTURE                       |
+-----------------------------------------------------------------------------------+
|  [React Frontend] <=== (SSE / WebSocket Stream) ===> [FastAPI Backend]            |
|        |                                                   |                      |
|        |-- (Inbound WS frame: INTERRUPT) ----------------->|                      |
|        |                                                   v                      |
|        |                                       Set asyncio.Event Flag             |
|        |                                       Pause Graph at Node Boundary       |
|        |                                                   |                      |
|        |<-- (Outbound SSE frame: EVENT_TYPE) -------------+                      |
|        |    {"event_type": "tool_call_start", ...}                                |
+-----------------------------------------------------------------------------------+
```

## 4. Future Lab Blueprint

### Lab 1: Baseline Architecture
Construct an async FastAPI backend serving a streaming endpoint (`GET /api/agent/stream`) utilizing `StreamingResponse` and async generators to stream synthetic LLM tokens and tool execution progress logs over Server-Sent Events (SSE).

### Lab 2: Intermediate Capability Integration
Build a full-duplex WebSocket backend (`ws://localhost:8000/ws/agent`) that streams real-time agent graph node transitions while concurrently handling incoming client interrupt signals (`INTERRUPT_TURN`) mapped to backend `asyncio.Event` primitives.

### Lab 3: Enterprise Resilience & Advanced Edge Cases
Architect a multiplexed session graph stream chunking protocol featuring standardized JSON SSE frame serialization, stream buffer backpressure management, client reconnection state recovery via `Last-Event-ID`, and distributed Redis Pub/Sub backend state broadcasting across multiple stateless FastAPI workers.

### Stretch Goal: Production Hardening
Engineer a production-grade streaming API gateway featuring token-level rate limiting, TLS encapsulation, client heartbeat keepalives, graceful disconnect cancellation of upstream model calls, and OpenTelemetry trace context propagation injected directly into SSE frame headers.
