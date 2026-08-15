# Stub: split MX and UX channels

This folder has an SSE lab that yields mixed frames (`token_delta` next to `tool_call_start`). `02_mx_vs_ux.md` is a separate idea: name which payload is for the person and which is for the model, then keep them off the same text box. There is no `lab_mx_vs_ux.py`. This page is not a lab. There is no script to run.

A real lab would cover:

- A function that takes one frame and returns `{ "channel": "ux" }` or `{ "channel": "mx" }` from `event_type` or from `{ "type": "token" }` / `{ "type": "tool" }`.
- UX kept as visible tokens, buttons, and one-sentence errors. MX kept as tool JSON, traces, and `<think>`.
- A check that `tool_call_start` args and `<think>` do not land in the same string as `token_delta`.
- How this sits before chapter 12 (the CoT demuxer) and after lab 1 (the mixed stream).

What not to add:

- Runnable steps, a `.py` file, a React debug panel, or the chapter 12 splitter.
- A second copy of `generate_agent_sse_stream`.
- A PATH.md edit. That list is a later pass.
- Dumping MX into the main view.
