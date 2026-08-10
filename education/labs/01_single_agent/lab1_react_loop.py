import json
import urllib.request

# 1. Target Local Ollama Host & Model
OLLAMA_URL = "http://192.168.1.29:11434/api/chat"
MODEL_NAME = "qwen3.6:35b-a3b-65k"

# 2. Local Python Tool Capabilities
def add_numbers(a: float, b: float) -> str:
    """Adds two numbers together."""
    return str(a + b)

def multiply_numbers(a: float, b: float) -> str:
    """Multiplies two numbers together."""
    return str(a * b)

# Tool Dispatcher Registry mapping tool names to Python functions
TOOL_REGISTRY = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers
}

# 3. Tool Schemas (Data Contract provided to Ollama)
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

    # Stateful Conversation History Memory Array
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when calculations are required."},
        {"role": "user", "content": user_prompt}
    ]

    for turn in range(1, max_turns + 1):
        print(f"--- TURN {turn}/{max_turns} ---")

        # Prepare HTTP POST payload to /api/chat
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

        # Append model response to conversation history
        messages.append(message)

        tool_calls = message.get("tool_calls", [])

        # Check if model wants to execute a tool (ACT phase)
        if tool_calls:
            for call in tool_calls:
                fn = call.get("function", {})
                tool_name = fn.get("name")
                tool_args = fn.get("arguments", {})
                
                print(f"[ACTION] Model invoked tool: '{tool_name}' with args: {tool_args}")
                
                # Dispatch execution to Python function
                if tool_name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[tool_name](**tool_args)
                    print(f"[OBSERVATION] Tool output: {result}\n")
                    
                    # Append tool observation back to context window memory
                    messages.append({
                        "role": "tool",
                        "content": result
                    })
                else:
                    print(f"[ERROR] Unknown tool: {tool_name}")
        else:
            # Model generated final text answer without tool calls -> Task Complete!
            final_text = message.get("content", "").strip()
            print(f"[FINAL ANSWER]:\n{final_text}\n")
            print(f"ReAct Loop completed successfully in {turn} turn(s).")
            return final_text

    print("[WARNING] ReAct loop reached max turns threshold.")

if __name__ == "__main__":
    prompt = "What is 42 plus 58, and then multiply that result by 3?"
    run_react_agent(prompt)
