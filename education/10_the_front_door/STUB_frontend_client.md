# Stub: frontend page as a client

This folder has labs for SSE frames and a WebSocket interrupt. `01_frontend.md` is a separate idea: a page that holds `tokens`, `job_id`, and an interrupt control, and does not own the agent loop. There is no `lab_frontend_*.py`. This page is not a lab. There is no script to run.

A real lab would cover:

- A page (React or a single HTML file) that opens `EventSource` on the SSE route and appends the token field to a `tokens` string.
- A `job_id` stored from the start POST or the first frame, so two clicks do not mix streams.
- A stop button that sends `{ "type": "interrupt" }` on a WebSocket. SSE cannot send that message.
- Proof that `useEffect` (or `DOMContentLoaded`) only opens the socket. It does not run ReAct, pick tools, or own the chapter 06 queue.

What not to add:

- Runnable steps, a `.py` file, a Next.js app, or a CSS kit.
- A second copy of `generate_agent_sse_stream` or `run_agent_graph`.
- A PATH.md edit. That list is a later pass.
- Putting the agent loop in the browser.
