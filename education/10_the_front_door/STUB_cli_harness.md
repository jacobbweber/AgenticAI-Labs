# Stub: terminal as a client of the kernel

This folder has labs for SSE frames and a WebSocket interrupt. `03_cli_harness.md` is a separate idea: stdin and stdout as another client of chapter 07 `run_turn`, with a y/n line before writes. There is no `lab_cli_harness.py`. This page is not a lab. There is no script to run.

A real lab would cover:

- `input()` (or `sys.stdin.readline`) to read one user line, then `CoreAgentKernel.run_turn(session_id, line)`.
- Print the `response` field on stdout. Keep `thinking` off the default print (MX).
- A y/n prompt before a write tool. Do not call the tool on `n`.
- The same `state_store/{session_id}.json` keys as chapter 07: `session_id`, `messages`, `turn_count`.
- Proof that FastAPI and a browser are not required for the loop.

What not to add:

- Runnable steps, a `.py` file, a TUI, or a FastAPI app.
- A second copy of `CoreAgentKernel` or of `run_agent_graph`.
- A PATH.md edit. That list is a later pass.
- Moving the loop into the terminal UI.
