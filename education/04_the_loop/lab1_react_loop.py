"""Reference solution: ReAct while/for loop over a tool registry. Chapter 04."""
import json
import os
import sys
import urllib.request
from pathlib import Path

_ROOT = next(
    p for p in [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
    if (p / "load_env.py").is_file()
)
sys.path.insert(0, str(_ROOT))
from load_env import load_env

load_env()
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/chat"
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

def add_numbers(a: float, b: float) -> str:
    """Adds two numbers together."""
    return str(a + b)

def multiply_numbers(a: float, b: float) -> str:
    """Multiplies two numbers together."""
    return str(a * b)

TOOL_REGISTRY = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply_numbers",
            "description": "Multiply two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def run_react_agent(user_prompt: str, max_turns: int = 5):
    """Executes a stateful ReAct (Reason + Act) process control loop."""
    print(f"=== STARTING REACT AGENT LOOP ===")
    print(f"User Goal: '{user_prompt}'\n")

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when calculations are required."},
        {"role": "user", "content": user_prompt}
    ]

    for turn in range(1, max_turns + 1):
        print(f"--- TURN {turn}/{max_turns} ---")

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "tools": TOOLS_SCHEMA,
            "stream": False,
            "options": {"temperature": 0.0}
        }

        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            message = data.get("message", {})

        messages.append(message)

        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            for call in tool_calls:
                fn = call.get("function", {})
                tool_name = fn.get("name")
                tool_args = fn.get("arguments", {})

                print(f"[ACTION] Model invoked tool: '{tool_name}' with args: {tool_args}")

                if tool_name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[tool_name](**tool_args)
                    print(f"[OBSERVATION] Tool output: {result}\n")

                    messages.append({
                        "role": "tool",
                        "content": result
                    })
                else:
                    print(f"[ERROR] Unknown tool: {tool_name}")
        else:
            final_text = message.get("content", "").strip()
            print(f"[FINAL ANSWER]:\n{final_text}\n")
            print(f"ReAct Loop completed successfully in {turn} turn(s).")
            return final_text

    print("[WARNING] ReAct loop reached max turns threshold.")

if __name__ == "__main__":
    prompt = "What is 42 plus 58, and then multiply that result by 3?"
    run_react_agent(prompt)
