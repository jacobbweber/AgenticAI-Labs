import json
import re
import urllib.request

OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

class StreamDemuxer:
    """
    Stream Demuxer (Demultiplexer):
    Splits incoming token stream into two separate outputs:
    1. Thinking Stream -> Telemetry Log
    2. Content/Action Stream -> Console Output / Tool Dispatcher
    """
    def __init__(self):
        self.in_think_block = False
        self.think_buffer = []
        self.content_buffer = []

    def process_token(self, token: str):
        # Check for start of reasoning block <think>
        if "<think>" in token:
            self.in_think_block = True
            token = token.replace("<think>", "")
        
        # Check for end of reasoning block </think>
        if "</think>" in token:
            parts = token.split("</think>")
            self.think_buffer.append(parts[0])
            self.in_think_block = False
            token = parts[1] if len(parts) > 1 else ""

        # Route token to correct output channel
        if self.in_think_block:
            self.think_buffer.append(token)
            # Channel 1: Internal Thinking Telemetry Stream
            print(f"\033[90m[THINK STREAM] {token}\033[0m", end="", flush=True)
        else:
            if token:
                self.content_buffer.append(token)
                # Channel 2: Action / User Content Stream
                print(f"\033[92m[CONTENT STREAM] {token}\033[0m", end="", flush=True)

def run_demux_lab():
    print("=== STARTING REASONING TOKEN DEMUXER LAB ===")
    print(f"Model: {MODEL_NAME}\n")

    payload = {
        "model": MODEL_NAME,
        "prompt": "Analyze why token demuxing is essential for AI harnesses in 2 short bullet points.",
        "stream": True,
        "options": {"temperature": 0.0}
    }

    json_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json_bytes,
        headers={"Content-Type": "application/json"}
    )

    demuxer = StreamDemuxer()

    with urllib.request.urlopen(req) as resp:
        for line in resp:
            if not line:
                continue
            chunk = json.loads(line.decode("utf-8"))
            token = chunk.get("response", "")
            demuxer.process_token(token)

    print("\n\n=== DEMUXED SUMMARY ===")
    print(f"Captured Thinking Tokens (Length): {len(''.join(demuxer.think_buffer))} chars")
    print(f"Captured Content Tokens (Length) : {len(''.join(demuxer.content_buffer))} chars")

if __name__ == "__main__":
    run_demux_lab()
