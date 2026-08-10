import json
import urllib.request
from typing import Tuple

OLLAMA_URL = "http://192.168.1.29:11434/api/generate"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 1. State Machine CoT Stream Demuxer
class CoTStreamDemuxer:
    """State machine that demultiplexes <think> reasoning tokens from response payloads."""
    def __init__(self):
        self.state = "IDLE"  # IDLE, THINKING, RESPONSE
        self.buffer = ""

    def feed(self, chunk: str) -> Tuple[str, str]:
        """Processes a token chunk and returns (thinking_tokens, response_tokens)."""
        self.buffer += chunk
        thinking_out, response_out = "", ""

        while self.buffer:
            if self.state == "IDLE":
                if "<think>" in self.buffer:
                    pre, post = self.buffer.split("<think>", 1)
                    response_out += pre
                    self.buffer = post
                    self.state = "THINKING"
                else:
                    response_out += self.buffer
                    self.buffer = ""
            elif self.state == "THINKING":
                if "</think>" in self.buffer:
                    think_text, post = self.buffer.split("</think>", 1)
                    thinking_out += think_text
                    self.buffer = post
                    self.state = "RESPONSE"
                else:
                    thinking_out += self.buffer
                    self.buffer = ""
            elif self.state == "RESPONSE":
                response_out += self.buffer
                self.buffer = ""

        return thinking_out, response_out

# 2. Main Streaming Execution Loop
def run_demuxed_reasoning_stream(prompt: str):
    print("=== STARTING REASONING MODEL COT DEMUXER LAB ===")
    print(f"[REASONING ENGINE] Model: '{MODEL_NAME}' | Endpoint: LAN Ollama Host")
    
    demuxer = CoTStreamDemuxer()
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {"temperature": 0.0}
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=json_bytes, headers={"Content-Type": "application/json"}
    )

    full_thinking = []
    full_response = []

    print("\n=== DEMUXED STREAMING OUTPUT ===")
    with urllib.request.urlopen(req, timeout=120) as resp:
        for line in resp:
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            chunk = data.get("response", "")
            
            thinking_token, response_token = demuxer.feed(chunk)
            
            if thinking_token:
                full_thinking.append(thinking_token)
                print(f"[THINKING LOG] {thinking_token}", end="", flush=True)
            if response_token:
                full_response.append(response_token)
                print(f"[RESPONSE PAYLOAD] {response_token}", end="", flush=True)

    print("\n\n=== FINAL DEMUXED SUMMARY ===")
    print(f"Total Thinking Characters : {len(''.join(full_thinking))}")
    print(f"Total Response Characters : {len(''.join(full_response))}")

if __name__ == "__main__":
    prompt = "Solve step-by-step: If a train travels at 60 mph for 2.5 hours, how far does it travel?"
    run_demuxed_reasoning_stream(prompt)
