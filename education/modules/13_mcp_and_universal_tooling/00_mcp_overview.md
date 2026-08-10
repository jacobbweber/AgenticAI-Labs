# Module 13 Overview: Model Context Protocol (MCP) & Universal Tooling Interface

## 1. Macro Concept & System Need

Building custom tool wrappers for every individual API or system command creates tight coupling and code duplication. **Model Context Protocol (MCP)** is an open JSON-RPC 2.0 specification that standardizes how host applications (like Claude Code, Antigravity, or IDEs) expose tools, resources, and prompt templates to AI agents over `stdio` or HTTP streams.

Without a standardized protocol like MCP:
1. **Tool Schema Fragmentation**: Every tool framework invents its own JSON schema format for tool definitions.
2. **Brittle Integration**: Adding a new tool requires modifying the core agent codebase and re-deploying the runtime.
3. **No Transport Isolation**: Running tool logic inside the same process as the agent engine poses memory crash and security risks.

MCP decouples **Tool Providers** (servers) from **Agent Runtimes** (clients), enabling plug-and-play tool ecosystems.

---

## 2. Low-Level Capabilities vs. High-Level User Features

| System Layer | Low-Level Capability (Under the Hood Primitive) | High-Level User Feature |
| :--- | :--- | :--- |
| **Transport Layer** | `StdioJSONRPCFramingEngine` | Process-isolated tool communication |
| **Tool Registry** | `MCPCapabilityNegotiator` | One-click plugin tool integration |
| **Resource Provider** | `MCPResourceTemplateResolver` | Dynamic prompt and context loading |

---

## 3. Architecture & Data Control Flow

> *Btw, this is WHEN and WHY we need this framing concept:*
> **WHEN**: You need your agent to interact with external services (databases, terminal shells, local file systems) through isolated sub-processes.
> **WHY**: Hardcoding tools inside the agent loop prevents modular reuse. MCP standardizes requests into strict JSON-RPC `tools/list` and `tools/call` schemas.

```mermaid
flowchart LR
    subgraph Agent Host (MCP Client)
        A["Agent Core Loop"] --> B["MCP Client Protocol Handler"]
    end
    
    subgraph Tool Process (MCP Server)
        C["Stdio Reader (stdin/stdout)"] --> D["JSON-RPC 2.0 Router"]
        D --> E1["Tool: execute_shell"]
        D --> E2["Tool: read_db_schema"]
    end
    
    B <--"JSON-RPC Over Stdio Pipe"--> C
```

---

## 4. Code Architecture & Component Spec

```python
# MCP JSON-RPC 2.0 Message Structure
import json
from typing import Dict, Any

class MCPStdioMessage:
    @staticmethod
    def format_request(method: str, params: Dict[str, Any], msg_id: int) -> str:
        payload = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "method": method,
            "params": params
        }
        return json.dumps(payload) + "\n"

    @staticmethod
    def parse_line(line: str) -> Dict[str, Any]:
        return json.loads(line.strip())
```

---

## 5. Lab Progression Roadmap

1. **Lab 1 (`lab1_mcp_stdio_server.py`)**: Implement an executable MCP stdio server handling initialization handshakes and requests.
2. **Lab 2 (`lab2_mcp_tool_registry.py`)**: Build an MCP client that dynamically queries `tools/list` and registers tools into an OpenAI-compatible API call.
3. **Lab 3 (`lab3_mcp_resource_provider.py`)**: Implement an MCP server that serves file system resources and dynamic system prompt templates.
