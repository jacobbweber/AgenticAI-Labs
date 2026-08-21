"""Lab: proof that the HTML page is an SSE/WS client. Chapter 10."""
import os

PATH = os.path.join(os.path.dirname(__file__), "lab3_frontend_client.html")
html = open(PATH, encoding="utf-8").read()
needles = [
    "EventSource",
    "tokens",
    "job_id",
    "interrupt",
    "generate_agent_sse_stream",
    "run_agent_graph",
    "tool_calls",
]
must_have = {"EventSource", "tokens", "job_id", "interrupt"}
for name in needles:
    tag = "HAS" if name in html else "NO"
    print(tag, name)
    ok = tag == "HAS" if name in must_have else tag == "NO"
    if not ok:
        raise SystemExit(1)
