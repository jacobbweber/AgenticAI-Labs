import asyncio
import json
import time
from typing import AsyncGenerator

# 1. Standardized SSE Event Frame Serializer
def format_sse_frame(event_type: str, data: dict, event_id: int) -> str:
    """Formats payload into standard Server-Sent Events (SSE) text frame."""
    payload = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": time.time(),
        "data": data
    }
    return f"data: {json.dumps(payload)}\n\n"

# 2. Async Agent Event Stream Generator
async def generate_agent_sse_stream(prompt: str) -> AsyncGenerator[str, None]:
    """Generates structured SSE stream frames for token generation and tool execution."""
    print(f"\n[SSE STREAM] Starting agent stream for prompt: '{prompt}'...")
    event_id = 0

    # Frame 1: Stream Started
    event_id += 1
    yield format_sse_frame("session_started", {"status": "ACTIVE", "prompt": prompt}, event_id)
    await asyncio.sleep(0.1)

    # Frame 2: Token Streaming (Thinking)
    tokens = ["Analyzing ", "user ", "query... ", "Formulating ", "action ", "plan."]
    for token in tokens:
        event_id += 1
        yield format_sse_frame("token_delta", {"delta": token}, event_id)
        await asyncio.sleep(0.05)

    # Frame 3: Tool Call Initiated
    event_id += 1
    yield format_sse_frame("tool_call_start", {"tool_name": "read_file", "args": {"path": "config.json"}}, event_id)
    await asyncio.sleep(0.1)

    # Frame 4: Tool Execution Result
    event_id += 1
    yield format_sse_frame("tool_call_result", {"tool_name": "read_file", "output": "{'env': 'prod'}"}, event_id)
    await asyncio.sleep(0.1)

    # Frame 5: Stream Complete
    event_id += 1
    yield format_sse_frame("turn_complete", {"status": "SUCCESS", "total_events": event_id}, event_id)

# 3. Main Test Client
async def main():
    print("=== STARTING SERVER-SENT EVENTS (SSE) STREAMING API LAB ===")
    
    stream = generate_agent_sse_stream("Read config and summarize environment")
    
    print("\n=== RECEIVING SSE STREAM FRAMES FROM AGENT ===")
    async for sse_frame in stream:
        # Strip trailing newlines for clear console display
        raw_frame = sse_frame.strip()
        print(f"[CLIENT READ] {raw_frame}")

if __name__ == "__main__":
    asyncio.run(main())
