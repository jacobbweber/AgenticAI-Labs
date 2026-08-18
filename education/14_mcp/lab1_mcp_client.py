"""Lab: JSON-RPC tools/list and tools/call across a process. Chapter 14."""
import json
import subprocess
import sys


def add_numbers(a, b):
    return str(a + b)


def serve():
    for line in sys.stdin:
        req = json.loads(line)
        mid, method = req["id"], req["method"]
        if method == "tools/list":
            result = {"tools": [{"name": "add_numbers", "description": "Add two numbers."}]}
        elif method == "tools/call":
            args = req["params"]["arguments"]
            result = {"content": [{"type": "text", "text": add_numbers(**args)}]}
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601}}), flush=True)
            continue
        print(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}), flush=True)


def rpc(proc, req):
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())


if __name__ == "__main__":
    if "--server" in sys.argv:
        serve()
        raise SystemExit(0)
    proc = subprocess.Popen(
        [sys.executable, __file__, "--server"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
    )
    listed = rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
    for tool in listed["result"]["tools"]:
        print(tool["name"])
    called = rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                        "params": {"name": "add_numbers", "arguments": {"a": 2, "b": 3}}})
    print({"name": "add_numbers", "content": called["result"]["content"][0]["text"]})
    proc.stdin.close()
    proc.wait(timeout=5)
